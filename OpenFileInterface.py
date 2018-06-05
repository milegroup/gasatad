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
import os
import wx
import wx.lib.filebrowsebutton as filebrowse


class PageOne(wx.Panel):
    def __init__(self, parent, dirfrom, CSVSepChar):
        wx.Panel.__init__(self, parent)

        vSizer = wx.BoxSizer(wx.VERTICAL)

        self.fileName = None
        self.dirName = None
        self.sepchar = None
        fileExtensions = "CSV files (*.csv)|*.csv;*.CSV|All files (*.*)|*.*"


        fbb = filebrowse.FileBrowseButton(self, -1, labelText='File: ', fileMask=fileExtensions,
                                          startDirectory=dirfrom, size=(450, -1),
                                          changeCallback=self.fbbCallback)

        vSizer.Add(fbb, flag=wx.EXPAND | wx.ALL, border=10)

        # ---------------------------------------

        # CSV Separator

        lblList = ['Comma', 'Semicolon', 'Tab']

        self.box = wx.RadioBox(self, label='CSV character separator', pos=(80, 10), choices=lblList, majorDimension=1,
                               style=wx.RA_SPECIFY_ROWS)
        vSizer.Add(self.box, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        if CSVSepChar == "Comma":
            self.box.SetSelection(0)
        elif CSVSepChar == "Semicolon":
            self.box.SetSelection(1)
        elif CSVSepChar == "Tab":
            self.box.SetSelection(2)
        self.sepchar = CSVSepChar


        vSizer.AddStretchSpacer(1)


        # ---------------------------------------

        # Ok and Cancel buttons

        okay = wx.Button(self, wx.ID_OK)
        cancel = wx.Button(self, wx.ID_CANCEL)
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()

        vSizer.Add(btns,  flag=wx.EXPAND | wx.TOP | wx.BOTTOM,
                     border=10)

        self.SetSizer(vSizer)
        vSizer.Fit(self)
        self.Layout()
        self.Fit()
        self.Centre(wx.BOTH)

    def fbbCallback(self, evt):
        print ('FileBrowseButton: %s\n' % evt.GetString())
        self.fileName = os.path.basename(evt.GetString())
        self.dirName = os.path.dirname(evt.GetString())
        if self.box.GetSelection() == 0:
            self.sepchar = 'Comma'
        elif self.box.GetSelection() == 1:
            self.sepchar = 'Semicolon'
        else:
            self.sepchar = 'Tab'


    def getOpenFileOptions(self):
        openFileOptions = dict (
            fileName=self.fileName,
            dirName=self.dirName,
            sepchar=self.sepchar
        )
        return openFileOptions




class PageTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is a PageTwo object", (40, 40))


class OpenFileInterface(wx.Dialog):
    def __init__(self, parent, dirfrom, CSVSepChar):
        wx.Dialog.__init__(self, None, title="Open file", size=(600, 400), pos = wx.DefaultPosition)

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Notebook(p)


        # add the pages to the notebook with the label to show on the tab
        self.one = PageOne(nb, dirfrom, CSVSepChar)
        page2 = PageTwo(nb)

        nb.AddPage(self.one, "CSV")
        nb.AddPage(page2, "XLS/XLSX")
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.activePage = 0

        # finally, put the notebook in a sizer for the panel to manage the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        self.Show(True)

    def OnPageChanged(self, event):
        self.activePage = event.GetSelection()
        print 'Page changed, new:%d' % (self.activePage)
        event.Skip()

    def getOpenFileOptions(self):
        if self.activePage == 0:
            openFileOptions = self.one.getOpenFileOptions()
            return openFileOptions
        else:
            return None
