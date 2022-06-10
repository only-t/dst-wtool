import wx
import base64
from wx.lib.floatcanvas import FloatCanvas
from customcanvas import CustomFloatCanvas, CustomNavCanvas
import customcanvas

world_size = 425
tile_size = 50

version = "VlJTTgABAAAA"

tiles = {
    "1": "IMPASSABLE",      #
    "2": "ROAD",            #
    "3": "ROCKY",           #
    "4": "DIRT",            #
    "5": "SAVANNA",         #
    "6": "GRASS",           #
    "7": "FOREST",          #
    '8': "MARSH",           #

    "10": "WOODFLOOR",      #
    "11": "CARPET",         #
    "12": "CHECKER",        #
    "13": "CAVE",           #
    "14": "FUNGUS",         #
    "15": "SINKHOLE",       #
    "16": "UNDERROCK",      #
    "17": "MUD",            #
    "18": "BRICK",          # Ruins Tiles, may be unstable
    "19": "BRICK_GLOW",     # Ruins Tiles, may be unstable
    "20": "TILES",          # Ruins Tiles, may be unstable
    "21": "TILES_GLOW",     # Ruins Tiles, may be unstable
    "22": "TRIM",           # Ruins Tiles, may be unstable
    "23": "TRIM_GLOW",      # Ruins Tiles, may be unstable
    "24": "FUNGUSRED",      #
    "25": "FUNGUSGREEN",    #

    "30": "DECIDUOUS",      #
    "31": "DESERT_DIRT",    #
    "32": "SCALE",          #

    "42": "PEBBLEBEACH",    #
    "43": "METEOR",         #
    "44": "SHELLBEACH",     #
    "45": "ARCHIVE",        #
    "46": "FUNGUSMOON",     #
    "47": "FARMING_SOIL",           #

    "201": "OCEAN_COASTAL",         #
    "202": "OCEAN_COASTAL_SHORE",   #
    "203": "OCEAN_SWELL",           #
    "204": "OCEAN_ROUGH",           #
    "205": "OCEAN_BRINEPOOL",           #?, wtf is that, placeholder
    "206": "OCEAN_BRINEPOOL_SHORE",     #?, wtf is that, placeholder
    "207": "OCEAN_HAZARDOUS",       #
    "208": "OCEAN_WATERLOG",        #
}


