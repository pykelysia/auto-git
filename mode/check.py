import os
import subprocess


# 查看目录是否是 Git 仓库
# return
# - False -> 不是 Git 仓库
# - True  -> 是 Git 仓库
def is_git_repository():
    """
    检查当前目录是否已经初始化为 Git 仓库
    
    Returns:
        bool: 如果当前目录是 Git 仓库则返回 True，否则返回 False
    """
    try:
        # 检查是否存在 .git 目录
        if os.path.isdir('.git'):
            return True
        
        # 或者使用 git 命令检查
        result = subprocess.run(['git', 'rev-parse', '--git-dir'], 
                                capture_output=True, 
                                text=True)
        return result.returncode == 0
    except Exception:
        return False


# 获取Git仓库根目录
# return
# - None -> 不是 Git 仓库
# - str -> Git 仓库根目录的绝对路径
def get_git_root():
    """
    获取 Git 仓库的根目录路径
    
    Returns:
        str: Git 仓库根目录的绝对路径，如果不是 Git 仓库则返回 None
    """
    try:
        result = subprocess.run(['git', 'rev-parse', '--show-toplevel'], 
                                capture_output=True, 
                                text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except Exception:
        return None