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
import sys
from sys import platform

import numpy
import wx
import wx.adv
import wx.grid
from pandas import to_numeric
from pandas.io.excel import read_excel
from pandas.io.parsers import read_csv

from AddColumnInterface import AddColumnInterface
from AskFileType import AskFileType
from BasicStatisticsInterface import BasicStatisticsInterface
from Controller import Controller
from GraphsInterface import HistogramInterface, ScatterPlotInterface, \
    PieChartInterface, BoxPlotInterface, BarChartInterface
from Model import OptionsInExportInterface
from OpenFileInterface import OpenCSVFile, OpenXLSFile
from SignificanceTestInterface import SignificanceTestInterface


###########################################################################
## Class MainFrame
###########################################################################

class MainFrame(wx.Frame):
    tagsAndValues = {}
    histogramOptions = {}
    scatterPlotOptions = {}
    boxPlotOptions = {}
    pieChartOptions = {}
    barChartOptions = {}

    def __init__(self, parent):

        bmp = wx.Image(str(os.path.dirname(__file__)) + "/icons/SplashScreen2.0.png").ConvertToBitmap()
        splash = wx.adv.SplashScreen(bmp, wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT, 3000, None,
                                     style=wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)  # msec. of splash

        wx.Yield()

        self.configInit()

        # print "Invoked from directory:",self.params['options']['dirfrom']

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="GASATaD")

        if platform != "darwin":
            # image = wx.Image('GasatadLogo.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
            # icon = wx.EmptyIcon()
            # icon.CopyFromBitmap(image)
            # self.SetIcon(icon)

            # ib = wx.IconBundle()
            # ib.AddIconFromFile("GasatadLogo.ico", wx.BITMAP_TYPE_ANY)
            # self.SetIcons(ib)

            icon = wx.Icon("GasatadLogo.ico", wx.BITMAP_TYPE_ICO)
            self.SetIcon(icon)

        self.CheckUpdates()

        # self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        # MENU BAR
        self.m_menubar1 = wx.MenuBar(0)

        # ------------ File menu

        self.m_fileMenu = wx.Menu()
        if sys.platform == "linux":
            self.m_menuNewFile = wx.MenuItem(self.m_fileMenu, wx.ID_NEW, u"Open new file...", wx.EmptyString,
                                             wx.ITEM_NORMAL)
            self.m_menuAddFile = wx.MenuItem(self.m_fileMenu, wx.ID_OPEN, u"Add file...", wx.EmptyString,
                                             wx.ITEM_NORMAL)
        else:
            self.m_menuNewFile = wx.MenuItem(self.m_fileMenu, wx.ID_NEW, u"Open new file...\tCtrl+N", wx.EmptyString,
                                             wx.ITEM_NORMAL)
            self.m_menuAddFile = wx.MenuItem(self.m_fileMenu, wx.ID_OPEN, u"Add file...\tCtrl+O", wx.EmptyString,
                                             wx.ITEM_NORMAL)
        self.m_fileMenu.Append(self.m_menuNewFile)
        self.m_fileMenu.Append(self.m_menuAddFile)

        self.m_menuAddFile.Enable(False)

        self.m_fileMenu.AppendSeparator()
        if sys.platform == "linux":
            self.m_menuExportData = wx.MenuItem(self.m_fileMenu, wx.ID_SAVE, u"Save data...", wx.EmptyString,
                                                wx.ITEM_NORMAL)
        else:
            self.m_menuExportData = wx.MenuItem(self.m_fileMenu, wx.ID_SAVE, u"Save data...\tCtrl+S", wx.EmptyString,
                                                wx.ITEM_NORMAL)
        self.m_fileMenu.Append(self.m_menuExportData)

        self.m_menuExportData.Enable(False)

        self.m_fileMenu.AppendSeparator()

        if sys.platform == "linux":
            self.m_menuResetData = wx.MenuItem(self.m_fileMenu, wx.ID_CLOSE, u"Close data", wx.EmptyString,
                                               wx.ITEM_NORMAL)
            self.m_menuQuit = wx.MenuItem(self.m_fileMenu, wx.ID_EXIT, u"Quit", wx.EmptyString, wx.ITEM_NORMAL)
        else:
            self.m_menuResetData = wx.MenuItem(self.m_fileMenu, wx.ID_CLOSE, u"Close data\tCtrl+W", wx.EmptyString,
                                               wx.ITEM_NORMAL)
            self.m_menuQuit = wx.MenuItem(self.m_fileMenu, wx.ID_EXIT, u"Quit\tCtrl+Q", wx.EmptyString, wx.ITEM_NORMAL)

        self.m_fileMenu.Append(self.m_menuResetData)
        self.m_menuResetData.Enable(False)
        self.m_fileMenu.Append(self.m_menuQuit)

        self.accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('N'), self.m_menuNewFile.GetId()),
            (wx.ACCEL_CTRL, ord('O'), self.m_menuAddFile.GetId()),
            (wx.ACCEL_CTRL, ord('S'), self.m_menuExportData.GetId()),
            (wx.ACCEL_CTRL, ord('W'), self.m_menuResetData.GetId()),
            (wx.ACCEL_CTRL, ord('Q'), self.m_menuQuit.GetId())
        ])

        # ------------ Edit menu

        self.m_editMenu = wx.Menu()

        self.m_undo = wx.MenuItem(self.m_fileMenu, wx.ID_UNDO, u"Undo", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_editMenu.Append(self.m_undo)
        self.m_undo.Enable(False)

        self.m_editMenu.AppendSeparator()

        self.m_deletedSelectedCR = wx.MenuItem(self.m_fileMenu, wx.ID_ANY, u"Delete selected columns/rows",
                                               wx.EmptyString, wx.ITEM_NORMAL)
        self.m_editMenu.Append(self.m_deletedSelectedCR)
        self.m_deletedSelectedCR.Enable(False)

        self.m_editMenu.AppendSeparator()

        self.m_renameSelectedCol = wx.MenuItem(self.m_fileMenu, wx.ID_ANY, u"Rename selected column", wx.EmptyString,
                                               wx.ITEM_NORMAL)
        self.m_editMenu.Append(self.m_renameSelectedCol)
        self.m_renameSelectedCol.Enable(False)

        self.m_moveSelectedCol = wx.MenuItem(self.m_fileMenu, wx.ID_ANY, u"Move selected column", wx.EmptyString,
                                             wx.ITEM_NORMAL)
        self.m_editMenu.Append(self.m_moveSelectedCol)
        self.m_moveSelectedCol.Enable(False)

        self.m_replaceInCol = wx.MenuItem(self.m_fileMenu, wx.ID_ANY, u"Replace in selected column...", wx.EmptyString,
                                          wx.ITEM_NORMAL)
        self.m_editMenu.Append(self.m_replaceInCol)
        self.m_replaceInCol.Enable(False)

        self.m_sortSubMenu = wx.Menu()
        self.m_sortAscending = self.m_sortSubMenu.Append(wx.ID_ANY, "ascending")
        self.m_sortDescending = self.m_sortSubMenu.Append(wx.ID_ANY, "descending")
        self.sortMenuID = wx.NewId()
        self.m_editMenu.Append(self.sortMenuID, "Sort using selected column", self.m_sortSubMenu)
        self.m_editMenu.Enable(self.sortMenuID, False)

        self.m_discretizeSelectedCol = wx.MenuItem(self.m_fileMenu, wx.ID_ANY, u"Convert selected column to text",
                                                   wx.EmptyString, wx.ITEM_NORMAL)
        self.m_editMenu.Append(self.m_discretizeSelectedCol)
        self.m_discretizeSelectedCol.Enable(False)

        self.m_numerizeSelectedCol = wx.MenuItem(self.m_fileMenu, wx.ID_ANY, u"Convert selected column to numbers",
                                                 wx.EmptyString, wx.ITEM_NORMAL)
        self.m_editMenu.Append(self.m_numerizeSelectedCol)
        self.m_numerizeSelectedCol.Enable(False)

        self.m_editMenu.AppendSeparator()

        self.m_addNewColumn = wx.MenuItem(self.m_fileMenu, wx.ID_ANY, u"Add text column...", wx.EmptyString,
                                          wx.ITEM_NORMAL)
        self.m_editMenu.Append(self.m_addNewColumn)
        self.m_addNewColumn.Enable(False)

        self.m_deleteColumns = wx.MenuItem(self.m_fileMenu, wx.ID_ANY, u"Delete columns...", wx.EmptyString,
                                           wx.ITEM_NORMAL)
        self.m_editMenu.Append(self.m_deleteColumns)
        self.m_deleteColumns.Enable(False)

        # ------------ About menu

        self.m_aboutMenu = wx.Menu()

        if platform != "darwin":
            self.m_menuAbout = wx.MenuItem(self.m_aboutMenu, wx.ID_ABOUT, u"About GASATaD", wx.EmptyString,
                                           wx.ITEM_NORMAL)
        else:
            self.m_menuAbout = wx.MenuItem(self.m_aboutMenu, wx.ID_ANY, u"About GASATaD", wx.EmptyString,
                                           wx.ITEM_NORMAL)

        self.m_aboutMenu.Append(self.m_menuAbout)

        self.m_menubar1.Append(self.m_fileMenu, u"File")
        self.m_menubar1.Append(self.m_editMenu, u"Edit")
        # self.m_menubar1.Append( self.m_optionsMenu, u"Options")
        self.m_menubar1.Append(self.m_aboutMenu, u"About")

        self.SetMenuBar(self.m_menubar1)

        # self.m_menubar1.SetFocus()

        globalSizer = wx.BoxSizer(wx.HORIZONTAL)

        leftSizer = wx.BoxSizer(wx.VERTICAL)

        #  -------------------- Information part of the interface

        informationSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.VERTICAL)

        self.m_staticText2 = wx.StaticText(informationSizer.GetStaticBox(), wx.ID_ANY, u"Data information",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        self.m_staticText2.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                    False, wx.EmptyString))

        informationSizer.Add(self.m_staticText2, 0, wx.ALL, 5)

        informationBoxSizer = wx.BoxSizer(wx.VERTICAL)
        textInfo = u"Rows: 0   Columns: 0   Nulls: 0"
        self.m_information = wx.StaticText(informationSizer.GetStaticBox(), wx.ID_ANY, textInfo, wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        informationBoxSizer.Add(self.m_information, 0, wx.LEFT, 0)

        informationSizer.Add(informationBoxSizer, 1, wx.RIGHT | wx.LEFT | wx.BOTTOM, 10)

        leftSizer.Add(informationSizer, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, border=10)

        #  -------------------- Buttons of the interface

        buttonsSizer = wx.BoxSizer(wx.VERTICAL)

        buttonsSubSizer1 = wx.GridSizer(rows=2, cols=2, vgap=0, hgap=0)

        self.openNewFileBtn = wx.Button(self, wx.ID_ANY, u"Open new file", wx.DefaultPosition, wx.DefaultSize, 0)
        buttonsSubSizer1.Add(self.openNewFileBtn, 0, wx.TOP | wx.BOTTOM | wx.LEFT | wx.EXPAND, 5)

        self.addFileBtn = wx.Button(self, wx.ID_ANY, u"Add file", wx.DefaultPosition, wx.DefaultSize, 0)
        buttonsSubSizer1.Add(self.addFileBtn, 0, wx.ALL | wx.EXPAND, 5)
        self.addFileBtn.Enable(False)

        self.exportDataBtn = wx.Button(self, wx.ID_ANY, u"Save data", wx.DefaultPosition, wx.DefaultSize, 0)
        buttonsSubSizer1.Add(self.exportDataBtn, 0, wx.TOP | wx.BOTTOM | wx.LEFT | wx.EXPAND, 5)
        self.exportDataBtn.Enable(False)

        self.resetDataBtn = wx.Button(self, wx.ID_ANY, u"Close data", wx.DefaultPosition, wx.DefaultSize, 0)
        buttonsSubSizer1.Add(self.resetDataBtn, 0, wx.ALL | wx.EXPAND, 5)
        self.resetDataBtn.Enable(False)

        buttonsSizer.Add(buttonsSubSizer1, 0, wx.EXPAND, 0)

        buttonsSizer.AddSpacer(10)

        self.descriptiveStatsBtn = wx.Button(self, wx.ID_ANY, u"Basic statistics", wx.DefaultPosition, wx.DefaultSize,
                                             0)
        self.descriptiveStatsBtn.Enable(False)
        # self.descriptiveStatsBtn.SetMinSize( wx.Size( -1,25 ) )

        buttonsSizer.Add(self.descriptiveStatsBtn, 0, wx.ALL | wx.EXPAND, 5)

        self.significanceTestBtn = wx.Button(self, wx.ID_ANY, u"Significance tests", wx.DefaultPosition, wx.DefaultSize,
                                             0)
        self.significanceTestBtn.Enable(False)
        # self.significanceTestBtn.SetMinSize( wx.Size( -1,25 ) )

        buttonsSizer.Add(self.significanceTestBtn, 0, wx.ALL | wx.EXPAND, 5)

        buttonsSizer.AddSpacer(10)

        leftSizer.Add(buttonsSizer, flag=wx.ALL | wx.EXPAND, border=5)

        #  -------------------- Buttons for plot

        gSizerChart = wx.GridSizer(0, 3, 0, 0)

        # Images needed for the buttons
        self.histogramBmp = wx.Image(str(os.path.dirname(__file__)) + "/icons/histogram1.png",
                                     wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.scatterPlotmBmp = wx.Image(str(os.path.dirname(__file__)) + "/icons/scatterPlot1.png",
                                        wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.pieChartmBmp = wx.Image(str(os.path.dirname(__file__)) + "/icons/pieChart1.png",
                                     wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.boxPlotBmp = wx.Image(str(os.path.dirname(__file__)) + "/icons/boxPlot1.png",
                                   wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.barChartBmp = wx.Image(str(os.path.dirname(__file__)) + "/icons/barChart1.png",
                                    wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        self.histogramBtn = wx.BitmapButton(self, wx.ID_ANY, self.histogramBmp, wx.DefaultPosition, wx.Size(80, 80),
                                            wx.BU_AUTODRAW)
        gSizerChart.Add(self.histogramBtn, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.histogramBtn.Enable(False)
        self.histogramBtn.SetToolTip(wx.ToolTip("Histogram"))

        self.scatterPlotBtn = wx.BitmapButton(self, wx.ID_ANY, self.scatterPlotmBmp, wx.DefaultPosition,
                                              wx.Size(80, 80), wx.BU_AUTODRAW)
        gSizerChart.Add(self.scatterPlotBtn, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.scatterPlotBtn.Enable(False)
        self.scatterPlotBtn.SetToolTip(wx.ToolTip("Scatter Plot"))

        self.pieChartBtn = wx.BitmapButton(self, wx.ID_ANY, self.pieChartmBmp, wx.DefaultPosition, wx.Size(80, 80),
                                           wx.BU_AUTODRAW)
        gSizerChart.Add(self.pieChartBtn, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.pieChartBtn.Enable(False)
        self.pieChartBtn.SetToolTip(wx.ToolTip("Pie Chart"))

        self.boxPlotBtn = wx.BitmapButton(self, wx.ID_ANY, self.boxPlotBmp, wx.DefaultPosition, wx.Size(80, 80),
                                          wx.BU_AUTODRAW)
        gSizerChart.Add(self.boxPlotBtn, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.boxPlotBtn.Enable(False)
        self.boxPlotBtn.SetToolTip(wx.ToolTip("Box Plot"))

        self.barChartBtn = wx.BitmapButton(self, wx.ID_ANY, self.barChartBmp, wx.DefaultPosition, wx.Size(80, 80),
                                           wx.BU_AUTODRAW)
        gSizerChart.Add(self.barChartBtn, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.barChartBtn.Enable(False)
        self.barChartBtn.SetToolTip(wx.ToolTip("Bar Chart"))

        leftSizer.Add(gSizerChart, flag=wx.ALL | wx.EXPAND, border=5)

        # ------------------- Info about upgrades

        if self.params['upgradable']:
            import wx.lib.agw.gradientbutton as GB

            leftSizer.AddStretchSpacer(1)
            # self.upgradeButton = wx.Button( self, wx.ID_ANY, u"* New version: "+self.params['availableVersionToUpgrade']+" *", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.upgradeButton = GB.GradientButton(self, label="New version available: " + (
                self.params['availableVersionToUpgrade'].decode('utf-8')))
            self.upgradeButton.SetBaseColours(startcolour=wx.TheColourDatabase.Find('PALE GREEN'),
                                              foregroundcolour=wx.BLACK)
            self.upgradeButton.SetPressedBottomColour(wx.TheColourDatabase.Find('LIGHT GREY'))
            self.upgradeButton.SetPressedTopColour(wx.TheColourDatabase.Find('LIGHT GREY'))
            boldFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            boldFont.SetWeight(wx.BOLD)
            self.upgradeButton.SetFont(boldFont)
            self.Bind(wx.EVT_BUTTON, self.openBrowserDownload, id=self.upgradeButton.GetId())

            leftSizer.Add(self.upgradeButton, flag=wx.ALL | wx.EXPAND, border=5)

        globalSizer.Add(leftSizer, flag=wx.EXPAND | wx.ALL, border=10)

        # ------------------- Data table

        self.m_dataTable = wx.grid.Grid(self)

        # Grid
        self.m_dataTable.CreateGrid(45, 45)
        self.m_dataTable.EnableEditing(False)
        self.m_dataTable.EnableGridLines(True)
        self.m_dataTable.EnableDragGridSize(False)
        self.m_dataTable.SetMargins(0, 0)

        # Columns
        self.m_dataTable.EnableDragColMove(False)
        self.m_dataTable.EnableDragColSize(False)
        self.m_dataTable.SetColLabelSize(30)
        self.m_dataTable.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.m_dataTable.EnableDragRowSize(False)
        self.m_dataTable.SetRowLabelSize(80)
        self.m_dataTable.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Cell Defaults
        self.m_dataTable.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTER)

        # Selection mode
        self.m_dataTable.SetSelectionMode(wx.grid.Grid.wxGridSelectRows | wx.grid.Grid.wxGridSelectColumns)
        # self.m_dataTable.EnableEditing(True)

        fgSizer8 = wx.BoxSizer(wx.VERTICAL)
        fgSizer8.Add(self.m_dataTable)
        self.m_dataTable.Enable(False)
        self.m_dataTable.Show(True)

        globalSizer.Add(fgSizer8, flag=wx.ALL | wx.EXPAND, border=10)

        # Options to show the GUI
        self.SetSizer(globalSizer)
        self.Layout()
        self.Centre(wx.BOTH)

        self.Show(True)
        # self.Move((0,0))
        widthScreen, heightScreen = wx.GetDisplaySize()
        widthWindow = 1440
        heightWindow = 900
        if ((widthScreen >= widthWindow) and (heightScreen > heightWindow)):
            self.SetSize((widthWindow, heightWindow))
        else:
            self.Maximize()
        self.SetMinSize((1024, 768))

        # Binding between buttons and functions which will control the events

        self.Bind(wx.EVT_CLOSE, self.closeApp)  # Close window

        self.Bind(wx.EVT_MENU, self.openFile, self.m_menuNewFile)
        self.Bind(wx.EVT_BUTTON, self.openFile, self.openNewFileBtn)
        self.Bind(wx.EVT_MENU, self.addFile, self.m_menuAddFile)
        self.Bind(wx.EVT_BUTTON, self.addFile, self.addFileBtn)
        self.Bind(wx.EVT_MENU, self.saveFile, self.m_menuExportData)
        self.Bind(wx.EVT_MENU, self.resetData, self.m_menuResetData)
        self.Bind(wx.EVT_MENU, self.undo, self.m_undo)
        self.Bind(wx.EVT_MENU, self.createNewColumn, self.m_addNewColumn)
        self.Bind(wx.EVT_MENU, self.deleteColumnsByLabels, self.m_deleteColumns)
        self.Bind(wx.EVT_MENU, self.deleteColumnsRows, self.m_deletedSelectedCR)
        self.Bind(wx.EVT_MENU, self.renameCol, self.m_renameSelectedCol)
        self.Bind(wx.EVT_MENU, self.moveCol, self.m_moveSelectedCol)
        self.Bind(wx.EVT_MENU, self.replaceInCol, self.m_replaceInCol)
        self.Bind(wx.EVT_MENU, self.discretizeCol, self.m_discretizeSelectedCol)
        self.Bind(wx.EVT_MENU, self.numerizeCol, self.m_numerizeSelectedCol)
        self.Bind(wx.EVT_MENU, self.sortAscendingCol, self.m_sortAscending)
        self.Bind(wx.EVT_MENU, self.sortDescendingCol, self.m_sortDescending)
        self.Bind(wx.EVT_MENU, self.appInformation, self.m_menuAbout)
        self.Bind(wx.EVT_MENU, self.closeApp, self.m_menuQuit)
        self.Bind(wx.EVT_BUTTON, self.createBasicStatisticsInterface, self.descriptiveStatsBtn)
        self.Bind(wx.EVT_BUTTON, self.resetData, self.resetDataBtn)
        self.Bind(wx.EVT_BUTTON, self.saveFile, self.exportDataBtn)
        self.Bind(wx.EVT_BUTTON, self.createHistogram, self.histogramBtn)
        self.Bind(wx.EVT_BUTTON, self.createScatterPlot, self.scatterPlotBtn)
        self.Bind(wx.EVT_BUTTON, self.createPieChart, self.pieChartBtn)
        self.Bind(wx.EVT_BUTTON, self.createBoxPlot, self.boxPlotBtn)
        self.Bind(wx.EVT_BUTTON, self.createBarChart, self.barChartBtn)
        self.Bind(wx.EVT_BUTTON, self.doSignificanceTest, self.significanceTestBtn)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.rightClickOnTable, self.m_dataTable)
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.rightClickOnTable, self.m_dataTable)
        self.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self.contentSelected, self.m_dataTable)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.cellModification, self.m_dataTable)

        # A controller object is created
        self.controller = Controller()

        HelpString = (
            "      -help: shows this information\n"
            "      -loadCSV fileName: loads CSV file (full path is required)\n"
        )

        if (len(sys.argv) != 1 and (sys.platform == 'linux' or sys.platform == 'darwin')):
            arguments = sys.argv[1:]
            possibleArguments = ['-help', '-loadCSV']

            for argument in arguments:
                if argument[0] == '-':
                    if argument not in possibleArguments:
                        print("\n** ERROR: command '" + argument + "' not recognized **\n")
                        print("** GASATaD terminal mode commands:")
                        print(HelpString)
                        sys.exit(0)

            if "-help" in arguments:
                print("\n** GASATaD: terminal mode **\n")
                print(HelpString)
                sys.exit(0)

            else:
                if "-loadCSV" in arguments:
                    CSVFileName = arguments[arguments.index("-loadCSV") + 1]
                    print("Loading CSV file: " + CSVFileName)
                    self.OpenCSVFileNoGUI(CSVFileName)

    def undo(self, event):
        self.controller.recoverData()
        if not self.m_dataTable.IsEnabled():
            self.m_dataTable.Enable()

        self.refreshGUI()

        self.m_undo.SetText("Undo")
        self.m_undo.Enable(False)

    def cellModification(self, event):
        dlg = wx.TextEntryDialog(self, "Type new value for cell (empty for 'null'):", 'Change cell', '')
        if dlg.ShowModal() == wx.ID_OK:
            newValue = dlg.GetValue()
            dlg.Destroy()
            if newValue == "":
                newValue2 = numpy.NaN
            else:
                try:
                    newValue2 = numpy.float64(newValue)
                except:
                    newValue2 = newValue

            self.controller.storeData()
            self.m_undo.SetText("Undo change cell")
            self.m_undo.Enable()

            self.controller.changeCellValue(event.GetRow(), event.GetCol(), newValue2)
            self.controller.detectColumnTypes()
            self.refreshGUI()
            event.Skip()
        else:
            dlg.Destroy()

    def contentSelected(self, event):

        columnsSelected = self.m_dataTable.GetSelectedCols()
        rowsSelected = self.m_dataTable.GetSelectedRows()

        if len(rowsSelected) == 0 and len(columnsSelected) == 0:
            self.m_deletedSelectedCR.Enable(False)
        else:
            self.m_deletedSelectedCR.Enable()

        if len(rowsSelected) == 0 and len(columnsSelected) == 1:
            self.m_renameSelectedCol.Enable()
            self.m_moveSelectedCol.Enable()
            self.m_editMenu.Enable(self.sortMenuID, True)
            columnSelectedLabel = self.m_dataTable.GetColLabelValue(self.m_dataTable.GetSelectedCols()[0])
            if columnSelectedLabel not in self.controller.characterValues:
                self.m_discretizeSelectedCol.Enable()
            if columnSelectedLabel in self.controller.characterValues:
                self.m_numerizeSelectedCol.Enable()
                self.m_replaceInCol.Enable()

        else:
            self.m_renameSelectedCol.Enable(False)
            self.m_moveSelectedCol.Enable(False)
            self.m_discretizeSelectedCol.Enable(False)
            self.m_numerizeSelectedCol.Enable(False)
            self.m_replaceInCol.Enable(False)
            self.m_editMenu.Enable(self.sortMenuID, False)

        event.Skip()

    def deleteColumnsRows(self, event):

        rowsSelected = self.m_dataTable.GetSelectedRows()
        columnsSelected = self.m_dataTable.GetSelectedCols()

        self.controller.storeData()
        self.m_undo.SetText("Undo delete columns/rows")
        self.m_undo.Enable()

        columnsSelectedLabels = []
        for columnIndex in columnsSelected:
            columnsSelectedLabels.append(self.m_dataTable.GetColLabelValue(columnIndex))
        self.controller.deleteColumns(columnsSelectedLabels)
        if len(rowsSelected) > 0:
            self.controller.deleteRows(rowsSelected)

        if self.controller.programState.dataToAnalyse.empty:
            self.controller.resetDataToAnalyse()
        self.refreshGUI()

    def rightClickOnTable(self, event):
        columnClicked = event.GetCol()
        columnsSelected = self.m_dataTable.GetSelectedCols()

        if columnClicked in columnsSelected:

            popupMenu = wx.Menu()

            textPopupDelete = "Delete column"
            if len(columnsSelected) > 1:
                textPopupDelete += "s"
            self.popupDeleteID = wx.NewId()
            popupMenu.Append(self.popupDeleteID, textPopupDelete)
            self.Bind(wx.EVT_MENU, self.deleteColumns, id=self.popupDeleteID)

            if len(columnsSelected) == 1:

                # Renaming menu entry
                popupRenameID = wx.NewId()
                popupMenu.Append(popupRenameID, "Rename column")
                self.Bind(wx.EVT_MENU, self.renameCol, id=popupRenameID)

                # Moving menu entry
                popupMoveID = wx.NewId()
                popupMenu.Append(popupMoveID, "Move column")
                self.Bind(wx.EVT_MENU, self.moveCol, id=popupMoveID)

                columnSelectedLabel = self.m_dataTable.GetColLabelValue(self.m_dataTable.GetSelectedCols()[0])

                if columnSelectedLabel in self.controller.characterValues:
                    self.popupReplaceInColID = wx.NewId()
                    popupMenu.Append(self.popupReplaceInColID, "Replace in column")
                    self.Bind(wx.EVT_MENU, self.replaceInCol, id=self.popupReplaceInColID)

                # Sort menu entry
                popupSortSubMenuID = wx.NewId()
                popupSortAscendingID = wx.NewId()
                popupSortDescendingID = wx.NewId()
                popupSubMenuSort = wx.Menu()
                popupSubMenuSort.Append(popupSortAscendingID, "ascending")
                popupSubMenuSort.Append(popupSortDescendingID, "descending")
                popupMenu.Append(popupSortSubMenuID, "Sort using column", popupSubMenuSort)
                self.Bind(wx.EVT_MENU, self.sortAscendingCol, id=popupSortAscendingID)
                self.Bind(wx.EVT_MENU, self.sortDescendingCol, id=popupSortDescendingID)

                # self.m_sortDescending = self.m_sortSubMenu.Append(wx.ID_ANY, "Descending")
                # self.sortMenuID = wx.NewId()
                # self.m_editMenu.AppendMenu(self.sortMenuID, "Sort using selected column",self.m_sortSubMenu )
                # self.m_editMenu.Enable(self.sortMenuID,False)

                # Discretizing menu entry

                if columnSelectedLabel not in self.controller.characterValues:
                    self.popupDiscretizeID = wx.NewId()
                    popupMenu.Append(self.popupDiscretizeID, "Convert column to text")
                    self.Bind(wx.EVT_MENU, self.discretizeCol, id=self.popupDiscretizeID)
                if columnSelectedLabel in self.controller.characterValues:
                    self.popupNumerizeID = wx.NewId()
                    popupMenu.Append(self.popupNumerizeID, "Convert column to numbers")
                    self.Bind(wx.EVT_MENU, self.numerizeCol, id=self.popupNumerizeID)

            self.PopupMenu(popupMenu)
            popupMenu.Destroy()

        rowClicked = event.GetRow()
        rowsSelected = self.m_dataTable.GetSelectedRows()
        if rowClicked in rowsSelected:
            textPopupDelete = "Delete row"
            if len(rowsSelected) > 1:
                textPopupDelete += "s"
            popupMenu = wx.Menu()
            self.popupDeleteID = wx.NewId()
            popupMenu.Append(self.popupDeleteID, textPopupDelete)
            self.Bind(wx.EVT_MENU, self.deleteRows, id=self.popupDeleteID)
            self.PopupMenu(popupMenu)
            popupMenu.Destroy()

        event.Skip()

    def deleteColumns(self, event):  # Used after right-click on selected columns

        columnsSelectedIndex = self.m_dataTable.GetSelectedCols()

        columnsSelectedLabels = []
        for columnIndex in columnsSelectedIndex:
            columnsSelectedLabels.append(self.m_dataTable.GetColLabelValue(columnIndex))

        self.controller.storeData()
        self.m_undo.SetText("Undo delete columns")
        self.m_undo.Enable()

        self.controller.deleteColumns(columnsSelectedLabels)

        if self.controller.programState.dataToAnalyse.empty:
            self.controller.resetDataToAnalyse()
        self.refreshGUI()

    def moveCol(self, event):
        columnsSelectedIndex = self.m_dataTable.GetSelectedCols()
        oldPos = columnsSelectedIndex[0]
        maxPos = self.controller.getNumberOfColumns() - 1
        newPosOk = False
        while not newPosOk:
            dlg = wx.TextEntryDialog(self, "New position for column (between 0 and " + str(maxPos) + "):",
                                     "Move column", "")
            if dlg.ShowModal() == wx.ID_OK:
                newPos = dlg.GetValue()
                dlg.Destroy()
                try:
                    newPos = int(newPos)
                    newPosOk = True
                except:
                    None
                if newPosOk and (newPos < 0 or newPos > maxPos):
                    newPosOk = False
            else:
                dlg.Destroy()
                break
        if newPosOk:
            self.controller.storeData()
            self.m_undo.SetText("Undo move column")
            self.m_undo.Enable()

            colIndex = list(self.controller.getDataToAnalyse().columns)
            label = colIndex[columnsSelectedIndex[0]]
            colIndex.pop(columnsSelectedIndex[0])
            colIndex.insert(newPos, label)
            self.controller.reorderColumns(colIndex)

            self.refreshGUI(updateDataInfo=False)

            self.m_dataTable.SetGridCursor(0, newPos)
            self.m_dataTable.MakeCellVisible(0, newPos)
            self.m_dataTable.SelectCol(newPos)

    def renameCol(self, event):
        columnsSelectedIndex = self.m_dataTable.GetSelectedCols()
        oldLabel = self.m_dataTable.GetColLabelValue(columnsSelectedIndex[0])
        dlg = wx.TextEntryDialog(self, "Type new label for column '" + oldLabel + "':", 'Rename column', '')
        if dlg.ShowModal() == wx.ID_OK:
            newLabel = dlg.GetValue()
            dlg.Destroy()

            self.controller.storeData()
            self.m_undo.SetText("Undo rename column")
            self.m_undo.Enable()

            self.controller.renameColumn(oldLabel, newLabel)

            self.refreshGUI(updateDataInfo=False, markNans=False)

            self.m_dataTable.SetGridCursor(0, columnsSelectedIndex[0])
            self.m_dataTable.MakeCellVisible(0, columnsSelectedIndex[0])
            self.m_dataTable.SelectCol(columnsSelectedIndex[0])
        else:
            dlg.Destroy()

    def replaceInCol(self, event):
        columnsSelectedIndex = self.m_dataTable.GetSelectedCols()
        colLabel = self.m_dataTable.GetColLabelValue(columnsSelectedIndex[0])
        listTags = list(self.controller.programState.dataToAnalyse[str(colLabel)].unique())

        if numpy.NaN in listTags:
            listTags.remove(numpy.NaN)
            listTags.insert(0, 'null')

        selectValuesInterface = ReplaceInColInterface(self, listTags)

        if selectValuesInterface.ShowModal() == wx.ID_OK:
            self.controller.storeData()
            self.m_undo.SetText("Undo replace")
            self.m_undo.Enable()

            oldTag, newTag = selectValuesInterface.getValues()
            if oldTag == 'null':
                oldTag = numpy.NaN
            if newTag == "":
                newTag = numpy.NaN

            self.controller.replaceInTextCol(colLabel, oldTag, newTag)

            self.refreshGUI()

            self.m_dataTable.SetGridCursor(0, columnsSelectedIndex[0])
            self.m_dataTable.MakeCellVisible(0, columnsSelectedIndex[0])
            self.m_dataTable.SelectCol(columnsSelectedIndex[0])

    def discretizeCol(self, event):
        columnsSelectedIndex = self.m_dataTable.GetSelectedCols()
        columnSelectedLabel = self.m_dataTable.GetColLabelValue(columnsSelectedIndex[0])

        self.controller.storeData()
        self.m_undo.SetText("Undo convert to text")
        self.m_undo.Enable()

        self.controller.programState.dataToAnalyse[columnSelectedLabel] = self.controller.programState.dataToAnalyse[
            columnSelectedLabel].astype(str)
        self.controller.characterValues.append(columnSelectedLabel)
        if columnSelectedLabel in self.controller.floatValues:
            self.controller.floatValues.remove(columnSelectedLabel)
        if columnSelectedLabel in self.controller.integerValues:
            self.controller.integerValues.remove(columnSelectedLabel)

        self.refreshGUI(updateDataInfo=False)

        self.m_dataTable.SetGridCursor(0, columnsSelectedIndex[0])
        self.m_dataTable.MakeCellVisible(0, columnsSelectedIndex[0])

    def numerizeCol(self, event):
        columnsSelectedIndex = self.m_dataTable.GetSelectedCols()
        columnSelectedLabel = self.m_dataTable.GetColLabelValue(columnsSelectedIndex[0])

        self.controller.storeData()
        self.m_undo.SetText("Undo convert to numbers")
        self.m_undo.Enable()

        oldType = self.controller.programState.dataToAnalyse[columnSelectedLabel].dtypes
        self.controller.programState.dataToAnalyse[columnSelectedLabel] = to_numeric(
            self.controller.programState.dataToAnalyse[columnSelectedLabel], errors='ignore')
        newType = self.controller.programState.dataToAnalyse[columnSelectedLabel].dtypes
        if oldType == newType:
            dlg = wx.MessageDialog(None,
                                   "The column '" + columnSelectedLabel + "' could not be converted to numerical values",
                                   "Invalid conversion", wx.OK | wx.ICON_INFORMATION)

            if dlg.ShowModal() == wx.ID_OK:
                dlg.Destroy()
        else:
            self.controller.characterValues.remove(columnSelectedLabel)
            if newType == 'float64':
                self.controller.floatValues.append(columnSelectedLabel)
            else:
                self.controller.integerValues.append(columnSelectedLabel)

            self.refreshGUI(updateDataInfo=False)

            self.m_dataTable.SetGridCursor(0, columnsSelectedIndex[0])
            self.m_dataTable.MakeCellVisible(0, columnsSelectedIndex[0])

    def sortAscendingCol(self, event):
        self.sortCol(True)

    def sortDescendingCol(self, event):
        self.sortCol(False)

    def sortCol(self, ascendingBool):
        self.controller.storeData()
        self.m_undo.SetText("Undo sort rows")
        self.m_undo.Enable()

        columnsSelectedIndex = self.m_dataTable.GetSelectedCols()
        columnSelectedLabel = self.m_dataTable.GetColLabelValue(columnsSelectedIndex[0])
        self.controller.programState.dataToAnalyse.sort_values(columnSelectedLabel, ascending=ascendingBool,
                                                               inplace=True)

        self.refreshGUI(updateDataInfo=False)

        self.m_dataTable.SetGridCursor(0, columnsSelectedIndex[0])
        self.m_dataTable.MakeCellVisible(0, columnsSelectedIndex[0])
        self.m_dataTable.SelectCol(columnsSelectedIndex[0])

    def deleteRows(self, event):  # Used after right-click on selected rows

        rowsSelectedIndex = self.m_dataTable.GetSelectedRows()

        rowsSelectedLabels = []
        for rowIndex in rowsSelectedIndex:
            rowsSelectedLabels.append(self.m_dataTable.GetRowLabelValue(rowIndex))

        self.controller.storeData()
        self.m_undo.SetText("Undo delete rows")
        self.m_undo.Enable()

        self.controller.deleteRows(rowsSelectedIndex)

        if self.controller.programState.dataToAnalyse.empty:
            self.controller.resetDataToAnalyse()
        self.refreshGUI()

    def CheckUpdates(self):
        from sys import argv
        import urllib.request, urllib.error
        import os

        remoteVersion = ""
        remoteVersionFile = ""

        if (platform == "linux" or platform == "linux2") and argv[0] == "/usr/share/gasatad/GASATaD_2_0.py":
            remoteVersionFile = "https://raw.githubusercontent.com/milegroup/gasatad/master/docs/programVersions/deb.txt"

        elif (platform == "darwin") and ("GASATaD.app" in os.path.realpath(__file__)):
            remoteVersionFile = "https://raw.githubusercontent.com/milegroup/gasatad/master/docs/programVersions/mac.txt"

        elif platform == "win32" and argv[0].endswith(".exe"):
            remoteVersionFile = "https://raw.githubusercontent.com/milegroup/gasatad/master/docs/programVersions/win.txt"

        elif argv[0].endswith("GASATaD_2_0.py"):
            # print "# Running GASATaD from source"
            remoteVersionFile = "https://raw.githubusercontent.com/milegroup/gasatad/master/docs/programVersions/src.txt"

        if remoteVersionFile:
            try:
                if platform != "darwin":
                    remoteFile = urllib.request.urlopen(remoteVersionFile)
                    remoteVersion = remoteFile.readline().strip()
                    remoteFile.close()
                else:
                    import ssl
                    context = ssl._create_unverified_context()
                    remoteFile = urllib.request.urlopen(remoteVersionFile, context=context)
                    remoteVersion = remoteFile.readline().strip()
                    remoteFile.close()
                # print "# Version available in GASATaD web page: ", remoteVersion
            except urllib.error.URLError:
                # print "# I couldn't check for updates"
                None

        if remoteVersion:
            # print "# Version file exists"
            if float(remoteVersion) > float(self.params['version']):
                self.params['upgradable'] = True
                self.params['availableVersionToUpgrade'] = remoteVersion

            # self.params['upgradable'] = True
            # self.params['availableVersionToUpgrade'] = remoteVersion

    def openBrowserDownload(self, event):
        import webbrowser
        webbrowser.open("https://milegroup.github.io/gasatad/#download")

    def updateDataInfo(self):
        if self.controller.programState.dataToAnalyse.empty:
            textInfo = u"Rows: 0   Columns: 0   Nulls: 0"
            self.m_information.SetLabel(textInfo)
        else:
            numRows = self.controller.getNumberOfRows()
            numCols = self.controller.getNumberOfColumns()
            textInfo = "Rows: {0:d}   Columns: {1:d}   Nulls: {2:d}".format(numRows, numCols, self.params['noOfNulls'])
            # textInfo += "\nText columns: {0:d}".format(len(self.controller.characterValues))
            # textInfo += "\nInteger columns: {0:d}".format(len(self.controller.integerValues))
            # textInfo += "\nFloat columns: {0:d}".format(len(self.controller.floatValues))
            self.m_information.SetLabel(textInfo)

    def OpenCSVFileNoGUI(self, fileName):

        self.data = None

        try:
            self.Datafile = open(fileName, 'rU')
            self.data = read_csv(self.Datafile, sep=None, engine='python', encoding='utf-8')

            self.data.drop(self.data.columns[[0]], axis=1, inplace=True)
            self.data.rename(columns={'Unnamed: 0': 'NoTag'}, inplace=True)

            self.controller.OpenFile(self.data)

        except UnicodeDecodeError:
            print("Error: non ascii files in file")
            return

        except:
            print("Error: ", sys.exc_info()[0])
            print("There was some problem with the file")
            return

        self.refreshGUI()

        print("File: " + fileName + " loaded")

    def openFile(self, event):
        askfile = AskFileType(self, -1, "open")
        askfile.CenterOnScreen()
        askfile.ShowModal()
        askfile.Destroy()

    def addFile(self, event):
        askfile = AskFileType(self, -1, "add")
        askfile.CenterOnScreen()
        askfile.ShowModal()
        askfile.Destroy()

    def selectCSV(self, additionalFile):
        openFileInterf = OpenCSVFile(self, -1, additionalFile=additionalFile, dirfrom=self.params['options']['dirfrom'])

    def selectXLS(self, additionalFile):
        openFileInterf = OpenXLSFile(self, -1, additionalFile=additionalFile, dirfrom=self.params['options']['dirfrom'])

    def OpenAddCSV(self, openFileOptions):
        # print "Gonna open CSV file"
        # print openFileOptions

        self.params['options']['dirfrom'] = openFileOptions['dirName']
        readCorrect = True
        self.data = None
        discardCol = openFileOptions['discardFirstCol']
        sepChar = ''
        if openFileOptions['sepchar'] == "Comma":
            sepChar = ','
        elif openFileOptions['sepchar'] == "Semicolon":
            sepChar = ';'
        elif openFileOptions['sepchar'] == "Tab":
            sepChar = '\t'

        try:
            self.data = read_csv(os.path.join(openFileOptions['dirName'], openFileOptions['fileName']), sep=sepChar,
                                 header=0,
                                 engine='python', encoding='utf-8')
        except:
            # print "Error: ", sys.exc_info()
            type, value, traceback = sys.exc_info()
            self.dlg = wx.MessageDialog(None, "Error reading file " + openFileOptions['fileName'] + "\n" + str(value),
                                        "File error", wx.OK | wx.ICON_EXCLAMATION)
            if self.dlg.ShowModal() == wx.ID_OK:
                self.dlg.Destroy()
            readCorrect = False

        if readCorrect:
            if discardCol:
                self.data.drop(self.data.columns[[0]], axis=1, inplace=True)
            self.data.rename(columns={'Unnamed: 0': 'NoTag'}, inplace=True)

        if openFileOptions['additionalFile'] and readCorrect and (
                self.m_dataTable.GetNumberRows() != len(self.data.index)):
            self.dlg = wx.MessageDialog(None,
                                        "Number of rows does not match: \n  Loaded data has " + str(
                                            self.m_dataTable.GetNumberRows()) + " rows \n  File " + openFileOptions[
                                            'fileName'] + " has " + str(
                                            len(self.data.index)) + " rows ", "File error",
                                        wx.OK | wx.ICON_EXCLAMATION)
            if self.dlg.ShowModal() == wx.ID_OK:
                self.dlg.Destroy()
            readCorrect = False

        if readCorrect:

            if openFileOptions['additionalFile']:
                self.controller.storeData()
                self.m_undo.SetText("Undo add file")
                self.m_undo.Enable()
                self.controller.OpenAdditionalFile(self.data)
            else:
                self.controller.OpenFile(self.data)

            self.refreshGUI()

            if self.controller.nullValuesInFile(self.data):
                self.dlg = wx.MessageDialog(None, "File " + self.filename + " has one or more missing values",
                                            "Missing values", wx.OK | wx.ICON_WARNING)
                if self.dlg.ShowModal() == wx.ID_OK:
                    self.dlg.Destroy()

            if openFileOptions['additionalFile']:
                # Move the view of the table to the last column
                self.m_dataTable.SetGridCursor(0, self.controller.getNumberOfColumns() - 1)
                self.m_dataTable.MakeCellVisible(0, self.controller.getNumberOfColumns() - 1)

    def OpenAddXLS(self, openFileOptions):
        # print "File to load: ", openFileOptions['fileName']
        self.params['options']['dirfrom'] = openFileOptions['dirName']
        readCorrect = True
        self.data = None
        rowColNames = openFileOptions['rowColNames']
        noColsDiscard = openFileOptions['noColsDiscard']
        sheetNumber = openFileOptions['sheetNumber']

        # print "Reading col names from row: ", rowColNames

        try:
            self.data = read_excel(os.path.join(openFileOptions['dirName'], openFileOptions['fileName']),
                                   sheet_name=sheetNumber, header=rowColNames,
                                   index_col=None)
            if noColsDiscard != 0:
                self.data.drop(self.data.columns[range(noColsDiscard)], axis=1, inplace=True)
            # self.data = self.preprocessExcel(self.data)
        except:
            # print "Error: ", sys.exc_info()
            type, value, traceback = sys.exc_info()
            self.dlg = wx.MessageDialog(None, "Error reading file " + openFileOptions['fileName'] + "\n" + str(value),
                                        "File error", wx.OK | wx.ICON_EXCLAMATION)
            if self.dlg.ShowModal() == wx.ID_OK:
                self.dlg.Destroy()
            readCorrect = False

        if readCorrect:
            self.data.rename(columns={'Unnamed: 0': 'NoTag'}, inplace=True)

        if openFileOptions['additionalFile'] and readCorrect and (
                self.m_dataTable.GetNumberRows() != len(self.data.index)):
            self.dlg = wx.MessageDialog(None,
                                        "Number of rows does not match: \n  Loaded data has " + str(
                                            self.m_dataTable.GetNumberRows()) + " rows \n  File " + openFileOptions[
                                            'fileName'] + " has " + str(
                                            len(self.data.index)) + " rows ", "File error",
                                        wx.OK | wx.ICON_EXCLAMATION)
            if self.dlg.ShowModal() == wx.ID_OK:
                self.dlg.Destroy()
            readCorrect = False

        if readCorrect:
            if openFileOptions['additionalFile']:
                self.controller.storeData()
                self.m_undo.SetText("Undo add file")
                self.m_undo.Enable()
                self.controller.OpenAdditionalFile(self.data)
            else:
                self.controller.OpenFile(self.data)

            self.refreshGUI()

            if self.controller.nullValuesInFile(self.data):
                self.dlg = wx.MessageDialog(None,
                                            "File " + openFileOptions['fileName'] + " has one or more missing values",
                                            "Missing values", wx.OK | wx.ICON_WARNING)
                if self.dlg.ShowModal() == wx.ID_OK:
                    self.dlg.Destroy()

            if openFileOptions['additionalFile']:
                # Move the view of the table to the last column
                self.m_dataTable.SetGridCursor(0, self.controller.getNumberOfColumns() - 1)
                self.m_dataTable.MakeCellVisible(0, self.controller.getNumberOfColumns() - 1)

    def preprocessExcel(self, data):
        for row in range(len(data.index)):
            for col in range(len(data.columns)):
                if type(data.iloc[row, col]) == unicode or type(data.iloc[row, col]) == str:
                    if data.iloc[row, col].isspace():
                        data.iloc[row, col] = numpy.nan
                if type(data.iloc[row, col]) == int:
                    data.iloc[row, col] = float(data.iloc[row, col])

        data.dropna(axis=0, how='all', inplace=True)

        for col in data.columns:
            allNumbers = True;
            for row in data.index:
                if not isinstance(data.loc[row, col], (int, long, float)):
                    allNumbers = False;
            if allNumbers:
                data[col] = data[col].astype(numpy.float64)

        return data

    def adaptSizeOfGrid(self):

        '''
        This function calculates the number of rows and columns to adapt the grid
        '''

        numColsDataframe = self.controller.getNumberOfColumns()
        numRowsDataframe = self.controller.getNumberOfRows()

        numColsGrid = self.m_dataTable.GetNumberCols()
        numRowsGrid = self.m_dataTable.GetNumberRows()

        if numColsDataframe < numColsGrid:

            self.m_dataTable.DeleteCols(0, (numColsGrid - numColsDataframe))

        else:

            self.m_dataTable.AppendCols((numColsDataframe - numColsGrid))

        if numRowsDataframe < numRowsGrid:

            self.m_dataTable.DeleteRows(0, (numRowsGrid - numRowsDataframe))

        else:

            self.m_dataTable.AppendRows((numRowsDataframe - numRowsGrid))

    def fillInGrid(self):

        colLabels = self.controller.getLabelsOfColumns()
        numRows = self.controller.getNumberOfRows()
        numCols = self.controller.getNumberOfColumns()
        dataToAnalyse = self.controller.getDataToAnalyse()

        self.adaptSizeOfGrid()

        for i in range(len(colLabels)):
            self.m_dataTable.SetColLabelValue(i, colLabels[i])

        for row in range(numRows):
            for col in range(numCols):
                if dataToAnalyse.iloc[row, col] != dataToAnalyse.iloc[row, col]:
                    self.m_dataTable.SetCellValue(row, col, "nan")
                elif type(dataToAnalyse.iloc[row, col]) == float:
                    dataToAnalyse.iloc[row, col] = numpy.float64(dataToAnalyse.iloc[row, col])

                elif type(dataToAnalyse.iloc[row, col]) in (int, float, complex, numpy.float64, numpy.int64):
                    self.m_dataTable.SetCellValue(row, col, '{:5g}'.format(dataToAnalyse.iloc[row, col]))
                else:
                    self.m_dataTable.SetCellValue(row, col, dataToAnalyse.iloc[row, col])

        self.controller.detectColumnTypes()

    def markNans(self):
        # print "# Going to mark nans"
        numRows = self.controller.getNumberOfRows()
        numCols = self.controller.getNumberOfColumns()
        self.params['noOfNulls'] = 0
        for row in range(numRows):
            for col in range(numCols):
                content = self.m_dataTable.GetCellValue(row, col)
                if content == 'nan' or content == 'null' or content.lower() == "no data":  # This checks for nan
                    # print "# Nan detected in cell:",row,"  ",col 
                    self.m_dataTable.SetCellValue(row, col, "null")
                    # self.m_dataTable.SetCellBackgroundColour(row,col,'peachpuff')
                    self.m_dataTable.SetCellBackgroundColour(row, col, wx.Colour(255, 218, 185))
                    self.params['noOfNulls'] += 1
                else:
                    if self.m_dataTable.GetColLabelValue(col) in self.controller.characterValues:
                        self.m_dataTable.SetCellBackgroundColour(row, col, wx.Colour(250, 250, 210))
                    elif self.m_dataTable.GetColLabelValue(col) in self.controller.integerValues:
                        self.m_dataTable.SetCellBackgroundColour(row, col, wx.Colour(240, 255, 255))
                    else:
                        self.m_dataTable.SetCellBackgroundColour(row, col, 'white')

    def saveFile(self, event):
        askfile = AskFileType(self, -1, "save")
        askfile.CenterOnScreen()
        askfile.ShowModal()
        askfile.Destroy()

    def saveToCSV(self):

        self.fileExtensions = "CSV files (*.csv)|*.csv;*.CSV|All files (*.*)|*.*"
        saveFile = wx.FileDialog(self, message='Save file', defaultDir=self.params['options']['dirfrom'],
                                 defaultFile='untitled.csv', wildcard=self.fileExtensions,
                                 style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if saveFile.ShowModal() == wx.ID_OK:
            self.filename = saveFile.GetFilename()
            self.directory = saveFile.GetDirectory()

            fileExtension = self.filename.rpartition(".")[-1]
            if fileExtension.lower() != "csv":
                self.dlg = wx.MessageDialog(None,
                                            "Error exporting file " + self.filename + "\nFile extension (.csv) is required",
                                            "File error", wx.OK | wx.ICON_EXCLAMATION)
                if self.dlg.ShowModal() == wx.ID_OK:
                    self.dlg.Destroy()
            else:
                path = os.path.join(self.directory, self.filename)
                exportCsv = ExportCsvOptions(self)

                if exportCsv.ShowModal() == wx.ID_OK:
                    try:
                        self.controller.exportDataCSV(path, exportCsv.getSelectedExportOptions())
                    except:
                        self.dlg = wx.MessageDialog(None, "Error saving to file " + self.filename,
                                                    "File error", wx.OK | wx.ICON_EXCLAMATION)
                        if self.dlg.ShowModal() == wx.ID_OK:
                            self.dlg.Destroy()
                        return
                    dlg = wx.MessageDialog(None, "Data saved to file: " + self.filename, "File operation",
                                           wx.OK | wx.ICON_INFORMATION)
                    self.params['options']['dirfrom'] = self.directory

                    if dlg.ShowModal() == wx.ID_OK:
                        dlg.Destroy()

    def saveToXLS(self):

        self.fileExtensions = "Excel files (*.xls;*.xlsx)|*.xls;*.xlsx;*.XLS;*.XLSX|All files (*.*)|*.*"
        saveFile = wx.FileDialog(self, message='Save file', defaultDir=self.params['options']['dirfrom'],
                                 defaultFile='untitled.xlsx',
                                 wildcard=self.fileExtensions, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if saveFile.ShowModal() == wx.ID_OK:
            self.filename = saveFile.GetFilename()
            self.directory = saveFile.GetDirectory()

            fileExtension = self.filename.rpartition(".")[-1]
            if fileExtension.lower() not in ["xls", "xlsx"]:
                self.dlg = wx.MessageDialog(None,
                                            "Error exporting file " + self.filename + "\nFile extension (.xls|.xlsx) is required",
                                            "File error", wx.OK | wx.ICON_EXCLAMATION)
                if self.dlg.ShowModal() == wx.ID_OK:
                    self.dlg.Destroy()

            else:
                path = os.path.join(self.directory, self.filename)
                try:
                    self.controller.exportDataExcel(path)
                except:
                    self.dlg = wx.MessageDialog(None, "Error saving to file " + self.filename,
                                                "File error", wx.OK | wx.ICON_EXCLAMATION)
                    if self.dlg.ShowModal() == wx.ID_OK:
                        self.dlg.Destroy()
                    return
                dlg = wx.MessageDialog(None, "Data saved to file: " + self.filename, "File operation",
                                       wx.OK | wx.ICON_INFORMATION)
                self.params['options']['dirfrom'] = self.directory

                if dlg.ShowModal() == wx.ID_OK:
                    dlg.Destroy()

    def resetData(self, event):
        self.controller.storeData()
        self.m_undo.SetText("Undo close data")
        self.m_undo.Enable()

        self.controller.resetDataToAnalyse()
        self.refreshGUI()

    def refreshGUI(self, updateDataInfo=True, markNans=True):

        # Reset plots options
        self.histogramOptions = {}
        self.scatterPlotOptions = {}
        self.boxPlotOptions = {}
        self.pieChartOptions = {}
        self.barChartOptions = {}

        if not self.controller.programState.dataToAnalyse.empty:  # data present
            self.fillInGrid()  # Fills wxgrid from the data of the pandas dataframe
            self.m_dataTable.AutoSize()
            lastColumnOrigSize = self.m_dataTable.GetColSize(self.controller.getNumberOfColumns() - 1)
            self.m_dataTable.SetColSize(self.controller.getNumberOfColumns() - 1, lastColumnOrigSize + 30)
            self.m_dataTable.ClearSelection()
            if markNans:
                self.markNans()
            if updateDataInfo:
                self.updateDataInfo()
            self.Layout()
            self.m_dataTable.Enable(True)
            self.m_dataTable.SetFocus()

            # Graphs
            self.histogramBtn.Enable(True)
            self.scatterPlotBtn.Enable(True)
            self.pieChartBtn.Enable(True)
            self.boxPlotBtn.Enable(True)
            self.barChartBtn.Enable(True)

            # Buttons
            self.openNewFileBtn.Enable(False)
            self.addFileBtn.Enable(True)
            self.resetDataBtn.Enable(True)
            self.exportDataBtn.Enable(True)
            self.descriptiveStatsBtn.Enable(True)
            self.significanceTestBtn.Enable(True)

            # Menus
            self.m_menuNewFile.Enable(False)
            self.m_menuAddFile.Enable(True)
            self.m_menuResetData.Enable(True)
            self.m_menuExportData.Enable(True)
            self.m_addNewColumn.Enable(True)
            self.m_deleteColumns.Enable(True)

        else:  # no data
            self.fillInGrid()

            self.m_dataTable.AppendRows(45)
            self.m_dataTable.AppendCols(45)

            self.m_dataTable.Enable(False)

            # Graphs
            self.histogramBtn.Enable(False)
            self.scatterPlotBtn.Enable(False)
            self.pieChartBtn.Enable(False)
            self.boxPlotBtn.Enable(False)
            self.barChartBtn.Enable(False)

            # Buttons
            self.openNewFileBtn.Enable(True)
            self.addFileBtn.Enable(False)
            self.resetDataBtn.Enable(False)
            self.exportDataBtn.Enable(False)
            self.descriptiveStatsBtn.Enable(False)
            self.significanceTestBtn.Enable(False)

            # Menus
            self.m_menuNewFile.Enable(True)
            self.m_menuAddFile.Enable(False)
            self.m_menuResetData.Enable(False)
            self.m_menuExportData.Enable(False)
            self.m_addNewColumn.Enable(False)
            self.m_deleteColumns.Enable(False)

            self.updateDataInfo()

            self.m_dataTable.SetColLabelSize(30)
            self.m_dataTable.SetRowLabelSize(80)
            self.Layout()

    def deleteColumnsByLabels(self, event):

        selectedColumnsInterface = DeleteColumnsInterface(self,
                                                          list(self.controller.programState.dataToAnalyse.columns))

        if selectedColumnsInterface.ShowModal() == wx.ID_OK:
            self.controller.storeData()
            self.m_undo.SetText("Undo delete columns")
            self.m_undo.Enable()

            listOfColumns = selectedColumnsInterface.getSelectedColumns()
            self.controller.deleteColumns(listOfColumns)

            self.refreshGUI()

            # if self.controller.programState.dataToAnalyse.empty:
            #     self.resetData(None)
            # else:
            #     self.refreshGUI()

    def createNewColumn(self, event):

        if (len(self.controller.integerValues + self.controller.floatValues) != 0):
            # Minimun and maximum for using when spinCtrls are created
            minimum = int(self.controller.programState.dataToAnalyse.min(numeric_only=True).min().round()) - 1
            maximum = int(self.controller.programState.dataToAnalyse.max(numeric_only=True).max().round()) + 1

            factorFrame = AddColumnInterface(self, (self.controller.integerValues + self.controller.floatValues),
                                             list(self.controller.programState.dataToAnalyse.columns), minimum, maximum)
            factorFrame.Show(True)

            if factorFrame.ShowModal() == wx.ID_OK:
                self.controller.storeData()
                self.m_undo.SetText("Undo add new column")
                self.m_undo.Enable()

                factorsFromInterface, self.selectedRadioButton, tagRestValues, nameOfFactor = factorFrame.returnFactors()
                self.controller.addColumn(factorsFromInterface, self.selectedRadioButton, tagRestValues, nameOfFactor)

                self.refreshGUI()

                numCols = self.controller.getNumberOfColumns()
                self.m_dataTable.SetGridCursor(0, numCols - 1)
                self.m_dataTable.MakeCellVisible(0, numCols - 1)
                self.m_dataTable.SelectCol(numCols - 1)


        else:

            wx.MessageBox("There are no numerical values", "ERROR")

    def createBasicStatisticsInterface(self, event):

        if (len(self.controller.integerValues + self.controller.floatValues) != 0):
            self.tagsAndValues.clear()

            for value in self.controller.characterValues:
                listTags = list(self.controller.programState.dataToAnalyse[value].unique())
                # listTags = [x for x in listTags if unicode(x).encode('utf-8') != 'nan']
                listTags = [x for x in listTags if str(x) != 'nan']
                self.tagsAndValues[value] = numpy.asarray(listTags)

                # self.tagsAndValues[value] = self.controller.programState.dataToAnalyse[str(value)].unique()

            dataFrame = self.controller.programState.dataToAnalyse
            variablesList = self.controller.floatValues + self.controller.integerValues
            minimum = int(self.controller.programState.dataToAnalyse.min(numeric_only=True).min().round()) - 1
            maximum = int(self.controller.programState.dataToAnalyse.max(numeric_only=True).max().round()) + 1

            basicStatsInterface = BasicStatisticsInterface(self, variablesList, self.tagsAndValues,
                                                           self.controller.integerValues, dataFrame)

            if basicStatsInterface.ShowModal() == wx.ID_CLOSE:
                basicStatsInterface.Destroy()

        else:

            wx.MessageBox("There are no numerical values in the data", "ERROR", wx.OK | wx.ICON_EXCLAMATION)

    def doSignificanceTest(self, event):

        if (len(self.controller.integerValues + self.controller.floatValues) != 0):
            self.tagsAndValues.clear()

            for value in self.controller.characterValues:
                listTags = list(self.controller.programState.dataToAnalyse[value].unique())
                listTags = [x for x in listTags if str(x) != 'nan']
                # listTags = [x for x in listTags if unicode(x).encode('utf-8') != 'nan']
                self.tagsAndValues[value] = numpy.asarray(listTags)

                # self.tagsAndValues[value] = self.controller.programState.dataToAnalyse[str(value)].unique()

            dataFrame = self.controller.programState.dataToAnalyse
            variablesList = self.controller.floatValues + self.controller.integerValues

            significanceTestFrame = SignificanceTestInterface(self, variablesList, self.tagsAndValues,
                                                              self.controller.integerValues, dataFrame)
            significanceTestFrame.Show()

            if significanceTestFrame.ShowModal() == wx.ID_CANCEL:
                significanceTestFrame.Destroy()

        else:

            wx.MessageBox("There are no numerical values", "ERROR")

    def createHistogram(self, event):

        if (len(self.controller.integerValues + self.controller.floatValues) != 0):

            histogramFrame = HistogramInterface(self, self.controller.floatValues + self.controller.integerValues,
                                                self.controller.characterValues, self.histogramOptions)

            if histogramFrame.ShowModal() == wx.ID_OK:
                self.histogramOptions = histogramFrame.getHistogramOptions()

                self.controller.createHistogram(self.histogramOptions)
        else:

            wx.MessageBox("There are no numerical values", "ERROR")

    def createScatterPlot(self, event):

        if (len(self.controller.integerValues + self.controller.floatValues) != 0):

            scatterFrame = ScatterPlotInterface(self, self.controller.floatValues + self.controller.integerValues,
                                                self.scatterPlotOptions)

            if scatterFrame.ShowModal() == wx.ID_OK:
                self.scatterPlotOptions = scatterFrame.getScatterPlotOptions()
                self.controller.createScatterPlot(self.scatterPlotOptions)
        else:

            wx.MessageBox("There are no numerical values", "Attention")

    def createPieChart(self, event):

        if (len(self.controller.characterValues) != 0):

            pieChartFrame = PieChartInterface(self, self.controller.characterValues, self.pieChartOptions)

            if pieChartFrame.ShowModal() == wx.ID_OK:
                self.pieChartOptions = pieChartFrame.getPieChartOptions()

                self.controller.createPieChart(self.pieChartOptions)

        else:

            wx.MessageBox("There are no categorical variables", "ERROR")

    def createBoxPlot(self, event):

        if (len(self.controller.integerValues + self.controller.floatValues) != 0):

            boxPlotFrame = BoxPlotInterface(self, self.controller.floatValues + self.controller.integerValues,
                                            self.controller.characterValues, self.boxPlotOptions)

            if boxPlotFrame.ShowModal() == wx.ID_OK:
                self.boxPlotOptions = boxPlotFrame.getBoxPlotOptions()
                self.controller.createBoxPlot(self.boxPlotOptions)
        else:

            wx.MessageBox("There are no numerical variables", "ERROR")

    def createBarChart(self, event):

        if (len(self.controller.integerValues + self.controller.floatValues) != 0):

            barChartFrame = BarChartInterface(self, self.controller.floatValues + self.controller.integerValues,
                                              self.controller.characterValues, self.barChartOptions)

            if barChartFrame.ShowModal() == wx.ID_OK:
                self.barChartOptions = barChartFrame.getBarChartOptions()
                self.controller.createBarChart(self.barChartOptions)

        else:

            wx.MessageBox("There are no numerical variables", "ERROR")

    def showWarning(self):

        dlg = wx.MessageDialog(None, "Lower limit must be smaller than the upper limit", "Be careful!",
                               wx.OK | wx.ICON_EXCLAMATION)

        if dlg.ShowModal() == wx.ID_OK:
            dlg.Destroy()

    def informationAboutNullValues(self):

        dlg = wx.MessageDialog(None, "There are null values in this File", "Null Values", wx.OK | wx.ICON_INFORMATION)

        if dlg.ShowModal() == wx.ID_OK:
            dlg.Destroy()

    def appInformation(self, event):

        description = u'Graphical Application for Statistical Analysis of TAbulated Data\n\nDaniel Pereira Alonso\nLeandro Rodr\u00EDguez Liñares\nMar\u00EDa Jos\u00E9 Lado Touriño'

        info = wx.adv.AboutDialogInfo()

        info.SetName('GASATaD')
        info.SetVersion(str(self.params['version']))
        info.SetDescription(description)
        info.SetCopyright(u"\u00A9 2021");
        info.SetIcon(wx.Icon(os.path.dirname(os.path.abspath(__file__)) + "/GasatadLogo.ico", wx.BITMAP_TYPE_ICO))
        info.SetWebSite("https://milegroup.github.io/gasatad/")

        wx.adv.AboutBox(info)

    def closeApp(self, event):
        emptyData = False
        try:
            emptyData = self.controller.programState.dataToAnalyse.empty
        except:
            emptyData = True

        if not emptyData:
            dlg = wx.MessageDialog(self, "Do you really want to close GASATaD?", "Confirm Exit",
                                   wx.OK | wx.CANCEL | wx.ICON_QUESTION | wx.CANCEL_DEFAULT)
            result = dlg.ShowModal()
            dlg.Destroy()
            if result == wx.ID_OK:
                self.configSave()
                self.Destroy()
        else:
            self.configSave()
            self.Destroy()

    def configInit(self):
        """If config dir and file does not exist, it is created
        If config file exists, it is loaded"""

        # print "Intializing configuration"

        if not os.path.exists(self.params['configDir']):
            # print "Directory does not exists ... creating"
            os.makedirs(self.params['configDir'])

        if os.path.exists(self.params['configFile']):
            # print "Loading config"
            self.configLoad()
        else:
            # print "Saving config"
            self.configSave()

    def configSave(self):
        """ Saves configuration file"""
        try:
            # from ConfigParser import SafeConfigParser
            # options = SafeConfigParser()

            import configparser
            options = configparser.ConfigParser()

            options.add_section('gasatad')

            for param in self.params['options'].keys():
                # In windows, if the path contains non-ascii characters, it is not saved in the configuration file
                validParam = True
                if param == "dirfrom" and sys.platform == "win32":
                    tmpStr = self.params['options'][param]
                    if any(ord(char) > 126 for char in tmpStr):
                        validParam = False
                if validParam:
                    options.set('gasatad', param, self.params['options'][param])
                    # print "  ",param,"  -  ",self.params['options'][param]

            tempF = open(self.params['configFile'], 'w')
            # print("Trying to write configuration in ", self.params['configFile'])
            options.write(tempF)
            tempF.close()

            if platform == "win32":
                import win32api, win32con
                win32api.SetFileAttributes(self.params['configDir'], win32con.FILE_ATTRIBUTE_HIDDEN)
        except:
            return

    def configLoad(self):
        """ Loads configuration file"""
        # print "Loading file",self.params['configFile']
        try:
            import configparser
            options = configparser.ConfigParser()
            options.read(self.params['configFile'])
            for section in options.sections():
                for param, value in options.items(section):
                    self.params['options'][param] = value
                    # print "param",param,"  -  value",value
        except:
            # print "Problem loading configuration file", self.params['configFile']
            try:
                os.remove(self.params['configFile'])
            except:
                pass
            return


class ReplaceInColInterface(wx.Dialog):
    def __init__(self, parent, listOfTags):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Replace in column", size=wx.DefaultSize,
                           pos=wx.DefaultPosition)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        topSizer = wx.BoxSizer(wx.HORIZONTAL)

        leftSizer = wx.BoxSizer(wx.VERTICAL)
        leftSizer.Add(wx.StaticText(self, -1, "Old value:"))
        self.cb = wx.ComboBox(self, choices=listOfTags, value=listOfTags[0], size=(160, -1))
        leftSizer.Add(self.cb, 0, wx.TOP | wx.LEFT, 5)
        topSizer.Add(leftSizer, 0, wx.ALL, 10)

        rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer.Add(wx.StaticText(self, -1, "New value (empty for 'null'):"))
        self.tc = wx.TextCtrl(self, size=(160, -1))
        rightSizer.Add(self.tc, 0, wx.TOP | wx.LEFT | wx.EXPAND, 5)
        topSizer.Add(rightSizer, 0, wx.ALL, 10)

        mainSizer.Add(topSizer)

        # Ok and Cancel buttons
        okay = wx.Button(self, wx.ID_OK)
        cancel = wx.Button(self, wx.ID_CANCEL)
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()

        mainSizer.Add(btns, 0, wx.BOTTOM | wx.ALIGN_RIGHT, 10)
        mainSizer.Fit(self)

        self.SetSizer(mainSizer)

        self.Layout()
        self.Fit()
        self.Centre(wx.BOTH)

        self.Show(True)

    def getValues(self):
        return self.cb.GetValue(), self.tc.GetValue()


class DeleteColumnsInterface(wx.Dialog):

    def __init__(self, parent, listOfColumns):

        # The dictionary is initialized -> Key = name of column; value = False (because neither checkbox is selected yet)
        self.selectedColumns = dict.fromkeys(listOfColumns, False)

        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Delete columns", pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        gbSizer1 = wx.GridBagSizer(0, 0)
        gbSizer1.SetFlexibleDirection(wx.BOTH)
        gbSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # Sizer where the names of the columns are placed
        fgSizerCheckBoxColumns = wx.FlexGridSizer(0, 4, 0, 0)
        fgSizerCheckBoxColumns.SetFlexibleDirection(wx.BOTH)
        fgSizerCheckBoxColumns.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        fgSizerCheckBoxColumns.AddGrowableCol(1)

        for column in listOfColumns:
            self.m_checkBox = wx.CheckBox(self, wx.ID_ANY, str(column), wx.DefaultPosition, wx.DefaultSize, 0)
            fgSizerCheckBoxColumns.Add(self.m_checkBox, 0, wx.EXPAND | wx.ALL, 5)
            self.Bind(wx.EVT_CHECKBOX, self.changeValueCheckBox, self.m_checkBox)

        gbSizer1.Add(fgSizerCheckBoxColumns, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALIGN_RIGHT | wx.EXPAND | wx.ALL,
                     5)

        # Ok and Cancel buttons
        okay = wx.Button(self, wx.ID_OK)
        cancel = wx.Button(self, wx.ID_CANCEL)
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()

        gbSizer1.Add(btns, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.BOTTOM | wx.ALIGN_RIGHT, 10)

        self.SetSizer(gbSizer1)
        gbSizer1.Fit(self)
        self.Layout()
        self.Fit()
        self.Centre(wx.BOTH)

        self.Show(True)

    def changeValueCheckBox(self, event):
        checkBox = event.GetEventObject()
        if checkBox.IsChecked():
            self.selectedColumns[checkBox.GetLabel()] = True
        else:
            self.selectedColumns[checkBox.GetLabel()] = False

    def getSelectedColumns(self):
        listSelectedColumns = []
        for key in self.selectedColumns.keys():
            if self.selectedColumns[key]:
                listSelectedColumns.append(key)
        return listSelectedColumns


class ExportCsvOptions(wx.Dialog):

    def __init__(self, parent):

        self.exportOptions = OptionsInExportInterface()

        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Export csv", pos=wx.DefaultPosition, size=wx.DefaultSize,
                           style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        gbSizer1 = wx.GridBagSizer(0, 0)
        gbSizer1.SetFlexibleDirection(wx.BOTH)
        gbSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # Sizer for the options
        fgSizerExportOptions = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizerExportOptions.SetFlexibleDirection(wx.BOTH)
        fgSizerExportOptions.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        fgSizerExportOptions.AddGrowableCol(1)

        self.characterSet = wx.StaticText(self, wx.ID_ANY, u"Character set:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.characterSet.Wrap(-1)
        fgSizerExportOptions.Add(self.characterSet, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        m_comboBox3Choices = ["UTF-8", "ASCII", "Latin_1"]
        self.m_comboBox3 = wx.ComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       m_comboBox3Choices, wx.CB_READONLY)
        self.m_comboBox3.SetSelection(0)
        self.Bind(wx.EVT_COMBOBOX, self.setCharacterSetValue, self.m_comboBox3)
        fgSizerExportOptions.Add(self.m_comboBox3, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)

        self.xAxisName = wx.StaticText(self, wx.ID_ANY, u"Field delimiter:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.xAxisName.Wrap(-1)
        fgSizerExportOptions.Add(self.xAxisName, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        m_comboBox3Choices = [",", ";", ":", "{Tab}", "{Space}"]
        self.m_comboBox3 = wx.ComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       m_comboBox3Choices, wx.CB_READONLY)
        self.m_comboBox3.SetSelection(0)
        self.Bind(wx.EVT_COMBOBOX, self.setFieldDelimiterValue, self.m_comboBox3)
        fgSizerExportOptions.Add(self.m_comboBox3, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)

        self.yAxisName = wx.StaticText(self, wx.ID_ANY, u"Decimal separator:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.yAxisName.Wrap(-1)
        fgSizerExportOptions.Add(self.yAxisName, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        m_comboBox3Choices = [".", ","]
        self.m_comboBox3 = wx.ComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       m_comboBox3Choices, wx.CB_READONLY)
        self.m_comboBox3.SetSelection(0)
        self.Bind(wx.EVT_COMBOBOX, self.setDecimalSeparatorValue, self.m_comboBox3)
        fgSizerExportOptions.Add(self.m_comboBox3, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)

        gbSizer1.Add(fgSizerExportOptions, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.ALL, 5)

        # Additional options
        AdditionalOptSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Additional options"), wx.HORIZONTAL)

        self.wColumnNames = wx.CheckBox(self, wx.ID_ANY, "Write column names", wx.DefaultPosition, wx.DefaultSize, 0)
        AdditionalOptSizer.Add(self.wColumnNames, 0, wx.ALL, 10)
        self.wColumnNames.SetValue(True)
        self.Bind(wx.EVT_CHECKBOX, self.setWriteColumnNameValue, self.wColumnNames)

        self.wRowNames = wx.CheckBox(self, wx.ID_ANY, "Write row names (Index)", wx.DefaultPosition, wx.DefaultSize, 0)
        AdditionalOptSizer.Add(self.wRowNames, 0, wx.ALL, 10)
        self.wRowNames.SetValue(True)
        self.Bind(wx.EVT_CHECKBOX, self.setWriteRowNames, self.wRowNames)

        gbSizer1.Add(AdditionalOptSizer, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 20)

        # Ok and Cancel buttons
        okay = wx.Button(self, wx.ID_OK)
        cancel = wx.Button(self, wx.ID_CANCEL)
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()

        gbSizer1.Add(btns, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.ALL, 5)

        self.SetSizer(gbSizer1)
        gbSizer1.Fit(self)
        self.Layout()
        self.Fit()
        self.Centre(wx.BOTH)

        self.Fit()
        self.Show(True)

    def setCharacterSetValue(self, event):

        option = event.GetEventObject().GetValue().lower()

        self.exportOptions.setCharacterSet(option)

    def setFieldDelimiterValue(self, event):

        option = event.GetEventObject().GetValue()
        if option == "{Tab}":

            self.exportOptions.setFieldDelimiter("\t")

        elif option == "{Space}":

            self.exportOptions.setFieldDelimiter(" ")

        else:

            self.exportOptions.setFieldDelimiter(option)

    def setDecimalSeparatorValue(self, event):

        option = event.GetEventObject().GetValue()

        self.exportOptions.setdecimalSeparator(option)

    def setWriteColumnNameValue(self, event):

        option = event.GetEventObject().GetValue()

        self.exportOptions.setWriteColNames(option)

    def setWriteRowNames(self, event):

        option = event.GetEventObject().GetValue()

        self.exportOptions.setWriteRowNames(option)

    def getSelectedExportOptions(self):

        return self.exportOptions
