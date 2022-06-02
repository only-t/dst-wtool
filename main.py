import wx
import base64

world_size = 65
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


class App(wx.App):
    def OnInit(self):
        print("gdfgdf")
        icon_frame = wx.Frame(None, -1, title='WTool', size=(640, 480))
        icon_frame.Show(True)
        icon_frame.SetIcon(wx.Icon("C:/Users/lukas/OneDrive/Pulpit/funny/t_emotes/t_prof.png"))

        self.SetTopWindow(icon_frame)

        wx.Frame()

        return True


if __name__ == '__main__':
    main_window = App()
    main_window.MainLoop()

# "C:/Users/lukas/OneDrive/Pulpit/funny/t_emotes/t_prof.png"