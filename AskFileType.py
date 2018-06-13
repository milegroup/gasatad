# -*- coding: utf-8 -*-

'''
This file is part of GASATaD.

GASATaD is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

GASATaD is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with GASATaD.  If not, see <http://www.gnu.org/licenses/>.
'''

import wx
import os

class AskFileType(wx.Dialog):
    def __init__(self, parent, ID, function, size=wx.DefaultSize, pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE):
        self.parent = parent
        self.function = function
        # function = "save" for saving files
        # function = "open" for opening new files
        # function = "add" for adding files to the data


        if self.function=="save":
            title = "Save data to file"
        elif self.function == "open":
            title = "Open new file"
        elif self.function=="add":
            title = "Add file to data"

        pre = wx.PreDialog()
        pre.Create(parent, ID, title, pos, size, style)
        self.PostCreate(pre)

        vSizer = wx.BoxSizer(wx.VERTICAL)

        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        csvIcon = wx.Image(str(os.path.dirname(__file__)) + "/icons/csv.png",
                           wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        csvButton = wx.BitmapButton(self, wx.ID_ANY, csvIcon, wx.DefaultPosition,
                                    wx.Size(100, 100), wx.BU_AUTODRAW)
        hSizer.Add(csvButton, 0, border=10, flag=wx.ALL)
        self.Bind(wx.EVT_BUTTON, self.CSVSelected, csvButton)

        xlsIcon = wx.Image(str(os.path.dirname(__file__)) + "/icons/xls.png",
                           wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        xlsButton = wx.BitmapButton(self, wx.ID_ANY, xlsIcon, wx.DefaultPosition,
                                    wx.Size(100, 100), wx.BU_AUTODRAW)
        hSizer.Add(xlsButton, 0, border=10, flag=wx.ALL)
        self.Bind(wx.EVT_BUTTON, self.XLSSelected, xlsButton)

        vSizer.Add(hSizer, 1, border=10, flag=wx.TOP | wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND)

        cancel = wx.Button(self, wx.ID_CANCEL, u"Cancel")
        vSizer.Add(cancel, 0, border=20, flag=wx.RIGHT | wx.BOTTOM | wx.ALIGN_RIGHT)

        self.SetSizer(vSizer)
        vSizer.Fit(self)

        self.Layout()
        self.Fit()
        self.Centre(wx.BOTH)
        self.Show(True)

    def CSVSelected(self, event):
        if self.function=='save':
            self.parent.saveToCSV()
        elif self.function == "open":
            self.parent.selectCSV(additionalFile=False)
        elif self.function == "add":
            self.parent.selectCSV(additionalFile=True)
        self.Close()

    def XLSSelected(self, event):
        if self.function == 'save':
            self.parent.saveToXLS()
        self.Close()

