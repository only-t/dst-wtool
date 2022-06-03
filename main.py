import wx
import base64
import subprocess

world_size = 65
tiles_index = 33
version = "VlJTTgABAAAA"
tiles_base64 = {
    "255": "INVALID",
    "1": "IMPASSABLE",

    "2": "ROAD",
    "3": "ROCKY",
    "4": "DIRT",
    "5": "SAVANNA",
    "6": "GRASS",
    "7": "FOREST",
    '8': "MARSH",
    "9": "WEB",
    "10": "WOODFLOOR",
    "11": "CARPET",
    "12": "CHECKER",

    "13": "CAVE",
    "14": "FUNGUS",
    "15": "SINKHOLE",
    "16": "UNDERROCK",
    "17": "MUD",
    "18": "BRICK",
    "19": "BRICK_GLOW",
    "20": "TILES",
    "21": "TILES_GLOW",
    "22": "TRIM",
    "23": "TRIM_GLOW",
    "24": "FUNGUSRED",
    "25": "FUNGUSGREEN",

    "30": "DECIDUOUS",
    "31": "DESERT_DIRT",
    "32": "SCALE",

    "33": "LAVAARENA_FLOOR",
    "34": "LAVAARENA_TRIM",

    "35": "QUAGMIRE_PEATFOREST",
    "36": "QUAGMIRE_PARKFIELD",
    "37": "QUAGMIRE_PARKSTONE",
    "38": "QUAGMIRE_GATEWAY",
    "39": "QUAGMIRE_SOIL",
    "41": "QUAGMIRE_CITYSTONE",

    "42": "PEBBLEBEACH",
    "43": "METEOR",
    "44": "SHELLBEACH",

    "45": "ARCHIVE",
    "46": "FUNGUSMOON",

    "47": "FARMING_SOIL",

    "120": "FUNGUSMOON_NOISE",
    "121": "METEORMINE_NOISE",
    "122": "METEORCOAST_NOISE",
    "123": "DIRT_NOISE",
    "124": "ABYSS_NOISE",
    "125": "GROUND_NOISE",
    "126": "CAVE_NOISE",
    "127": "FUNGUS_NOISE",

    "128": "UNDERGROUND",

    "129": "WALL_ROCKY",
    "130": "WALL_DIRT",
    "131": "WALL_MARSH",
    "132": "WALL_CAVE",
    "133": "WALL_FUNGUS",
    "134": "WALL_SINKHOLE",
    "135": "WALL_MUD",
    "136": "WALL_TOP",
    "137": "WALL_WOOD",
    "138": "WALL_HUNESTONE",
    "139": "WALL_HUNESTONE_GLOW",
    "140": "WALL_STONEEYE",
    "141": "WALL_STONEEYE_GLOW",

    "200": "FAKE_GROUND",

    "201": "OCEAN_COASTAL",
    "202": "OCEAN_COASTAL_SHORE",
    "203": "OCEAN_SWELL",
    "204": "OCEAN_ROUGH",
    "205": "OCEAN_BRINEPOOL",
    "206": "OCEAN_BRINEPOOL_SHORE",
    "207": "OCEAN_HAZARDOUS",
    "208": "OCEAN_WATERLOG",

    "247": "OCEAN_END",
}


