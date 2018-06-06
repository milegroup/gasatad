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

    # Panel for csv files

    def __init__(self, parent, dirfrom):
        wx.Panel.__init__(self, parent)

        vSizer = wx.BoxSizer(wx.VERTICAL)

        self.fileName = None
        self.dirName = None
        fileExtensions = "CSV files (*.csv)|*.csv;*.CSV|All files (*.*)|*.*"
        self.previewNRows = 4
        self.previewNCols = 6
        self.colLabelsDefault = ['A','B','C','D','E','F']


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
        self.Bind(wx.EVT_RADIOBOX, self.optionsChanged, self.CSVSepRBBox)

        self.CSVSepRBBox.SetSelection(0)

        # ---------------------------------------

        # Options

        optionsSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Options"), wx.HORIZONTAL)

        self.discardFirstCol = wx.CheckBox(self, wx.ID_ANY, "Discard first column", wx.DefaultPosition, wx.DefaultSize, 0)
        optionsSizer.Add(self.discardFirstCol, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        self.Bind(wx.EVT_CHECKBOX, self.optionsChanged, self.discardFirstCol)

        vSizer.Add(optionsSizer, flag = wx.EXPAND | wx.ALL, border = 10)

        # ---------------------------------------

        self.provDataTable = wx.grid.Grid(self)

        # Grid
        self.provDataTable.CreateGrid(self.previewNRows, self.previewNCols)
        self.provDataTable.EnableEditing(False)
        self.provDataTable.EnableGridLines(True)
        self.provDataTable.EnableDragGridSize(False)
        self.provDataTable.SetMargins(0, 0)

        # Columns
        self.provDataTable.EnableDragColMove(False)
        self.provDataTable.EnableDragColSize(False)
        self.provDataTable.SetColLabelSize(30)
        self.provDataTable.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.provDataTable.EnableDragRowSize(False)
        self.provDataTable.SetRowLabelSize(80)
        self.provDataTable.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Cell Defaults
        self.provDataTable.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTER)

        dataSizer = wx.BoxSizer(wx.HORIZONTAL)
        dataSizer.Add(self.provDataTable)
        self.provDataTable.Enable(False)
        self.provDataTable.Show(True)
        self.provDataTable.AutoSize()

        vSizer.Add(dataSizer, flag = wx.ALL | wx.EXPAND, border=10)

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

        self.updatePreview()

    def optionsChanged(self, evt):
        self.updatePreview()

    def updatePreview(self):

        from pandas.io.parsers import read_csv
        import sys, numpy


        try:

            if self.CSVSepRBBox.GetSelection() == 0:
                sepchar = ','
            elif self.CSVSepRBBox.GetSelection() == 1:
                sepchar = ';'
            else:
                sepchar = '\t'

            self.data = read_csv(os.path.join(self.dirName, self.fileName), sep=sepchar, header=0, engine='python', encoding='utf-8')

            if self.discardFirstCol.IsChecked():
                self.data.drop(self.data.columns[[0]], axis=1, inplace=True)
            nRows = len(self.data.index)
            nCols = len(self.data.columns)
            # print "Rows: ", nRows
            # print "Cols: ", nCols

            colLabels = self.data.columns
            for col in range(self.previewNCols):
                if col >= nCols:
                    self.provDataTable.SetColLabelValue(col, self.colLabelsDefault[col])
                    continue
                self.provDataTable.SetColLabelValue(col, colLabels[col])

            for row in range(self.previewNRows):
                for col in range(self.previewNCols):
                    if row >= nRows or col >= nCols:
                        self.provDataTable.SetCellValue(row, col, "")
                        continue

                    if self.data.iloc[row, col] != self.data.iloc[row, col]:
                        self.provDataTable.SetCellValue(row, col, "nan")
                    elif type(self.data.iloc[row, col]) in (int, float, long, complex, numpy.float64, numpy.int64):
                        self.provDataTable.SetCellValue(row, col, '{:5g}'.format(self.data.iloc[row, col]))
                    else:
                        self.provDataTable.SetCellValue(row, col, self.data.iloc[row, col])
            self.provDataTable.Enable(True)
            self.provDataTable.AutoSize()
        except:
            # print "Error: ", sys.exc_info()
            self.cleanPreview()

    def cleanPreview(self):
        for col in range(self.previewNCols):
            self.provDataTable.SetColLabelValue(col, self.colLabelsDefault[col])
            # self.provDataTable.SetColSize(col, self.provDataTable.GetDefaultColSize()-10)
        for row in range(self.previewNRows):
            for col in range(self.previewNCols):
                self.provDataTable.SetCellValue(row, col, "")
        self.provDataTable.AutoSize()
        self.provDataTable.Enable(False)


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




class PageTwo(wx.Panel):

    # Panel for xls files


    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is a PageTwo object", (40, 40))


class OpenFileInterface(wx.Dialog):
    def __init__(self, parent, dirfrom):
        wx.Dialog.__init__(self, None, title="Open file", size=(600, 500), pos = wx.DefaultPosition, style=wx.RESIZE_BORDER)

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Notebook(p)


        # add the pages to the notebook with the label to show on the tab
        self.one = PageOne(nb, dirfrom)
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
