import subprocess
import util
from mode import check


def say_name():
    print("hello, default_mode.py")


def default_mode():
    """
    默认模式：
    默认为在该目录下推送 git，
    不断推送，直到推送成功。
    """
    util.print_success("Get into default mode.")

    """
    优先确保位于存在 Git 仓库的目录下。
    """
    # 检查是否为 Git 仓库
    util.print_start("Check git repository.")

    # 是 Git 仓库
    if check.is_git_repository():
        util.print_success("This is a git repository.")

    # 不是 Git 仓库
    else:
        util.print_error("This is not a git repository.")
        util.print_warning("Please change directory to a git repository.")
        return

    util.print_end("Check git repository.")
    # 检查结束


    """
    由于会遇到若干的原因导致推送失败，
    所以要多次推送以完成任务。
    """
    # 开始执行默认推送
    util.print_start("Push git repository.")
    is_push_over = False # 标记是否推送完毕

    while not is_push_over:
        responses = subprocess.run(["git", "push"],
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   encoding= "gbk")
        output = responses.stdout
        output_code = check_output(output)
        if output_code == -1:
            return
        if output_code == 0:
            is_push_over = True

    util.print_end("Push git repository.")


def check_output(output: str) -> int:
    """
    分析输出，确定情况
    return:
     -1：出现未知错误;
      0: 已经是最新状态;
      1: 网络链接重置;
    """
    if output.find("Everything up-to-date") != -1:
        util.print_success("Remote repository is latest.")
        return 0
    if output.find("Connect was reset") != -1:
        util.print_error("Push error: Connect was reset.")
        return 1
    if output.find("Could not connect to server") != -1:
        util.print_error("Push error: Could not connect to server.")
        return 2
    if output.find("completed") != -1:
        util.print_success("Push successfully.")
        return 3
    util.print_error("Push error: unknow wrong.")
    return -1


if __name__ == '__main__':
    say_name()