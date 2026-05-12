"""Typer CLI entry point for auto-git."""

import typer

from auto_git import ui
from auto_git.sync import SyncState, sync_repo

app = typer.Typer(
    name="auto-git",
    help="Automatically sync a git repository with its remote.",
)


def _exit_code(state: SyncState) -> int:
    mapping = {
        SyncState.UP_TO_DATE: 0,
        SyncState.UNCOMMITTED: 1,
        SyncState.CONFLICT: 1,
        SyncState.NO_REMOTE: 1,
        SyncState.NO_UPSTREAM: 1,
        SyncState.ERROR: 1,
        SyncState.NETWORK_ERROR: 2,
    }
    return mapping.get(state, 1)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    path: str = typer.Argument(".", help="Path to the git repository"),
    rebase: bool = typer.Option(False, "--rebase", help="Use rebase instead of merge when pulling"),
    show_version: bool = typer.Option(False, "--version", help="Show version and exit", is_eager=True),
) -> None:
    """Synchronize the repository at PATH with its remote."""
    if ctx.invoked_subcommand is not None:
        return
    if show_version:
        from importlib.metadata import version as _version
        ui.info(f"auto-git {_version('auto-git')}")
        raise typer.Exit()
    state = sync_repo(path=path, rebase=rebase)
    raise typer.Exit(code=_exit_code(state))
