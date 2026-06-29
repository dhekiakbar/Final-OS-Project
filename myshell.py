import os
import shutil
import subprocess
from pathlib import Path
from colorama import init, Fore, Style

# =====================================================
# INITIALIZATION
# =====================================================

init(autoreset=True)

print(Fore.CYAN + "=" * 50)
print(Fore.CYAN + "             MyShell v1.0")
print(Fore.CYAN + "=" * 50)
print(Fore.YELLOW + "Type 'help' to show available commands.\n")


# =====================================================
# INPUT TOKENIZER
# =====================================================

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


# =====================================================
# HELP
# =====================================================

def show_help():

    print(Style.BRIGHT + Fore.GREEN)
    print("\n============== HELP MENU ==============\n")

    print(Fore.GREEN +"BUILT-IN COMMANDS")
    print("")

    print("help")
    print("  Menampilkan seluruh command.\n")

    print("exit")
    print("  Keluar dari shell.\n")

    print("cd <directory>")
    print("  Berpindah direktori.")
    print("  Contoh: cd Documents\n")

    print("pwd")
    print("  Menampilkan direktori aktif.\n")

    print(Fore.GREEN + "EXTERNAL COMMANDS")
    print("")

    print("ls")
    print("  Menampilkan isi direktori.\n")

    print("ls -la")
    print("  Menampilkan seluruh file termasuk hidden file.\n")

    print("mkdir <folder>")
    print("  Membuat folder baru.\n")

    print("touch <file>")
    print("  Membuat file kosong.\n")

    print("cp <source> <destination>")
    print("  Menyalin file atau folder.\n")

    print("mv <source> <destination>")
    print("  Memindahkan file/folder.\n")

    print("rm <file>")
    print("  Menghapus file.\n")

    print("rm -r <folder>")
    print("  Menghapus folder beserta isinya.\n")

    print("clear")
    print("  Membersihkan layar terminal.\n")

    print("cat <file>")
    print("  Menampilkan isi file.\n")

    print("nano <file>")
    print("  Membuka file menggunakan Notepad.\n")

    print(Fore.GREEN + "ADVANCED FEATURES")
    print("")

    print("command > file")
    print("  Redirect output ke file.")
    print("  Contoh: ls > hasil.txt\n")

    print("command < file")
    print("  Redirect input dari file.")
    print("  Contoh: cat < data.txt\n")

    print("command1 | command2")
    print("  Menghubungkan output command pertama")
    print("  menjadi input command kedua.")
    print("  Contoh: ls | help\n")


# =====================================================
# WINDOWS COMMAND TRANSLATOR
# =====================================================

def translate_command(args):

    if len(args) == 0:
        return args

    cmd = args[0]

    # ls
    if cmd == "ls":

        if len(args) > 1 and args[1] == "-la":
            return ["cmd", "/c", "dir", "/a"]

        return ["cmd", "/c", "dir"]

    # clear
    elif cmd == "clear":
        return ["cmd", "/c", "cls"]

    # nano
    elif cmd == "nano":
        return ["notepad"] + args[1:]

    return args


# =====================================================
# EXTERNAL COMMAND
# =====================================================

def execute_external(args):

    args = translate_command(args)

    try:
        subprocess.run(args)

    except FileNotFoundError:
        print(Fore.RED + f"{args[0]}: command not found")

    except Exception as e:
        print(Fore.RED + str(e))


# =====================================================
# OUTPUT / INPUT REDIRECTION
# =====================================================

def execute_redirection(args):

    # OUTPUT >
    if ">" in args:

        idx = args.index(">")

        command = translate_command(args[:idx])
        filename = args[idx + 1]

        try:
            with open(filename, "w", encoding="utf-8") as f:
                subprocess.run(command, stdout=f)

        except Exception as e:
            print(Fore.RED + str(e))

        return True

    # INPUT <
    elif "<" in args:

        idx = args.index("<")

        command = translate_command(args[:idx])
        filename = args[idx + 1]

        try:
            with open(filename, "r", encoding="utf-8") as f:
                subprocess.run(command, stdin=f)

        except Exception as e:
            print(Fore.RED + str(e))

        return True

    return False


