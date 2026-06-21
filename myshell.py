import os
from colorama import init, Fore, Back, Style

# Initialize colorama (autoreset ensures colors reset after every print statement)
init(autoreset=True)
print(Fore.RED + "This text is red!")


def parse_input(command):
    input_arr = command.split(" ")

    cli_input = input_arr[0]
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
            os.chdir(input_arr[1])
            return True
        
        case "pwd":
            print(Style.BRIGHT + Fore.GREEN + os.getcwd())
            return True
        
        case _:
            print('Unknown command. Use "help" to list usable commands.')
            return True

while True:
    print(Style.BRIGHT + Fore.YELLOW + "user@myshell:~$ ", end="")
    command = input()

    if command.strip() == "":
        continue

    elif command == "help":
        print("Available commands:")
        print("- help")
        print("- exit")


    else:
        next = parse_input(command)

        if next is False:
            break