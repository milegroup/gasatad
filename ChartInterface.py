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
import wx.xrc

from Model import ChartOptions


class HistogramInterface ( wx.Dialog ): 
        
    position = 'by default'
    
    def __init__( self, parent, listOfVariables, listOfTags ):
        
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Chart", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        #Histogram options
        fgSizerchartOptions = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizerchartOptions.SetFlexibleDirection( wx.BOTH )
        fgSizerchartOptions.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        fgSizerchartOptions.AddGrowableCol(1)
        
        self.histogramName = wx.StaticText( self, wx.ID_ANY, u"Histogram Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.histogramName.Wrap( -1 )
        fgSizerchartOptions.Add( self.histogramName, 0, wx.ALIGN_CENTER|wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.histogramNameTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizerchartOptions.Add( self.histogramNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL, 5 )
        
        self.xAxisName = wx.StaticText( self, wx.ID_ANY, u"X Axis Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.xAxisName.Wrap( -1 )
        fgSizerchartOptions.Add( self.xAxisName, 0, wx.ALIGN_CENTER|wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.xAxisNameTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizerchartOptions.Add( self.xAxisNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL, 5 )
        
        self.yAxisName = wx.StaticText( self, wx.ID_ANY, u"Y Axis Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.yAxisName.Wrap( -1 )
        fgSizerchartOptions.Add( self.yAxisName, 0, wx.ALIGN_CENTER|wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.yAxisNameTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizerchartOptions.Add( self.yAxisNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL, 5 ) 
        
        gbSizer1.Add( fgSizerchartOptions, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND | wx.ALL, 5 )

        #Display Grid        
        displayGridsSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Display Grids" ), wx.HORIZONTAL )

        self.xAxischeckBox = wx.CheckBox( self, wx.ID_ANY, "X Axis", wx.DefaultPosition, wx.DefaultSize, 0 )
        displayGridsSizer.Add(self.xAxischeckBox, 0, wx.ALL, 10)
        self.yAxischeckBox = wx.CheckBox( self, wx.ID_ANY, "Y Axis", wx.DefaultPosition, wx.DefaultSize, 0 )
        displayGridsSizer.Add(self.yAxischeckBox, 0, wx.ALL, 10)
        
        gbSizer1.Add( displayGridsSizer, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 20 ) 
                
        #Place the legend of the histogram
        positions = ['Upper Right', 'Upper Left', 'Lower Left', 'Lower Right', 'Right', 'Center Left', 'Center Right',
                     'Lower Center', 'Upper Center', 'Center']
        
        legendPosSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Select the position of the Legend" ), wx.HORIZONTAL )
        
        gbSizer1.Add( legendPosSizer, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 20 )
        
        fgLegendSizer = wx.FlexGridSizer( 0, 4, 0, 0 )
        fgLegendSizer.SetFlexibleDirection( wx.BOTH )
        fgLegendSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        legendPosSizer.Add( fgLegendSizer, 1, wx.EXPAND, 5 )
        
        self.m_radioBtn15 = wx.RadioButton( self, wx.ID_ANY, "By Default", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
        fgLegendSizer.Add( self.m_radioBtn15, 0, wx.ALL, 5 )
        
        self.Bind(wx.EVT_RADIOBUTTON, self.updateLegendPosition, self.m_radioBtn15)
        
        for position in positions:
            
            self.m_radioBtn = wx.RadioButton( self, wx.ID_ANY, position, wx.DefaultPosition, wx.DefaultSize, 0 )
            fgLegendSizer.Add( self.m_radioBtn, 0, wx.ALL, 5 )
        
            self.Bind(wx.EVT_RADIOBUTTON, self.updateLegendPosition, self.m_radioBtn)     
        
        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"X Variables" ), wx.VERTICAL )
        sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Tags" ), wx.VERTICAL )
        
        
        fgSizer3 = wx.FlexGridSizer( 1, 0, 0, 0 )
        fgSizer3.SetFlexibleDirection( wx.BOTH )
        fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        fgSizer5 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer5.SetFlexibleDirection( wx.BOTH )
        fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        #Here the RadioButtons are created       
        for i in listOfVariables:
            
            #First element
            if i == listOfVariables[0]:
                self.m_radioBtn15 = wx.RadioButton( self, wx.ID_ANY, i, wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
                fgSizer5.Add( self.m_radioBtn15, 0, wx.ALL, 5 )
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedVariablesRadioButton, self.m_radioBtn15)
            else:    
                self.m_radioBtn15 = wx.RadioButton( self, wx.ID_ANY, i, wx.DefaultPosition, wx.DefaultSize, 0 )
                fgSizer5.Add( self.m_radioBtn15, 0, wx.ALL, 5 )
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedVariablesRadioButton, self.m_radioBtn15)
        

        fgSizer6 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer6.SetFlexibleDirection( wx.BOTH )
        fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )        
        
        #Not use a label (for example in Level: High, Low)
        self.m_radioBtn16 = wx.RadioButton( self, wx.ID_ANY, "Not use label", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
        fgSizer6.Add( self.m_radioBtn16, 0, wx.ALL, 5 )
        self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedTagsRadioButton, self.m_radioBtn16)
        
        for i in listOfTags:
 
            self.m_radioBtn16 = wx.RadioButton( self, wx.ID_ANY, i, wx.DefaultPosition, wx.DefaultSize, 0 )
            fgSizer6.Add( self.m_radioBtn16, 0, wx.ALL, 5 )
            self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedTagsRadioButton, self.m_radioBtn16)
                
                    
        #As a default the name of the axis are the selected variables
        self.xAxisNameTextCtrl.SetValue(listOfVariables[0])
        self.yAxisNameTextCtrl.SetValue('Not use label')

        sbSizer1.Add( fgSizer5, 1, wx.EXPAND, 5 )
        sbSizer2.Add( fgSizer6, 1, wx.EXPAND, 5 )
        
        fgSizer3.Add( sbSizer1, 1, wx.EXPAND | wx.ALL, 5 )
        fgSizer3.Add( sbSizer2, 1, wx.EXPAND | wx.ALL, 5 )

        gbSizer1.Add( fgSizer3, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.EXPAND|wx.ALL, 5 )       
        
        #Ok and Cancel buttons
        okay = wx.Button( self, wx.ID_OK )
        cancel = wx.Button( self, wx.ID_CANCEL )
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        
        gbSizer1.Add( btns, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND | wx.ALL, 5 )
        
        self.SetSizer( gbSizer1 )
        gbSizer1.Fit(self)
        self.Layout()
        self.Fit()
        self.Centre( wx.BOTH )      
        
       
        #Variable to save the selected radiobutton
        self.selectedRadioButtonVariables = listOfVariables[0]
        self.selectedRadioButtonTags = 'Not use label'
        
        self.Fit()
        self.Show(True)
        
      

    def updateSelectedVariablesRadioButton(self, event):
        
        radioButton = event.GetEventObject()
        
        self.selectedRadioButtonVariables = radioButton.GetLabelText()
        self.xAxisNameTextCtrl.SetValue(radioButton.GetLabelText())
            
    
    def updateSelectedTagsRadioButton(self, event):
        
        radioButton = event.GetEventObject()
        
        self.selectedRadioButtonTags = radioButton.GetLabelText()
        self.yAxisNameTextCtrl.SetValue(radioButton.GetLabelText())


    def chartVariables(self):
        
        return self.selectedRadioButtonVariables, self.selectedRadioButtonTags
    
    
    def getHistogramDescription(self):
        
        return self.histogramNameTextCtrl.GetValue(), self.xAxisNameTextCtrl.GetValue(), self.yAxisNameTextCtrl.GetValue()
    
    
    def updateLegendPosition(self, event):
        
        radioButton = event.GetEventObject()
        
        self.position = radioButton.GetLabelText()
    
    
    def getHistogramOptions(self):
        
        histogramOptions = ChartOptions(self.histogramNameTextCtrl.GetValue(), self.xAxisNameTextCtrl.GetValue(), 
                                      self.yAxisNameTextCtrl.GetValue(), False,self.xAxischeckBox.IsChecked(), 
                                      self.yAxischeckBox.IsChecked(), self.selectedRadioButtonVariables, 
                                      self.selectedRadioButtonTags, self.position, [])
        
        return histogramOptions 




    
class ScatterPlotInterface ( wx.Dialog ):
    
    def __init__( self, parent, listOfVariables):
        
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Variables for the Scatter Plot", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        
        #Scatter Plot Options
        fgSizerchartOptions = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizerchartOptions.SetFlexibleDirection( wx.BOTH )
        fgSizerchartOptions.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        fgSizerchartOptions.AddGrowableCol(1)
        
        self.scatterName = wx.StaticText( self, wx.ID_ANY, u"Scatter Plot Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.scatterName.Wrap( -1 )
        fgSizerchartOptions.Add( self.scatterName, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.scatterNameTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizerchartOptions.Add( self.scatterNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL, 5 )
        
        self.xAxisName = wx.StaticText( self, wx.ID_ANY, u"X Axis Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.xAxisName.Wrap( -1 )
        fgSizerchartOptions.Add( self.xAxisName, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.xAxisNameTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizerchartOptions.Add( self.xAxisNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL, 5 )
        
        
        self.yAxisName = wx.StaticText( self, wx.ID_ANY, u"Y Axis Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.yAxisName.Wrap( -1 )
        fgSizerchartOptions.Add( self.yAxisName, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.yAxisNameTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizerchartOptions.Add( self.yAxisNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL, 5 ) 
        
        gbSizer1.Add( fgSizerchartOptions, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND | wx.ALL, 5 )
        
        #Grid        
        displayGridsSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Display Grids" ), wx.HORIZONTAL )
        
        self.xAxischeckBox = wx.CheckBox( self, wx.ID_ANY, "X Axis", wx.DefaultPosition, wx.DefaultSize, 0 )
        displayGridsSizer.Add(self.xAxischeckBox, 0, wx.ALL, 10)
        self.yAxischeckBox = wx.CheckBox( self, wx.ID_ANY, "Y Axis", wx.DefaultPosition, wx.DefaultSize, 0 )
        displayGridsSizer.Add(self.yAxischeckBox, 0, wx.ALL, 10)
        
        gbSizer1.Add( displayGridsSizer, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 20 ) 

        #Variables
        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"X Variables" ), wx.VERTICAL )
        sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Y Variables" ), wx.VERTICAL )
        
        
        fgSizer3 = wx.FlexGridSizer( 1, 0, 0, 0 )
        fgSizer3.SetFlexibleDirection( wx.BOTH )
        fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        fgSizer5 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer5.SetFlexibleDirection( wx.BOTH )
        fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        
        #Here the RadioButtons are created
        for i in listOfVariables:
            
            #First element
            if i == listOfVariables[0]:
                self.m_radioBtn15 = wx.RadioButton( self, wx.ID_ANY, i, wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
                fgSizer5.Add( self.m_radioBtn15, 0, wx.ALL, 5 )
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedVariablesRadioButton, self.m_radioBtn15)
            else:    
                self.m_radioBtn15 = wx.RadioButton( self, wx.ID_ANY, i, wx.DefaultPosition, wx.DefaultSize, 0 )
                fgSizer5.Add( self.m_radioBtn15, 0, wx.ALL, 5 )
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedVariablesRadioButton, self.m_radioBtn15)
        
 
        fgSizer6 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer6.SetFlexibleDirection( wx.BOTH )
        fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )        
        
        for i in listOfVariables:
            
            #First element
            if i == listOfVariables[0]:
            
                self.m_radioBtn16 = wx.RadioButton( self, wx.ID_ANY, i, wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
                fgSizer6.Add( self.m_radioBtn16, 0, wx.ALL, 5 )
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedTagsRadioButton, self.m_radioBtn16)
            
            else:
                self.m_radioBtn16 = wx.RadioButton( self, wx.ID_ANY, i, wx.DefaultPosition, wx.DefaultSize, 0 )
                fgSizer6.Add( self.m_radioBtn16, 0, wx.ALL, 5 )
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedTagsRadioButton, self.m_radioBtn16)

        #The name of the axis by default
        self.xAxisNameTextCtrl.SetValue(listOfVariables[0])
        self.yAxisNameTextCtrl.SetValue(listOfVariables[0])
        
        sbSizer1.Add( fgSizer5, 1, wx.EXPAND, 5 )
        sbSizer2.Add( fgSizer6, 1, wx.EXPAND, 5 )
        
        fgSizer3.Add( sbSizer1, 1, wx.EXPAND | wx.ALL, 5 )
        fgSizer3.Add( sbSizer2, 1, wx.EXPAND | wx.ALL, 5 )

        gbSizer1.Add( fgSizer3, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.EXPAND|wx.ALL, 5 )       
    
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
       
        #Radiobutton selected a the beginning
        self.selectedRadioButtonVariables = listOfVariables[0]
        self.selectedRadioButtonTags = listOfVariables[0]
        
        self.Fit()
        self.Show(True)        
      
        
    def updateSelectedVariablesRadioButton(self, event):
        
        radioButton = event.GetEventObject()
        
        self.selectedRadioButtonVariables = radioButton.GetLabelText()
        self.xAxisNameTextCtrl.SetValue(radioButton.GetLabelText())
            
    
    def updateSelectedTagsRadioButton(self, event):
        
        radioButton = event.GetEventObject()
        
        self.selectedRadioButtonTags = radioButton.GetLabelText()
        self.yAxisNameTextCtrl.SetValue(radioButton.GetLabelText())
        
    def chartVariables(self):
        
        return self.selectedRadioButtonVariables, self.selectedRadioButtonTags
    
    def getScatterPlotDescription(self):
        
        return self.scatterNameTextCtrl.GetValue(), self.xAxisNameTextCtrl.GetValue(), self.yAxisNameTextCtrl.GetValue()
    
    def getScatterPlotOptions(self):
        
        scatterOptions = ChartOptions(self.scatterNameTextCtrl.GetValue(), self.xAxisNameTextCtrl.GetValue(), 
                                      self.yAxisNameTextCtrl.GetValue(), False, self.xAxischeckBox.IsChecked(), 
                                      self.yAxischeckBox.IsChecked(), self.selectedRadioButtonVariables, 
                                      self.selectedRadioButtonTags, '', [])
        
        return scatterOptions
    
    
    
    
class PieChartInterface ( wx.Dialog ):
    
    
    position = 'by default'
    
    def __init__( self, parent, listOfTags ):
        
        
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Chart", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        
        #Pie Chart Options
        fgSizerchartOptions = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizerchartOptions.SetFlexibleDirection( wx.BOTH )
        fgSizerchartOptions.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        fgSizerchartOptions.AddGrowableCol(1)
        
        
        self.histogramName = wx.StaticText( self, wx.ID_ANY, u"Pie Chart Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.histogramName.Wrap( -1 )
        fgSizerchartOptions.Add( self.histogramName, 0, wx.ALIGN_CENTER|wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.histogramNameTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizerchartOptions.Add( self.histogramNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL, 5 )
        

        gbSizer1.Add( fgSizerchartOptions, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND | wx.ALL, 5 )
        
                
        #To place the legend, all positions
        positions = ['Upper Right', 'Upper Left', 'Lower Left', 'Lower Right', 'Right', 'Center Left', 'Center Right',
                     'Lower Center', 'Upper Center', 'Center']
        
        legendPosSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Select the position of the Legend" ), wx.HORIZONTAL )
        
        gbSizer1.Add( legendPosSizer, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 20 )
        
        fgLegendSizer = wx.FlexGridSizer( 0, 4, 0, 0 )
        fgLegendSizer.SetFlexibleDirection( wx.BOTH )
        fgLegendSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        legendPosSizer.Add( fgLegendSizer, 1, wx.EXPAND, 5 )
        
        self.m_radioBtn15 = wx.RadioButton( self, wx.ID_ANY, "By Default", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
        fgLegendSizer.Add( self.m_radioBtn15, 0, wx.ALL, 5 )
        
        self.Bind(wx.EVT_RADIOBUTTON, self.updateLegendPosition, self.m_radioBtn15)
        
        for position in positions:
            
            self.m_radioBtn = wx.RadioButton( self, wx.ID_ANY, position, wx.DefaultPosition, wx.DefaultSize, 0 )
            fgLegendSizer.Add( self.m_radioBtn, 0, wx.ALL, 5 )
        
            self.Bind(wx.EVT_RADIOBUTTON, self.updateLegendPosition, self.m_radioBtn)
                
        
        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Descriptive Variables" ), wx.VERTICAL )
        
        fgSizer3 = wx.FlexGridSizer( 1, 0, 0, 0 )
        fgSizer3.SetFlexibleDirection( wx.BOTH )
        fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        fgSizer5 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer5.SetFlexibleDirection( wx.BOTH )
        fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        

        #Here the RadioButtons are created
        for i in listOfTags:
            
            #First one
            if i == listOfTags[0]:
                self.m_radioBtn15 = wx.RadioButton( self, wx.ID_ANY, i, wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
                fgSizer5.Add( self.m_radioBtn15, 0, wx.ALL, 5 )
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedVariablesRadioButton, self.m_radioBtn15)
            else:    
                self.m_radioBtn15 = wx.RadioButton( self, wx.ID_ANY, i, wx.DefaultPosition, wx.DefaultSize, 0 )
                fgSizer5.Add( self.m_radioBtn15, 0, wx.ALL, 5 )
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedVariablesRadioButton, self.m_radioBtn15)
        
        
        sbSizer1.Add( fgSizer5, 1, wx.EXPAND, 5 )
        
        fgSizer3.Add( sbSizer1, 1, wx.EXPAND | wx.ALL, 5 )

        
        gbSizer1.Add( fgSizer3, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.EXPAND|wx.ALL, 5 )       
    

        #Buttons OK and Cancel
        okay = wx.Button( self, wx.ID_OK )
        cancel = wx.Button( self, wx.ID_CANCEL )
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        
        gbSizer1.Add( btns, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND | wx.ALL, 5 )     
    
        
        self.SetSizer( gbSizer1 )
        gbSizer1.Fit(self)
        self.Layout()
        self.Fit()
        self.Centre( wx.BOTH )
        
        #RadioButton selected by default
        self.selectedRadioButtonTags = listOfTags[0]
        
        
        self.Fit()
        self.Show(True)
        
      
        
    def updateSelectedVariablesRadioButton(self, event):
        
        radioButton = event.GetEventObject()
        
        self.selectedRadioButtonTags = radioButton.GetLabelText()

        
    def chartVariables(self):
        
        return self.selectedRadioButtonVariables, self.selectedRadioButtonTags

    
    
    def updateLegendPosition(self, event):
        
        radioButton = event.GetEventObject()
        
        self.position = radioButton.GetLabelText()
    
    
    def getPieChartOptions(self):
        
        histogramOptions = ChartOptions(self.histogramNameTextCtrl.GetValue(), '', '', False, False, False, self.selectedRadioButtonTags, 
                                        None, self.position, [])
        
        return histogramOptions
    
    
    
class BoxPlotInterface ( wx.Dialog ):
    
    position = 'by default'
    
    def __init__( self, parent, listOfVariables, listOfCharacterValues ):
        
        
        self.selectedCheckBoxes = []
        
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Chart", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        
        #Box PLot Options        
        fgSizerchartOptions = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizerchartOptions.SetFlexibleDirection( wx.BOTH )
        fgSizerchartOptions.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        fgSizerchartOptions.AddGrowableCol(1)
        
        
        self.histogramName = wx.StaticText( self, wx.ID_ANY, u"Box Plot Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.histogramName.Wrap( -1 )
        fgSizerchartOptions.Add( self.histogramName, 0, wx.ALIGN_CENTER|wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.histogramNameTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizerchartOptions.Add( self.histogramNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL, 5 )
        
    
        gbSizer1.Add( fgSizerchartOptions, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND | wx.ALL, 5 )        
        
        
        #Grid
        displayGridsSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Display Grids" ), wx.HORIZONTAL )

        
        self.showGridRadioButton = wx.RadioButton( self, wx.ID_ANY, "Show Grid", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
        displayGridsSizer.Add(self.showGridRadioButton, 0, wx.ALL, 10)
        self.Bind(wx.EVT_RADIOBUTTON, self.updateShowGrid, self.showGridRadioButton)
        
        self.hideGridRadioButton = wx.RadioButton( self, wx.ID_ANY, "Hide Grid", wx.DefaultPosition, wx.DefaultSize )
        displayGridsSizer.Add(self.hideGridRadioButton, 0, wx.ALL, 10)
        self.Bind(wx.EVT_RADIOBUTTON, self.updateShowGrid, self.hideGridRadioButton)
        
        # By Default, grid is shown
        self.showGrid = True
 
        gbSizer1.Add( displayGridsSizer, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 20 )
        
        
        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Descriptive Variables" ), wx.VERTICAL )
        
        fgSizer3 = wx.FlexGridSizer( 1, 0, 0, 0 )
        fgSizer3.SetFlexibleDirection( wx.BOTH )
        fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        fgSizer5 = wx.FlexGridSizer( 0, 3, 0, 0 )
        fgSizer5.SetFlexibleDirection( wx.BOTH )
        fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        
        
        #Here the RadioButtons are created
        for i in listOfVariables:
            
            self.m_checkBox = wx.CheckBox( self, wx.ID_ANY, str(i), wx.DefaultPosition, wx.DefaultSize, 0 )
            fgSizer5.Add( self.m_checkBox, 0, wx.ALL| wx.EXPAND, 5 )
            
            self.Bind(wx.EVT_CHECKBOX, self.updateSelectedCheckBoxes,self.m_checkBox)
        

        sbSizer1.Add( fgSizer5, 1, wx.EXPAND, 5 )
        
        fgSizer3.Add( sbSizer1, 1, wx.EXPAND | wx.ALL, 5 )

        
        gbSizer1.Add( fgSizer3, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.EXPAND|wx.ALL, 5 )
        
        #Group By
        legendPosSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Group by:" ), wx.HORIZONTAL )
        
        gbSizer1.Add( legendPosSizer, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 20 )
        
        fgLegendSizer = wx.FlexGridSizer( 0, 3, 0, 0 )
        fgLegendSizer.SetFlexibleDirection( wx.BOTH )
        fgLegendSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        legendPosSizer.Add( fgLegendSizer, 1, wx.EXPAND, 5 )
        
        self.m_radioBtn15 = wx.RadioButton( self, wx.ID_ANY, "None", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
        fgLegendSizer.Add( self.m_radioBtn15, 0, wx.ALL, 5 )
        
        self.Bind(wx.EVT_RADIOBUTTON, self.updateGroupByOption, self.m_radioBtn15)
        
        #Variable to group BoxPlot
        self.groupByOption = 'None'
        
        for value in listOfCharacterValues:
            
            self.m_radioBtn = wx.RadioButton( self, wx.ID_ANY, value, wx.DefaultPosition, wx.DefaultSize, 0 )
            fgLegendSizer.Add( self.m_radioBtn, 0, wx.ALL, 5 )
        
            self.Bind(wx.EVT_RADIOBUTTON, self.updateGroupByOption, self.m_radioBtn)
 
        
        #Buttons OK and Cancel
        okay = wx.Button( self, wx.ID_OK, validator = ValidatorForFactors(self.selectedCheckBoxes) )
        cancel = wx.Button( self, wx.ID_CANCEL )
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        
        
        gbSizer1.Add( btns, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND | wx.ALL, 5 )      
        
        self.SetSizer( gbSizer1 )
        gbSizer1.Fit(self)
        self.Layout()
        self.Fit()
        self.Centre( wx.BOTH )
        
        self.Fit()
        self.Show(True)
        
      
        
    def updateSelectedVariablesRadioButton(self, event):
        
        radioButton = event.GetEventObject()
        
        self.selectedRadioButtonTags = radioButton.GetLabelText()
        
        
    def updateGroupByOption(self, event):
        
        radioButton = event.GetEventObject()
        
        self.groupByOption = radioButton.GetLabelText()
    
    def updateSelectedCheckBoxes(self, event):
        
        checkBox = event.GetEventObject()
        
        
        if checkBox.IsChecked():
            
            self.selectedCheckBoxes.append(checkBox.GetLabel().encode("utf-8"))
                        
        else:
            
            self.selectedCheckBoxes.remove(checkBox.GetLabel().encode("utf-8"))
        
    def updateShowGrid(self, event):
        
        radioButton = event.GetEventObject()
        
        if radioButton.GetLabelText() == "Show Grid":
            
            self.showGrid = True
        
        else:
            
            self.showGrid = False 
        
        
    def chartVariables(self):
        
        return self.selectedRadioButtonVariables, self.selectedRadioButtonTags

    
    
    def updateLegendPosition(self, event):
        
        radioButton = event.GetEventObject()
        
        self.position = radioButton.GetLabelText()
    
    
    def getBoxPlotOptions(self):
        
        boxPlotOptions = ChartOptions(self.histogramNameTextCtrl.GetValue(), '', '', self.showGrid, False, False, None, 
                                        self.groupByOption, self.position, self.selectedCheckBoxes)
        
        return boxPlotOptions
    
    

                        
class BarChartInterface ( wx.Dialog ): 
    
    position = 'by default'
    
    def __init__( self, parent, listOfVariables, listOfTags ):
        
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Chart", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        

        #BarChart options
        fgSizerchartOptions = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizerchartOptions.SetFlexibleDirection( wx.BOTH )
        fgSizerchartOptions.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        fgSizerchartOptions.AddGrowableCol(1)
        
        self.histogramName = wx.StaticText( self, wx.ID_ANY, u"Chart Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.histogramName.Wrap( -1 )
        fgSizerchartOptions.Add( self.histogramName, 0, wx.ALIGN_CENTER|wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.histogramNameTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizerchartOptions.Add( self.histogramNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL, 5 )
        
        self.xAxisName = wx.StaticText( self, wx.ID_ANY, u"X Axis Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.xAxisName.Wrap( -1 )
        fgSizerchartOptions.Add( self.xAxisName, 0, wx.ALIGN_CENTER|wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.xAxisNameTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizerchartOptions.Add( self.xAxisNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL, 5 )
        
        self.yAxisName = wx.StaticText( self, wx.ID_ANY, u"Y Axis Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.yAxisName.Wrap( -1 )
        fgSizerchartOptions.Add( self.yAxisName, 0, wx.ALIGN_CENTER|wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.yAxisNameTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizerchartOptions.Add( self.yAxisNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL, 5 ) 
        
        gbSizer1.Add( fgSizerchartOptions, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND | wx.ALL, 5 )

        #Display Grid        
        displayGridsSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Display Grids" ), wx.HORIZONTAL )

        self.xAxischeckBox = wx.CheckBox( self, wx.ID_ANY, "X Axis", wx.DefaultPosition, wx.DefaultSize, 0 )
        displayGridsSizer.Add(self.xAxischeckBox, 0, wx.ALL, 10)
        self.yAxischeckBox = wx.CheckBox( self, wx.ID_ANY, "Y Axis", wx.DefaultPosition, wx.DefaultSize, 0 )
        displayGridsSizer.Add(self.yAxischeckBox, 0, wx.ALL, 10)

        
        gbSizer1.Add( displayGridsSizer, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 20 ) 

        #Variables, tags and operations Options
        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"X Variables" ), wx.VERTICAL )
        sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Tags" ), wx.VERTICAL )
        sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Operations" ), wx.VERTICAL )
        
        
        fgSizer3 = wx.FlexGridSizer( 1, 0, 0, 0 )
        fgSizer3.SetFlexibleDirection( wx.BOTH )
        fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        fgSizer5 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer5.SetFlexibleDirection( wx.BOTH )
        fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        #Here the RadioButtons are created       
        for i in listOfVariables:
            
            #First element
            if i == listOfVariables[0]:
                self.m_radioBtn15 = wx.RadioButton( self, wx.ID_ANY, i, wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
                fgSizer5.Add( self.m_radioBtn15, 0, wx.ALL, 5 )
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedVariablesRadioButton, self.m_radioBtn15)
            else:    
                self.m_radioBtn15 = wx.RadioButton( self, wx.ID_ANY, i, wx.DefaultPosition, wx.DefaultSize, 0 )
                fgSizer5.Add( self.m_radioBtn15, 0, wx.ALL, 5 )
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedVariablesRadioButton, self.m_radioBtn15)
        

        fgSizer6 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer6.SetFlexibleDirection( wx.BOTH )
        fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )        
        
        
        #Not use a label (for example in Level: High, Low)
        self.m_radioBtn16 = wx.RadioButton( self, wx.ID_ANY, "None", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
        fgSizer6.Add( self.m_radioBtn16, 0, wx.ALL, 5 )
        self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedTagsRadioButton, self.m_radioBtn16)
        
        for i in listOfTags:
           
            self.m_radioBtn16 = wx.RadioButton( self, wx.ID_ANY, i, wx.DefaultPosition, wx.DefaultSize, 0 )
            fgSizer6.Add( self.m_radioBtn16, 0, wx.ALL, 5 )
            self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedTagsRadioButton, self.m_radioBtn16)
                
       
                
        #As a default the name of the axis are the selected variables
        self.xAxisNameTextCtrl.SetValue(listOfVariables[0])
        self.yAxisNameTextCtrl.SetValue('None')
        
        
        listOperations = ['Mean', 'Median', 'Std Deviation', 'Variance']
        #By default, Mean selected
        self.selectedOperation = str(listOperations[0])
        
        
        fgSizer7 = wx.FlexGridSizer( 1,0 , 0, 0 )
        fgSizer7.SetFlexibleDirection( wx.BOTH )
        fgSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )        
        
        for i in listOperations:
            #First
            if i == listOperations[0]:
            
                self.m_radioBtn16 = wx.RadioButton( self, wx.ID_ANY, i, wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
                fgSizer7.Add( self.m_radioBtn16, 0, wx.ALL, 5 )
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedOperationRadioButton, self.m_radioBtn16)
            
            else:
                self.m_radioBtn16 = wx.RadioButton( self, wx.ID_ANY, i, wx.DefaultPosition, wx.DefaultSize, 0 )
                fgSizer7.Add( self.m_radioBtn16, 0, wx.ALL, 5 )
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedOperationRadioButton, self.m_radioBtn16)
                
        
        sbSizer1.Add( fgSizer5, 1, wx.EXPAND, 5 )
        sbSizer2.Add( fgSizer6, 1, wx.EXPAND, 5 )
        sbSizer3.Add( fgSizer7, 1, wx.EXPAND, 5 )
        
        fgSizer3.Add( sbSizer1, 1, wx.EXPAND | wx.ALL, 5 )
        fgSizer3.Add( sbSizer2, 1, wx.EXPAND | wx.ALL, 5 )

        gbSizer1.Add( fgSizer3, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.EXPAND|wx.ALL, 5 )
        gbSizer1.Add( sbSizer3, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )        
        
        #Ok and Cancel buttons
        okay = wx.Button( self, wx.ID_OK )
        cancel = wx.Button( self, wx.ID_CANCEL )
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        
        gbSizer1.Add( btns, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND | wx.ALL, 5 )
        
        self.SetSizer( gbSizer1 )
        gbSizer1.Fit(self)
        self.Layout()
        self.Fit()
        self.Centre( wx.BOTH )      
        
        #Variable to save the selected radiobutton
        self.selectedRadioButtonVariables = listOfVariables[0]
        self.selectedRadioButtonTags = 'None'
        
        self.Fit()
        self.Show(True)
        
      

    def updateSelectedVariablesRadioButton(self, event):
        
        radioButton = event.GetEventObject()
        
        self.selectedRadioButtonVariables = radioButton.GetLabelText()
        self.xAxisNameTextCtrl.SetValue(radioButton.GetLabelText())
            
    
    def updateSelectedTagsRadioButton(self, event):
        
        radioButton = event.GetEventObject()
        
        self.selectedRadioButtonTags = radioButton.GetLabelText()
        self.yAxisNameTextCtrl.SetValue(radioButton.GetLabelText())

    def updateSelectedOperationRadioButton(self, event):
        
        radioButton = event.GetEventObject()
        self.selectedOperation = radioButton.GetLabelText()
        

        
    def chartVariables(self):
        
        return self.selectedRadioButtonVariables, self.selectedRadioButtonTags
    
    
    def getBarChartDescription(self):
        
        return self.histogramNameTextCtrl.GetValue(), self.xAxisNameTextCtrl.GetValue(), self.yAxisNameTextCtrl.GetValue()
    
    
    def updateLegendPosition(self, event):
        
        radioButton = event.GetEventObject()
        
        self.position = radioButton.GetLabelText()
    
    
    def getBarChartOptions(self):
        
        histogramOptions = ChartOptions(self.histogramNameTextCtrl.GetValue(), self.xAxisNameTextCtrl.GetValue(), 
                                      self.yAxisNameTextCtrl.GetValue(), False,self.xAxischeckBox.IsChecked(), 
                                      self.yAxischeckBox.IsChecked(), self.selectedRadioButtonVariables, 
                                      self.selectedRadioButtonTags, self.position, [])
        
        return histogramOptions 

    def getSelectedOperation(self):
        
        return self.selectedOperation




class ValidatorForFactors(wx.PyValidator):
    
    def __init__(self, selectedCheckBoxes):
        
        wx.PyValidator.__init__(self)
        self.selectedCheckBoxes = selectedCheckBoxes

    def Clone(self):
        return ValidatorForFactors(self.selectedCheckBoxes)
    
    def Validate(self, win):
        
        if not self.selectedCheckBoxes:
            
            wx.MessageBox("Please, select unless one checkBox", "Attention!", wx.OK | wx.ICON_EXCLAMATION)
            return False
            
        else:
            return True
        
    def TransferToWindow(self):
        
        return True
    
    def TransferFromWindow(self):
        return True
    
    
    def noCheckBoxSelectedWarning(self):
        
        dlg = wx.MessageDialog(self, "Please, select unless one checkBox", "Attention!", wx.OK | wx.ICON_EXCLAMATION)

        if dlg.ShowModal() == wx.ID_OK:
            
            dlg.Destroy()
        else:
            
            dlg.Destroy()
