import os
import subprocess

def print_in_cmd(command: str):
    responses = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(responses.communicate()[0].decode("gbk"))
    print(responses.communicate()[1].decode("gbk"))

def main():
    mode_select = input("select mode: \n")
    print_in_cmd(mode_select)

if __name__ == '__main__':
    main()
    print("end")

# (base) PS D:\note> git push
# fatal: unable to access 'https://github.com/pykelysia/note.git/': Failed to connect to github.com port 443 after 2088 ms: Could not connect to server
# (base) PS D:\note> git push
# Enumerating objects: 8, done.
# Counting objects: 100% (8/8), done.
# Delta compression using up to 28 threads
# Compressing objects: 100% (6/6), done.
# Writing objects: 100% (6/6), 1.23 KiB | 1.23 MiB/s, done.
# Total 6 (delta 1), reused 0 (delta 0), pack-reused 0 (from 0)
# remote: Resolving deltas: 100% (1/1), completed with 1 local object.
# To https://github.com/pykelysia/note.git
#    779cc64..4cca2a5  main -> main