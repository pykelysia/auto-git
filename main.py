import getopt
import sys
import path
import mode
import util

shortopts = 'd:f'
longopts = ['default', 'fast']

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
    opts, args = getopt.gnu_getopt(sys.argv[1:], shortopts, longopts)
    for o, a in opts:
        if o in ('-d', '--default'):
            path.to_current_path(a)
            mode.default_mode()
            return True
        if o in ('-f', '--fast') :
            mode.default_mode()
            return True
    return False


if __name__ == '__main__':
    util.print_start("Starting...")
    main()
    util.print_end("All done.")
