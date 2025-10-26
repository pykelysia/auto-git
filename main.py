import getopt
import sys
import path
import mode
import util
from path import to_current_path

shortopts = 'dp'
longopts = ['default', 'path']

def main():
    if run_with_cmd():
        return

    # 前往正确的路径
    while True:
        path_str = input("path of git repository: ")
        flag = path.to_current_path(path_str)
        if flag:
            break

    # 选择模式
    mode_select = input("select mode: ")
    # 默认
    if mode_select == "":
        mode.default_mode()

def run_with_cmd()->bool:
    opts, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
    for o, a in opts:
        if o in ('-p', '--path'):
            to_current_path(a)
        if o in ('-d', '--default'):
            mode.default_mode()
            return True
    return False


if __name__ == '__main__':
    util.print_start("Starting...")
    main()
    util.print_end("All done.")
