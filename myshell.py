import os
from pathlib import Path
from colorama import init, Fore, Style

# ==========================================
# INITIALIZATION
# ==========================================

init(autoreset=True)

print(Fore.CYAN + "===================================")
print(Fore.CYAN + "          MyShell v1.0             ")
print(Fore.CYAN + "===================================")
print(Fore.YELLOW + "Type 'help' to see available commands.\n")


# ==========================================
# INPUT TOKENIZER
# ==========================================

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


# ==========================================
# HELP
# ==========================================

def show_help():

    print(Style.BRIGHT + Fore.GREEN +
          "\n=========== HELP ===========\n")

    print("BUILT-IN COMMANDS\n")

    print("help")
    print("  Menampilkan seluruh command.\n")

    print("exit")
    print("  Keluar dari shell.\n")

    print("cd <directory>")
    print("  Berpindah direktori.")
    print("  Contoh: cd Documents\n")

    print("pwd")
    print("  Menampilkan direktori aktif.\n")

    print("----------------------------------")

    print("\nEXTERNAL COMMANDS\n")

    print("ls")
    print("  Menampilkan isi direktori.\n")

    print("ls -la")
    print("  Menampilkan seluruh file termasuk hidden file.\n")

    print("mkdir <folder>")
    print("  Membuat direktori baru.\n")

    print("touch <file>")
    print("  Membuat file kosong.\n")

    print("cp <source> <destination>")
    print("  Menyalin file.\n")

    print("mv <source> <destination>")
    print("  Memindahkan file.\n")

    print("rm <file>")
    print("  Menghapus file.\n")

    print("rm -r <folder>")
    print("  Menghapus direktori beserta isinya.\n")

    print("clear")
    print("  Membersihkan layar terminal.\n")

    print("cat <file>")
    print("  Menampilkan isi file.\n")

    print("nano <file>")
    print("  Mengedit file menggunakan nano.\n")

    print("----------------------------------")

    print("\nADVANCED FEATURES\n")

    print("command > file")
    print("  Redirect output ke file.")
    print("  Contoh: ls > hasil.txt\n")

    print("command < file")
    print("  Redirect input dari file.")
    print("  Contoh: cat < data.txt\n")

    print("command1 | command2")
    print("  Menghubungkan output command pertama")
    print("  menjadi input command kedua.")
    print("  Contoh: ls | grep txt\n")


# ==========================================
# EXTERNAL COMMAND
# fork + execvp + waitpid
# ==========================================

def execute_external(args):

    pid = os.fork()

    # CHILD PROCESS
    if pid == 0:

        try:
            os.execvp(args[0], args)

        except FileNotFoundError:
            print(f"{args[0]}: Command not found")

        except Exception as e:
            print("Execution Error:", e)

        os._exit(1)

    # PARENT PROCESS
    else:
        os.waitpid(pid, 0)


# ==========================================
# REDIRECTION
# ==========================================

def execute_redirection(args):

    if ">" in args:

        index = args.index(">")

        command = args[:index]
        filename = args[index + 1]

        pid = os.fork()

        if pid == 0:

            fd = os.open(
                filename,
                os.O_WRONLY |
                os.O_CREAT |
                os.O_TRUNC,
                0o644
            )

            os.dup2(fd, 1)
            os.close(fd)

            os.execvp(command[0], command)

        else:
            os.waitpid(pid, 0)

        return True

    elif "<" in args:

        index = args.index("<")

        command = args[:index]
        filename = args[index + 1]

        pid = os.fork()

        if pid == 0:

            fd = os.open(filename, os.O_RDONLY)

            os.dup2(fd, 0)
            os.close(fd)

            os.execvp(command[0], command)

        else:
            os.waitpid(pid, 0)

        return True

    return False


# ==========================================
# PIPE
# ==========================================

def execute_pipe(args):

    if "|" not in args:
        return False

    index = args.index("|")

    cmd1 = args[:index]
    cmd2 = args[index + 1:]

    read_fd, write_fd = os.pipe()

    pid1 = os.fork()

    # CHILD 1
    if pid1 == 0:

        os.dup2(write_fd, 1)

        os.close(read_fd)
        os.close(write_fd)

        os.execvp(cmd1[0], cmd1)

    pid2 = os.fork()

    # CHILD 2
    if pid2 == 0:

        os.dup2(read_fd, 0)

        os.close(read_fd)
        os.close(write_fd)

        os.execvp(cmd2[0], cmd2)

    os.close(read_fd)
    os.close(write_fd)

    os.waitpid(pid1, 0)
    os.waitpid(pid2, 0)

    return True


# ==========================================
# PARSER
# ==========================================

def parse_input(command):

    args = split_input(command)

    if len(args) == 0:
        return True

    cmd = args[0]

    match cmd:

        # =====================
        # EXIT
        # =====================
        case "exit":
            print(Fore.RED + "Leaving shell...")
            return False

        # =====================
        # HELP
        # =====================
        case "help":
            show_help()
            return True

        # =====================
        # CD
        # =====================
        case "cd":

            # cd tanpa argumen -> HOME
            if len(args) == 1:

                os.chdir(Path.home())
                return True

            try:
                os.chdir(args[1])

            except FileNotFoundError:
                print("cd: no such directory")

            except NotADirectoryError:
                print("cd: not a directory")

            return True

        # =====================
        # PWD
        # =====================
        case "pwd":

            print(
                Style.BRIGHT +
                Fore.GREEN +
                os.getcwd()
            )

            return True

        # =====================
        # EXTERNAL COMMAND
        # =====================
        case _:

            # PIPE
            if execute_pipe(args):
                return True

            # REDIRECTION
            if execute_redirection(args):
                return True

            # NORMAL COMMAND
            execute_external(args)

            return True


# ==========================================
# MAIN REPL LOOP
# ==========================================

while True:

    try:

        current_dir = os.getcwd()

        print(
            Style.BRIGHT +
            Fore.YELLOW +
            f"user@myshell:{current_dir}$ ",
            end=""
        )

        command = input()

        # kosong
        if command.strip() == "":
            continue

        if not parse_input(command):
            break

    except KeyboardInterrupt:
        print("\n(use 'exit' to quit)")

    except EOFError:
        print()
        break