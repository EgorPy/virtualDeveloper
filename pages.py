import tkinter
import pickle
import time
import math
import traceback
import os
import webbrowser
import win32com.client
import threading
import os
from functools import partial
from io import StringIO
from contextlib import redirect_stdout
from copy import deepcopy

print("pages.py init")


class VDA_FileBrowser:
    # VDA File Browser

    def __init__(self, output_func):
        self.NAME = "VDA File Browser"

        self.output_func = output_func

        print(f"{self.NAME} init")

    def open_folder(self, directory: str):
        # this function opens folder
        self.output_func(f"opening files in folder \"{directory}\"\n\n")
        self.output_func(len(os.listdir(str(directory))))
        return_list = []
        for f in os.listdir(str(directory)):
            try:
                file = open(f"{str(directory)}\\{f}", "r", encoding="utf-8")
            except UnicodeDecodeError as e:
                return_list.append(f"<Cannot decode data, error: {e}>")
            except ValueError as e:
                return_list.append(f"<Path is not in str format (Program error), error: {e}>")
            except PermissionError as e:
                return_list.append(f)
            except FileNotFoundError as e:
                return_list.append(f"<Folder not found, error: {e}>")

        return return_list

    def open_file(self, file_path):
        # this function opens application
        wsh = win32com.client.Dispatch("WScript.Shell")
        wsh.Run("\"" + file_path + "\"")


class VDA_SimpleLangExecutor:
    # VDA Simple Query Language
    # Simple Query Language developed for queries for virtual assistant

    # commands:

    # <input> = not necessary input
    # [input] = necessary input

    # execute [file_path] = execute python file

    # code [file_path] <app_name> = open code editor D.E.T.D.O.M. by default (can be changeable)
    # code can be opened in D.E.T.D.O.M. or VS Code or PyCharm or NotePad or PyCharm Professional

    # open [file_path] = open file in specified app or in txt format (maybe show dialog window)
    # example: open notepad
    # example: open C:\Users\Egor\Desktop\file.txt; and then show dialog window "Do you want to save this app path?" if yes, you input app name and it will save path with name

    # request [web_request] you can also save common requests with names, for example: youtube instead of https://youtube.com
    # example: request https://youtube.com

    # openfolder [directory]
    # example: openfolder ..
    # example: openfolder C:\Users\Egor\Desktop

    # sequence = execute a sequence of commands
    # example:
    # sequence:
    # open Telegram
    # open PyCharm
    # gmail
    # youtube
    # stepik

    # key [key_name] = press any key virtually

    # waitkey [key_name] = wait for key press

    # mouse [button_number] = press mouse button virtually, button numbers: 0 - left, 1 - middle, 2 - right

    # mousepos [position] = set mouse position virtually

    def __init__(self, output_func):
        self.NAME = "VDA Simple Query Language"

        self.output_func = output_func

        print(f"{self.NAME} init")

        # commands in this dict can be added
        self.commands = {
            "execute": self.execute,
            "code": self.code,
            "openfolder": self.open_folder,
            "open": self.open_file,
            "request": self.request,
            "key": self.key,
            "waitkey": self.wait_key,
            "mouse": self.mouse,
            "mousepos": self.mouse_pos,
            "search": self.search
        }

        self.file_browser = VDA_FileBrowser(self.output_func)

    def run(self, command: str, *args):
        # this function converts Simple Query Language commands into python code and executes it
        for i in self.commands.keys():
            if command == i:
                if command != "code":
                    self.commands[i](args[0])
                else:
                    self.commands[i](args[0], args[1])

    def open_simple_lang_file(self, file_path: str):
        # this function reads and runs file with Simple Query Language commands
        pass

    def execute(self, file_path: str):
        # this function executes python code from .py file
        pass

    def code(self, file_path: str):
        # this function opens code editor
        pass

    def open_file(self, file_path: str):
        # this function opens application
        self.output_func(f"opening {file_path}")
        self.file_browser.open_file(file_path)

    def open_folder(self, directory: str):
        # this function opens folder
        self.file_browser.open_folder(directory)

    def request(self, web_request: str, secure=True):
        # this function opens web request in browser # internet connection needed
        if "https://" in web_request:
            query = web_request
        else:
            query = f"https://{web_request}"
        self.output_func(f"requesting {query}")
        webbrowser.open(query)

    def search(self, web_request: str):
        self.output_func(f"searching {web_request}")
        webbrowser.open("https://google.com")
        time.sleep(2)
        wsh = win32com.client.Dispatch("WScript.Shell")
        wsh.SendKeys(f"{web_request}~")

    def key(self, key_name):
        # this function presses any key virtually
        pass

    def wait_key(self, key_name):
        # this function checks if any key is pressed or not
        pass

    def mouse(self, mouse: int):
        # this function presses any mouse button virtually
        # button numbers: 0 - left, 1 - middle, 2 - right
        pass

    def mouse_pos(self, x: int, y: int):
        # this function changes mouse position virtually
        pass


