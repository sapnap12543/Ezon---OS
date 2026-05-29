import os
import json
import time
import math

# ==================================================
# ROOT (DO NOT CHANGE NAME)
# ==================================================
BASE_DIR = "ezon_users (please don't touch)"
os.makedirs(BASE_DIR, exist_ok=True)

UI = "========================================"

# ==================================================
# USER DB
# ==================================================
USER_DB_FILE = os.path.join(BASE_DIR, "users.json")

if os.path.exists(USER_DB_FILE):
    with open(USER_DB_FILE, "r") as f:
        users = json.load(f)
else:
    users = {"admin": {"password": "1234", "role": "admin"}}
    with open(USER_DB_FILE, "w") as f:
        json.dump(users, f)

def save_users():
    with open(USER_DB_FILE, "w") as f:
        json.dump(users, f)

# ==================================================
# BOOT
# ==================================================
def boot():
    print(f"""
{UI}
            ⚡ EZON OS ⚡
{UI}
Booting system...
Loading modules...
Starting...
{UI}
""")
    time.sleep(0.8)

# ==================================================
# SIGNUP
# ==================================================
def signup():
    print(f"\n{UI}\nCREATE ACCOUNT\n{UI}")

    while True:
        u = input("Username: ")
        if u in users:
            print("Taken")
        else:
            break

    p = input("Password: ")

    users[u] = {"password": p, "role": "user"}
    save_users()

    path = os.path.join(BASE_DIR, u)
    os.makedirs(os.path.join(path, "files"), exist_ok=True)

    with open(os.path.join(path, "settings.json"), "w") as f:
        json.dump({"theme": "light", "prompt": "Ezon"}, f)

    print("Account created!")

# ==================================================
# LOGIN
# ==================================================
def login():

    print(f"""
{UI}
            ⚡ EZON OS ⚡
{UI}
""")

    while True:
        print("\n🔐 LOGIN")
        u = input("Username: ")

        if u == "signup":
            signup()
            continue

        p = input("Password: ")

        if u in users and users[u]["password"] == p:
            print(f"\n{UI}\nWelcome {u}\n{UI}\n")
            return u, users[u]["role"]

        print("Wrong login\n")

# ==================================================
# PROFILE
# ==================================================
def load_profile(user):
    path = os.path.join(BASE_DIR, user)
    files = os.path.join(path, "files")
    settings_path = os.path.join(path, "settings.json")

    os.makedirs(files, exist_ok=True)

    if not os.path.exists(settings_path):
        with open(settings_path, "w") as f:
            json.dump({"theme": "light", "prompt": "Ezon"}, f)

    with open(settings_path, "r") as f:
        settings = json.load(f)

    return path, files, settings_path, settings

# ==================================================
# HELP MENU (CLEAN + FULL)
# ==================================================
def help_menu():
    print(f"""
{UI}
            ⚡ EZON COMMANDS ⚡
{UI}

📁 FILE SYSTEM
  dir / ls        → show files
  open <file>     → open file
  save <file>     → save text
  edit            → write text
  del <file>      → delete file

🧠 BASIC
  say <msg>       → print message
  write <msg>     → same

📦 APPS
  run coder       → EZON coding system
  run calc        → calculator
  run clock       → time

👤 SYSTEM
  whoami          → user info
  help            → menu
  exit            → quit

{UI}
""")

