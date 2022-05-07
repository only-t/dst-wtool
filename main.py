import tkinter as tk
import base64
from PIL import Image, ImageTk
from tkinter import filedialog

version = "VlJTTgABAAAA"
tiles_base64 = {
    "": "impassable",
    "É‡": "ocean_end",
    "": "rocky",
}


class MainScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.minsize(640, 480)
        self.geometry("640x480")
        self.title("WTool")
        self.iconphoto(True, tk.PhotoImage(file="C:/Users/lukas/OneDrive/Pulpit/funny/t_emotes/t_prof.png"))
        self.configure(background="#c9c9c9")

        self.mainMenuBar = WindowMenuBar(self)
        self.config(menu=self.mainMenuBar)

        self.fileMenu = FileMenu(self.mainMenuBar)
        self.mainMenuBar.add_cascade(label="File", menu=self.fileMenu)

        self.topControlPanel = TopPanel(self)
        self.topControlPanel.grid(row=0, column=0, columnspan=3, sticky="new")

        self.bottomControlPanel = BottomPanel(self)
        self.bottomControlPanel.grid(row=2, column=0, columnspan=3, sticky="sew")

        self.rightControlPanel = RightPanel(self)
        self.rightControlPanel.grid(row=1, column=2, sticky="snw")

        self.editingArea = EditingArea(self)
        self.editingArea.grid(row=1, column=0, sticky="snew")


class WindowMenuBar(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)


def start_of_tiles(line):
    starting_index = 0
    ending_index = 0

    if line.find("tiles=") >= 0:
        starting_index = line.find("tiles=") + len("tiles=") + len(version) + 1
        ending_index = line.find(",") - 1

    return starting_index, ending_index


def open_file():
    file = filedialog.askopenfile()

    if file:
        for line in file.readlines():
            if line.find("tiles=") >= 0:
                starting_index, ending_index = start_of_tiles(line)

                # codedBytes = line[starting_index:ending_index]
                codedBytes = open("C:/Users/lukas/OneDrive/Pulpit/tiles_encoded.txt", "r").readline()
                decodedBytes = base64.b64decode(codedBytes)
                decodedString = str(decodedBytes, "utf-8")

                main_window.editingArea.import_tiles_data(decodedString, 61)


class FileMenu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent, tearoff=False)
        self.add_command(label="New", command=close_program)
        self.add_command(label="Open", command=open_file)
        self.add_command(label="Save", command=close_program)
        self.add_command(label="Save As", command=close_program)
        self.add_separator()
        self.add_command(label="Exit", command=close_program)


class TopPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, height=50, bg="red")


class BottomPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, height=25, bg="green")


class RightPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=250, bg="#bababa")


class EditingArea(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = tk.Canvas(self, highlightthickness=4, highlightbackground="gray")
        self.canvas.grid(row=0, column=0, sticky="snew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas.bind("<ButtonPress-3>", self.scroll_start)
        self.canvas.bind("<ButtonRelease-3>", self.scroll_stop)
        self.canvas.bind("<B3-Motion>", self.scroll_move)

        self.empty_label = tk.Label(self, text="Empty", font=("Helvetica", "64"), fg="#e5e5e5")
        self.empty_label.grid(row=0, column=0)

    def draw_grid(self, tiles, world_size):
        self.size = world_size
        self.canvas.tiles = []
        self.empty_label.destroy()

        self.construct_scrollers()

        for row in range(0, self.size):
            self.canvas.tiles.append([])

            for column in range(0, self.size):
                print(str(row*2*self.size + column*2) + " " + str(row*2*self.size + column*2 + 1))
                tile_name = tiles_base64[tiles[row*2*self.size + column*2] + tiles[row*2*self.size + column*2 + 1]]
                tile = ImageTk.PhotoImage(Image.open("images/" + tile_name + ".png").resize((50, 50)))
                self.canvas.create_image(row*50, column*50, image=tile, anchor="nw")
                self.canvas.tiles[row].append(tile)

    def construct_scrollers(self):
        self.horizontal_scroll = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.vertical_scroll = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vertical_scroll.set, xscrollcommand=self.horizontal_scroll.set)
        self.canvas.configure(scrollregion=(0, 0, self.size*50, self.size*50))

        self.horizontal_scroll.grid(row=1, column=0, sticky="ew")
        self.vertical_scroll.grid(row=0, column=1, sticky="sn")

    def import_tiles_data(self, tiles_data, world_size):
        print(tiles_data)

        self.draw_grid(tiles_data, world_size)

    def scroll_start(self, event):
        self.canvas.configure(cursor="fleur")
        self.canvas.scan_mark(event.x, event.y)

    def scroll_stop(self, event):
        self.canvas.configure(cursor="arrow")

    def scroll_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)


def close_program():
    main_window.quit()


main_window = MainScreen()
main_window.rowconfigure(1, weight=1)
main_window.columnconfigure(0, weight=1)

main_window.mainloop()
