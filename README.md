# Auto-Git

***pyke elysia***

自动同步本地 Git 仓库与远程仓库，自动检测仓库状态并执行相应的操作（fetch / pull / push），在网络不稳定时自动重试。

## 开发原因

由于家中网络问题，不得不多次进行 `git push` 操作，
每次 `push` 失败就要消耗不少时间。

因此开发了较为自动化的 `git` 同步脚本，自动检测仓库状态并执行需要的操作，
在网络不稳定时自动重试。

## 项目结构

```
auto-git/
├── src/
│   └── auto_git/
│       ├── __init__.py
│       ├── __main__.py     # python -m auto_git 入口
│       ├── cli.py          # typer CLI 入口
│       ├── sync.py         # 同步状态机核心逻辑
│       ├── git.py          # git 子进程封装
│       └── ui.py           # 格式化输出
├── tests/
├── pyproject.toml
└── README.md
```

## 使用

### 前置要求

- Python >= 3.11
- [uv](https://docs.astral.sh/uv/)（推荐）或 pip

### 从源码运行

```shell
# 安装依赖
uv sync

# 同步当前目录的仓库
uv run auto-git

# 同步指定路径的仓库
uv run auto-git /path/to/git/repo

# 使用 rebase 替代 merge 进行拉取
uv run auto-git --rebase

# 查看版本
uv run auto-git --version
```

### 安装后使用

```shell
# 安装到当前 virtualenv
uv pip install -e .

# 直接使用
auto-git [PATH] [--rebase]
```

### 打包

```shell
pip install pyinstaller
pyinstaller -F src/auto_git/__main__.py -n auto-git
```

## 功能

- 自动检测仓库状态（ahead / behind / diverged / up-to-date）
- 拉取远程变更（merge 模式，可通过 `--rebase` 切换）
- 推送本地变更，网络错误自动重试（指数退避，最多 5 次）
- 合并冲突检测并给出明确提示
- 未提交变更时警告并跳过
- 跨平台支持（Linux / Windows / macOS）

***创建于2025/8/8***
