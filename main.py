__author__ = "Egor Mironov @ved3v"

"""

This is a Virtual Developer virtual assistant project.

It is like Jarvis, but better and his name is Dev, Aboba, Jarvis and maybe some other names.

Date of creation: 12.11.22

VDA = Virtual Developer Assistant

"""

import tkinter
import tkinter.ttk
import tkinter.messagebox
import tkinter.filedialog
import tkinter.font
import ctypes
import pickle
import locale
import time
import os
import threading
from ctypes import windll
from copy import deepcopy
import webbrowser
import win32com.client
# import torch
# import sounddevice as sd
from pages import *


class VDA_FileBrowser:
    # VDA File Browser

    def __init__(self):
        self.NAME = "VDA File Browser"

        print(f"{self.NAME} init")

    def open_folder(self, directory: str):
        # this function opens folder
        print(f"opening files in folder \"{directory}\"\n\n")
        print(len(os.listdir(str(directory))))
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

    def __init__(self):
        self.NAME = "VDA Simple Query Language"

        print(f"{self.NAME} init")

        # commands in this dict can be added
        self.commands = {
            "execute": self.execute,
            "code": self.code,
            "open": self.open_file,
            "folder": self.open_folder,
            "request": self.request,
            "key": self.key,
            "waitkey": self.wait_key,
            "mouse": self.mouse,
            "mousepos": self.mouse_pos,
            "search": self.search
        }

        self.file_browser = VDA_FileBrowser()

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
        print(f"opening {file_path}")
        self.file_browser.open_file(file_path)

    def open_folder(self, directory: str):
        # this function opens folder
        print(*self.file_browser.open_folder(directory), sep="\n", end="\n\n")

    def request(self, web_request: str, secure=True):
        # this function opens web request in browser # internet connection needed
        if "https://" in web_request:
            query = web_request
        else:
            query = f"https://{web_request}"
        print(f"requesting {query}")
        webbrowser.open(query)

    def search(self, web_request: str):
        print(f"searching {web_request}")
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


class App:
    # def say(self):
    #     language = "ru"
    #     model_id = "ru_v3"
    #     sample_rate = 24000
    #     speaker = "aidar"
    #     put_accent = False
    #     put_yo = False
    #     device = torch.device("cpu")  # cpu or gpu
    #     text = "Абоба"
    #
    #     model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
    #                               model='silero_tts',
    #                               language=language,
    #                               speaker=model_id,
    #                               skip_validation=True)
    #     model.to(device)
    #
    #     audio = model.apply_tts(text=text,
    #                             speaker=speaker,
    #                             sample_rate=sample_rate,
    #                             put_accent=put_accent,
    #                             put_yo=put_yo)
    #
    #     print(text)
    #
    #     sd.play(audio, sample_rate)
    #     time.sleep(len(audio) / (sample_rate / 1.5))
    #     sd.stop()

    def execute(self, event=None):
        pass

    def config(self):
        # defining app class variables

        self.NAME = "Virtual Developer Assistant"
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

        self.simple_lang_executor = VDA_SimpleLangExecutor()
        self.COMMANDS = self.simple_lang_executor.commands

        # queries:
        self.DEFAULT_QUERIES = {"youtube": "request youtube.com",
                                "search <input_request_name>": "request <input_request_name>",
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

        # user relative info
        # # network activities
        # try:
        #     with open("savedData/network_activities.dat", "rb") as file:
        #         self.network_activities = pickle.load(file)
        # except FileNotFoundError:
        #     self.network_activities = ["YouTube", "Search", "Translate"]
        #     with open("savedData/network_activities.dat", "wb") as file:
        #         pickle.dump(self.network_activities, file)
        # # activities without network
        # try:
        #     with open("savedData/activities.dat", "rb") as file:
        #         self.activities = pickle.load(file)
        # except FileNotFoundError:
        #     self.activities = ["Calculator", "Calendar"]
        #     with open("savedData/activities.dat", "wb") as file:
        #         pickle.dump(self.activities, file)
        # ["Kundalik", "Gmail", "YouTube", "Telegram", "Search", "Translate", "GitHub", "Itch", "Quora"]
        # ["Calculator", "Calendar", "VS Code", "PyCharm", "PyCharm Professional"]
        # possible pages:
        # login
        # main
        # milestones
        # calendar
        # push_ups
        # music # maybe implement in all pages

        # colors
        self.mainColor = "#000000"

        self.titleColor = "#FFFFFF"
        self.backgroundColor = "#000000"
        self.sectionBackgroundColor = "#03A9F4"
        self.buttonColor = "#2196F3"
        self.textInputColor = "#000000"
        self.textHintColor = "#555555"
        self.descriptionColor = "#999999"
        self.selectForegroundColor = "black"
        self.selectBackgroundColor = "red"
        self.insertBackgroundColor = "red"

        # fonts
        self.bigFont = tkinter.font.Font(family="Segoe UI", size=self.WIDTH // 70)
        self.mainFont = tkinter.font.Font(family="Segoe UI", size=self.WIDTH // 100)
        self.titleFont = tkinter.font.Font(family="Segoe UI", size=self.WIDTH // 60)
        self.subtitleFont = tkinter.font.Font(family="Segoe UI", size=self.WIDTH // 80)
        self.codeFont = tkinter.font.Font(family="Courier", size=self.WIDTH // 100)
        self.codeFontBold = tkinter.font.Font(family="Courier", size=self.WIDTH // 100, weight="bold")

    def rootConfig(self):
        self.WIDTH = 1920  # self.root.winfo_screenwidth()
        self.HEIGHT = 1080  # self.root.winfo_screenheight()
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.state("zoomed")
        self.root.resizable(False, True)
        self.root.tk_focusFollowsMouse()
        # this line of code needed to get rid of blurred fonts (see https://stackoverflow.com/questions/41315873/attempting-to-resolve-blurred-tkinter-text-scaling-on-windows-10-high-dpi-disp)
        windll.shcore.SetProcessDpiAwareness(1)

    def __init__(self):
        self.root = tkinter.Tk()

        self.root.title("Virtual Developer Assistant")

        self.rootConfig()

        self.config()

        self.root.config(bg=self.mainColor)

        print(f"{self.NAME} init")

        # get OS language
        windll = ctypes.windll.kernel32
        self.LANGUAGE = locale.windows_locale[windll.GetUserDefaultUILanguage()]  # format: en_US

        # root events
        self.root.bind("<Return>", self.execute)

        # handling close event
        self.root.protocol("WM_DELETE_WINDOW", self.onClosing)

        print(f"""
resolution: {self.WIDTH}x{self.HEIGHT}
language: {self.LANGUAGE}
first_launch: {self.FIRST_LAUNCH}
page: {self.PAGE}""", end="\n\n")

        # page_login(self.root, self)

        page_main(self.root, self, "Egor")  # test

        self.root.mainloop()

    def onClosing(self, event=None):
        self.saveData()
        self.root.destroy()

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


if __name__ == '__main__':
    app = App()
