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
                                   stderr=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   encoding= "gbk")
        error = responses.stderr
        output = responses.stdout
        if responses.returncode == 0:
            util.print_success("Push over.")
            break
        else:
            check_output(error)
    util.print_end("Push git repository.")


def check_output(output: str):
    # 128
    if output.find("Connection was reset") != -1:
        util.print_error("Connect was reset.")
    # 128
    elif output.find("Could not connect to server") != -1:
        util.print_error("Could not connect to server.")
    # 128
    elif output.find("Could not resolve host") != -1:
        util.print_error("Could not resolve host.")
    else:
        util.print_error("Unknow wrong.")

if __name__ == '__main__':
    say_name()