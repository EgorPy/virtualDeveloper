import tkinter
import pickle
import time
import math
import traceback
from functools import partial
from io import StringIO
from contextlib import redirect_stdout
import os

print("pages.py init")


def page_main(root, main_self, username):
    def output(text: str, end="\n"):
        output_text.config(state="normal")
        output_text.insert("end", text + end)
        output_text.config(state="disabled")

    def execute_query(command: str, *args):
        # this function will execute command with specified algorithm for only this command
        # every command have its own algorithm to be executed
        # this algorithm must be saved with command
        main_self.simple_lang_executor.run(command, *args)

    def check_query(event=None):
        user_query = input_entry.get()

        possible_queries = check_for_similar(user_query.lower(), main_self.QUERIES)

        if not len(possible_queries):
            possible_queries = check_for_similar(user_query.lower().split()[0], list(main_self.COMMANDS.keys()))
            # print(user_query.lower().split()[1:])
            if len(possible_queries):
                execute_query(possible_queries[0], *user_query.lower().split()[1:])
            else:
                possible_queries = check_for_similar(user_query.lower().split()[0], list(main_self.APP_PATHS.keys()))
                # print(main_self.APP_PATHS[possible_queries[0].split()[0]], *user_query.lower().split()[1:])
                if len(possible_queries):
                    execute_query("open", main_self.APP_PATHS[possible_queries[0].split()[0]])
                else:
                    print("Command not found")
            # execute_query(main_self.QUERIES[possible_queries[0]])
        else:
            expr = main_self.QUERIES[possible_queries[0]]
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
    output_text.config(state="disabled")
    output_text_frame.pack_propagate(False)
    output_text.pack(fill="both", expand=True)

    # slide_up_animation(canvas, main_self, root, current=-200, when_stop=0)
    slide_up_animation(user_label, main_self, root, when_stop=475)
    slide_up_animation(date_label, main_self, root, when_stop=425, step=6)
    slide_up_animation(input_entry_frame, main_self, root, current=-400, when_stop=350, step=8)
    slide_up_animation(output_text_frame, main_self, root, current=-400, when_stop=-100, step=8)

    update()


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
