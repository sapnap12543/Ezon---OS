import time
import random
import string

UI = "=" * 70

# ==================================================
# CLOUD SYSTEM (SAFE STATE MODEL - NO GLOBAL BUGS)
# ==================================================
cloud = {}
active_link = None

SYSTEM = {
    "files": {},
    "buffer": "",
    "vars": {}
}

# ==================================================
# LINK SYSTEM
# ==================================================
def gen_link():
    return "EZON-" + "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

def autosync():
    global active_link

    if active_link is None:
        active_link = gen_link()

    cloud[active_link] = {
        "files": SYSTEM["files"].copy(),
        "buffer": SYSTEM["buffer"],
        "vars": SYSTEM["vars"].copy()
    }

# ==================================================
# BOOT SCREEN
# ==================================================
def boot():
    print(f"""
{UI}
            EZON OS v4.1 (FIXED CORE)
{UI}
Booting system...
Loading modules...
Cloud sync ready...
{UI}
""")
    time.sleep(0.5)

# ==================================================
# HELP MENU
# ==================================================
def help_menu():
    print(f"""
{UI}
EZON OS COMMANDS
{UI}

📁 FILE SYSTEM
  edit        → write buffer
  save name   → save file
  open name   → open file
  dir         → list files
  del name    → delete file

☁️ CLOUD
  /link       → show save link
  /newlink    → create new world
  /load CODE  → load world

🧠 CODER
  run coder   → open mini language

⚙️ SYSTEM
  cls, echo, time, vars, reset, help, exit
{UI}
""")

# ==================================================
# CODER ENGINE (SAFE VERSION)
# ==================================================
def coder():
    print("""
EZON CODER v4.1

say hello
set x 10
add x 5
sub x 2
mul x 2
div x 2

if x equals 20
/view
/exit
""")

    vars_ = SYSTEM["vars"]
    memory = []

    while True:
        parts = input("coder> ").split()
        if not parts:
            continue

        cmd = parts[0]
        args = parts[1:]

        memory.append(" ".join(parts))

        if cmd == "/exit":
            autosync()
            break

        elif cmd == "/view":
            print(vars_)

        elif cmd == "say":
            print(">>", " ".join(args))

        elif cmd == "set":
            vars_[args[0]] = int(args[1])

        elif cmd == "add":
            vars_[args[0]] = vars_.get(args[0], 0) + int(args[1])

        elif cmd == "sub":
            vars_[args[0]] = vars_.get(args[0], 0) - int(args[1])

        elif cmd == "mul":
            vars_[args[0]] = vars_.get(args[0], 0) * int(args[1])

        elif cmd == "div":
            vars_[args[0]] = vars_.get(args[0], 0) // int(args[1])

        elif cmd == "if":
            if len(args) >= 3:
                if args[1] == "equals":
                    if vars_.get(args[0]) == int(args[2]):
                        print("TRUE")
                    else:
                        print("FALSE")

        else:
            print("unknown")

# ==================================================
# CLOUD FUNCTIONS (NO GLOBAL ERROR RISK)
# ==================================================
def show_link():
    print(active_link if active_link else "No save yet")

def new_link():
    global active_link
    active_link = gen_link()
    autosync()
    print("NEW LINK:")
    print(active_link)

def load_link(code):
    global active_link

    if code not in cloud:
        print("Invalid link")
        return

    data = cloud[code]

    SYSTEM["files"] = data["files"].copy()
    SYSTEM["buffer"] = data["buffer"]
    SYSTEM["vars"] = data["vars"].copy()

    active_link = code
    print("Loaded:", code)

# ==================================================
# MAIN LOOP
# ==================================================
def main():
    boot()

    history = []

    while True:
        cmd = input("EZON> ").strip()
        history.append(cmd)

        parts = cmd.split()
        if not parts:
            continue

        c = parts[0]
        a = parts[1:]

        # EXIT
        if c == "exit":
            break

        # HELP
        elif c == "help":
            help_menu()

        # FILE SYSTEM
        elif c == "edit":
            SYSTEM["buffer"] = input("text: ")
            autosync()

        elif c == "save":
            SYSTEM["files"][a[0]] = SYSTEM["buffer"]
            autosync()

        elif c == "open":
            print(SYSTEM["files"].get(a[0], "not found"))

        elif c == "dir":
            print(list(SYSTEM["files"].keys()))

        elif c == "del":
            SYSTEM["files"].pop(a[0], None)
            autosync()

        # CLOUD
        elif c == "/link":
            show_link()

        elif c == "/newlink":
            new_link()

        elif c == "/load":
            load_link(a[0])

        # SYSTEM TOOLS
        elif c == "cls":
            print("\n" * 50)

        elif c == "echo":
            print(">>", " ".join(a))

        elif c == "time":
            print(time.strftime("%H:%M:%S"))

        elif c == "vars":
            print(SYSTEM["vars"])

        elif c == "reset":
            SYSTEM["files"].clear()
            SYSTEM["vars"].clear()
            SYSTEM["buffer"] = ""
            print("system reset")

        # CODER
        elif c == "run":
            if a and a[0] == "coder":
                coder()

        else:
            print("unknown command")

main()