class PageMain:
    def __init__(self, root, main_self, username):
        def output(text, start="", end="\n", tag=None):
            output_text.config(state="normal")
            if text != output_text.get("end-2c linestart", "end-2c lineend"):
                output_text.insert("end", start + text + end, tag)
            output_text.config(state="disabled")
            output_text.see("end")

        def execute_query(command: str, *args):
            # this function will execute command with specified algorithm for only this command
            # every command have its own algorithm to be executed
            # this algorithm must be saved with command
            self.simple_lang_executor.run(command, *args)

        def check_query(event=None):
            user_query = input_entry.get()

            possible_queries = check_for_similar(user_query.lower(), self.QUERIES)

            if user_query:
                if not len(possible_queries):
                    possible_queries = check_for_similar(user_query.lower().split()[0], list(self.COMMANDS.keys()))
                    if len(possible_queries):
                        execute_query(possible_queries[0], *user_query.lower().split()[1:])
                    else:
                        possible_queries = check_for_similar(user_query.lower().split()[0], list(self.APP_PATHS.keys()))
                        if len(possible_queries):
                            execute_query("open", self.APP_PATHS[possible_queries[0].split()[0]])
                        else:
                            output("Command not found", tag="red")
                else:
                    expr = self.QUERIES[possible_queries[0]]
                    com = expr.split()[0]
                    args = expr.split()[1:]
                    execute_query(com, *args)

            return "break"

        def visualisation_animation():
            canvas.delete("all")
            w = canvas.winfo_reqwidth()  # width of canvas
            cx = w / 2  # half of width (center of x)
            nw = w / 2.7  # part of width when circle is fully in canvas
            qw = w / 4  # quarter of width
            mw = w / 10
            t = time.time() / 2
            for i in range(180):
                x1 = math.sin(deg_to_rad(i * 2)) * nw + cx - 5
                y1 = math.cos(deg_to_rad(i * 2)) * nw + cx - 5
                x2 = math.sin(deg_to_rad(i * 2)) * nw + cx + 5
                y2 = math.cos(deg_to_rad(i * 2)) * nw + cx + 5
                v = deg_to_rad(i * 6) + t  # value to make cool effect
                canvas.create_rectangle(
                    x1 + math.sin(v) * mw,
                    y1 + math.sin(v) * mw,
                    x2,
                    y2,
                    fill=None,
                    width=1,
                    outline="green"  # main_self.sectionBackgroundColor
                )

        def update():
            date_label["text"] = time.ctime()

            # visualisation_animation()

            root.after(50, update)

        def config():
            # defining class variables

            self.main_self = main_self

            self.simple_lang_executor = VDA_SimpleLangExecutor(output)

            self.DEFAULT_USERNAME = "Unknown"
            self.USERNAME = deepcopy(self.DEFAULT_USERNAME)
            self.PAGES = ["login", "main", "milestones", "calendar", "push_ups"]
            self.PAGE = self.PAGES[0]
            self.VA_ANGLE = 0  # visualization animation angle
            self.CALCULATOR_PATH = "calculator.py"
            self.CALENDAR_PATH = "calendar.py"
            self.MILESTONES_PATH = "milestones.py"
            # self.APP_PATHS = {"telegram": "D:\\PortableApps\\Telegram\\Telegram.exe",
            #                   "chrome": "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            #                   "lego_mindstorms_ev3": "C:\\Program Files (x86)\\LEGO Software\\LEGO MINDSTORMS Edu EV3\\MindstormsEV3.exe",
            #                   "lego_digital_designer": "D:\\LEGO Digital Designer\\LDD.exe",
            #                   "acrobat": "C:\\Program Files\\Adobe\\Acrobat DC\\Acrobat\\Acrobat.exe",
            #                   "android_studio": "C:\\Program Files\\Android\\Android Studio\\bin\\studio64.exe",
            #                   "cmd": "%windir%\\system32\\cmd.exe",
            #                   "git_bash": "C:\\Users\\Egor\\AppData\\Local\\Programs\\Git\\git-bash.exe",
            #                   "git_cmd": "C:\\Users\\Egor\\AppData\\Local\\Programs\\Git\\git-cmd.exe",
            #                   "git_gui": "C:\\Users\\Egor\\AppData\\Local\\Programs\\Git\\cmd\\git-gui.exe",
            #                   "intellij_idea": "D:\\IntellijIdea\\IntelliJ IDEA Community Edition 2021.3.1\\bin\\idea64.exe",
            #                   "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
            #                   "code": "C:\\Users\\Egor\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
            #                   "movavi": "D:\\Movavi\\Movavi Video Editor Plus\\VideoEditorPlus.exe",
            #                   "punto": "C:\\Program Files (x86)\\Yandex\\Punto Switcher\\punto.exe",
            #                   "putty": "C:\\Program Files\\PuTTY\\putty.exe",
            #                   "pycharm": "D:\\Desktop\pycharm\\PyCharm Community Edition 2020.2\\bin\\pycharm64.exe",
            #                   "idle37": "C:\\Users\\Egor\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\idlelib\\idle.pyw",
            #                   "idle39": "C:\\Users\\Egor\\AppData\\Local\\Programs\\Python\\Python39\\pythonw.exe \"C:\\Users\\Egor\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\idlelib\\idle.pyw\"",
            #                   "roblox": "C:\\Users\\Egor\\AppData\\Local\\Roblox\\Versions\\version-04be97a13ff0427b\\RobloxPlayerLauncher.exe",
            #                   "roblox_studio": "C:\\Users\\Egor\\AppData\\Local\\Roblox\\Versions\\RobloxStudioLauncherBeta.exe",
            #                   "minecraft": "C:\\Users\\Egor\\AppData\\Roaming\\.minecraft\\Tlauncher.exe"}

            self.COMMANDS = self.simple_lang_executor.commands

            # queries:
            self.DEFAULT_QUERIES = {"youtube": "request youtube.com",
                                    "search <input_request_name>": "request <input_request_name>",
                                    "gmail": "request gmail.com",
                                    "translate": "request translate",
                                    "calculator": f"execute {self.CALCULATOR_PATH}",
                                    "calendar": f"execute {self.CALENDAR_PATH}",
                                    "milestones": f"execute {self.MILESTONES_PATH}"}

            # getting saved queries for user
            try:
                with open("savedData/queries.dat", "rb") as file:
                    self.saved_queries = pickle.load(file)
                    if len(self.saved_queries) > len(self.DEFAULT_QUERIES):
                        self.QUERIES = self.saved_queries
                    else:
                        self.QUERIES = deepcopy(self.DEFAULT_QUERIES)
            except FileNotFoundError:
                self.QUERIES = deepcopy(self.DEFAULT_QUERIES)
                with open("savedData/queries.dat", "wb") as file:
                    pickle.dump(self.QUERIES, file)

            # getting app paths for user
            try:
                with open("savedData/app_paths.dat", "rb") as file:
                    self.saved_app_paths = pickle.load(file)
                    if len(self.saved_app_paths) > 0:
                        self.APP_PATHS = self.saved_app_paths
                    else:
                        self.APP_PATHS = {}
            except FileNotFoundError:
                self.APP_PATHS = {}
                with open("savedData/app_paths.dat", "wb") as file:
                    pickle.dump(self.APP_PATHS, file)

            # loading first launch variable
            try:
                with open("savedData/firstLaunch.dat", "rb") as file:
                    self.FIRST_LAUNCH = pickle.load(file)
            except FileNotFoundError:
                self.FIRST_LAUNCH = True

        config()

        user_label = tkinter.Label(root, text=f"Welcome back, {username}", font=main_self.titleFont, foreground=main_self.titleColor, background=main_self.backgroundColor)
        date_label = tkinter.Label(root, text=f"{time.ctime()}", font=main_self.mainFont, foreground=main_self.titleColor, background=main_self.backgroundColor)
        canvas = tkinter.Canvas(root, width=main_self.WIDTH / 2, height=main_self.WIDTH / 2, background=main_self.backgroundColor, highlightthickness=0)

        input_entry_frame = tkinter.Frame(root, width=main_self.WIDTH - 50, height=30)
        input_entry = tkinter.Entry(input_entry_frame, background=main_self.backgroundColor, foreground=main_self.titleColor, insertbackground=main_self.insertBackgroundColor,
                                    selectbackground=main_self.selectBackgroundColor, selectforeground=main_self.selectForegroundColor, font=main_self.codeFontBold, justify="center")
        input_entry_frame.pack_propagate(False)
        input_entry.pack(fill="both", expand=True)

        input_entry.bind("<Return>", check_query)

        output_text_frame = tkinter.Frame(root, width=main_self.WIDTH - 50, height=main_self.HEIGHT // 1.5)
        output_text = tkinter.Text(output_text_frame, background=main_self.backgroundColor, foreground=main_self.titleColor, insertbackground=main_self.insertBackgroundColor,
                                   selectbackground=main_self.selectBackgroundColor, selectforeground=main_self.selectForegroundColor, font=main_self.codeFont)
        output_text_scroll = tkinter.Scrollbar(output_text, command=output_text.yview)
        output_text.config(state="disabled", yscrollcommand=output_text_scroll.set)
        output_text_frame.pack_propagate(False)
        output_text.pack(fill="both", expand=True)
        output_text_scroll.pack(fill="y", side="right")

        output_text.tag_config("red", foreground="red")

        # slide_up_animation(canvas, main_self, root, current=-200, when_stop=0)
        slide_up_animation(user_label, main_self, root, when_stop=475)
        slide_up_animation(date_label, main_self, root, when_stop=425, step=6)
        slide_up_animation(input_entry_frame, main_self, root, current=-400, when_stop=350, step=8)
        slide_up_animation(output_text_frame, main_self, root, current=-400, when_stop=-100, step=8)

        main_self.root.protocol("WM_DELETE_WINDOW", self.onClosing)

        update()

    def onClosing(self, event=None):
        self.saveData()
        self.main_self.root.destroy()

    def saveData(self):
        # saving latest run info

        # saving latest run
        try:
            file = open("savedData/latestRun.txt", "w")
            file.write(str(time.ctime()))
        except FileNotFoundError:
            os.mkdir("savedData")
            file = open("savedData/latestRun.txt", "w")
            file.write(str(time.ctime()))

        # saving first launch
        if self.FIRST_LAUNCH:
            with open("savedData/firstLaunch.dat", "wb") as file:
                pickle.dump(False, file)

        # saving queries for user
        with open("savedData/queries.dat", "wb") as file:
            pickle.dump(self.QUERIES, file)

        # saving app paths for user
        with open("savedData/app_paths.dat", "wb") as file:
            pickle.dump(self.APP_PATHS, file)


def page_login(root, main_self):
    def submit(event, self):
        def createNewUser(self):
            print("creating new user...")

            u, p = get_login()
            user_path, password_path = get_path()

            os.mkdir(user_path)
            with open(password_path, "wb") as file:
                pickle.dump(p, file)
            print("new user created")
            print(f"Username: {u}")
            print(f"Password: {p}", end="\n\n")
            print("login successful")
            quit_page_login(self, u)

        def get_login():
            # get username and password values
            return username_entry.get(), password_entry.get()

        def get_path():
            # get user and password paths
            u = username_entry.get()
            return f"{path}\\{u}", f"{path}\\{u}\\p.txt"

        submit_button_check()

        os_user = os.getlogin()
        path = f"C:\\Users\\{os_user}\\AppData\\Roaming\\VirtualDev"
        # check if app folder exists in AppData
        if os.path.exists(path):
            # check if this user exists
            u, p = get_login()
            user_path, password_path = get_path()

            if os.path.exists(user_path):
                if os.path.isfile(password_path):
                    with open(password_path, "rb") as file:
                        saved_password = pickle.load(file)
                        if p == saved_password:
                            print("login successful")
                            quit_page_login(self, u)
                else:
                    print("no password set for current user")
            else:
                print("user path does not exist")
                createNewUser(self)
        else:
            print("app folder does not exist")
            print("creating app folder...", end=" ")
            os.mkdir(path)
            print("complete")

            print("no user record")
            createNewUser(self)

    def submit_button_check(event=None):
        val_u = username_entry.get()
        val_p = password_entry.get()
        if val_u and val_p and val_u != "username" and val_p != "password":
            submit_button["foreground"] = main_self.titleColor
        else:
            submit_button["foreground"] = main_self.textHintColor

        if event != "break":
            root.after(20, submit_button_check, "break")

    def username_entry_hint_enter(event=None):
        if username_entry.get() == "username":
            username_entry.delete(0, "end")
            username_entry["foreground"] = main_self.titleColor

    def username_entry_hint_leave(event=None):
        if username_entry.get() == "":
            username_entry.delete(0, "end")
            username_entry.insert(0, "username")
            username_entry["foreground"] = main_self.textHintColor

    def password_entry_hint_enter(event=None):
        if password_entry.get() == "password":
            password_entry.delete(0, "end")
            password_entry["foreground"] = main_self.titleColor

    def password_entry_hint_leave(event=None):
        if password_entry.get() == "":
            password_entry.delete(0, "end")
            password_entry.insert(0, "password")
            password_entry["foreground"] = main_self.textHintColor

    def quit_page_login(self, user):
        self.USERNAME = user

        welcome_label.place_forget()
        description_label.place_forget()
        login_label.place_forget()
        username_entry.place_forget()
        password_entry.place_forget()
        submit_button.place_forget()

        # start page main after login
        self.PAGE = "main"
        page_main(root, main_self, self.USERNAME)

    welcome_label = tkinter.Label(root, text="Welcome to Virtual Developer Assistant", font=main_self.titleFont, foreground=main_self.titleColor, background=main_self.backgroundColor)
    description_label = tkinter.Label(root, text="Next generation tool for digital automation", font=main_self.subtitleFont, foreground=main_self.descriptionColor,
                                      background=main_self.backgroundColor)
    login_label = tkinter.Label(root, text="Log In", font=main_self.subtitleFont, foreground=main_self.titleColor, background=main_self.backgroundColor)
    username_entry = tkinter.Entry(root, font=main_self.subtitleFont, foreground=main_self.textHintColor, background=main_self.backgroundColor, insertbackground=main_self.titleColor,
                                   selectbackground=main_self.titleColor,
                                   selectforeground=main_self.backgroundColor)
    password_entry = tkinter.Entry(root, font=main_self.subtitleFont, foreground=main_self.textHintColor, background=main_self.backgroundColor, insertbackground=main_self.titleColor,
                                   selectbackground=main_self.titleColor,
                                   selectforeground=main_self.backgroundColor)
    submit_button = tkinter.Button(root, text="Submit", font=main_self.mainFont, foreground=main_self.textHintColor, background=main_self.backgroundColor, relief="flat", width=15,
                                   command=partial(submit, main_self))

    username_entry.insert(0, "username")
    password_entry.insert(0, "password")

    username_entry.bind("<Enter>", username_entry_hint_enter)
    username_entry.bind("<FocusIn>", username_entry_hint_enter)
    username_entry.bind("<Leave>", username_entry_hint_leave)
    username_entry.bind("<FocusOut>", username_entry_hint_leave)

    username_entry.bind("<Key>", submit_button_check)
    password_entry.bind("<Key>", submit_button_check)

    password_entry.bind("<Enter>", password_entry_hint_enter)
    password_entry.bind("<FocusIn>", password_entry_hint_enter)
    password_entry.bind("<Leave>", password_entry_hint_leave)
    password_entry.bind("<FocusOut>", password_entry_hint_leave)

    submit_button.bind("<Return>", partial(submit, main_self))

    slide_up_animation(welcome_label, main_self, root, current=0, when_stop=400)
    slide_up_animation(description_label, main_self, root, current=0, when_stop=340)
    slide_up_animation(login_label, main_self, root, current=-200, when_stop=200)
    slide_up_animation(username_entry, main_self, root, current=-200, when_stop=125)
    slide_up_animation(password_entry, main_self, root, current=-200, when_stop=50)
    slide_up_animation(submit_button, main_self, root, current=-200, when_stop=-25)


def check_for_similar(string_to_check: str, list_to_check: list[str]):
    s = string_to_check.lower()

    return_values = []

    for possible_element in list_to_check:
        el = possible_element.lower()
        if s == el:
            return_values.append(el)
        elif s[0:3] == el[0:3]:
            if len(s) <= len(el):
                if s in el:
                    return_values.append(el)
            else:
                if el in s:
                    return_values.append(el)

    return return_values


def slide_up_animation(widget, self, root, current=0, when_stop=400, step=5, x=0):
    if round(current) >= when_stop:
        return None
    else:
        current += (when_stop - current) / step
    widget.place(x=(self.WIDTH - widget.winfo_reqwidth()) / 2 + x, y=(self.HEIGHT - widget.winfo_reqheight()) / 2 - current)
    root.after(20, slide_up_animation, widget, self, root, current, when_stop, step, x)


def touched(x1, weight1, x2, weight2, y1, height1, y2, height2):
    if (x1 <= x2 and x2 <= (x1 + weight1)
        and y1 <= y2 and y2 <= (y1 + height1)) \
            or (x1 <= (x2 + weight2) and (x1 + weight1) >= x2
                and y1 <= (y2 + height2) and (y1 + height1) >= y2):
        return True
    else:
        return False


def deg_to_rad(degree):
    return degree * math.pi / 180


def rad_to_deg(radian):
    return radian * 180 / math.pi
