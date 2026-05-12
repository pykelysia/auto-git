"""Thin wrappers around git subprocess commands.

Each function returns a ``GitResult`` named tuple with:
- ``ok`` — whether the command succeeded (exit code 0)
- ``stdout`` / ``stderr`` — captured output
"""

import subprocess
from typing import NamedTuple


class GitResult(NamedTuple):
    ok: bool
    stdout: str
    stderr: str


def _run(*args: str, cwd: str | None = None) -> GitResult:
    proc = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    return GitResult(
        ok=proc.returncode == 0,
        stdout=proc.stdout.strip(),
        stderr=proc.stderr.strip(),
    )


def fetch(cwd: str | None = None) -> GitResult:
    return _run("fetch", "--all", cwd=cwd)


def rev_list_count(left: str, right: str, cwd: str | None = None) -> GitResult:
    return _run("rev-list", "--left-right", "--count", f"{left}...{right}", cwd=cwd)


def status_porcelain(cwd: str | None = None) -> GitResult:
    return _run("status", "--porcelain", cwd=cwd)


def pull(rebase: bool = False, cwd: str | None = None) -> GitResult:
    if rebase:
        return _run("pull", "--rebase", cwd=cwd)
    return _run("pull", "--no-rebase", cwd=cwd)


def push(cwd: str | None = None) -> GitResult:
    return _run("push", cwd=cwd)


def current_branch(cwd: str | None = None) -> GitResult:
    return _run("rev-parse", "--abbrev-ref", "HEAD", cwd=cwd)


def remote_names(cwd: str | None = None) -> GitResult:
    return _run("remote", cwd=cwd)


def is_git_repo(cwd: str | None = None) -> bool:
    return _run("rev-parse", "--git-dir", cwd=cwd).ok


def get_upstream(cwd: str | None = None) -> GitResult:
    return _run("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}", cwd=cwd)


def unmerged_files(cwd: str | None = None) -> GitResult:
    return _run("diff", "--name-only", "--diff-filter=U", cwd=cwd)
