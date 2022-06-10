import wx
import numpy as N
from wx.lib.floatcanvas import Resources, GUIMode
from wx.lib.floatcanvas import NavCanvas, FloatCanvas


class CustomFloatCanvas(FloatCanvas.FloatCanvas):
    def Zoom(self, factor, center=None, centerCoords="World", keepPointInPlace=False):
        if (self.Scale >= 2 and factor > 1) or (self.Scale <= 0.35 and factor < 1):
            return None

        self.Parent.Parent.Parent.GenerateTiles()

        super().Zoom(factor, center=None, centerCoords="World", keepPointInPlace=False)

    def MoveImage(self, shift, CoordType, ReDraw=True):
        super().MoveImage(shift, CoordType, ReDraw=True)

        self.Parent.Parent.Parent.GenerateTiles()


class CustomNavCanvas(NavCanvas.NavCanvas):
    def __init__(self, parent, id = wx.ID_ANY, size = wx.DefaultSize, **kwargs):
        """
        Default class constructor.

        :param wx.Window `parent`: parent window. Must not be ``None``;
        :param integer `id`: window identifier. A value of -1 indicates a default value;
        :param `size`: a tuple or :class:`wx.Size`
        :param `**kwargs`: will be passed on to :class:`~lib.floatcanvas.FloatCanvas.FloatCanvas`
        """
        wx.Panel.__init__(self, parent, id, size=size)

        self.Modes = [
            ("Pointer",  GUIMode.GUIMouse(),   Resources.getPointerBitmap()),
            ("Pan",      GUIMode.GUIMove(),    Resources.getHandBitmap())
        ]

        self.BuildToolbar()
        self.ZoomButton.Destroy()
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.ToolBar, 0, wx.ALL | wx.ALIGN_LEFT | wx.GROW, 4)

        self.Canvas = CustomFloatCanvas(self, **kwargs)
        box.Add(self.Canvas, 1, wx.GROW)

        self.SetSizerAndFit(box)

        self.Canvas.SetMode(self.Modes[0][1])

        return None