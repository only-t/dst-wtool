import tkinter as tk
from tkinter import ttk
from math import ceil

main_window = tk.Tk()
main_window.minsize(640, 480)
main_window.geometry("640x480")
main_window.title("WTool")
main_window.iconphoto(True, tk.PhotoImage(file="C:/Users/lukas/OneDrive/Pulpit/funny/t_emotes/t_prof.png"))
main_window.configure(background="#c9c9c9")

mainMenuBar = tk.Menu(main_window)
main_window.config(menu=mainMenuBar)

fileMenu = tk.Menu(mainMenuBar, tearoff=False)
fileMenu.add_command(label="New", command=main_window.quit)
fileMenu.add_command(label="Open", command=main_window.quit)
fileMenu.add_command(label="Save", command=main_window.quit)
fileMenu.add_command(label="Save As", command=main_window.quit)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=main_window.quit)
mainMenuBar.add_cascade(label="File", menu=fileMenu)

topControlPanel = tk.Frame(main_window, bg="red", height=25)
topControlPanel.grid(row=0, column=0, columnspan=3, sticky="nwe")

rightControlPanel = tk.Frame(main_window, bg="black", width=200)
rightControlPanel.grid(row=1, column=2, sticky="nsw")
rightControlPanelLine = ttk.Separator(rightControlPanel, orient="vertical")
rightControlPanelLine.place(relheight=1, width=10)

editingArea = tk.Frame(main_window, bg="blue")
editingArea.grid(row=1, column=0, sticky="snew")

main_window.rowconfigure(1, weight=1)
main_window.columnconfigure(0, weight=1)

tk.mainloop()
