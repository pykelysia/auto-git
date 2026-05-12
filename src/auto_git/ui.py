"""Formatted console output."""


def start(message: str) -> None:
    print(f"[start]   {message}")


def end(message: str) -> None:
    print(f"[end]     {message}")


def success(message: str) -> None:
    print(f"[success] {message}")


def error(message: str) -> None:
    print(f"[error]   {message}")


def warn(message: str) -> None:
    print(f"[warning] {message}")


def info(message: str) -> None:
    print(f"[info]    {message}")
