"""Git repository sync state machine.

Detects the current state of a repository relative to its remote and
repeatedly executes the appropriate git commands until fully synchronized.
"""

import time
from enum import Enum
from typing import NamedTuple

from auto_git import git as _git
from auto_git import ui

class _AheadBehind(NamedTuple):
    ahead: int
    behind: int

MAX_RETRIES = 5
RETRY_DELAYS = [1, 2, 4, 8, 16]


class SyncState(Enum):
    UP_TO_DATE = "up-to-date"
    UNCOMMITTED = "uncommitted"
    NO_REMOTE = "no-remote"
    NO_UPSTREAM = "no-upstream"
    CONFLICT = "conflict"
    NETWORK_ERROR = "network-error"
    ERROR = "error"


def _get_ahead_behind(cwd: str | None = None) -> _AheadBehind | None:
    result = _git.rev_list_count("@{upstream}", "HEAD", cwd=cwd)
    if not result.ok:
        return None
    parts = result.stdout.split()
    if len(parts) != 2:
        return None
    try:
        return _AheadBehind(ahead=int(parts[1]), behind=int(parts[0]))
    except ValueError:
        return None


def _is_network_error(stderr: str) -> bool:
    lowered = stderr.lower()
    signals = [
        "connection was reset",
        "could not connect",
        "could not resolve host",
        "timed out",
        "connection refused",
        "network is unreachable",
    ]
    return any(s in lowered for s in signals)


def _push_with_retry(cwd: str | None = None) -> bool:
    for i, delay in enumerate(RETRY_DELAYS):
        result = _git.push(cwd=cwd)
        if result.ok:
            return True
        if _is_network_error(result.stderr):
            ui.warn(
                f"Network error, retrying in {delay}s... ({i + 1}/{MAX_RETRIES})"
            )
            time.sleep(delay)
        else:
            ui.error(f"Push failed: {result.stderr}")
            return False
    ui.error("Max retries reached, push aborted.")
    return False


def _push_new_branch_with_retry(branch: str, cwd: str | None = None) -> bool:
    for i, delay in enumerate(RETRY_DELAYS):
        result = _git.push_upstream(branch, cwd=cwd)
        if result.ok:
            return True
        if _is_network_error(result.stderr):
            ui.warn(
                f"Network error, retrying in {delay}s... ({i + 1}/{MAX_RETRIES})"
            )
            time.sleep(delay)
        else:
            ui.error(f"Push failed: {result.stderr}")
            return False
    ui.error("Max retries reached, push aborted.")
    return False


def _check_conflict(cwd: str | None = None) -> list[str]:
    result = _git.unmerged_files(cwd=cwd)
    if result.ok and result.stdout:
        return result.stdout.splitlines()
    return []


def sync_repo(path: str = ".", rebase: bool = False) -> SyncState:
    """Run the sync loop for the repository at *path*.

    Returns the final :class:`SyncState` after the loop completes (or stops
    on an unrecoverable condition).
    """
    ui.start(f"Syncing repository: {path}")

    # --- Prerequisites -------------------------------------------------------
    if not _git.is_git_repo(cwd=path):
        ui.error("Not a git repository.")
        return SyncState.ERROR

    result = _git.status_porcelain(cwd=path)
    if result.ok and result.stdout:
        ui.warn("Uncommitted changes detected. Please commit or stash them first.")
        ui.info(result.stdout)
        return SyncState.UNCOMMITTED

    result = _git.remote_names(cwd=path)
    if not result.ok or not result.stdout:
        ui.warn("No remote repository configured.")
        return SyncState.NO_REMOTE

    # --- Sync loop -----------------------------------------------------------
    while True:
        _git.fetch(cwd=path)

        branch_result = _git.current_branch(cwd=path)
        branch = branch_result.stdout if branch_result.ok else "HEAD"

        upstream_result = _git.get_upstream(cwd=path)
        if not upstream_result.ok:
            ui.start(f'Pushing new branch "{branch}" and setting upstream...')
            ok = _push_new_branch_with_retry(branch, cwd=path)
            if not ok:
                return SyncState.NETWORK_ERROR
            ui.success(f'Branch "{branch}" pushed with upstream configured.')
            continue

        ab = _get_ahead_behind(cwd=path)
        if ab is None:
            ui.error("Failed to determine ahead/behind status.")
            return SyncState.ERROR
        ui.info(
            f"[{branch}] ahead={ab.ahead}  behind={ab.behind}  "
            f"upstream={upstream_result.stdout}"
        )

        if ab.ahead == 0 and ab.behind == 0:
            ui.success("Repository is up to date.")
            return SyncState.UP_TO_DATE

        # Pull when behind (also handles diverged state).
        if ab.behind > 0:
            method = "rebase" if rebase else "merge"
            ui.start(f"Pulling ({method})...")
            pull_result = _git.pull(rebase=rebase, cwd=path)
            if not pull_result.ok:
                conflicted = _check_conflict(cwd=path)
                if conflicted:
                    ui.error("Merge conflict detected in files:")
                    for f in conflicted:
                        ui.info(f"  {f}")
                    ui.warn("Please resolve conflicts manually, then run again.")
                    return SyncState.CONFLICT
                ui.error(f"Pull failed: {pull_result.stderr}")
                return SyncState.ERROR
            ui.success("Pull completed.")
            continue  # re-fetch + re-check (may still need to push)

        # Push when ahead.
        if ab.ahead > 0:
            ui.start("Pushing...")
            ok = _push_with_retry(cwd=path)
            if not ok:
                return SyncState.NETWORK_ERROR
            ui.success("Push completed.")
            continue  # re-fetch + re-check
