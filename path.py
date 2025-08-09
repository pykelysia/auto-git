import subprocess

# 前往指定的 git 位置
def to_current_path(path: str) -> bool:
    response = subprocess.run(["cd", path], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if response.returncode != 0:
        error = response.stderr.decode("gbk")
        print(error)
        return False
    else:
        output = response.stdout.decode("gbk")
        print(output)
        return True


if __name__ == "__main__":
    path = input("path of git repository: ")
    to_current_path(path = path)