import tkinter.filedialog
import tkinter.font
import tkinter.ttk
import threading
from tkinter import *
from tkinter import ttk
from main import play, filename,stop_playback



root = tkinter.Tk()
title = root.title("midi-to-appeal")
textInsert = tkinter.Text(root, height=2)
textInsert.pack()



def open_file():
    filedialog = tkinter.filedialog.askopenfilename(initialdir='/', title="Select file", filetypes = (("MIDI files", "*.mid"),))
    textInsert.delete("1.0", tkinter.END)
    textInsert.insert('1.0', str(filename))




top = Frame(root)
top.pack()
bottom = Frame(root)
bottom.pack(side=BOTTOM)
bottom2 = Frame(root)
bottom2.pack(side=BOTTOM)

button1 = Button(top, text="hii faggot!",fg="red")
button1.pack()
button2 = Button(bottom2, text="open a file", fg="red", command= open_file)
button2.pack()


root.mainloop()
