import os
import subprocess
from pathlib import Path
from colorama import init, Fore, Back, Style

init(autoreset=True)
# print(Fore.RED + "This text is red!")

def split_input(command):
    result = []
    current = ""
    in_quote = False
    quote_char = None

    for c in command:
        if c in ("'", '"'):
            if in_quote and c == quote_char:
                in_quote = False
                quote_char = None
            elif not in_quote:
                in_quote = True
                quote_char = c
            else:
                current += c
        elif c == " " and not in_quote:
            if current:
                result.append(current)
                current = ""
        else:
            current += c

    if current:
        result.append(current)

    return result

def parse_input(command):
    input_arr = split_input(command)

    if not input_arr:
        return True

    cli_input = input_arr[0]

    # for n in input_arr:
    #     print(n, end="|")

    # os.getcwd()       # membaca direktori aktif
    # os.chdir("folder") # mengganti direktori aktif shell Python
    # os.listdir(".")   # melihat isi folder
    # os.mkdir("test")  # membuat folder
    # os.remove("a.txt") # menghapus file

    #update new
    # os.fork() ditangani oleh subprocess.run()
    
    match cli_input:
        case "exit":
            print("Leaving Shell....")
            return False

        case "help":
            print("Commands:")
            print("- help")
            print("- exit")
            print("- cd <dir>")
            print("- cp <origin_dir> <destination>")
            print("- pwd")
            print("- ls")
            print("- ls -la")
            print("- mkdir")
            print("- touch")
            print("- rm")
            print("- rm -r")
            return True

        case "cd":
            if len(input_arr) < 2:
                os.chdir(Path.home())
                return True
            target = Path(input_arr[1])
            if not target.exists():
                print("cd: not found")
            elif not target.is_dir():
                print("cd: not a directory")
            else:
                os.chdir(target)
            return True

        case "pwd":
            print(Style.BRIGHT + Fore.GREEN + os.getcwd())
            return True

        case _:
            try:
                result = subprocess.run(input_arr)
                if result.returncode != 0:
                    print(f"{cli_input}: exited with code {result.returncode}")
            except FileNotFoundError:
                print(f'{cli_input}: command not found. Use "help" to list usable commands.')
            return True


while True:
    try:
        print(Style.BRIGHT + Fore.YELLOW + "user@myshell:~$ ", end="")
        command = input()

        if command.strip() == "":
            continue

        if not parse_input(command):
            break

    except KeyboardInterrupt:
        print("\n(use 'exit' to quit)")