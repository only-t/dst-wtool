from tkinter import *
from tkinter.ttk import *
program = Tk()
program_icon = PhotoImage(file="C:/Users/lukas/OneDrive/Pulpit/funny/flesh.png")

program.iconphoto(True, program_icon)
program.minsize(300, 150)
program.geometry("1280x720")

frame = Frame(program, padding=40)
frame.pack(side=TOP)
button = Button(frame, text='Press Me!')
button.pack(side=TOP)
program.title("WTool")
mainloop()
