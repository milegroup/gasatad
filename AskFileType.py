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
    def __init__(self, parent, ID, function, size=wx.DefaultSize, pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE,
                 *args, **kw):

        wx.Dialog.__init__(self)

        self.parent = parent
        self.function = function
        # function = "save" for saving files
        # function = "open" for opening new files
        # function = "add" for adding files to the data

        if self.function == "save":
            title = "Save data to file"
        elif self.function == "open":
            title = "Open new file"
        elif self.function == "add":
            title = "Add file to data"

        self.Create(parent, ID, title, pos, size, style)

        vSizer = wx.BoxSizer(wx.VERTICAL)

        hSizer = wx.BoxSizer(wx.HORIZONTAL)


        if self.function == "open" or self.function == "add":
            csvIcon = wx.Image(str(os.path.dirname(__file__)) + "/icons/FromCSV.png",
                               wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        else:
            csvIcon = wx.Image(str(os.path.dirname(__file__)) + "/icons/ToCSV.png",
                               wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        csvButton = wx.BitmapButton(self, wx.ID_ANY, csvIcon, wx.DefaultPosition, wx.Size(100, 100), wx.BU_AUTODRAW)
        hSizer.Add(csvButton, 0, border=10, flag=wx.ALL)
        self.Bind(wx.EVT_BUTTON, self.CSVSelected, csvButton)


        if self.function == "open" or self.function == "add":
            xlsIcon = wx.Image(str(os.path.dirname(__file__)) + "/icons/FromXLS.png",
                               wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        else:
            xlsIcon = wx.Image(str(os.path.dirname(__file__)) + "/icons/ToXLS.png",
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
        if self.function == 'save':
            self.parent.saveToCSV()
        elif self.function == "open":
            self.parent.selectCSV(additionalFile=False)
        elif self.function == "add":
            self.parent.selectCSV(additionalFile=True)
        self.Close()

    def XLSSelected(self, event):
        if self.function == 'save':
            self.parent.saveToXLS()
        elif self.function == "open":
            self.parent.selectXLS(additionalFile=False)
        elif self.function == "add":
            self.parent.selectXLS(additionalFile=True)
        self.Close()
