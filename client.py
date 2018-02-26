from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *


# GUI Functions
def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def enter(event=None):
    if enterText.get() == "" or enterText.get() in user_names:
        print("Please enter a valid name")
    else:
        global name
        name = enterText.get()
        r_thread = Thread(target=receive)
        r_thread.start()
        send_name()
        enter_chat()


def enter_chat():
    master.withdraw()
    global global_screen
    global_screen.deiconify()
    global_screen.title("Global Chat")
    global_screen.geometry('600x325')

    field_message.set("Type your messages here.")
    scrollbar.pack(side=RIGHT, fill=Y)

    messages_list.pack(side=LEFT, fill=BOTH)
    messages_list.pack()
    messages_frame.pack()

    entry_field = Entry(global_screen, textvariable=field_message)
    entry_field.bind(sendMessage)
    entry_field.pack()
    send_button = Button(global_screen, text="Send", command=sendMessage)
    send_button.pack()

    pm_button = Button(global_screen, text="Private Chat", command=private_message)
    pm_button.pack()

    center(global_screen)


def private_message():
    global pm_screen
    pm_screen.deiconify()
    pm_screen.title("Private Message")
    pm_screen.geometry('200x300')

    global pm_message
    pm_message.set("Enter the name of the person you want to chat with")
    pm_scrollbar.pack(side=RIGHT, fill=Y)

    pm_list.pack(side=LEFT, fill=BOTH)
    pm_list.pack()
    pm_frame.pack()

    private_entry.bind(sendPrivate)
    private_entry.pack()

    private_button = Button(pm_screen, text="Send", command=sendPrivate)
    private_button.pack()

    center(pm_screen)


def sendPrivate():
    global private_entry
    message = private_entry.get()

    for i in user_names:
        if i in message:
            n = i
            pm_message .set("")
            pm_list.insert(END, "You are now chatting with " + n)
            break

    else:
        message = "@" + private_entry.get()
        pm_message.set("")
        pm_list.insert(END, message)
        s.send(bytes(message, "utf8"))


def sendMessage():
    message = field_message.get()
    field_message.set("")
    messages_list.insert(END, message)
    s.send(bytes(message, "utf8"))
    if message == "q":
        s.close()
        global global_screen
        global_screen.quit()


def onselect(evt):
    global lastselectionList
    w = evt.widget

    changedSelection = set(lastselectionList).symmetric_difference(set(w.curselection()))
    lastselectionList = w.curselection()

    index = int(list(changedSelection)[0])
    value = w.get(index)

    privateChat = Tk()
    name = Label(privateChat, text=value)
    name.pack()

    privateChat.geometry('300x300')

    messages_frame = Frame(privateChat)
    field_message.set("Type your messages here.")
    scrollbar = Scrollbar(messages_frame)

    messages_list = Listbox(messages_frame, height=15, width=550, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    messages_list.pack(side=LEFT, fill=BOTH)
    messages_list.pack()
    messages_frame.pack()

    entry_field = Entry(privateChat, textvariable=field_message)
    entry_field.bind("<Return>", send)
    entry_field.pack()
    send_button = Button(privateChat, text="Send", command=send)
    send_button.pack()


def send_name():
    message = enterText.get()
    s.send(bytes(message, "utf8"))


def receive():
    global user_names
    while True:
        try:
            message = s.recv(1024).decode("utf8")

            if "Active Users: " in message and "Welcome" not in message:
                list = message.split(":")
                users = list[1].split(",")
                for i in users:
                    user_names.append(i)
                messages_list.insert(END, message)
            elif "Active Users:" in message and "Welcome" in message:
                sentence = message.split(".")
                messages_list.insert(END, sentence[1])
            elif "Active Users:" not in message and "@" not in message:
                messages_list.insert(END, message)
            elif "@" in message:
                pm_list.insert(END, message)

        except OSError:
            break


# Other GUI stuff

# Global Chat Room
global_screen = Tk()
global_screen.withdraw()
messages_frame = Frame(global_screen)
scrollbar = Scrollbar(messages_frame)
messages_list = Listbox(messages_frame, height=15, width=550, yscrollcommand=scrollbar.set)

field_message = StringVar()
pm_message = StringVar()

user_names = []
name = ""

pm_screen = Tk()
pm_screen.withdraw()
pm_frame = Frame(pm_screen)
pm_scrollbar = Scrollbar(pm_frame)
pm_list = Listbox(pm_frame, height=15, width=550, yscrollcommand=scrollbar.set)

private_entry = Entry(pm_screen,textvariable=pm_message)
# GUI Home Screen
master = Tk()

master.title("MILESTONE - 1")
master.config(background="#0a0d0f")
master.geometry('200x150')

enterLabel = Label(master, text="Please enter your name here", fg="#c2e1fb", bg="#0a0d0f", font=("Calibri", 12))
enterLabel.pack()
enterLabel.place(relx=.5, rely=.30, anchor="center")

enterText = Entry(master)
enterText.pack()
enterText.place(relx=.5, rely=.50, anchor="center")

enterButton = Button(master, text="Enter", command=enter)
enterButton.pack()
enterButton.place(relx=.5, rely=.70, anchor="center")

HOST = '127.0.0.1'
PORT = 49152
ADDRESS = (HOST, PORT)

s = socket(AF_INET, SOCK_STREAM)
s.connect(ADDRESS)

center(master)

mainloop()
