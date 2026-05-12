# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Auto-Git is a Python CLI tool that automates `git push` for unreliable networks. It loops retrying pushes until they succeed, handling transient errors like connection resets and DNS failures. Targets Windows (uses `gbk` encoding).

## Commands

```bash
# Run from source
python main.py

# CLI mode — specify repo path and push automatically
python main.py -d <repo-path>

# Fast mode — push the current directory's repo
python main.py -f

# Build standalone executable
pip install pyinstaller
pyinstaller -F main.py
```

## Architecture

- `main.py` — Entry point. Parses CLI args (`-d`/`--default <path>`, `-f`/`--fast`) or runs interactively (prompts for path, then mode).
- `path.py` — Directory navigation. Validates path exists and `os.chdir`s into it.
- `mode/` — Push strategy package:
  - `default_mode.py` — Core loop: verify git repo → `git push` → on failure, classify error and retry.
  - `check.py` — Git repo detection via `.git` dir check or `git rev-parse --git-dir`.
  - `mode_select.py` — Stub for future mode selection.
- `util/__print__.py` — Logging helpers: `print_start`, `print_success`, `print_error`, `print_warning`, `print_info` with bracketed level tags.

## Key Details

- The main loop in `default_mode.py` calls `git push` with `shell=True` and `encoding="gbk"`. Error output is parsed against known failure strings (connection reset, server unreachable, DNS failure). Unknown errors fall through to retry.
- `-f`/`--fast` runs default mode in current directory without path prompt.
- `-d`/`--default` combines path navigation and default mode in one command.