# =====================================================
# PIPE
# =====================================================

def execute_pipe(args):

    if "|" not in args:
        return False

    idx = args.index("|")

    cmd1 = translate_command(args[:idx])
    cmd2 = translate_command(args[idx + 1:])

    try:

        p1 = subprocess.Popen(
            cmd1,
            stdout=subprocess.PIPE,
            text=True
        )

        p2 = subprocess.Popen(
            cmd2,
            stdin=p1.stdout
        )

        p1.stdout.close()
        p2.communicate()

    except Exception as e:
        print(Fore.RED + str(e))

    return True


# =====================================================
# PARSER
# =====================================================

def parse_input(command):

    args = split_input(command)

    if len(args) == 0:
        return True

    cmd = args[0]

    # =============================================
    # BUILT-IN COMMANDS
    # =============================================

    if cmd == "exit":
        print(Fore.RED + "Leaving Shell...")
        return False

    elif cmd == "help":
        show_help()
        return True

    elif cmd == "pwd":
        print(
            Style.BRIGHT +
            Fore.GREEN +
            os.getcwd()
        )
        return True

    elif cmd == "cd":

        # cd tanpa argumen -> home
        if len(args) == 1:
            os.chdir(Path.home())
            return True

        target = Path(args[1])

        if not target.exists():
            print(Fore.RED + "cd: directory not found")

        elif not target.is_dir():
            print(Fore.RED + "cd: not a directory")

        else:
            os.chdir(target)

        return True

    # =============================================
    # CP
    # =============================================

    elif cmd == "cp":

        if len(args) < 3:
            print("Usage: cp <source> <destination>")
            return True

        source = args[1]
        destination = args[2]

        try:

            if os.path.isdir(source):
                shutil.copytree(source, destination)

            else:
                shutil.copy2(source, destination)

        except Exception as e:
            print(Fore.RED + str(e))

        return True

    # =============================================
    # TOUCH
    # =============================================

    elif cmd == "touch":

        if len(args) < 2:
            print("Usage: touch <filename>")
            return True

        try:
            Path(args[1]).touch()

        except Exception as e:
            print(Fore.RED + str(e))

        return True

    # =============================================
    # RM
    # =============================================

    elif cmd == "rm":

        if len(args) < 2:
            print("Usage: rm <file>")
            return True

        try:

            if args[1] == "-r":

                if len(args) < 3:
                    print("Usage: rm -r <folder>")
                    return True

                shutil.rmtree(args[2])

            else:
                os.remove(args[1])

        except Exception as e:
            print(Fore.RED + str(e))

        return True

    # =============================================
    # CAT
    # =============================================

    elif cmd == "cat":

        if len(args) < 2:
            print("Usage: cat <file>")
            return True

        try:

            with open(args[1], "r", encoding="utf-8") as f:
                print(f.read())

        except Exception as e:
            print(Fore.RED + str(e))

        return True

    # =============================================
    # MV
    # =============================================

    elif cmd == "mv":

        if len(args) < 3:
            print("Usage: mv <source> <destination>")
            return True

        try:
            shutil.move(args[1], args[2])

        except Exception as e:
            print(Fore.RED + str(e))

        return True

    # =============================================
    # ADVANCED FEATURES
    # =============================================

    if execute_pipe(args):
        return True

    if execute_redirection(args):
        return True

    # =============================================
    # EXTERNAL COMMAND
    # =============================================

    execute_external(args)

    return True


# =====================================================
# MAIN LOOP (REPL)
# =====================================================

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

        if command.strip() == "":
            continue

        if not parse_input(command):
            break

    except KeyboardInterrupt:
        print(Fore.RED + "\n(use 'exit' to quit)")

    except EOFError:
        print()
        break