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
import wx.richtext as rt
import wx.lib.scrolledpanel 

from pandas.core.config import set_option
from pandas.core.frame import DataFrame
#To modify how to show the Dataframe's data
set_option('expand_frame_repr', False)


class BasicStatisticsInterface ( wx.Dialog ):
    
    def __init__( self, parent, namesCheckBox,  tagsAndValues, integerValues, dataFrame ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Basic statistics", pos = wx.DefaultPosition, size =(1200, 600))
        
        self.dataToAnalyse = dataFrame
        
        #Inicialización de las listas necesarias para obtener las opciones elegidas por el usuario
        #self.listOfCheckBoxes = []
        
        #self.checkBoxStatus = {}
    
        self.listOfSpinCtrl = []
        
        self.intervalNameAndLimitsLeft = {}
    
        self.activatedCheckBoxes = []
    
        #self.checkBoxTagLeft = []
        
        self.selectedCheckBoxes = []
        
        self.selectedVariablesInColumn = dict.fromkeys(tagsAndValues.keys())
        
        #The values of each key in the dictionary are initialized as an empty list
        for key in self.selectedVariablesInColumn.keys():
            
            self.selectedVariablesInColumn[key] = []
        
        self.integerValues = integerValues
        
        
        #Panel for all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)
        
        #Definition of the scrolled panel
        self.scrolledPanel = wx.lib.scrolledpanel.ScrolledPanel(self.panel, -1, style = wx.TAB_TRAVERSAL)
 
        self.scrolledPanel.SetAutoLayout(1)
        self.scrolledPanel.SetupScrolling()
        
        self.scrollSizer = wx.BoxSizer(wx.HORIZONTAL)

        dataSelectionSizer = wx.StaticBoxSizer( wx.StaticBox( self.scrolledPanel, wx.ID_ANY, u"Data selection" ), wx.VERTICAL )
        
        self.scrollSizer.Add( dataSelectionSizer, 1, wx.EXPAND | wx.ALL, 10 )
        
        fgSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer.SetFlexibleDirection( wx.BOTH )
        fgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        dataSelectionSizer.Add(fgSizer, 1, wx.ALL | wx.EXPAND, 5)
        
        #Definition of the Sizer where the checkBoxes will be created
        checkSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
        checkSizer.SetFlexibleDirection( wx.BOTH )
        checkSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        fgSizer.Add( checkSizer, 0,  wx.ALL| wx.EXPAND, 5)
 
        for i in namesCheckBox:
        
            self.m_checkBox = wx.CheckBox( self.scrolledPanel, wx.ID_ANY, str(i), wx.DefaultPosition, wx.DefaultSize, 0 )
            checkSizer.Add( self.m_checkBox, 0, wx.ALL| wx.EXPAND, 5 )
            #self.listOfCheckBoxes.append(self.m_checkBox)
            
            self.Bind(wx.EVT_CHECKBOX, self.changeValueCheckBox,self.m_checkBox)
        

        tagsSizer = wx.FlexGridSizer( 0, 1, 0, 0 )
        tagsSizer.SetFlexibleDirection( wx.BOTH )
        tagsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        fgSizer.Add( tagsSizer, 1, wx.ALL| wx.EXPAND, 5 )
        
        for tag, values in tagsAndValues.iteritems():
            
            #self.checkBoxTagLeft.append(SelectedValuesOfTag(tag, values))
            
            sbSizer = wx.StaticBoxSizer( wx.StaticBox( self.scrolledPanel, wx.ID_ANY, str(tag) ), wx.VERTICAL )
            
            for j in values:
                
                self.m_checkBox = wx.CheckBox(parent = self.scrolledPanel, id = wx.ID_ANY, label = str(j), pos = wx.DefaultPosition, size = wx.DefaultSize, name = str(tag) )
                sbSizer.Add( self.m_checkBox, 0, wx.EXPAND, 5 )
                self.Bind(wx.EVT_CHECKBOX, self.changeValueTagCheckBox, self.m_checkBox)
                
                
            tagsSizer.Add( sbSizer, 0, wx.EXPAND | wx.ALL, 5 )
        

        #INTEGER VALUES
        if integerValues:
            
            #Definition of the Sizer where the checkBoxes will be created
            auxSizer2 = wx.FlexGridSizer( 0, 5, 0, 0 )
            auxSizer2.SetFlexibleDirection( wx.BOTH )
            auxSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
            fgSizer.Add( auxSizer2, 0,  wx.ALL| wx.EXPAND, 5)
            
            for i in integerValues:
                minumum = int(min(self.dataToAnalyse[i]))
                maximum = int(max(self.dataToAnalyse[i]))

                self.m_checkBox = wx.CheckBox( self.scrolledPanel, wx.ID_ANY, str(i), wx.DefaultPosition, wx.DefaultSize, 0 )
                self.m_checkBox.SetFont( wx.Font( 10, wx.DEFAULT, wx.NORMAL, wx.BOLD, False, wx.EmptyString ) )
                self.Bind(wx.EVT_CHECKBOX, self.changeStatusSpinCtrl, self.m_checkBox)
                
                auxSizer2.Add( self.m_checkBox, 0,wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

            
                self.m_staticText11 = wx.StaticText( self.scrolledPanel, wx.ID_ANY, u"From:", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.m_staticText11.Wrap( -1 )
                auxSizer2.Add( self.m_staticText11, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, 5 )

                self.m_spinCtrl11 = wx.SpinCtrlDouble( self.scrolledPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), wx.SP_ARROW_KEYS | wx.ALIGN_RIGHT, minumum, maximum, minumum,1, str(i) + "-LimitInf")
            
                # self.m_spinCtrl11 = wx.SpinCtrl( self.scrolledPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 65,-1 ), wx.SP_ARROW_KEYS, minumum, maximum, minumum, str(i) + "-LimitInf")
                auxSizer2.Add( self.m_spinCtrl11, 0, wx.ALL, 5 )
                self.m_spinCtrl11.Enable(False)
            
                self.m_staticText21 = wx.StaticText( self.scrolledPanel, wx.ID_ANY, u"To:", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.m_staticText21.Wrap( -1 )
                auxSizer2.Add( self.m_staticText21, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, 5 )
            
                self.m_spinCtrl21 = wx.SpinCtrlDouble( self.scrolledPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), wx.SP_ARROW_KEYS| wx.ALIGN_RIGHT, minumum, maximum, maximum, 1, str(i) + "-LimitSup")
                auxSizer2.Add( self.m_spinCtrl21, 0, wx.ALL, 5 )
                self.m_spinCtrl21.Enable(False) 
                
                self.listOfSpinCtrl.append(self.m_spinCtrl11)
                self.listOfSpinCtrl.append(self.m_spinCtrl21)
        
        
        self.m_textCtrl1 = rt.RichTextCtrl( self.scrolledPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.VSCROLL | wx.HSCROLL | wx.TE_MULTILINE | wx.TE_READONLY | wx.NO_BORDER)
        self.m_textCtrl1.SetMargins((20,20))
        
        self.scrollSizer.Add( self.m_textCtrl1, 1, wx.EXPAND | wx.ALL, 10 )
        
        self.scrolledPanel.SetSizer(self.scrollSizer)
       
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(self.scrolledPanel, 1, wx.EXPAND)
        
        close = wx.Button( self.panel, wx.ID_CANCEL, label = "Cancel" )
        showResults = wx.Button( self.panel, wx.ID_ANY, label = "Show results" )
        self.Bind(wx.EVT_BUTTON, self.calculateData, showResults)
        sizerBtns = wx.BoxSizer(wx.HORIZONTAL)
        sizerBtns.Add( showResults, 1, wx.EXPAND | wx.ALL, 5 )
        sizerBtns.Add( close, 1, wx.EXPAND | wx.ALL, 5 )
        panelSizer.Add(sizerBtns, 0 , wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
       
        self.panel.SetSizer(panelSizer)
        self.Centre( wx.BOTH )
        self.Show(True)



    
    def changeStatusSpinCtrl(self, event):
        
        checkBox = event.GetEventObject()

        if checkBox.IsChecked():
            
            self.activatedCheckBoxes.append(checkBox.GetLabel().encode("utf-8"))
            
            i = 0
            
            while checkBox.GetLabel().encode("utf-8") != self.listOfSpinCtrl[i].GetName().split("-")[0].encode("utf-8"):
    
                i = i+1
             
             
            if checkBox.GetLabel().encode("utf-8") == self.listOfSpinCtrl[i].GetName().split("-")[0].encode("utf-8"):
                
                self.listOfSpinCtrl[i].Enable()
                self.listOfSpinCtrl[i + 1].Enable()
                        
        else:
            
            self.activatedCheckBoxes.remove(checkBox.GetLabel().encode("utf-8"))
            
            i = 0
            
            while checkBox.GetLabel().encode("utf-8") != self.listOfSpinCtrl[i].GetName().split("-")[0].encode("utf-8"):
    
                i = i+1
            
            if checkBox.GetLabel().encode("utf-8") == self.listOfSpinCtrl[i].GetName().split("-")[0].encode("utf-8"):
                
                self.listOfSpinCtrl[i].Enable(False)
                self.listOfSpinCtrl[i + 1].Enable(False)
                
                #self.listIntervalNameAndLimits.pop(i)



    def changeValueCheckBox(self, event):   
        
        checkBox = event.GetEventObject()
        
        
        if checkBox.IsChecked():
            
            self.selectedCheckBoxes.append(checkBox.GetLabel().encode("utf-8"))
                        
        else:
            
            self.selectedCheckBoxes.remove(checkBox.GetLabel().encode("utf-8"))


    
    def changeValueTagCheckBox(self, event):
        
        checkBox = event.GetEventObject()
        
        label = checkBox.GetLabel().encode("utf-8")
        nameCheckBox = checkBox.GetName().encode("utf-8")       
                
        if checkBox.IsChecked():
            
            self.selectedVariablesInColumn[nameCheckBox].append(label)
                        
        else:
            
            self.selectedVariablesInColumn[nameCheckBox].remove(label)


         
    def getSelectedData(self):
        
        self.intervalNameAndLimitsLeft.clear()
        # Obtain values from spinctrl to check them

        for checkBox in self.activatedCheckBoxes:
            i = 0
            
            while checkBox != self.listOfSpinCtrl[i].GetName().split("-")[0].encode("utf-8"):
                i = i+1
            
            if checkBox == self.listOfSpinCtrl[i].GetName().split("-")[0].encode("utf-8"):
                limitInf = self.listOfSpinCtrl[i].GetValue()
                limitSup = self.listOfSpinCtrl[i + 1].GetValue()
                self.intervalNameAndLimitsLeft[checkBox] = [limitInf, limitSup]
        
        self.wrongInterval = False
        
        for nameVariable, paarList in self.intervalNameAndLimitsLeft.iteritems():
            if paarList[0] > paarList[1]:
                self.wrongInterval = True 
        
        if not self.selectedCheckBoxes:
            self.noCheckBoxSelectedWarning()
            return DataFrame()
        
        elif self.wrongInterval:
            self.wrongIntervalWarning()
            return DataFrame()
            
        else: # Everything is Ok
            tempList = []
            
            # Lista de listas
            indices = []
            indicesToReturn = []
    
            for i in self.selectedVariablesInColumn.values():
                tempList.extend(i) 

            # tempList contains the marked discrete variables
            
            if not tempList:
                
                auxIndex1 = list(self.dataToAnalyse.index)
                indices.append(auxIndex1)
            
                if self.intervalNameAndLimitsLeft:
                    for nameVariable, paarList in self.intervalNameAndLimitsLeft.iteritems():
                        
                        auxIndex = []
                        #if -1 not in paarList:
                        for i in range(len(self.dataToAnalyse.index)):
                            if ( (self.dataToAnalyse.loc[i,nameVariable] >= paarList[0])
                                 and (self.dataToAnalyse.loc[i,nameVariable] <= paarList[1])):
                                auxIndex.append(i)
                        indices.append(auxIndex)
                        #del auxIndex[:]
                
                #se crea una única lista en la que se concatenan las obtenidas anteriormente
                auxIndices2 = []
    
                for i in range(len(indices)):
                    auxIndices2.extend(indices[i])
                
                for i in range(len(indices[0])):
                    if auxIndices2.count(indices[0][i]) == len(indices):# Si es igual a esto quiere decir que cumple todas las condiciones seleccionadas en la interfaz gráfica 
                        indicesToReturn.append(indices[0][i])
            
            else: # tempList (marked discrete variables) is not empty

                auxIndex1 = []
               
                for name, value in self.selectedVariablesInColumn.items():

                    if value:
                        tagsColumn = self.dataToAnalyse[name]
                        auxIndex1 = [x for x in range(len(tagsColumn)) if tagsColumn[x] in value ]
                        indices.append(auxIndex1)
                    
                    # if value:
                    #     auxIndex1 = []
                    #     for i in range(len(self.dataToAnalyse.index)):
                            
                    #         if (self.dataToAnalyse.loc[i+1,name] in value):
                            
                    #             auxIndex1.append(i+1)
                              
                    #     indices.append(auxIndex1)

                
                if self.intervalNameAndLimitsLeft:
                    for nameVariable, paarList in self.intervalNameAndLimitsLeft.iteritems():
                        
                        auxIndex = []
                        #if -1 not in paarList:
                        
                        for i in range(len(self.dataToAnalyse.index)):
                            
                            if ( (self.dataToAnalyse.loc[i,nameVariable] >= paarList[0])
                                 and (self.dataToAnalyse.loc[i,nameVariable] <= paarList[1])):
                            
                                auxIndex.append(i+1)
                                
                        indices.append(auxIndex)
                        #del auxIndex[:]
                
                #se crea una única lista en la que se concatenan las obtenidas anteriormente
                auxIndices2 = []
    
                for i in range(len(indices)):
                    auxIndices2.extend(indices[i])
    
                
                for i in range(len(indices[0])):
                    
                    if auxIndices2.count(indices[0][i]) == len(indices):# Si es igual a esto quiere decir que cumple todas las condiciones 
                                                                    #seleccionadas en la interfaz gráfica 
                        indicesToReturn.append(indices[0][i])
            
             
            return self.dataToAnalyse.loc[indicesToReturn, self.selectedCheckBoxes]
    
    
    def calculateData(self, event):
        
        self.m_textCtrl1.Clear()
        
        
        
        self.toShow = ''
        
        data = self.getSelectedData()
                
        if not data.empty:

            self.m_textCtrl1.BeginAlignment(wx.TEXT_ALIGNMENT_CENTER)
            self.m_textCtrl1.BeginBold()
            self.m_textCtrl1.BeginFontSize(15)
            self.m_textCtrl1.WriteText('BASIC STATISTICS\n\n')
            self.m_textCtrl1.EndAlignment()
            self.m_textCtrl1.EndBold()
            self.m_textCtrl1.EndFontSize()

            self.toShow = self.toShow + 'Maximum:\n' + data.max().round(3).to_string() + '\n'
            self.toShow = self.toShow + '\nMinimum:\n' + data.min().round(3).to_string() + '\n'            
            self.toShow = self.toShow + '\nMean:\n' + data.mean().round(3).to_string() + '\n'            
            self.toShow = self.toShow + '\nMedian:\n' + data.median().round(3).to_string() + '\n'            
            self.toShow = self.toShow + '\nStd Deviation:\n' + data.std().round(3).to_string() + '\n'
            self.toShow = self.toShow + '\nVariance:\n' + data.var().round(3).to_string() + '\n'
            self.toShow = self.toShow + '\nCovariance:\n' + data.cov().round(3).to_string() + '\n'
            self.toShow = self.toShow + '\nQuantile 25%:\n' + data.quantile(q = 0.25).round(3).to_string() + '\n'
            self.toShow = self.toShow + '\nQuantile 50%:\n' + data.quantile(q = 0.5).round(3).to_string() + '\n'
            self.toShow = self.toShow + '\nQuantile 75%:\n' + data.quantile(q = 0.75).round(3).to_string() + '\n'
            self.toShow = self.toShow + '\nCorrelation (Pearson):\n' + data.corr(method = 'pearson').round(3).to_string() + '\n'
            #self.toShow = self.toShow + '\nCorrelation (Kendall):\n' + data.corr(method = 'kendall').round(3).to_string() + '\n'
            #self.toShow = self.toShow + '\nCorrelation (Spearman):\n' + data.corr(method = 'spearman').round(3).to_string() + '\n'
            self.toShow = self.toShow + '\nKurtosis:\n' + data.kurtosis().round(3).to_string() + '\n'
            self.toShow = self.toShow + '\nSkew:\n' + data.skew().round(3).to_string() + '\n'
            
            self.m_textCtrl1.AppendText(self.toShow)
            self.m_textCtrl1.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Ubuntu Mono'))
        
        # else:
        #     wx.MessageBox("There is no data that match the selected filters", "ERROR", wx.OK | wx.ICON_EXCLAMATION)


    def noCheckBoxSelectedWarning(self):
        
        dlg = wx.MessageDialog(self, "Please, select at least one variable", "ERROR", wx.OK | wx.ICON_EXCLAMATION)

        if dlg.ShowModal() == wx.ID_OK:
            dlg.Destroy()
        else:
            dlg.Destroy()
            
    
    def wrongIntervalWarning(self):
        
        dlg = wx.MessageDialog(self, "Bad defined interval", "ERROR", wx.OK | wx.ICON_EXCLAMATION)

        if dlg.ShowModal() == wx.ID_OK:
            dlg.Destroy()
        else:
            dlg.Destroy()        