# ==================================================
# CODER (EZON LANGUAGE - NO PYTHON LEAK)
# ==================================================
def coder_app(FILE_DIR):

    print(f"""
{UI}
            ⚡ EZON CODER ⚡
{UI}

LANGUAGE GUIDE:

🧠 BASICS
  say hello
  ask name
  show name

📦 VARIABLES
  set x 10
  add x 5
  sub x 2

🐢 TURTLE
  turtle
  forward 10
  backward 10
  left
  right
  goto 10 10
  circle 5
  draw

🔧 SYSTEM
  /view   → variables
  /clear  → reset
  /exit   → leave coder
{UI}
""")

    variables = {}

    # =========================
    # TURTLE GRID
    # =========================
    w, h = 40, 20
    x, y = w // 2, h // 2
    direction = "right"
    canvas = []

    def reset():
        nonlocal canvas
        canvas = [[" " for _ in range(w)] for _ in range(h)]

    def plot(px, py):
        if 0 <= px < w and 0 <= py < h:
            canvas[py][px] = "#"

    def draw():
        print()
        for r in canvas:
            print("".join(r))
        print()

    reset()
    plot(x, y)

    # =========================
    # VIEW VARIABLES
    # =========================
    def view():
        print(f"\n{UI}\nVARIABLES\n{UI}")
        if not variables:
            print("No variables")
        else:
            for k, v in variables.items():
                print(f"{k} = {v}")
        print(UI)

    # =========================
    # LOOP
    # =========================
    while True:

        line = input("Coder> ").strip().split()
        if not line:
            continue

        cmd = line[0]
        args = line[1:]

        # EXIT
        if cmd == "/exit":
            break

        elif cmd == "/view":
            view()

        elif cmd == "/clear":
            variables = {}
            reset()
            print("Reset done")

        # =========================
        # EZON LANGUAGE
        # =========================

        elif cmd == "say":
            print(">>", " ".join(args))

        elif cmd == "ask":
            variables[args[0]] = input(args[0] + ": ")

        elif cmd == "show":
            print(variables.get(args[0], "undefined"))

        elif cmd == "set":
            variables[args[0]] = int(args[1])

        elif cmd == "add":
            variables[args[0]] = variables.get(args[0], 0) + int(args[1])

        elif cmd == "sub":
            variables[args[0]] = variables.get(args[0], 0) - int(args[1])

        # =========================
        # TURTLE
        # =========================

        elif cmd == "turtle":
            reset()
            print("Turtle ON")

        elif cmd == "draw":
            draw()

        elif cmd == "forward":
            n = int(args[0])
            for _ in range(n):
                if direction == "right": x += 1
                elif direction == "left": x -= 1
                elif direction == "up": y -= 1
                elif direction == "down": y += 1
                plot(x, y)

        elif cmd == "backward":
            n = int(args[0])
            for _ in range(n):
                if direction == "right": x -= 1
                elif direction == "left": x += 1
                elif direction == "up": y += 1
                elif direction == "down": y -= 1
                plot(x, y)

        elif cmd == "left":
            direction = "left"

        elif cmd == "right":
            direction = "right"

        elif cmd == "goto":
            x = int(args[0])
            y = int(args[1])
            plot(x, y)

        elif cmd == "circle":
            r = int(args[0])
            for a in range(360):
                nx = int(x + r * math.cos(math.radians(a)))
                ny = int(y + r * math.sin(math.radians(a)))
                plot(nx, ny)

        else:
            print("Unknown command")

# ==================================================
# START SYSTEM
# ==================================================
boot()

user, role = login()
USER_PATH, FILE_DIR, SETTINGS_PATH, settings = load_profile(user)

file_buffer = ""

while True:

    raw = input(f"[{user}@ezon] {settings['prompt']} $ ")
    parts = raw.strip().split()

    if not parts:
        continue

    cmd = parts[0]
    args = parts[1:]

    # EXIT
    if cmd in ["exit", "quit", "bye"]:
        print("Goodbye 👋")
        break

    # HELP
    elif cmd in ["help", "?"]:
        help_menu()

    # BASIC
    elif cmd in ["say", "write"]:
        print(">>", " ".join(args))

    # FILE SYSTEM
    elif cmd == "dir":
        print(f"\n{UI}\nFILES\n{UI}")
        for f in os.listdir(FILE_DIR):
            print(" •", f)
        print(UI)

    elif cmd == "open":
        path = os.path.join(FILE_DIR, args[0])
        print(open(path).read() if os.path.exists(path) else "Not found")

    elif cmd == "save":
        with open(os.path.join(FILE_DIR, args[0]), "w") as f:
            f.write(file_buffer)

    elif cmd == "edit":
        file_buffer = input("Text: ")

    elif cmd == "del":
        os.remove(os.path.join(FILE_DIR, args[0]))

    # APPS
    elif cmd == "run":

        if args[0] == "coder":
            coder_app(FILE_DIR)

        elif args[0] == "calc":
            while True:
                e = input("Calc> ")
                if e == "exit":
                    break
                try:
                    print(eval(e))
                except:
                    print("error")

        elif args[0] == "clock":
            print(time.strftime("%H:%M:%S"))

    elif cmd == "whoami":
        print(user, role)

    else:
        print("Unknown command, type 'help' to see avaliable commands")