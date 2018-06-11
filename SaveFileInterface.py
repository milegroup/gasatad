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


class CVSPanel(wx.Panel):

    # Panel for csv files

    def __init__(self, parent, dirfrom):
        wx.Panel.__init__(self, parent)

        vSizer = wx.BoxSizer(wx.VERTICAL)

        self.fileName = None
        self.dirName = None
        fileExtensions = "CSV files (*.csv)|*.csv;*.CSV|All files (*.*)|*.*"

        fbb = filebrowse.FileBrowseButton(self, -1, labelText='File: ', fileMask=fileExtensions,
                                          startDirectory=dirfrom, size=(450, -1),
                                          changeCallback=self.fbbCallback)

        vSizer.Add(fbb, flag=wx.EXPAND | wx.ALL, border=10)

        # ---------------------------------------

        # CSV Separator

        lblList = ['Comma', 'Semicolon', 'Tab']

        self.CSVSepRBBox = wx.RadioBox(self, label='CSV character separator', pos=(80, 10), choices=lblList, majorDimension=1,
                                       style=wx.RA_SPECIFY_ROWS)
        vSizer.Add(self.CSVSepRBBox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        self.CSVSepRBBox.SetSelection(0)

        # ---------------------------------------

        # Options

        optionsSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Options"), wx.VERTICAL)

        self.discardFirstCol = wx.CheckBox(self, wx.ID_ANY, "Discard first column", wx.DefaultPosition, wx.DefaultSize, 0)
        optionsSizer.Add(self.discardFirstCol, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)

        vSizer.Add(optionsSizer, flag = wx.EXPAND | wx.ALL, border = 10)

        # ---------------------------------------

        vSizer.AddStretchSpacer(1)

        # Ok and Cancel buttons

        okay = wx.Button(self, wx.ID_OK)
        cancel = wx.Button(self, wx.ID_CANCEL)
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()

        vSizer.Add(btns,  flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=10)

        self.SetSizer(vSizer)
        vSizer.Fit(self)
        self.Layout()
        self.Fit()
        self.Centre(wx.BOTH)

    def fbbCallback(self, evt):
        # print ('FileBrowseButton: %s\n' % evt.GetString())
        self.fileName = os.path.basename(evt.GetString())
        self.dirName = os.path.dirname(evt.GetString())


    def getOpenFileOptions(self):

        if self.CSVSepRBBox.GetSelection() == 0:
            sepchar = 'Comma'
        elif self.CSVSepRBBox.GetSelection() == 1:
            sepchar = 'Semicolon'
        else:
            sepchar = 'Tab'

        openFileOptions = dict(
            fileType='csv',
            fileName=self.fileName,
            dirName=self.dirName,
            sepchar=sepchar,
            discardFirstCol=self.discardFirstCol.IsChecked()
        )
        return openFileOptions




class XLSPanel(wx.Panel):

    # Panel for xls files

    def __init__(self, parent, dirfrom):
        wx.Panel.__init__(self, parent)

        vSizer = wx.BoxSizer(wx.VERTICAL)

        self.fileName = None
        self.dirName = None
        fileExtensions = "Excel files (*.xls;*.xlsx)|*.xls;*.xlsx;*.XLS;*.XLSX|All files (*.*)|*.*"

        # ---------------------------------------

        fileSizer = wx.BoxSizer(wx.HORIZONTAL)

        fileSizer.Add(wx.StaticText(self, label='File:'), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)

        fileSizer.Add(wx.TextCtrl(self,0,'afsdf'), 0, wx.EXPAND)

        vSizer.Add(fileSizer, flag=wx.EXPAND | wx.ALL, border=10)

        # ---------------------------------------

        fbb = filebrowse.FileBrowseButton(self, -1, labelText='File: ', fileMask=fileExtensions,
                                          startDirectory=dirfrom, size=(450, -1),
                                          changeCallback=self.fbbCallback)

        vSizer.Add(fbb, flag=wx.EXPAND | wx.ALL, border=10)


        # ---------------------------------------

        # Options

        optionsBoxSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Options"), wx.VERTICAL)

        optionsGridSizer = wx.FlexGridSizer(rows=3, cols=2, vgap=4, hgap=4)

        self.RowWithColNames = wx.SpinCtrl(self, value='0', size=(80, -1))
        self.RowWithColNames.SetRange(0, 100)
        optionsGridSizer.Add(wx.StaticText(self, label='Row containing col. names:'), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        optionsGridSizer.Add(self.RowWithColNames, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)


        self.NoColsDiscard = wx.SpinCtrl(self, value='0', size=(80, -1))
        self.NoColsDiscard.SetRange(0, 100)
        optionsGridSizer.Add(wx.StaticText(self, label='No. of columns to discard:'), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        optionsGridSizer.Add(self.NoColsDiscard, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)


        self.sheetNumber = wx.SpinCtrl(self, value='0', size=(80, -1))
        self.sheetNumber.SetRange(0, 10)
        optionsGridSizer.Add(wx.StaticText(self, label='Sheet number:'), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        optionsGridSizer.Add(self.sheetNumber, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)

        optionsBoxSizer.Add(optionsGridSizer, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)

        vSizer.Add(optionsBoxSizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # ---------------------------------------

        vSizer.AddStretchSpacer(1)

        # ---------------------------------------

        # Ok and Cancel buttons

        okay = wx.Button(self, wx.ID_OK)
        cancel = wx.Button(self, wx.ID_CANCEL)
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()

        vSizer.Add(btns, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=10)

        self.SetSizer(vSizer)
        vSizer.Fit(self)
        self.Layout()
        self.Fit()
        self.Centre(wx.BOTH)


    def fbbCallback(self, evt):
        print ('FileBrowseButton: %s\n' % evt.GetString())
        self.fileName = os.path.basename(evt.GetString())
        self.dirName = os.path.dirname(evt.GetString())

    def getOpenFileOptions(self):

        openFileOptions = dict(
            fileType='xls',
            fileName=self.fileName,
            dirName=self.dirName,
            rowColNames=self.RowWithColNames.GetValue(),
            noColsDiscard=self.NoColsDiscard.GetValue(),
            sheetNumber=self.sheetNumber.GetValue()
        )
        return openFileOptions





class SaveFileInterface(wx.Dialog):
    def __init__(self, parent, dirfrom):
        wx.Dialog.__init__(self, None, title="Open file", size=(600, 500), pos = wx.DefaultPosition, style=wx.RESIZE_BORDER)

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # add the pages to the notebook with the label to show on the tab
        self.one = CVSPanel(nb, dirfrom)
        self.two = XLSPanel(nb, dirfrom)

        nb.AddPage(self.one, "CSV")
        nb.AddPage(self.two, "XLS/XLSX")
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.activePage = 0

        # finally, put the notebook in a sizer for the panel to manage the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        self.Show(True)

    def OnPageChanged(self, event):
        self.activePage = event.GetSelection()
        # print 'Page changed, new:%d' % (self.activePage)
        event.Skip()

    def getOpenFileOptions(self):
        if self.activePage == 0:
            openFileOptions = self.one.getOpenFileOptions()
            return openFileOptions
        elif self.activePage == 1:
            openFileOptions = self.two.getOpenFileOptions()
            return openFileOptions
        else:
            return None
