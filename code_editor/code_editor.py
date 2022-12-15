"""

This is a Developing and Editing Tool for Developing in Offline Mode: D.E.T.D.O.M.

Date of creation: 08.12.22

"""

__author__ = "Egor Mironov @ved3v"

import tkinter
from tkinter import filedialog
import tkinter.font
import ctypes
import locale
from ctypes import windll
from io import StringIO
from contextlib import redirect_stdout
import traceback
import re


class CustomText(tkinter.Text):
    # https://stackoverflow.com/questions/3781670/how-to-highlight-text-in-a-tkinter-text-widget
    """
    Wrapper for the tkinter.Text widget with additional methods for
    highlighting and matching regular expressions.

    highlight_all(pattern, tag) - Highlights all matches of the pattern.
    highlight_pattern(pattern, tag) - Cleans all highlights and highlights all matches of the pattern.
    clean_highlights(tag) - Removes all highlights of the given tag.
    search_re(pattern) - Uses the python re library to match patterns.
    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master

        # sample tag
        self.tag_config("match", foreground="red")

    def highlight(self, tag, start, end):
        self.tag_add(tag, start, end)

    def highlight_all(self, pattern, tag):
        for match in self.search_re(pattern):
            self.highlight(tag, match[0], match[1])

    def clean_highlights(self, tag):
        self.tag_remove(tag, "1.0", tkinter.END)

    def search_re(self, pattern):
        """
        Uses the python re library to match patterns.

        Arguments:
            pattern - The pattern to match.
        Return value:
            A list of tuples containing the start and end indices of the matches.
            e.g. [("0.4", "5.9"]
        """
        matches = []
        text = self.get("1.0", tkinter.END).splitlines()
        for i, line in enumerate(text):
            # print(text, pattern, line)

            # custom
            if "#" in line:
                for match in re.finditer(pattern, line):
                    matches.append((f"{i + 1}.{match.start()}", f"{i + 1}.end"))
                    break

            for match in re.finditer(pattern, line):
                matches.append((f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}"))

        return matches

    def highlight_pattern(self, pattern, tag="match"):
        """
        Cleans all highlights and highlights all matches of the pattern.

        Arguments:
            pattern - The pattern to match.
            tag - The tag to use for the highlights.
        """
        self.clean_highlights(tag)
        self.highlight_all(pattern, tag)


class App:
    # TODO: FINISH D.E.T.D.O.M.

    def show_menu_buttons(self):
        if not self.menuOpened:
            self.buttonOpenFile.grid()
            self.buttonSaveFile.grid()
            self.menuOpened = True
            return None
        if self.menuOpened:
            self.buttonOpenFile.grid_remove()
            self.buttonSaveFile.grid_remove()
            self.menuOpened = False
            return None

    def change_buttonMenu_color_1(self, event):
        self.buttonMenu.config(foreground='cyan')

    def change_buttonOpenFile_color_1(self, event):
        self.buttonOpenFile.config(foreground='cyan')

    def change_buttonSaveFile_color_1(self, event):
        self.buttonSaveFile.config(foreground='cyan')

    def change_buttonMenu_color_2(self, event):
        self.buttonMenu.config(foreground='black')

    def change_buttonOpenFile_color_2(self, event):
        self.buttonOpenFile.config(foreground='black')

    def change_buttonSaveFile_color_2(self, event):
        self.buttonSaveFile.config(foreground='black')

    def openFile(self):
        files = [("PY files", "*.py"),
                 ("TXT files", "*.txt"),
                 ('HTML files', '*.html;*.htm'),
                 ('All files', '*.*')]
        file = filedialog.askopenfile(filetype=files, defaultextension=files)
        f = open(file.name, 'r', encoding='UTF-8')
        self.mainText.insert(1.0, f.read())

    def saveFile(self):
        files = [("PY files", "*.py"),
                 ("TXT files", "*.txt"),
                 ('HTML files', '*.html;*.htm'),
                 ('All files', '*.*')]
        file = filedialog.asksaveasfilename(filetype=files, defaultextension=files, confirmoverwrite=True)
        f = open(file, 'w')
        s = self.mainText.get(1.0, 'end')
        f.write(s)

    def output(self, text):
        self.outputText.delete(1.0, 'end')
        self.outputText.insert('end', f'{str(text)}\n')

    def insert_into_main_text(self, event=None):
        self.mainText.highlight_pattern("1", "1")
        self.mainText.highlight_pattern("2", "2")
        self.mainText.highlight_pattern("3", "3")
        self.mainText.highlight_pattern("4", "4")
        self.mainText.highlight_pattern("5", "5")
        self.mainText.highlight_pattern("6", "6")
        self.mainText.highlight_pattern("7", "7")
        self.mainText.highlight_pattern("8", "8")
        self.mainText.highlight_pattern("9", "9")
        self.mainText.highlight_pattern("0", "0")
        # self.mainText.highlight_pattern("+", "+")
        self.mainText.highlight_pattern("-", "-")
        self.mainText.highlight_pattern("/", "/")
        self.mainText.highlight_pattern("\"", "string")
        # self.mainText.highlight_pattern("**")
        self.mainText.highlight_pattern("%")
        # self.mainText.highlight_pattern("(")
        # self.mainText.highlight_pattern(")")
        self.mainText.highlight_pattern("import", "import")
        self.mainText.highlight_pattern("print", "print")
        self.mainText.highlight_pattern("from", "from")
        self.mainText.highlight_pattern("as", "as")
        self.mainText.highlight_pattern("def", "def")
        self.mainText.highlight_pattern("class", "class")
        self.mainText.highlight_pattern("pass", "pass")
        self.mainText.highlight_pattern("if", "if")
        self.mainText.highlight_pattern("__init__", "__init__")
        self.mainText.highlight_pattern("self", "self")
        self.mainText.highlight_pattern(":", ":")
        self.mainText.highlight_pattern("=", "=")
        self.mainText.highlight_pattern("#", "#")

    def page_main(self):
        self.menuOpened = False
        self.infoOpened = False

        self.mainText = CustomText(self.root, bg='black', insertbackground='red', foreground='white', font=self.codeFont,
                                   wrap='word', height=25)
        self.outputText = tkinter.Text(self.root, bg='#000000', insertbackground='white', foreground='white', font=self.codeFont,
                                       wrap='word')
        self.frame = tkinter.Frame(self.root)
        self.buttonMenu = tkinter.Button(self.frame, text='Menu', command=self.show_menu_buttons, width=10, bg='#555555', relief='solid',
                                         activebackground='#555555', bd=1)
        self.buttonOpenFile = tkinter.Button(self.frame, text='Open file', command=self.openFile, width=10, bg='#555555', relief='solid',
                                             activebackground='#555555', bd=1)
        self.buttonSaveFile = tkinter.Button(self.frame, text='Save file', command=self.saveFile, width=10, bg='#555555', relief='solid',
                                             activebackground='#555555', bd=1)

        self.frame.pack(side='left', anchor='nw')
        self.mainText.pack(fill='both', expand=1)
        self.outputText.pack(fill='both', expand=1, pady=10)
        self.buttonMenu.grid(row=0, column=0, ipady=10)
        self.buttonOpenFile.grid(row=2, column=0, sticky='n', ipady=10)
        self.buttonSaveFile.grid(row=3, column=0, sticky='n', ipady=10)

        self.mainText.bind('<F5>', self.execute)

        self.buttonMenu.bind('<Enter>', self.change_buttonMenu_color_1)
        self.buttonOpenFile.bind('<Enter>', self.change_buttonOpenFile_color_1)
        self.buttonSaveFile.bind('<Enter>', self.change_buttonSaveFile_color_1)

        self.buttonMenu.bind('<Leave>', self.change_buttonMenu_color_2)
        self.buttonOpenFile.bind('<Leave>', self.change_buttonOpenFile_color_2)
        self.buttonSaveFile.bind('<Leave>', self.change_buttonSaveFile_color_2)

        self.buttonOpenFile.grid_remove()
        self.buttonSaveFile.grid_remove()

        self.mainText.tag_config("%", foreground="red")
        self.mainText.tag_config("=", foreground="red")
        self.mainText.tag_config("-", foreground="red")
        self.mainText.tag_config("/", foreground="red")
        self.mainText.tag_config("#", foreground="gray")
        self.mainText.tag_config("string", foreground="lightgreen")
        # self.mainText.tag_config("+", foreground="red")
        self.mainText.tag_config(":", foreground="red")
        # self.mainText.tag_config("(", foreground="cyan")
        # self.mainText.tag_config(")", foreground="cyan")
        self.mainText.tag_config("1", foreground="#AA00FF")
        self.mainText.tag_config("2", foreground="#AA00FF")
        self.mainText.tag_config("3", foreground="#AA00FF")
        self.mainText.tag_config("4", foreground="#AA00FF")
        self.mainText.tag_config("5", foreground="#AA00FF")
        self.mainText.tag_config("6", foreground="#AA00FF")
        self.mainText.tag_config("7", foreground="#AA00FF")
        self.mainText.tag_config("8", foreground="#AA00FF")
        self.mainText.tag_config("9", foreground="#AA00FF")
        self.mainText.tag_config("0", foreground="#AA00FF")
        self.mainText.tag_config("import", foreground="cyan")
        self.mainText.tag_config("print", foreground="cyan")
        self.mainText.tag_config("from", foreground="cyan")
        self.mainText.tag_config("as", foreground="cyan")
        self.mainText.tag_config("def", foreground="cyan")
        self.mainText.tag_config("class", foreground="cyan")
        self.mainText.tag_config("pass", foreground="cyan")
        self.mainText.tag_config("if", foreground="cyan")
        self.mainText.tag_config("__init__", foreground="cyan", font=self.codeFontItalic)
        self.mainText.tag_config("self", foreground="purple")

        self.mainText.bind("<KeyRelease>", self.insert_into_main_text)
        self.mainText.config(tabs=self.codeFont.measure("    "))

        self.outputText.bind("<BackSpace>", lambda _: "break")  # don't allow users to use backspace

    def execute(self, event=None):
        self.executor.execute(self.mainText.get(1.0, 'end'))

    def config(self):
        # defining app class variables

        self.CODE_EDITOR_NAME = "VDA DETDOM"
        self.PAGES = ["main"]
        self.PAGE = self.PAGES[0]

        self.menuOpened = False

        # user relative info

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
        self.codeFont = tkinter.font.Font(family="Courier", size=self.WIDTH // 100, weight="bold")
        self.codeFontItalic = tkinter.font.Font(family="Courier", size=self.WIDTH // 100, weight="bold", slant="italic")

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

        self.rootConfig()

        self.config()

        self.root.title(f"Virtual Developer Assistant: {self.CODE_EDITOR_NAME}")

        self.root.config(bg=self.mainColor)

        # get OS language
        windll = ctypes.windll.kernel32
        self.LANGUAGE = locale.windows_locale[windll.GetUserDefaultUILanguage()]  # format: en_US

        # root events

        # handling close event
        self.root.protocol("WM_DELETE_WINDOW", self.onClosing)

        self.executor = VDA_CodeExecutor()

        self.page_main()

        self.root.mainloop()

    def onClosing(self, event=None):
        self.root.destroy()


class VDA_CodeExecutor:
    # VDA DETDOM
    # class for executing python code in str format

    def __init__(self):
        self.NAME = "VDA DETDOM"

        print(f"{self.NAME} init")

    def execute(self, code: str):
        try:
            code = compile(code, 'file', 'exec')
            f = StringIO()
            with redirect_stdout(f):
                exec(code)
            return f.getvalue()
        except Exception:
            return f'Error: {traceback.format_exc()}'


if __name__ == '__main__':
    app = VDA_CodeExecutor()
