import os
from pathlib import Path
import shlex
from colorama import init, Fore, Back, Style

# Initialize colorama (autoreset ensures colors reset after every print statement)
init(autoreset=True)
print(Fore.RED + "This text is red!")

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

    target = ""

    cli_input = input_arr[0]
    for data in input_arr:
        if data and (data[0] == "/" or data[0] == "\\") :
            target = Path(data)

        
    # for n in input_arr:
    #     print(n, end="|")
    # os.getcwd()       # membaca direktori aktif
    # os.chdir("folder") # mengganti direktori aktif shell Python
    # os.listdir(".")   # melihat isi folder
    # os.mkdir("test")  # membuat folder
    # os.remove("a.txt") # menghapus file   

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
            return True
        
        case "cp":
            for n in input_arr:
                print(n, end=" ")
            return True
        
        case "ls": #todo : ubah ls jadi fork process
            data = os.listdir(".")
            for file in data :
                if os.path.isdir(file):
                    print(Style.BRIGHT + Fore.CYAN + file)
                else :
                    print(file)
            return True

        case "cd":
            if len(input_arr) < 2:
                print("cd: missing directory")
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
            print(f'{cli_input} : Unknown command. Use "help" to list usable commands.')
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