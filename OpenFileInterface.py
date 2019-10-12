"""
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
"""
import os
import wx
import wx.lib.filebrowsebutton as filebrowse


class OpenCSVFile(wx.Dialog):
    def __init__(self, parent, ID, additionalFile, dirfrom,
                 size=wx.DefaultSize,
                 # size=wx.Size(1800,1200),
                 pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self)
        self.parent = parent
        self.additionalFile = additionalFile

        if self.additionalFile is True:
            title = "Add CSV file"
        else:
            title = "Open CSV file"

        self.Create(parent, ID, title, pos, size, style)

        vSizer = wx.BoxSizer(wx.VERTICAL)

        self.fileName = None
        self.dirName = None
        fileExtensions = "CSV files (*.csv)|*.csv;*.CSV|All files (*.*)|*.*"
        self.previewNRows = 4
        self.previewNCols = 6
        self.colLabelsDefault = ['A', 'B', 'C', 'D', 'E', 'F']

        fbb = filebrowse.FileBrowseButton(self, -1, labelText='File: ', fileMask=fileExtensions,
                                          startDirectory=dirfrom, size=(600, -1),
                                          changeCallback=self.fbbCallback)

        vSizer.Add(fbb, flag=wx.EXPAND | wx.ALL, border=10)

        # ---------------------------------------

        # CSV Separator

        lblList = ['Comma', 'Semicolon', 'Tab']

        self.CSVSepRBBox = wx.RadioBox(self, label='CSV character separator', pos=(80, 10), choices=lblList,
                                       majorDimension=1,
                                       style=wx.RA_SPECIFY_ROWS)
        vSizer.Add(self.CSVSepRBBox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.Bind(wx.EVT_RADIOBOX, self.optionsChanged, self.CSVSepRBBox)

        self.CSVSepRBBox.SetSelection(0)

        # ---------------------------------------

        # Options

        optionsSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Options"), wx.VERTICAL)

        self.discardFirstCol = wx.CheckBox(self, wx.ID_ANY, "Discard first column", wx.DefaultPosition, wx.DefaultSize,
                                           0)
        optionsSizer.Add(self.discardFirstCol, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        self.Bind(wx.EVT_CHECKBOX, self.optionsChanged, self.discardFirstCol)

        vSizer.Add(optionsSizer, flag=wx.EXPAND | wx.ALL, border=10)

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
        self.cleanPreview()
        self.provDataTable.Enable(False)
        self.provDataTable.Show(True)
        self.provDataTable.AutoSize()

        vSizer.Add(dataSizer, flag=wx.ALL | wx.EXPAND, border=10)

        # ---------------------------------------

        vSizer.AddStretchSpacer(1)

        # Ok and Cancel buttons

        okay = wx.Button(self, wx.ID_OK)
        cancel = wx.Button(self, wx.ID_CANCEL)
        buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsSizer.Add(cancel, flag=wx.RIGHT, border=10)
        buttonsSizer.Add(okay)
        self.Bind(wx.EVT_BUTTON, self.OkSelected, okay)

        vSizer.Add(buttonsSizer, flag=wx.TOP | wx.BOTTOM | wx.RIGHT | wx.ALIGN_RIGHT, border=10)

        self.SetSizer(vSizer)
        vSizer.Fit(self)

        self.Layout()
        self.Fit()
        self.Centre(wx.BOTH)
        self.Show(True)

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

            self.data = read_csv(os.path.join(self.dirName, self.fileName), sep=sepchar, header=0, engine='python',
                                 encoding='utf-8')

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
                    elif type(self.data.iloc[row, col]) in (int, float, complex, numpy.float64, numpy.int64):
                        self.provDataTable.SetCellValue(row, col, '{:5g}'.format(self.data.iloc[row, col]))
                    else:
                        self.provDataTable.SetCellValue(row, col, self.data.iloc[row, col])
            self.provDataTable.Enable(True)
            self.provDataTable.AutoSize()
        except:
            # print("Error: ", sys.exc_info())
            self.cleanPreview()

    def cleanPreview(self):
        for col in range(self.previewNCols):
            self.provDataTable.SetColLabelValue(col, self.colLabelsDefault[col])
        for row in range(self.previewNRows):
            for col in range(self.previewNCols):
                self.provDataTable.SetCellValue(row, col, "- - -")
        self.provDataTable.AutoSize()
        self.provDataTable.Enable(False)

    def OkSelected(self, event):
        if self.CSVSepRBBox.GetSelection() == 0:
            sepchar = 'Comma'
        elif self.CSVSepRBBox.GetSelection() == 1:
            sepchar = 'Semicolon'
        else:
            sepchar = 'Tab'

        openFileOptions = dict(
            additionalFile=self.additionalFile,
            fileName=self.fileName,
            dirName=self.dirName,
            sepchar=sepchar,
            discardFirstCol=self.discardFirstCol.IsChecked()
        )
        self.parent.OpenAddCSV(openFileOptions)
        self.Close()


class OpenXLSFile(wx.Dialog):
    def __init__(self, parent, ID, additionalFile, dirfrom, size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self)
        self.parent = parent
        self.additionalFile = additionalFile

        if self.additionalFile == True:
            title = "Add XLS/XLSX file"
        else:
            title = "Open XLS/XLSX file"

        self.Create(parent, ID, title, pos, size, style)

        vSizer = wx.BoxSizer(wx.VERTICAL)

        self.fileName = None
        self.dirName = None
        fileExtensions = "Excel files (*.xls;*.xlsx)|*.xls;*.xlsx;*.XLS;*.XLSX|All files (*.*)|*.*"
        self.previewNRows = 4
        self.previewNCols = 6
        self.colLabelsDefault = ['A', 'B', 'C', 'D', 'E', 'F']

        fbb = filebrowse.FileBrowseButton(self, -1, labelText='File: ', fileMask=fileExtensions,
                                          startDirectory=dirfrom, size=(600, -1),
                                          changeCallback=self.fbbCallback)

        vSizer.Add(fbb, flag=wx.EXPAND | wx.ALL, border=10)

        # ---------------------------------------

        # Options

        optionsBoxSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Options"), wx.VERTICAL)

        optionsGridSizer = wx.FlexGridSizer(rows=3, cols=2, vgap=4, hgap=4)

        self.RowWithColNames = wx.SpinCtrl(self, value='0', size=(160, -1))
        self.RowWithColNames.SetRange(0, 100)
        optionsGridSizer.Add(wx.StaticText(self, label='Row containing col. names:'), 0,
                             wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        optionsGridSizer.Add(self.RowWithColNames, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        self.Bind(wx.EVT_SPINCTRL, self.optionsChanged, self.RowWithColNames)

        self.NoColsDiscard = wx.SpinCtrl(self, value='0', size=(160, -1))
        self.NoColsDiscard.SetRange(0, 100)
        optionsGridSizer.Add(wx.StaticText(self, label='No. of columns to discard:'), 0,
                             wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        optionsGridSizer.Add(self.NoColsDiscard, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        self.Bind(wx.EVT_SPINCTRL, self.optionsChanged, self.NoColsDiscard)

        self.sheetNumber = wx.SpinCtrl(self, value='0', size=(160, -1))
        self.sheetNumber.SetRange(0, 10)
        optionsGridSizer.Add(wx.StaticText(self, label='Sheet number:'), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        optionsGridSizer.Add(self.sheetNumber, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        self.Bind(wx.EVT_SPINCTRL, self.optionsChanged, self.sheetNumber)

        optionsBoxSizer.Add(optionsGridSizer, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)

        vSizer.Add(optionsBoxSizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

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

        vSizer.Add(dataSizer, flag=wx.ALL | wx.EXPAND, border=10)

        # ---------------------------------------

        vSizer.AddStretchSpacer(1)

        # ---------------------------------------

        # Ok and Cancel buttons

        okay = wx.Button(self, wx.ID_OK)
        cancel = wx.Button(self, wx.ID_CANCEL)
        buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsSizer.Add(cancel, flag=wx.RIGHT, border=10)
        buttonsSizer.Add(okay)
        self.Bind(wx.EVT_BUTTON, self.OkSelected, okay)

        vSizer.Add(buttonsSizer, flag=wx.TOP | wx.BOTTOM | wx.RIGHT | wx.ALIGN_RIGHT, border=10)

        self.SetSizer(vSizer)
        vSizer.Fit(self)
        self.Layout()
        self.Fit()
        self.Centre(wx.BOTH)
        self.Show(True)

    def fbbCallback(self, evt):
        # print ('FileBrowseButton: %s\n' % evt.GetString())
        self.fileName = os.path.basename(evt.GetString())
        self.dirName = os.path.dirname(evt.GetString())

        self.updatePreview()

    def optionsChanged(self, evt):
        self.updatePreview()

    def updatePreview(self):

        from pandas.io.excel import read_excel
        import sys, numpy

        try:

            rowColLabels = self.RowWithColNames.GetValue()
            numColsDiscard = self.NoColsDiscard.GetValue()
            sheetNumber = self.sheetNumber.GetValue()

            self.data = read_excel(os.path.join(self.dirName, self.fileName), sheet_name=sheetNumber,
                                   header=rowColLabels, index_col=None)

            if numColsDiscard != 0:
                self.data.drop(self.data.columns[range(numColsDiscard)], axis=1, inplace=True)

            nRows = len(self.data.index)
            nCols = len(self.data.columns)

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
                    elif type(self.data.iloc[row, col]) in (int, float, complex, numpy.float64, numpy.int64):
                        self.provDataTable.SetCellValue(row, col, '{:5g}'.format(self.data.iloc[row, col]))
                    else:
                        self.provDataTable.SetCellValue(row, col, self.data.iloc[row, col])
            self.provDataTable.Enable(True)
            self.provDataTable.AutoSize()
        except:
            print("Error: ", sys.exc_info())
            self.cleanPreview()

    def cleanPreview(self):
        for col in range(self.previewNCols):
            self.provDataTable.SetColLabelValue(col, self.colLabelsDefault[col])
        for row in range(self.previewNRows):
            for col in range(self.previewNCols):
                self.provDataTable.SetCellValue(row, col, "- - -")
        self.provDataTable.AutoSize()
        self.provDataTable.Enable(False)

    def OkSelected(self, event):
        openFileOptions = dict(
            fileName=self.fileName,
            dirName=self.dirName,
            additionalFile=self.additionalFile,
            rowColNames=self.RowWithColNames.GetValue(),
            noColsDiscard=self.NoColsDiscard.GetValue(),
            sheetNumber=self.sheetNumber.GetValue()
        )
        self.parent.OpenAddXLS(openFileOptions)
        self.Close()