class MainWindow ( wx.Frame ):
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 822,560 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.Size( 640,480 ), wx.DefaultSize )
        self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        self.MenuBar = wx.MenuBar( 0 )
        self.MenuFile = wx.Menu()
        self.MenuItemNew = wx.MenuItem( self.MenuFile, wx.ID_ANY, u"New", wx.EmptyString, wx.ITEM_NORMAL )
        self.MenuFile.Append( self.MenuItemNew )

        self.MenuItemOpen = wx.MenuItem( self.MenuFile, wx.ID_ANY, u"Open", u"Open an existing Don't Starve Together world file.", wx.ITEM_NORMAL )
        self.MenuFile.Append( self.MenuItemOpen )

        self.MenuItemSave = wx.MenuItem( self.MenuFile, wx.ID_ANY, u"Save", wx.EmptyString, wx.ITEM_NORMAL )
        self.MenuFile.Append( self.MenuItemSave )

        self.MenuBar.Append( self.MenuFile, u"File" )

        self.MenuGenerate = wx.Menu()
        self.MenuBar.Append( self.MenuGenerate, u"Generate" )

        self.SetMenuBar( self.MenuBar )

        MainSizer = wx.BoxSizer( wx.VERTICAL )

        self.MainWindowSplitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_3DBORDER|wx.SP_3DSASH|wx.SP_BORDER|wx.SP_LIVE_UPDATE|wx.SP_NOBORDER|wx.SP_NO_XP_THEME )
        self.MainWindowSplitter.SetSashGravity(1)
        self.MainWindowSplitter.Bind( wx.EVT_IDLE, self.MainWindowSplitterOnIdle )
        self.MainWindowSplitter.SetMinimumPaneSize( 200 )

        self.MainWindowSplitter.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        self.TilesCanvasPanel = CustomNavCanvas(self.MainWindowSplitter, BackgroundColor="#adadad", ProjectionFun=None, Debug=0)
        self.TilesCanvasPanel.SetMinSize( wx.Size( 300,-1 ) )

        self.OptionsPanel = wx.Panel( self.MainWindowSplitter, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
        self.OptionsPanel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )
        self.OptionsPanel.SetMinSize( wx.Size( 300,-1 ) )

        OptionsSizer = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        self.ButtonImpassable = wx.Button( self.OptionsPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE|wx.BU_EXACTFIT )

        self.ButtonImpassable.SetBitmap( wx.Bitmap( u"images/IMPASSABLE.jpg", wx.BITMAP_TYPE_ANY ) )
        self.ButtonImpassable.SetMaxSize( wx.Size( 50,50 ) )

        OptionsSizer.Add( self.ButtonImpassable, 0, 0, 5 )

        self.ButtonRoad = wx.Button( self.OptionsPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE|wx.BU_EXACTFIT )

        self.ButtonRoad.SetBitmap( wx.Bitmap( u"images/ROAD.jpg", wx.BITMAP_TYPE_ANY ) )
        self.ButtonRoad.SetMaxSize( wx.Size( 50,50 ) )

        OptionsSizer.Add( self.ButtonRoad, 0, 0, 5 )

        self.ButtonRocky = wx.Button( self.OptionsPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE|wx.BU_EXACTFIT )

        self.ButtonRocky.SetBitmap( wx.Bitmap( u"images/ROCKY.jpg", wx.BITMAP_TYPE_ANY ) )
        self.ButtonRocky.SetMaxSize( wx.Size( 50,50 ) )

        OptionsSizer.Add(self.ButtonRocky, 0, 0, 5)

        self.OptionsPanel.SetSizer( OptionsSizer )
        self.OptionsPanel.Layout()
        OptionsSizer.Fit( self.OptionsPanel )
        self.MainWindowSplitter.SplitVertically( self.TilesCanvasPanel, self.OptionsPanel, 604 )
        MainSizer.Add( self.MainWindowSplitter, 1, wx.EXPAND, 5 )

        self.SetSizer( MainSizer )
        self.Layout()
        self.StatusBar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_MENU, self.OpenFile, id = self.MenuItemOpen.GetId() )

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def OpenFile(self, event):
        openFileDialog = wx.FileDialog(self, "Open", "", "", "*.*", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()

        filepath = openFileDialog.GetPath()
        if filepath:
            file = open(filepath, "r")
            self.LoadWorldData(file)
        else:
            print("ERROR")

        openFileDialog.Destroy()

    def MainWindowSplitterOnIdle(self, event):
        self.MainWindowSplitter.SetSashPosition(484)
        self.MainWindowSplitter.Unbind(wx.EVT_IDLE)

    def LoadWorldData(self, datafile):
        for line in datafile.readlines():
            if line.find("tiles") > 0:
                self.tiles_data = []

                starting_index = line.find("\"", 0) + 1
                ending_index = line.find("\"", starting_index)

                base64encodedtilesdata = line[starting_index+len(version):ending_index]
                bytetilesdata = base64.b64decode(base64encodedtilesdata)

                for tile_index in range(len(bytetilesdata)):
                    if tile_index%2 == 0: # For some reason it should only check for every other byte, idk, that's how the map data works i guess...
                        x = tile_size * ((tile_index // 2) % world_size)
                        y = tile_size * ((tile_index // 2) // world_size)

                        self.tiles_data.append([bytetilesdata[tile_index], x, y])

                self.GenerateTiles()

    def FindTileImage(self, id):
        if id != 255 and id in tiles:
            return tiles[id]
        else:
            return "INVALID"

    def GenerateTiles(self):
        if not hasattr(self, "tiles_data") or self.tiles_data == []:
            return None

        bbox_x1 = self.TilesCanvasPanel.Canvas.ViewPortBB[0][0]
        bbox_y1 = self.TilesCanvasPanel.Canvas.ViewPortBB[0][1]
        bbox_x2 = self.TilesCanvasPanel.Canvas.ViewPortBB[1][0]
        bbox_y2 = self.TilesCanvasPanel.Canvas.ViewPortBB[1][1]

        for tiles_data_index in range(len(self.tiles_data)):
            tiledata = self.tiles_data[tiles_data_index]

            if tiledata != []:
                if (tiledata[1] >= bbox_x1 and tiledata[2] >= bbox_y1) and (tiledata[1] <= bbox_x2 and tiledata[2] <= bbox_y2):
                    tile_image = self.FindTileImage(str(tiledata[0]))

                    self.TilesCanvasPanel.Canvas.AddObject(FloatCanvas.ScaledBitmap(wx.Bitmap(
                        "images/"+tile_image+".jpg"),
                        (tiledata[1], tiledata[2]),
                        55, # Make the tile a little bigger then it should be to eliminate seams
                        Position="cc"))

                    self.tiles_data[tiles_data_index] = []

        self.TilesCanvasPanel.Canvas.Draw()


if __name__ == '__main__':
    app = wx.App()
    main_window = MainWindow(None)
    main_window.Show(True)

    app.MainLoop()
