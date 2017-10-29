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
import wx.grid
import os
import sys
from pandas.io.parsers import read_csv
from pandas.io.excel import read_excel
import numpy
from Controller import Controller
from FactorsInterface import FactorsInterface
from ChartInterface import HistogramInterface, ScatterPlotInterface,\
    PieChartInterface, BoxPlotInterface, BarChartInterface

from SignificanceTestInterface import SignificanceTestInterface


from Model import OptionsInExportInterface
from BasicStatisticsInterface import BasicStatisticsInterface

from sys import platform


###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

    tagsAndValues = {}
     
    def __init__( self, parent ):

        self.configInit()

        # print "Invoked from directory:",self.params['options']['dirfrom']
        
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = "GASATaD")

        if platform != "darwin":
            icon = wx.Icon("GasatadLogo.ico", wx.BITMAP_TYPE_ICO)
            self.SetIcon(icon)

        self.CheckUpdates()
        
        # self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
                
        #MENU BAR
        self.m_menubar1 = wx.MenuBar( 0 )
        
        
        # ------------ File menu

        self.m_fileMenu = wx.Menu()

        self.m_menuItem1 = wx.MenuItem( self.m_fileMenu, wx.ID_ANY, u"Open new file", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_fileMenu.AppendItem( self.m_menuItem1 )
        
        self.m_menuItem2 = wx.MenuItem( self.m_fileMenu, wx.ID_ANY, u"Add file", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_fileMenu.AppendItem( self.m_menuItem2 )
        self.m_menuItem2.Enable(False)

        self.m_menuItem4 = wx.MenuItem( self.m_fileMenu, wx.ID_ANY, u"Reset data", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_fileMenu.AppendItem(self.m_menuItem4)
        self.m_menuItem4.Enable(False)

        self.m_menuItem6 = wx.MenuItem( self.m_fileMenu, wx.ID_ANY, u"Quit", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_fileMenu.AppendItem( self.m_menuItem6 )

        # ------------ Options menu

        self.m_optionsMenu = wx.Menu()
        
        self.m_discardColumn = self.m_optionsMenu.Append(100, u"Discard first column", "", wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU_RANGE, self.discardColumnCheckboxChanged, id=100)
        if self.params['options']['discardfirstcolumn']=="True":
            self.m_discardColumn.Check()

        self.m_optionsSubMenu = wx.Menu()
        self.m_CVSSeparator1 = self.m_optionsSubMenu.Append(201, u"Comma", "", wx.ITEM_RADIO)
        self.m_CVSSeparator2 = self.m_optionsSubMenu.Append(202, u"Semicolon", "", wx.ITEM_RADIO)
        self.m_CVSSeparator3 = self.m_optionsSubMenu.Append(203, u"Tabulator", "", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU_RANGE, self.cvsCharacterSeparatorChanged, id=201, id2=203)
        if self.params['options']['sepchar']=="Comma":
            self.m_CVSSeparator1.Check()
        elif self.params['options']['sepchar']=="Semicolon":
            self.m_CVSSeparator2.Check()
        elif self.params['options']['sepchar']=="Tab":
            self.m_CVSSeparator3.Check()

        self.m_optionsMenu.AppendMenu(wx.NewId(), u"CVS character separator",self.m_optionsSubMenu)

        self.m_resetOptions = wx.MenuItem( self.m_optionsMenu, wx.ID_ANY, u"Reset options", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_optionsMenu.AppendItem(self.m_resetOptions)

        # ------------ About menu

        self.m_aboutMenu = wx.Menu()

        self.m_menuItem5 = wx.MenuItem( self.m_aboutMenu, wx.ID_ANY, u"About GASATaD", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_aboutMenu.AppendItem(self.m_menuItem5)
        
        self.m_menubar1.Append( self.m_fileMenu, u"File" )
        self.m_menubar1.Append( self.m_optionsMenu, u"Options")
        self.m_menubar1.Append( self.m_aboutMenu, u"About" )
                
        self.SetMenuBar( self.m_menubar1 )
        
        # self.m_menubar1.SetFocus()
        
        globalSizer = wx.BoxSizer(wx.HORIZONTAL)

        leftSizer = wx.BoxSizer(wx.VERTICAL)


        #  -------------------- Information part of the interface

        informationSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Information" ), wx.VERTICAL )
        
        self.m_staticText2 = wx.StaticText( informationSizer.GetStaticBox(), wx.ID_ANY, u"Main file:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        self.m_staticText2.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        
        informationSizer.Add( self.m_staticText2, 0, wx.ALL, 5 )
        
        bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText3 = wx.StaticText( informationSizer.GetStaticBox(), wx.ID_ANY, u"Columns:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        bSizer1.Add( self.m_staticText3, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        
        self.m_textCtrl1 = wx.TextCtrl( informationSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,20 ), wx.TE_READONLY )
        bSizer1.Add( self.m_textCtrl1, 0, wx.ALL, 5 )
        self.m_textCtrl1.Enable(False)
        
        self.m_staticText4 = wx.StaticText( informationSizer.GetStaticBox(), wx.ID_ANY, u"Rows:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        bSizer1.Add( self.m_staticText4, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        
        self.m_textCtrl2 = wx.TextCtrl( informationSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,20 ), wx.TE_READONLY )
        bSizer1.Add( self.m_textCtrl2, 0, wx.ALL, 5 )
        self.m_textCtrl2.Enable(False)
        
        informationSizer.Add( bSizer1, 1, wx.EXPAND|wx.LEFT, 5 )
        
        self.m_staticText9 = wx.StaticText( informationSizer.GetStaticBox(), wx.ID_ANY, u"Additional file:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )
        self.m_staticText9.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        
        informationSizer.Add( self.m_staticText9, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        
        bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText31 = wx.StaticText( informationSizer.GetStaticBox(), wx.ID_ANY, u"Columns:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText31.Wrap( -1 )
        bSizer11.Add( self.m_staticText31, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        
        self.m_textCtrl11 = wx.TextCtrl( informationSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,20 ), wx.TE_READONLY )
        bSizer11.Add( self.m_textCtrl11, 0, wx.ALL, 5 )
        self.m_textCtrl11.Enable(False)
        
        self.m_staticText41 = wx.StaticText( informationSizer.GetStaticBox(), wx.ID_ANY, u"Rows:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText41.Wrap( -1 )
        bSizer11.Add( self.m_staticText41, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        
        self.m_textCtrl21 = wx.TextCtrl( informationSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,20 ), wx.TE_READONLY )
        bSizer11.Add( self.m_textCtrl21, 0, wx.ALL, 5 )
        self.m_textCtrl21.Enable(False)
        
        informationSizer.Add( bSizer11, 1, wx.EXPAND|wx.LEFT, 5 )
       
        leftSizer.Add(informationSizer,flag= wx.ALL, border=5)

        #  -------------------- Buttons of the interface
        
        
        buttonsSizer = wx.BoxSizer(wx.VERTICAL)

        self.newColumnBtn = wx.Button( self, wx.ID_ANY, u"Add New Column", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.newColumnBtn.Enable( False )
        # self.newColumnBtn.SetMinSize( wx.Size( -1,25 ) )
        
        buttonsSizer.Add( self.newColumnBtn, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.resetDataBtn = wx.Button( self, wx.ID_ANY, u"Reset Data", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.resetDataBtn.Enable( False )
        #self.resetDataBtn.SetMinSize( wx.Size( -1,25 ) )
        
        buttonsSizer.Add( self.resetDataBtn, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.deleteColumnsBtn = wx.Button( self, wx.ID_ANY, u"Delete Columns", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.deleteColumnsBtn.Enable( False )
        #self.deleteColumnsBtn.SetMinSize( wx.Size( -1,25 ) )
        
        buttonsSizer.Add( self.deleteColumnsBtn, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.exportDataBtn = wx.Button( self, wx.ID_ANY, u"Export Data", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.exportDataBtn.Enable( False )
        #self.exportDataBtn.SetMinSize( wx.Size( -1,25 ) )
        
        buttonsSizer.Add( self.exportDataBtn, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.descriptiveStatsBtn = wx.Button( self, wx.ID_ANY, u"Descriptive Statistics", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.descriptiveStatsBtn.Enable( False )
        #self.descriptiveStatsBtn.SetMinSize( wx.Size( -1,25 ) )
        
        buttonsSizer.Add( self.descriptiveStatsBtn, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.significanceTestBtn = wx.Button( self, wx.ID_ANY, u"Significance Test", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.significanceTestBtn.Enable( False )
        #self.significanceTestBtn.SetMinSize( wx.Size( -1,25 ) )
        
        buttonsSizer.Add( self.significanceTestBtn, 0, wx.ALL|wx.EXPAND, 5 )
        
        leftSizer.Add( buttonsSizer, flag= wx.ALL | wx.EXPAND, border=5)

        

        #  -------------------- Buttons for plot
        
        gSizerChart = wx.GridSizer( 0, 3, 0, 0 )
        
        #Images needed for the buttons
        self.histogramBmp = wx.Image(str(os.path.dirname(__file__))+"/icons/histogram1.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.scatterPlotmBmp = wx.Image(str(os.path.dirname(__file__))+"/icons/scatterPlot1.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.pieChartmBmp = wx.Image(str(os.path.dirname(__file__))+"/icons/pieChart1.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.boxPlotBmp = wx.Image(str(os.path.dirname(__file__))+"/icons/boxPlot1.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.barChartBmp = wx.Image(str(os.path.dirname(__file__))+"/icons/barChart1.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        
        self.histogramBtn = wx.BitmapButton( self, wx.ID_ANY, self.histogramBmp, wx.DefaultPosition, wx.Size( 75,75 ), wx.BU_AUTODRAW )
        gSizerChart.Add( self.histogramBtn, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.histogramBtn.Enable(False)
        self.histogramBtn.SetToolTip(wx.ToolTip("Histogram"))
        
        self.scatterPlotBtn = wx.BitmapButton( self, wx.ID_ANY, self.scatterPlotmBmp, wx.DefaultPosition, wx.Size( 75,75 ), wx.BU_AUTODRAW )
        gSizerChart.Add( self.scatterPlotBtn, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.scatterPlotBtn.Enable(False)
        self.scatterPlotBtn.SetToolTip(wx.ToolTip("Scatter Plot"))
        
        self.pieChartBtn = wx.BitmapButton( self, wx.ID_ANY, self.pieChartmBmp, wx.DefaultPosition, wx.Size( 75,75 ), wx.BU_AUTODRAW )
        gSizerChart.Add( self.pieChartBtn, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.pieChartBtn.Enable(False)
        self.pieChartBtn.SetToolTip(wx.ToolTip("Pie Chart"))
        
        self.boxPlotBtn = wx.BitmapButton( self, wx.ID_ANY, self.boxPlotBmp, wx.DefaultPosition, wx.Size( 75,75 ), wx.BU_AUTODRAW )
        gSizerChart.Add( self.boxPlotBtn, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.boxPlotBtn.Enable(False)
        self.boxPlotBtn.SetToolTip(wx.ToolTip("Box Plot"))
        
        self.barChartBtn = wx.BitmapButton( self, wx.ID_ANY, self.barChartBmp, wx.DefaultPosition, wx.Size( 75,75 ), wx.BU_AUTODRAW )
        gSizerChart.Add( self.barChartBtn, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.barChartBtn.Enable(False)
        self.barChartBtn.SetToolTip(wx.ToolTip("Bar Chart"))  
        
        leftSizer.Add( gSizerChart, flag= wx.ALL | wx.EXPAND, border=5 )

        # ------------------- Info about upgrades

        if self.params['upgradable']:

            import wx.lib.agw.gradientbutton as GB

            leftSizer.AddStretchSpacer(1)
            # self.upgradeButton = wx.Button( self, wx.ID_ANY, u"* New version: "+self.params['availableVersionToUpgrade']+" *", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.upgradeButton = GB.GradientButton(self, label = "New version available: "+self.params['availableVersionToUpgrade'])
            self.upgradeButton.SetBaseColours(startcolour=wx.TheColourDatabase.Find('PALE GREEN'), foregroundcolour=wx.BLACK)
            self.upgradeButton.SetPressedBottomColour(wx.TheColourDatabase.Find('LIGHT GREY'))
            self.upgradeButton.SetPressedTopColour(wx.TheColourDatabase.Find('LIGHT GREY'))
            boldFont = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
            boldFont.SetWeight(wx.BOLD)
            self.upgradeButton.SetFont(boldFont)
            self.Bind(wx.EVT_BUTTON, self.openBrowserDownload, id=self.upgradeButton.GetId())

            leftSizer.Add( self.upgradeButton, flag= wx.ALL | wx.EXPAND, border=5 )


        globalSizer.Add( leftSizer, flag = wx.EXPAND|wx.ALL, border=10 )
        
        # ------------------- Data table

        self.m_dataTable = wx.grid.Grid(self)
        
        # Grid
        self.m_dataTable.CreateGrid( 45, 45 )
        self.m_dataTable.EnableEditing( False )
        self.m_dataTable.EnableGridLines( True )
        self.m_dataTable.EnableDragGridSize( False )
        self.m_dataTable.SetMargins( 0, 0 )
        
        # Columns
        self.m_dataTable.EnableDragColMove( False )
        self.m_dataTable.EnableDragColSize( False )
        self.m_dataTable.SetColLabelSize( 30 )
        self.m_dataTable.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        
        # Rows
        self.m_dataTable.EnableDragRowSize( False )
        self.m_dataTable.SetRowLabelSize( 80 )
        self.m_dataTable.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        

        # Cell Defaults
        self.m_dataTable.SetDefaultCellAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTER )

        fgSizer8 = wx.BoxSizer(wx.VERTICAL)
        fgSizer8.Add(self.m_dataTable)
        # fgSizer8.Add( self.m_dataTable, 0, wx.ALL|wx.EXPAND, 5 )
        self.m_dataTable.Enable(False)
        self.m_dataTable.Show(True)
        
        # globalSizer.Add( fgSizer8, wx.GBPosition( 0, 1 ), wx.GBSpan( 12, 12 ), wx.EXPAND, 5 )
        globalSizer.Add( fgSizer8, flag= wx.ALL | wx.EXPAND, border=10 )
        
        #Options to show the GUI
        self.SetSizer( globalSizer )
        self.Layout()
        self.Centre( wx.BOTH )
        
        self.Show(True)
        # self.Move((0,0))
        widthScreen, heightScreen = wx.GetDisplaySize()
        widthWindow = 1440
        heightWindow = 900
        if ((widthScreen>=widthWindow) and (heightScreen>heightWindow)):
            self.SetSize((widthWindow,heightWindow)) 
        else:
            self.Maximize()
        self.SetMinSize((1024,768))
        
        #Binding between buttons and functions which will control the events

        self.Bind(wx.EVT_CLOSE, self.closeApp) # Close window

        self.Bind(wx.EVT_MENU, self.OpenFile, self.m_menuItem1)
        self.Bind(wx.EVT_MENU, self.OpenAdditionalFile, self.m_menuItem2)
        self.Bind(wx.EVT_MENU, self.resetData, self.m_menuItem4)
        self.Bind(wx.EVT_MENU, self.resetOptions, self.m_resetOptions)
        self.Bind(wx.EVT_MENU, self.appInformation, self.m_menuItem5)
        self.Bind(wx.EVT_MENU, self.closeApp, self.m_menuItem6)
        self.Bind(wx.EVT_BUTTON, self.createBasicStatisticsInterface, self.descriptiveStatsBtn)
        self.Bind(wx.EVT_BUTTON, self.createNewColumn, self.newColumnBtn)
        self.Bind(wx.EVT_BUTTON, self.resetData, self.resetDataBtn)
        self.Bind(wx.EVT_BUTTON, self.deleteColumns, self.deleteColumnsBtn)
        self.Bind(wx.EVT_BUTTON, self.exportData, self.exportDataBtn)
        self.Bind(wx.EVT_BUTTON, self.createHistogram, self.histogramBtn)
        self.Bind(wx.EVT_BUTTON, self.createScatterPlot, self.scatterPlotBtn)
        self.Bind(wx.EVT_BUTTON, self.createPieChart, self.pieChartBtn)
        self.Bind(wx.EVT_BUTTON, self.createBoxPlot, self.boxPlotBtn)
        self.Bind(wx.EVT_BUTTON, self.createBarChart, self.barChartBtn)
        self.Bind(wx.EVT_BUTTON, self.doSignificanceTest, self.significanceTestBtn)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.rightClickOnTable,self.m_dataTable)
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.rightClickOnTable,self.m_dataTable)
        
        
        #A controller object is created
        self.controller = Controller()

        HelpString = (
            "      -help: shows this information\n"
            "      -loadCSV fileName: loads CSV file (full path is required)\n"
            )

        if (len(sys.argv) != 1 and (sys.platform=='linux2' or sys.platform=='darwin')):
            arguments = sys.argv[1:]
            possibleArguments = ['-help','-loadCSV']

            for argument in arguments:
                if argument[0] == '-':
                    if argument not in possibleArguments:
                        print "\n** ERROR: command '"+argument+"' not recognized **\n"
                        print "** GASATaD terminal mode commands:"
                        print HelpString
                        sys.exit(0)
            
            if "-help" in arguments:
                print ("\n** GASATaD: terminal mode **\n")
                print HelpString
                sys.exit(0)

            else:
                if "-loadCSV" in arguments:
                    CSVFileName = arguments[arguments.index("-loadCSV")+1]
                    print "Loading CSV file: "+CSVFileName
                    self.OpenCVSFileNoGUI(CSVFileName)


    def rightClickOnTable(self, event):
        columnClicked = event.GetCol()
        columnsSelected = self.m_dataTable.GetSelectedCols()
        if columnClicked in columnsSelected:
            textPopupDelete = "Delete column"
            if len(columnsSelected)>1:
                textPopupDelete += "s"
            popupMenu = wx.Menu()
            self.popupDeleteID = wx.NewId()
            popupMenu.Append(self.popupDeleteID,textPopupDelete)
            self.Bind(wx.EVT_MENU, self.onPopupDelete, id=self.popupDeleteID)
            self.PopupMenu( popupMenu )
            popupMenu.Destroy() 

        event.Skip()
    
    def onPopupDelete(self,event):
        dlg = wx.MessageDialog(self, "This action cannot be undone.\nAre you sure to proceed?",
                                   "Delete columns", wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_EXCLAMATION)
            
        if dlg.ShowModal() == wx.ID_OK:
            dlg.Destroy()

            columnsSelectedIndex = self.m_dataTable.GetSelectedCols()
            columnsSelectedLabels = []
            for columnIndex in columnsSelectedIndex:
                columnsSelectedLabels.append(self.m_dataTable.GetColLabelValue(columnIndex))
        
            self.controller.deleteColumns(columnsSelectedLabels)
            
            if self.controller.programState.dataToAnalyse.empty:
                self.resetData(None)
            else:
                self.fillInGrid()
            
            self.m_dataTable.AutoSize()
            self.Layout()
        else:
            dlg.Destroy()


    def CheckUpdates(self):
        from sys import argv
        import urllib2
        import os

        remoteVersion = ""
        remoteVersionFile = ""

        if argv[0].endswith("MainApp.py"):
            # print "## Running GASATaD from source"
            remoteVersionFile = "https://raw.githubusercontent.com/milegroup/gasatad/gh-pages/programVersions/src.txt"

        if platform=="linux2" and argv[0]=="/usr/share/gasatad/MainApp.py":
            remoteVersionFile = "https://raw.githubusercontent.com/milegroup/gasatad/gh-pages/programVersions/deb.txt"

        if platform=="darwin" and os.getcwd().startswith("/usr/local"):
            remoteVersionFile = "https://raw.githubusercontent.com/milegroup/gasatad/gh-pages/programVersions/mac.txt"

        if platform=="win32" and argv[0].endswith(".exe"):
            remoteVersionFile = "https://raw.githubusercontent.com/milegroup/gasatad/gh-pages/programVersions/win.txt"

        try:
            remoteFile = urllib2.urlopen(remoteVersionFile)
            remoteVersion=remoteFile.readline().strip()
            remoteFile.close()
            # print "## Version available in GASATaD web page: ", remoteVersion
        except urllib2.URLError:
            # print "## I couldn't check for updates"
            None

        if remoteVersion:
            # print "## Version file exists"
            if float(remoteVersion) > float(self.params['version']):
                self.params['upgradable'] = True
                self.params['availableVersionToUpgrade'] = remoteVersion

            # self.params['upgradable'] = True
            # self.params['availableVersionToUpgrade'] = remoteVersion

    def openBrowserDownload(self,event):
        import webbrowser
        webbrowser.open("https://milegroup.github.io/gasatad/#download")

    
    def OpenCVSFileNoGUI(self, fileName):       
        
        self.data = None
        
        try:
                self.Datafile = open(fileName, 'r')            
                self.data = read_csv(self.Datafile, sep = None, header=0, index_col = 0, engine = 'python')
                self.data.rename(columns={'Unnamed: 0':'NoTag'}, inplace=True)
                
                self.controller.OpenFile(self.data, os.path.basename(fileName))                    
                self.m_menuItem2.Enable(True)
                
                self.m_textCtrl1.SetValue(str(len(self.data.columns)))
                self.m_textCtrl2.SetValue(str(len(self.data.index)))  
                
                self.m_textCtrl11.Clear()
                self.m_textCtrl21.Clear()
                    
        except:
            
            print("Error: ", sys.exc_info()[0])
            print("There was some problem with the file")
            return 

        self.fillInGrid()
        self.descriptiveStatsBtn.Enable()
        self.newColumnBtn.Enable()
        self.resetDataBtn.Enable()
        self.deleteColumnsBtn.Enable()
        self.exportDataBtn.Enable()
        self.m_dataTable.Enable()
        self.m_menuItem4.Enable()
        self.histogramBtn.Enable()
        self.scatterPlotBtn.Enable()
        self.pieChartBtn.Enable()
        self.boxPlotBtn.Enable()
        self.barChartBtn.Enable()
        self.significanceTestBtn.Enable()   

        print "File: "+fileName+" loaded"

        self.params['dataPresent'] = True

        self.m_dataTable.AutoSize()
        self.Layout()




    def OpenFile(self, event, fileName = None):       
        
        self.Datafile = None
        self.data = None
        
        try:
            
            self.fileExtensions = "CSV files (*.csv)|*.csv|Excel files (*.xls;*.xlsx)|*.xls;*xlsx|All files (*.*)|*.*"
            
            wOpenFile = wx.FileDialog(self, message = 'Open file',defaultDir = self.params['options']['dirfrom'], defaultFile = '', wildcard = self.fileExtensions, style = wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)
            
            if wOpenFile.ShowModal() == wx.ID_OK:
                self.filename = wOpenFile.GetFilename()
                self.directory = wOpenFile.GetDirectory()
                self.params['options']['dirfrom'] = self.directory
                self.Datafile = open(os.path.join(self.directory, self.filename), 'r')
                self.fileExtension = self.filename.rpartition(".")[-1]


                discardCol = None
                if self.params['options']['discardfirstcolumn']=='True':
                    discardCol=0

                sepChar = ''
                if self.params['options']['sepchar']=="Comma":
                    sepChar=','
                elif self.params['options']['sepchar']=="Semicolon":
                    sepChar=';'
                elif self.params['options']['sepchar']=="Tab":
                    sepChar='\t'

                if self.fileExtension == "csv":
                    self.data = read_csv(self.Datafile, sep = sepChar, header=0, index_col = discardCol, engine = 'python')
                    self.data.rename(columns={'Unnamed: 0':'NoTag'}, inplace=True)
                
                if self.fileExtension == "xlsx" or self.fileExtension == "xls":
                    self.data = read_excel(self.Datafile,sheetname=0, header = 0, index_col = discardCol)
                    self.data.rename(columns={'Unnamed: 0':'NoTag'}, inplace=True)
                
                wOpenFile.Destroy()

                if (self.Datafile is not None):
                    self.controller.OpenFile(self.data, self.filename)
                    
                    self.m_menuItem2.Enable(True)
                        
                    self.m_textCtrl1.SetValue(str(len(self.data.columns)))
                    self.m_textCtrl2.SetValue(str(len(self.data.index)))  
                    
                    self.m_textCtrl11.Clear()
                    self.m_textCtrl21.Clear()
                        
                    self.fillInGrid()
                
                    self.descriptiveStatsBtn.Enable()
                    self.newColumnBtn.Enable()
                    self.resetDataBtn.Enable()
                    self.deleteColumnsBtn.Enable()
                    self.exportDataBtn.Enable()
                    self.m_dataTable.Enable()
                    self.m_menuItem4.Enable()
                    self.histogramBtn.Enable()
                    self.scatterPlotBtn.Enable()
                    self.pieChartBtn.Enable()
                    self.boxPlotBtn.Enable()
                    self.barChartBtn.Enable()
                    self.significanceTestBtn.Enable()   
                    
                    if self.controller.nullValuesInFile(self.data):
                       raise ValueError("There are null values in the file")

                    self.m_dataTable.AutoSize()
                    self.Layout()
                        
                    self.params['dataPresent'] = True
                    self.firstFileAdded()

        except:
            
            print("Error: ", sys.exc_info()[0])
            type, value, traceback = sys.exc_info()
            
            self.dlg = wx.MessageDialog(None, "Error reading file "+self.filename+"\n"+str(value), "File error", wx.OK | wx.ICON_EXCLAMATION)
            
            if self.dlg.ShowModal() == wx.ID_OK:
            
                self.dlg.Destroy()


                
    def OpenAdditionalFile(self, *events):       
        
        self.Datafile = None
        self.data = None

        try:
            
            self.fileExtensions = "CSV files (*.csv)|*.csv|Excel files (*.xls;*.xlsx)|*.xls;*xlsx|All files (*.*)|*.*"
             
            wOpenFile = wx.FileDialog(self, message = 'Open file',defaultDir = self.params['options']['dirfrom'], defaultFile = '', wildcard=self.fileExtensions, style = wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)
            
            if wOpenFile.ShowModal() == wx.ID_OK:
                self.filename = wOpenFile.GetFilename()
                self.directory = wOpenFile.GetDirectory()
                self.params['options']['dirfrom'] = self.directory
                self.Datafile = open(os.path.join(self.directory, self.filename), 'r')
                self.fileExtension = self.filename.rpartition(".")[-1]

                discardCol = None
                sepChar = ''

                if self.params['options']['discardfirstcolumn']=='True':
                    discardCol=0

                if self.params['options']['sepchar']=="Comma":
                    sepChar=','
                elif self.params['options']['sepchar']=="Semicolon":
                    sepChar=';'
                elif self.params['options']['sepchar']=="Tab":
                    sepChar='\t'

                if self.fileExtension == "csv":
                    self.data = read_csv(self.Datafile, sep = sepChar, header=0, index_col = discardCol, engine = 'python')
                    self.data.rename(columns={'Unnamed: 0':'NoTag'}, inplace=True)
                
                if self.fileExtension == "xlsx":
                    self.data = read_excel(self.Datafile,sheetname=0, header = 0, index_col = discardCol)
                    self.data.rename(columns={'Unnamed: 0':'NoTag'}, inplace=True)

                if (len(self.data.columns)==0):
                    raise ValueError("There was a problem reading the columns of the file")

                if (self.Datafile is not None):
                
                    if self.controller.OpenAdditionalFile(self.data, self.filename)==False:
                        raise ValueError("Number of rows do not match")

                    if self.controller.nullValuesInFile(self.data):
                       raise ValueError("There are null values in the file")

                    self.fillInGrid()
                    self.descriptiveStatsBtn.Enable()
                    self.newColumnBtn.Enable()
                    self.resetDataBtn.Enable()
                    self.deleteColumnsBtn.Enable()
                    self.exportDataBtn.Enable()
                    self.significanceTestBtn.Enable()
                    self.m_dataTable.Enable()
                
                    self.m_textCtrl11.SetValue(str(len(self.data.columns)))
                    self.m_textCtrl21.SetValue(str(len(self.data.index)))
                    self.m_menuItem2.Enable(False)

                    self.m_dataTable.AutoSize()
                    self.Layout()
        
        except:
            
            print("Error: ", sys.exc_info()[0])
            type, value, traceback = sys.exc_info()

            self.dlg = wx.MessageDialog(None, "Error reading file "+self.filename+"\n"+str(value), "File error", wx.OK | wx.ICON_EXCLAMATION)
            
            
            if self.dlg.ShowModal() == wx.ID_OK:
            
                self.dlg.Destroy()

       
    
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
        
        for i in range (len(colLabels)):
            
            self.m_dataTable.SetColLabelValue(i, colLabels[i])
        
        for row in range (numRows):
            
            for col in range (numCols):

                    if type(dataToAnalyse.iloc[row, col]) in (int, float, long, complex, numpy.float64, numpy.int64):
                             
                        self.m_dataTable.SetCellValue(row, col, str(dataToAnalyse.iloc[row, col].round(3)))

                    else:
                        
                        self.m_dataTable.SetCellValue(row, col, str(dataToAnalyse.iloc[row, col]))
        
        self.controller.sortVariables()


    
    def exportData(self, event):
        
        self.fileExtensions = ".CSV (*.csv*)|*.csv*"
        saveFile = wx.FileDialog(self, message = 'Open file',defaultDir = '', defaultFile = '', wildcard = self.fileExtensions, style = wx.SAVE | wx.FD_OVERWRITE_PROMPT)
            
        if saveFile.ShowModal() == wx.ID_OK:
            self.filename = saveFile.GetFilename()
            self.directory = saveFile.GetDirectory()
            
            path = self.directory + "/" + self.filename
            
            exportCsv = ExportCsvOptions(self)
            
            if exportCsv.ShowModal() == wx.ID_OK:
                
                self.controller.exportData(path + '.csv', exportCsv.getSelectedExportOptions())


    
    def resetData(self, event):
        
        self.controller.resetDataToAnalyse()
        
        self.fillInGrid()
        
        self.m_dataTable.AppendRows(45)
        self.m_dataTable.AppendCols(45)
        
        self.m_dataTable.Enable( False )

        self.descriptiveStatsBtn.Enable(False)
        self.newColumnBtn.Enable(False)
        self.resetDataBtn.Enable(False)
        self.deleteColumnsBtn.Enable(False)
        self.exportDataBtn.Enable(False)
        self.significanceTestBtn.Enable(False)
        
        self.m_menuItem2.Enable(False)
        self.m_menuItem4.Enable(False)
        
        #Graphs
        self.histogramBtn.Enable( False )
        self.scatterPlotBtn.Enable( False )
        self.pieChartBtn.Enable( False )
        self.boxPlotBtn.Enable( False )
        self.barChartBtn.Enable( False )
        
        #Clearing the information about the files
        self.m_textCtrl1.Clear()
        self.m_textCtrl2.Clear()
        self.m_textCtrl11.Clear()
        self.m_textCtrl21.Clear()

        self.params['dataPresent'] = False

        self.m_dataTable.SetColLabelSize( 30 )
        self.m_dataTable.SetRowLabelSize( 80 )
        #self.m_dataTable.AutoSize()
        self.Layout()


    def resetOptions(self,event):
        for key in self.params['optionsdefault'].keys():
            self.params['options'][key] = self.params['optionsdefault'][key]
        self.m_discardColumn.Check()
        self.m_CVSSeparator1.Check()

    
    def deleteColumns(self, event):
        
        selectedColumnsInterface = DeleteColumnsInterface(self, list(self.controller.programState.dataToAnalyse.columns))
        
        if  selectedColumnsInterface.ShowModal() == wx.ID_OK:
            
            dlg = wx.MessageDialog(self, "This action cannot be undone.\nAre you sure to proceed?",
                                   "Delete columns", wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_EXCLAMATION)
            
            
            if dlg.ShowModal() == wx.ID_OK:
                
                dlg.Destroy()
                
                listOfColumns = selectedColumnsInterface.getSelectedColumns()

                # print "##:",listOfColumns
                self.controller.deleteColumns(listOfColumns)
                
                if self.controller.programState.dataToAnalyse.empty:
                    self.resetData(None)
                else:
                    self.fillInGrid()
                
                self.m_dataTable.AutoSize()
                self.Layout()
  
            else:
            
                dlg.Destroy() 
            

        
    def createNewColumn(self, event):
        
        
        if (len(self.controller.integerValues + self.controller.floatValues) != 0):
            #Minimun and maximum for using when spinCtrls are created
            minimum = int(self.controller.programState.dataToAnalyse.min(numeric_only = True).min().round()) -1
            maximum = int(self.controller.programState.dataToAnalyse.max(numeric_only = True).max().round()) +1
            
            factorFrame = FactorsInterface(self, (self.controller.integerValues + self.controller.floatValues),
                                           list(self.controller.programState.dataToAnalyse.columns), minimum, maximum)
            factorFrame.Show(True)
            
            if  factorFrame.ShowModal() == wx.ID_OK:
                
                factorsFromInterface, self.selectedRadioButton, tagRestValues, nameOfFactor = factorFrame.returnFactors()
            
                self.controller.addColumn(factorsFromInterface, self.selectedRadioButton, tagRestValues, nameOfFactor)
                
                self.fillInGrid()
                self.m_dataTable.AutoSize()
                self.Layout()         
        else:
            
            wx.MessageBox("There are no numerical values", "Attention!")


    def createBasicStatisticsInterface(self, event):
        

        if (len(self.controller.integerValues + self.controller.floatValues) != 0):
            self.tagsAndValues.clear()
            
            for value in self.controller.characterValues:
                
                self.tagsAndValues[value] = self.controller.programState.dataToAnalyse[str(value)].unique()
            
            dataFrame = self.controller.programState.dataToAnalyse
            variablesList = self.controller.floatValues + self.controller.integerValues
            minimum = int(self.controller.programState.dataToAnalyse.min(numeric_only = True).min().round()) -1
            maximum = int(self.controller.programState.dataToAnalyse.max(numeric_only = True).max().round()) +1
            
            basicStatsInterface = BasicStatisticsInterface(self, variablesList, self.tagsAndValues, self.controller.integerValues,
                                                           minimum, maximum, dataFrame)
            
            
            if basicStatsInterface.ShowModal() == wx.ID_CLOSE:
                basicStatsInterface.Destroy()

        else:
            
            wx.MessageBox("There are no numerical values", "Attention!")



    def doSignificanceTest(self, event):
        
        if (len(self.controller.integerValues + self.controller.floatValues) != 0):
            self.tagsAndValues.clear()
            
            for value in self.controller.characterValues:
                
                self.tagsAndValues[value] = self.controller.programState.dataToAnalyse[str(value)].unique()
            
            
            dataFrame = self.controller.programState.dataToAnalyse
            variablesList = self.controller.floatValues + self.controller.integerValues
            minimum = int(self.controller.programState.dataToAnalyse.min(numeric_only = True).min().round()) -1
            maximum = int(self.controller.programState.dataToAnalyse.max(numeric_only = True).max().round()) +1
            
            significanceTestFrame = SignificanceTestInterface(self, variablesList, self.tagsAndValues, self.controller.integerValues,
                                                              minimum, maximum, dataFrame)
            significanceTestFrame.Show()
    
            if significanceTestFrame.ShowModal() == wx.ID_CANCEL:
                
                significanceTestFrame.Destroy()
        
        else:
            
            wx.MessageBox("There are no numerical values", "Attention!")



    def createHistogram(self, event):
        
        if (len(self.controller.integerValues + self.controller.floatValues) != 0):
                 
            histogramFrame = HistogramInterface(self, self.controller.floatValues + self.controller.integerValues, self.controller.characterValues)
            
            if  histogramFrame.ShowModal() == wx.ID_OK:
        
                    histogramOptions = histogramFrame.getHistogramOptions()
                    
                    self.controller.createHistogram(histogramOptions) 
        else:
            
            wx.MessageBox("There are no numerical values", "Attention!")
   
   
    def createScatterPlot(self, event):  
            
        if (len(self.controller.integerValues + self.controller.floatValues) != 0):
                
            scatterFrame = ScatterPlotInterface(self, self.controller.floatValues + self.controller.integerValues)
            
            if  scatterFrame.ShowModal() == wx.ID_OK:
        
                    scatterOptions = scatterFrame.getScatterPlotOptions()
                    
                    self.controller.createScatterPlot(scatterOptions)
        else:
            
            wx.MessageBox("There are no numerical values", "Attention!")        
                
    
    def createPieChart(self, event):  
            
        if (len(self.controller.characterValues) != 0):
                     
            pieChartFrame = PieChartInterface(self, self.controller.characterValues)
            
            if  pieChartFrame.ShowModal() == wx.ID_OK:
        
                    pieChartOptions = pieChartFrame.getPieChartOptions()
                    
                    self.controller.createPieChart(pieChartOptions)

        else:
            
            wx.MessageBox("There are no categorical variables", "Attention!") 


                
    def createBoxPlot(self, event):  
            
        if (len(self.controller.integerValues + self.controller.floatValues) != 0):
                    
            boxPlotFrame = BoxPlotInterface(self, self.controller.floatValues + self.controller.integerValues, self.controller.characterValues)
            
            if  boxPlotFrame.ShowModal() == wx.ID_OK:
        
                    boxPlotOptions = boxPlotFrame.getBoxPlotOptions()
                    
                    self.controller.createBoxPlot(boxPlotOptions)         
        else:
            
            wx.MessageBox("There are no numerical variables", "Attention!")
    
    
                   
    def createBarChart(self, event):
         
        if (len(self.controller.integerValues + self.controller.floatValues) != 0):
             
            barChartFrame = BarChartInterface(self, self.controller.floatValues + self.controller.integerValues, self.controller.characterValues)
            
            if  barChartFrame.ShowModal() == wx.ID_OK:
        
                    barChartOptions = barChartFrame.getBarChartOptions()
                    operation = barChartFrame.getSelectedOperation()
                    
                    self.controller.createBarChart(barChartOptions, operation) 
        
        else:
            
            wx.MessageBox("There are no numerical variables", "Attention!")

    
    def discardColumnCheckboxChanged(self, event):
        if self.m_discardColumn.IsChecked():
            self.params['options']['discardfirstcolumn']='True'
        else:
            self.params['options']['discardfirstcolumn']='False'

    def cvsCharacterSeparatorChanged(self, event):
        if self.m_CVSSeparator1.IsChecked():
            self.params['options']['sepchar']="Comma"
        if self.m_CVSSeparator2.IsChecked():
            self.params['options']['sepchar']="Semicolon"
        if self.m_CVSSeparator3.IsChecked():
            self.params['options']['sepchar']="Tab"
    
        
        
    def showWarning(self):
        
        dlg = wx.MessageDialog(None, "Lower limit must be smaller than the upper limit", "Be careful!", wx.OK | wx.ICON_EXCLAMATION)
            
            
        if dlg.ShowModal() == wx.ID_OK:
            
            dlg.Destroy()
    
    
    
    def firstFileAdded(self):
        
        dlg = wx.MessageDialog(None, "A file has been opened\nClick 'yes' to add another file to the data", "Additional File", wx.YES_NO | wx.ICON_INFORMATION)
                        
        if dlg.ShowModal() == wx.ID_YES:            
            self.OpenAdditionalFile()
    
        else:  
            dlg.Destroy()


    
    def informationAboutNullValues(self):
        
        dlg = wx.MessageDialog(None, "There are null values in this File", "Null Values", wx.OK | wx.ICON_INFORMATION)
                        
        if dlg.ShowModal() == wx.ID_OK:
            dlg.Destroy()
        
        
    def appInformation(self, event):
        
        description = u'Graphical Application for Statistical Analysis of TAbulated Data\n\nDaniel Pereira Alonso\nLeandro Rodr\u00EDguez Liñares\nMar\u00EDa Jos\u00E9 Lado Touriño'
        
        info = wx.AboutDialogInfo()    

        info.SetName('GASATaD')
        info.SetVersion(str(self.params['version']))
        info.SetDescription(description)
        info.SetCopyright(u"\u00A9 2017");
        info.SetIcon(wx.Icon(os.path.dirname(os.path.abspath(__file__)) + "/GasatadLogo.ico", wx.BITMAP_TYPE_ICO))
        
        wx.AboutBox(info)

    def closeApp(self,event):
        #print "Closing application"
        if self.params['dataPresent']:
            dlg = wx.MessageDialog(self, "Do you really want to close GASATaD?","Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION|wx.CANCEL_DEFAULT)
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
        
        from ConfigParser import SafeConfigParser

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
        from ConfigParser import SafeConfigParser
        options = SafeConfigParser()
        
        options.add_section('gasatad')
        
        for param in self.params['options'].keys():
            options.set('gasatad',param,self.params['options'][param])
        
        tempF = open(self.params['configFile'],'w')
        options.write(tempF)
        tempF.close()

        if platform=="win32":
            import win32api,win32con
            win32api.SetFileAttributes(self.params['configDir'],win32con.FILE_ATTRIBUTE_HIDDEN)

    def configLoad(self):
        """ Loads configuration file"""
        # print "Loading file",self.params['configFile']
        from ConfigParser import SafeConfigParser
        options=SafeConfigParser()
        options.read(self.params['configFile'])
        for section in options.sections():
            for param,value in options.items(section):
                self.params['options'][param]=value
                # print "param",param,"  -  value",value




class DeleteColumnsInterface ( wx.Dialog ):    

    
    def __init__( self, parent, listOfColumns ):

        #The dictionary is initialized -> Key = name of column; value = False (because neither checkbox is selected yet)
        self.selectedColumns = dict.fromkeys(listOfColumns, False)
        
        
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Delete Columns", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        #Sizer where the names of the columns are placed
        fgSizerCheckBoxColumns = wx.FlexGridSizer( 0, 4, 0, 0 )
        fgSizerCheckBoxColumns.SetFlexibleDirection( wx.BOTH )
        fgSizerCheckBoxColumns.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        fgSizerCheckBoxColumns.AddGrowableCol(1)
        
        for column in listOfColumns:
            
                self.m_checkBox = wx.CheckBox( self, wx.ID_ANY, str(column), wx.DefaultPosition, wx.DefaultSize, 0 )
                fgSizerCheckBoxColumns.Add( self.m_checkBox, 0, wx.EXPAND | wx.ALL, 5)
                self.Bind(wx.EVT_CHECKBOX, self.changeValueCheckBox, self.m_checkBox)

        gbSizer1.Add( fgSizerCheckBoxColumns, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.EXPAND|wx.ALL, 5 )        
        
        #Ok and Cancel buttons
        okay = wx.Button( self, wx.ID_OK )
        cancel = wx.Button( self, wx.ID_CANCEL )
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()

        gbSizer1.Add( btns, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND | wx.ALL, 5 )               
        
        self.SetSizer( gbSizer1 )
        gbSizer1.Fit(self)
        self.Layout()
        self.Fit()
        self.Centre( wx.BOTH )

        self.Show(True)



    def changeValueCheckBox(self, event):
        
        checkBox = event.GetEventObject()
        
        if checkBox.IsChecked():
            
            self.selectedColumns[checkBox.GetLabel().encode("utf-8")]= True
                        
        else:
            
            self.selectedColumns[checkBox.GetLabel().encode("utf-8")]= False

         
            
    def getSelectedColumns(self):
        
        listSelectedColumns = []
        
        for key in self.selectedColumns.keys():
            
            if self.selectedColumns[key]:
                
                listSelectedColumns.append(key)
                
        
        return listSelectedColumns



    
class ExportCsvOptions ( wx.Dialog ):
    
    def __init__( self, parent):
        
        self.exportOptions = OptionsInExportInterface()
        
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Export csv", pos = wx.DefaultPosition, size = wx.DefaultSize, 
                            style = wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        
        #Sizer for the options
        fgSizerExportOptions = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizerExportOptions.SetFlexibleDirection( wx.BOTH )
        fgSizerExportOptions.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        fgSizerExportOptions.AddGrowableCol(1)
        
        self.characterSet = wx.StaticText( self, wx.ID_ANY, u"Character set:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.characterSet.Wrap( -1 )
        fgSizerExportOptions.Add( self.characterSet, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
        
        m_comboBox3Choices = ["UTF-8","ASCII","Latin_1"]
        self.m_comboBox3 = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_comboBox3Choices, wx.CB_READONLY )
        self.m_comboBox3.SetSelection( 0 )
        self.Bind(wx.EVT_COMBOBOX, self.setCharacterSetValue, self.m_comboBox3)
        fgSizerExportOptions.Add( self.m_comboBox3, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5 )
        
        
        self.xAxisName = wx.StaticText( self, wx.ID_ANY, u"Field delimiter:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.xAxisName.Wrap( -1 )
        fgSizerExportOptions.Add( self.xAxisName, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
        
        m_comboBox3Choices = [",", ";", ":", "{Tab}", "{Space}"]
        self.m_comboBox3 = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_comboBox3Choices, wx.CB_READONLY )
        self.m_comboBox3.SetSelection( 0 )
        self.Bind(wx.EVT_COMBOBOX, self.setFieldDelimiterValue, self.m_comboBox3)
        fgSizerExportOptions.Add( self.m_comboBox3, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5 )
        
        
        self.yAxisName = wx.StaticText( self, wx.ID_ANY, u"Decimal separator:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.yAxisName.Wrap( -1 )
        fgSizerExportOptions.Add( self.yAxisName, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
        
        m_comboBox3Choices = [".", ","]
        self.m_comboBox3 = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_comboBox3Choices, wx.CB_READONLY )
        self.m_comboBox3.SetSelection( 0 )
        self.Bind(wx.EVT_COMBOBOX, self.setDecimalSeparatorValue, self.m_comboBox3)
        fgSizerExportOptions.Add( self.m_comboBox3, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5 )
        
        gbSizer1.Add( fgSizerExportOptions, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND | wx.ALL, 5 )

        
        #Additional options
        AdditionalOptSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Additional options" ), wx.HORIZONTAL )

        self.wColumnNames = wx.CheckBox( self, wx.ID_ANY, "Write column names", wx.DefaultPosition, wx.DefaultSize, 0 )
        AdditionalOptSizer.Add(self.wColumnNames, 0, wx.ALL, 10)
        self.wColumnNames.SetValue(True)
        self.Bind(wx.EVT_CHECKBOX, self.setWriteColumnNameValue, self.wColumnNames)
        
        self.wRowNames = wx.CheckBox( self, wx.ID_ANY, "Write row names (Index)", wx.DefaultPosition, wx.DefaultSize, 0 )
        AdditionalOptSizer.Add(self.wRowNames, 0, wx.ALL, 10)
        self.wRowNames.SetValue(True)
        self.Bind(wx.EVT_CHECKBOX, self.setWriteRowNames, self.wRowNames)
        
        gbSizer1.Add( AdditionalOptSizer, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 20 )   
        
        #Ok and Cancel buttons
        okay = wx.Button( self, wx.ID_OK )
        cancel = wx.Button( self, wx.ID_CANCEL )
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        
        gbSizer1.Add( btns, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND | wx.ALL, 5 )        
        
        self.SetSizer( gbSizer1 )
        gbSizer1.Fit(self)
        self.Layout()
        self.Fit()
        self.Centre( wx.BOTH )
        
        self.Fit()
        self.Show(True)


    
    def setCharacterSetValue(self, event):
        
        option = event.GetEventObject().GetValue().encode("utf-8").lower()
        
        self.exportOptions.setCharacterSet(option)
    
    
    def setFieldDelimiterValue(self, event):
        
        option = event.GetEventObject().GetValue().encode("utf-8")
        
        if option == "{Tab}":
            
            self.exportOptions.setFieldDelimiter("\t")
        
        elif option == "{Space}":
            
            self.exportOptions.setFieldDelimiter(" ")
        
        else:
            
            self.exportOptions.setFieldDelimiter(option)


            
    def setDecimalSeparatorValue(self,event):
        
        option = event.GetEventObject().GetValue().encode("utf-8")
        
        self.exportOptions.setdecimalSeparator(option)
    
    
    def setWriteColumnNameValue(self, event):
        
        option = event.GetEventObject().GetValue()
        
        self.exportOptions.setWriteColNames(option)
    
    
    def setWriteRowNames(self, event):
        
        option = event.GetEventObject().GetValue()
        
        self.exportOptions.setWriteRowNames(option)
    
    
    def getSelectedExportOptions(self):
        
        return self.exportOptions
        
        
