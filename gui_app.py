import tkinter.filedialog
import tkinter.font
import tkinter.ttk
import keyboard
import threading
from tkinter import *
from tkinter import ttk

from midireader import play, stop_playback


root = tkinter.Tk()
root.geometry("300x400")
title = root.title("midi-to-appeal")

frame1 = Frame(root,width=500,height=300)
frame1.pack()

textInsert = tkinter.Text(frame1, width=30, height=1)
textInsert.pack(side="left")
right = Frame(frame1)
right.pack(side="left")



def open_file():
    global filedialog
    filedialog = tkinter.filedialog.askopenfilename(initialdir='/', title="Select file", filetypes = (("MIDI files", "*.mid"),))
    textInsert.delete("1.0", tkinter.END)
    textInsert.insert('1.0', filedialog)

def change_text():
    var.set(filedialog)

var = StringVar()
var.set("Default")
textBottomThatConfirms = tkinter.Label(root, textvariable=var)
textBottomThatConfirms.config(font =("Terminus", 14))
textBottomThatConfirms.pack(side="bottom")



top = Frame(root)
top.pack()
bottom = Frame(root)
bottom.pack(side=BOTTOM)


button1 = Button(top, text="hii faggot!",fg="black", command=change_text)
button1.pack()
button2 = Button(right, text="open a file", fg="red", command= open_file)
button2.pack()


keyboard.add_hotkey("F5", lambda: play(filedialog))
keyboard.add_hotkey("F6", stop_playback)

root.mainloop()
