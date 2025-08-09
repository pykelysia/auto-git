import subprocess
import os


def to_current_path(path: str) -> bool:
    """
    前往指定的 git 位置
    return:
    - False -> 出现错误
    - True  -> 进入成功
    """
    if not os.path.exists(path):
        print("path not exists")
        return False
    try:
        os.chdir(path)
        print(f"进入目录：{os.getcwd()}")
        return True
    except Exception as e:
        print(f"切换出错：{e}")
        return False


if __name__ == "__main__":
    path = input("path of git repository: ")
    to_current_path(path = path)