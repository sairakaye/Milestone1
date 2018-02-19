from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

def receive():
    while True:
        try:
            message = s.recv(1024).decode("utf8")
            messages_list.insert(tkinter.END, message)
        except OSError:
            break


def send(event=None):
    message = field_message.get()
    field_message.set("")
    s.send(bytes(message, "utf8"))
    if message == "q":
        s.close()
        top.quit()


def close_window(event=None):
    field_message.set("q")
    send()


# GUI Layout
top = tkinter.Tk()
top.title("NETWORK - Milestone 1")

messages_frame = tkinter.Frame(top)
field_message = tkinter.StringVar()
field_message.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)

messages_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
messages_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
messages_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=field_message)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", close_window)


HOST = '127.0.0.1'
PORT = 49152
ADDRESS = (HOST, PORT)

s = socket(AF_INET, SOCK_STREAM)
s.connect(ADDRESS)

r_thread= Thread(target=receive)
r_thread.start()
tkinter.mainloop()