class MainWindow(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(822, 560), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.Size(640, 480), wx.DefaultSize)
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        self.MenuBar = wx.MenuBar(0)
        self.MenuFile = wx.Menu()
        self.MenuItemNew = wx.MenuItem(self.MenuFile, wx.ID_ANY, u"New", wx.EmptyString, wx.ITEM_NORMAL)
        self.MenuFile.Append(self.MenuItemNew)

        self.MenuItemOpen = wx.MenuItem(self.MenuFile, wx.ID_ANY, u"Open",
                                        u"Open an existing Don't Starve Together world file.", wx.ITEM_NORMAL)
        self.MenuFile.Append(self.MenuItemOpen)

        self.MenuItemSave = wx.MenuItem(self.MenuFile, wx.ID_ANY, u"Save", wx.EmptyString, wx.ITEM_NORMAL)
        self.MenuFile.Append(self.MenuItemSave)

        self.MenuBar.Append(self.MenuFile, u"File")

        self.MenuGenerate = wx.Menu()
        self.MenuBar.Append(self.MenuGenerate, u"Generate")

        self.SetMenuBar(self.MenuBar)

        self.ToolBar = self.CreateToolBar(wx.TB_HORIZONTAL, wx.ID_ANY)
        self.ToolBar.Realize()

        MainSizer = wx.FlexGridSizer(0, 2, 0, 0)
        MainSizer.AddGrowableCol(0)
        MainSizer.AddGrowableRow(0)
        MainSizer.SetFlexibleDirection(wx.BOTH)
        MainSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.MainWindowSplitter = wx.SplitterWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                    wx.SP_3D | wx.SP_LIVE_UPDATE)
        self.MainWindowSplitter.Bind(wx.EVT_IDLE, self.MainWindowSplitterOnIdle)
        self.MainWindowSplitter.SetMinimumPaneSize(200)

        self.TilesPanel = wx.Panel(self.MainWindowSplitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)
        self.TilesPanel.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))

        self.OptionsPanel = wx.Panel(self.MainWindowSplitter, wx.ID_ANY, wx.DefaultPosition, wx.Size(350, -1),
                                     wx.TAB_TRAVERSAL)
        self.OptionsPanel.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        wSizer1 = wx.WrapSizer(wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS)

        self.ButtonImpassable = wx.Button(self.OptionsPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                          wx.DefaultSize, wx.BORDER_NONE | wx.BU_EXACTFIT)

        self.ButtonImpassable.SetBitmap(wx.Bitmap(u"images/IMPASSABLE.png", wx.BITMAP_TYPE_ANY))
        wSizer1.Add(self.ButtonImpassable, 0, 0, 5)

        self.ButtonOceanBrinepool = wx.Button(self.OptionsPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                              wx.DefaultSize, wx.BORDER_NONE | wx.BU_EXACTFIT)

        self.ButtonOceanBrinepool.SetBitmap(wx.Bitmap(u"images/OCEAN_BRINEPOOL.png", wx.BITMAP_TYPE_ANY))
        wSizer1.Add(self.ButtonOceanBrinepool, 0, 0, 5)

        self.ButtonOceanBrinepoolShore = wx.Button(self.OptionsPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                   wx.DefaultSize, wx.BORDER_NONE | wx.BU_EXACTFIT)

        self.ButtonOceanBrinepoolShore.SetBitmap(wx.Bitmap(u"images/OCEAN_BRINEPOOL_SHORE.png", wx.BITMAP_TYPE_ANY))
        wSizer1.Add(self.ButtonOceanBrinepoolShore, 0, 0, 5)

        self.ButtonOceanCoastal = wx.Button(self.OptionsPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                            wx.DefaultSize, wx.BORDER_NONE | wx.BU_EXACTFIT)

        self.ButtonOceanCoastal.SetBitmap(wx.Bitmap(u"images/OCEAN_COASTAL.png", wx.BITMAP_TYPE_ANY))
        wSizer1.Add(self.ButtonOceanCoastal, 0, 0, 5)

        self.ButtonOceanCoastalShore = wx.Button(self.OptionsPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                 wx.DefaultSize, wx.BORDER_NONE | wx.BU_EXACTFIT)

        self.ButtonOceanCoastalShore.SetBitmap(wx.Bitmap(u"images/OCEAN_COASTAL_SHORE.png", wx.BITMAP_TYPE_ANY))
        wSizer1.Add(self.ButtonOceanCoastalShore, 0, 0, 5)

        self.ButtonOceanHazardous = wx.Button(self.OptionsPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                              wx.DefaultSize, wx.BORDER_NONE | wx.BU_EXACTFIT)

        self.ButtonOceanHazardous.SetBitmap(wx.Bitmap(u"images/OCEAN_HAZARDOUS.png", wx.BITMAP_TYPE_ANY))
        wSizer1.Add(self.ButtonOceanHazardous, 0, 0, 5)

        self.ButtonOceanRough = wx.Button(self.OptionsPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                          wx.DefaultSize, wx.BORDER_NONE | wx.BU_EXACTFIT)

        self.ButtonOceanRough.SetBitmap(wx.Bitmap(u"images/OCEAN_ROUGH.png", wx.BITMAP_TYPE_ANY))
        wSizer1.Add(self.ButtonOceanRough, 0, 0, 5)

        self.ButtonOceanSwell = wx.Button(self.OptionsPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                          wx.DefaultSize, wx.BORDER_NONE | wx.BU_EXACTFIT)

        self.ButtonOceanSwell.SetBitmap(wx.Bitmap(u"images/OCEAN_SWELL.png", wx.BITMAP_TYPE_ANY))
        wSizer1.Add(self.ButtonOceanSwell, 0, 0, 5)

        self.ButtonOceanWaterlog = wx.Button(self.OptionsPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                             wx.DefaultSize, wx.BORDER_NONE | wx.BU_EXACTFIT)

        self.ButtonOceanWaterlog.SetBitmap(wx.Bitmap(u"images/OCEAN_WATERLOG.png", wx.BITMAP_TYPE_ANY))
        wSizer1.Add(self.ButtonOceanWaterlog, 0, 0, 5)

        self.ButtonRoad = wx.Button(self.OptionsPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                    wx.BORDER_NONE | wx.BU_EXACTFIT)

        self.ButtonRoad.SetBitmap(wx.Bitmap(u"images/ROAD.png", wx.BITMAP_TYPE_ANY))
        wSizer1.Add(self.ButtonRoad, 0, 0, 5)

        self.ButtonRocky = wx.Button(self.OptionsPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                     wx.BORDER_NONE | wx.BU_EXACTFIT)

        self.ButtonRocky.SetBitmap(wx.Bitmap(u"images/ROCKY.png", wx.BITMAP_TYPE_ANY))
        wSizer1.Add(self.ButtonRocky, 0, 0, 5)

        self.OptionsPanel.SetSizer(wSizer1)
        self.OptionsPanel.Layout()
        self.MainWindowSplitter.SplitVertically(self.TilesPanel, self.OptionsPanel, 484)
        MainSizer.Add(self.MainWindowSplitter, 1, wx.EXPAND, 5)

        self.SetSizer(MainSizer)
        self.Layout()
        self.StatusBar = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_MENU, self.OpenFile, id=self.MenuItemOpen.GetId())

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def OpenFile(self, event):
        openFileDialog = wx.FileDialog(self, "Open", "", "", "*.*", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()

        filepath = openFileDialog.GetPath()
        file = open(filepath, "r")
        self.LoadWorldData(file)

        openFileDialog.Destroy()

    def MainWindowSplitterOnIdle(self, event):
        self.MainWindowSplitter.SetSashPosition(484)
        self.MainWindowSplitter.Unbind(wx.EVT_IDLE)

    def LoadWorldData(self, datafile):
        for line in datafile.readlines():
            if line.find("tiles") > 0:
                ending_index = line.find("\"", tiles_index)


if __name__ == '__main__':
    app = wx.App()
    main_window = MainWindow(None)
    main_window.Show(True)

    app.MainLoop()
