import time
import math
import random
import string

UI = "=" * 45

# ==================================================
# CLOUD STORAGE (IN MEMORY ONLY)
# ==================================================
cloud = {}
active_code = None

current = {
    "files": {},
    "buffer": "",
    "vars": {}
}

# ==================================================
# LINK SYSTEM
# ==================================================
def make_code():
    return "EZON-" + "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

def auto_sync():
    global active_code

    if not active_code:
        active_code = make_code()

    cloud[active_code] = {
        "files": current["files"].copy(),
        "buffer": current["buffer"],
        "vars": current["vars"].copy()
    }

# ==================================================
# BOOT
# ==================================================
def boot():
    print(f"""
{UI}
        EZON OS (CLOUD SYNC EDITION)
{UI}
Booting system...
Loading cloud engine...
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
  dir         → list files
  open <file> → open file
  save <file> → save buffer
  edit        → edit text
  del <file>  → delete file

☁️ CLOUD LINKS
  /link       → show current save link
  /newlink    → create new save link
  /load CODE  → load save link

🧠 CODER
  run coder   → EZON coding system

⚙️ SYSTEM
  help
  exit
{UI}
""")

# ==================================================
# CODER (EZON LANGUAGE)
# ==================================================
def coder_app():

    print(f"""
{UI}
EZON CODER
{UI}

say hello
ask name
show name

set x 10
add x 5
sub x 2

/view
/exit
{UI}
""")

    variables = current["vars"]

    while True:
        line = input("Coder> ").split()
        if not line:
            continue

        c = line[0]
        a = line[1:]

        if c == "/exit":
            auto_sync()
            break

        elif c == "/view":
            print("\nVARIABLES")
            for k, v in variables.items():
                print(k, "=", v)

        elif c == "say":
            print(">>", " ".join(a))

        elif c == "ask":
            variables[a[0]] = input(a[0] + ": ")
            auto_sync()

        elif c == "show":
            print(variables.get(a[0], "undefined"))

        elif c == "set":
            variables[a[0]] = int(a[1])
            auto_sync()

        elif c == "add":
            variables[a[0]] = variables.get(a[0], 0) + int(a[1])
            auto_sync()

        elif c == "sub":
            variables[a[0]] = variables.get(a[0], 0) - int(a[1])
            auto_sync()

        else:
            print("unknown")

# ==================================================
# CLOUD FUNCTIONS
# ==================================================
def show_link():
    print(active_code if active_code else "No save yet")

def new_link():
    global active_code
    active_code = make_code()
    auto_sync()
    print("NEW LINK CREATED:")
    print(active_code)

def load_link(code):
    global active_code

    if code not in cloud:
        print("Invalid link")
        return

    data = cloud[code]

    current["files"] = data["files"].copy()
    current["buffer"] = data["buffer"]
    current["vars"] = data["vars"].copy()

    active_code = code

    print("Loaded:", code)

# ==================================================
# START
# ==================================================
boot()

while True:

    raw = input("EZON> ").strip()
    parts = raw.split()

    if not parts:
        continue

    cmd = parts[0]
    args = parts[1:]

    # EXIT
    if cmd == "exit":
        break

    # HELP
    elif cmd == "help":
        help_menu()

    # FILE SYSTEM
    elif cmd == "dir":
        print(list(current["files"].keys()))

    elif cmd == "open":
        print(current["files"].get(args[0], "not found"))

    elif cmd == "save":
        current["files"][args[0]] = current["buffer"]
        auto_sync()

    elif cmd == "edit":
        current["buffer"] = input("text: ")
        auto_sync()

    elif cmd == "del":
        current["files"].pop(args[0], None)
        auto_sync()

    # CLOUD
    elif cmd == "/link":
        show_link()

    elif cmd == "/newlink":
        new_link()

    elif cmd == "/load":
        if args:
            load_link(args[0])
        else:
            print("Usage: /load CODE")

    # CODER
    elif cmd == "run":
        if args[0] == "coder":
            coder_app()

    else:
        print("unknown command")