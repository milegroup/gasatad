# -*- coding: utf-8 -*- 

import wx

from MainFrame import MainFrame



app = wx.App(False)
mainFrame = MainFrame(None)
mainFrame.Centre()
app.MainLoop()