while True:
    command = input("user@myshell:~$ ")

    if command.strip() == "":
        continue

    elif command == "exit":
        break

    elif command == "help":
        print("Available commands:")
        print("- help")
        print("- exit")

    else:
        print('Unknown command. Use "help" to list usable commands.')