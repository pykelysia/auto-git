import path
import mode
import util


def main():
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

if __name__ == '__main__':
    util.print_start("Starting...")
    main()
    util.print_end("All done.")
