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
from ctypes import windll
from copy import deepcopy
# import torch
# import sounddevice as sd
from pages import *


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

    def config(self):
        # defining app class variables

        # print(self.QUERIES)
        # print(self.APP_PATHS)

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

        self.NAME = "Virtual Developer Assistant"

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

        print(f"""
resolution: {self.WIDTH}x{self.HEIGHT}
language: {self.LANGUAGE}
""", end="\n\n")

        # page_login(self.root, self)

        PageMain(self.root, self, "Egor")  # test

        self.root.mainloop()


if __name__ == '__main__':
    app = App()
