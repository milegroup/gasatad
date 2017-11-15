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

import wx.lib.scrolledpanel
from scipy.stats.stats import ks_2samp, ranksums, ttest_ind
import wx.richtext as rt


class SignificanceTestInterface ( wx.Dialog ):
    
    def __init__( self, parent, namesCheckBox,  tagsAndValues, integerValues, minimum, maximum, dataFrame ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Significance test", size =(1200, 600), pos = wx.DefaultPosition)

        self.SetMinSize((640, 480))
                
        
        self.dataToAnalyse = dataFrame
        self.min = minimum
        self.max = maximum
        
        
        #All needed lists
        self.selectedVariablesInColumnLeft = dict.fromkeys(tagsAndValues.keys())
        self.selectedVariablesInColumnRight = dict.fromkeys(tagsAndValues.keys())
        
        for key in self.selectedVariablesInColumnLeft.keys():
            
            self.selectedVariablesInColumnLeft[key] = []
    
        for key in self.selectedVariablesInColumnRight.keys():
            
            self.selectedVariablesInColumnRight[key] = []
        
        self.listOfSpinCtrlLeft = []
        self.listOfSpinCtrlRight = []
        
        self.intervalNameAndLimitsLeft = {}
        self.intervalNameAndLimitsRight = {}
    
        self.activatedCheckBoxesLeft = []
        self.activatedCheckBoxesRight = []
        
        self.intervalNameAndLimits = {}
        self.integerValues = integerValues
        
        self.clickedRadiobuttonLeft = namesCheckBox[0]
        self.clickedRadiobuttonRight = namesCheckBox[0]        

        #Panel for all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)
        
        #Definition of the scrolled panel
        self.scrolledPanel = wx.lib.scrolledpanel.ScrolledPanel(self.panel, -1, style = wx.TAB_TRAVERSAL)
        self.scrolledPanel.SetAutoLayout(1)
        self.scrolledPanel.SetupScrolling()        
        
        self.scrollSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        
        
        #LEFT SIZER
        rightSizer = wx.StaticBoxSizer( wx.StaticBox( self.scrolledPanel, wx.ID_ANY, u"VARIABLES" ), wx.VERTICAL )
        self.scrollSizer.Add( rightSizer, 0, wx.ALL, 10 )
        
        fgSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer.SetFlexibleDirection( wx.BOTH )
        fgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        rightSizer.Add(fgSizer, 1, wx.ALL | wx.EXPAND, 5)
        
        #Definition of the Sizer where the checkBoxes will be created
        checkSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
        checkSizer.SetFlexibleDirection( wx.BOTH )
        checkSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        fgSizer.Add( checkSizer, 0,  wx.ALL| wx.EXPAND, 5)
 
        for i in namesCheckBox:
            
            #Si es el primer elemento
            if i == namesCheckBox[0]:
                self.m_radioBtn15 = wx.RadioButton( self.scrolledPanel, wx.ID_ANY, str(i), wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
                checkSizer.Add( self.m_radioBtn15, 0, wx.ALL| wx.EXPAND, 5 )
                self.Bind(wx.EVT_RADIOBUTTON, self.changeSelectedRadioButtonLeft, self.m_radioBtn15)
                
                
            else:    
                self.m_radioBtn15 = wx.RadioButton( self.scrolledPanel, wx.ID_ANY, str(i), wx.DefaultPosition, wx.DefaultSize, 0 )
                checkSizer.Add( self.m_radioBtn15, 0, wx.ALL| wx.EXPAND, 5 )
                self.Bind(wx.EVT_RADIOBUTTON, self.changeSelectedRadioButtonLeft, self.m_radioBtn15)
        
        
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
                self.Bind(wx.EVT_CHECKBOX, self.changeValueTagCheckBoxLeft, self.m_checkBox)
                
                
            tagsSizer.Add( sbSizer, 0, wx.EXPAND | wx.ALL, 5 )
        
        
        
        #INTEGER VALUES        
        if integerValues:
            
               
            #Definition of the Sizer where the checkBoxes will be created
            auxSizer2 = wx.FlexGridSizer( 0, 5, 0, 0 )
            auxSizer2.SetFlexibleDirection( wx.BOTH )
            auxSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
            fgSizer.Add( auxSizer2, 0,  wx.ALL| wx.EXPAND, 5)
            
            for i in integerValues:
            
                self.m_checkBox = wx.CheckBox( self.scrolledPanel, wx.ID_ANY, str(i), wx.DefaultPosition, wx.DefaultSize, 0 )
                self.m_checkBox.SetFont( wx.Font( 10, wx.DEFAULT, wx.NORMAL, wx.BOLD, False, wx.EmptyString ) )
                self.Bind(wx.EVT_CHECKBOX, self.changeStatusSpinCtrlLeft, self.m_checkBox)
                
                auxSizer2.Add( self.m_checkBox, 0,wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

            
                self.m_staticText11 = wx.StaticText( self.scrolledPanel, wx.ID_ANY, u"From:", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.m_staticText11.Wrap( -1 )
                auxSizer2.Add( self.m_staticText11, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, 5 )
            
                self.m_spinCtrl11 = wx.SpinCtrl( self.scrolledPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 65,-1 ), wx.SP_ARROW_KEYS, minimum, maximum, 0, str(i) + "-LimitInf")
                auxSizer2.Add( self.m_spinCtrl11, 0, wx.ALL, 5 )
                self.m_spinCtrl11.Enable(False)
            
                self.m_staticText21 = wx.StaticText( self.scrolledPanel, wx.ID_ANY, u"To:", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.m_staticText21.Wrap( -1 )
                auxSizer2.Add( self.m_staticText21, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, 5 )
            
                self.m_spinCtrl21 = wx.SpinCtrl( self.scrolledPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 65,-1 ), wx.SP_ARROW_KEYS, minimum, maximum, 0, str(i) + "-LimitSup")
                auxSizer2.Add( self.m_spinCtrl21, 0, wx.ALL, 5 )
                self.m_spinCtrl21.Enable(False) 
                
                self.listOfSpinCtrlLeft.append(self.m_spinCtrl11)
                self.listOfSpinCtrlLeft.append(self.m_spinCtrl21)
        
        
        #RIGHT SIZER
        leftSizer = wx.StaticBoxSizer( wx.StaticBox( self.scrolledPanel, wx.ID_ANY, u"VARIABLES" ), wx.VERTICAL )
        self.scrollSizer.Add( leftSizer, 0, wx.ALL, 10 )
        
        fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer2.SetFlexibleDirection( wx.BOTH )
        fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        leftSizer.Add(fgSizer2, 1, wx.ALL | wx.EXPAND, 5)
        
        #Definition of the Sizer where the checkBoxes will be created
        checkSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
        checkSizer2.SetFlexibleDirection( wx.BOTH )
        checkSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        fgSizer2.Add( checkSizer2, 0,  wx.ALL| wx.EXPAND, 5)
 
        for i in namesCheckBox:
            
            #Si es el primer elemento
            if i == namesCheckBox[0]:
                self.m_radioBtn15 = wx.RadioButton( self.scrolledPanel, wx.ID_ANY, str(i), wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
                checkSizer2.Add( self.m_radioBtn15, 0, wx.ALL| wx.EXPAND, 5 )
                self.Bind(wx.EVT_RADIOBUTTON, self.changeSelectedRadioButtonRight, self.m_radioBtn15)
                
            else:    
                self.m_radioBtn15 = wx.RadioButton( self.scrolledPanel, wx.ID_ANY, str(i), wx.DefaultPosition, wx.DefaultSize, 0 )
                checkSizer2.Add( self.m_radioBtn15, 0, wx.ALL| wx.EXPAND, 5 )
                self.Bind(wx.EVT_RADIOBUTTON, self.changeSelectedRadioButtonRight, self.m_radioBtn15)
                
        
        tagsSizer2 = wx.FlexGridSizer( 0, 1, 0, 0 )
        tagsSizer2.SetFlexibleDirection( wx.BOTH )
        tagsSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        fgSizer2.Add( tagsSizer2, 1, wx.ALL| wx.EXPAND, 5 )
        
        for tag, values in tagsAndValues.iteritems():
            
            #self.checkBoxTagRight.append(SelectedValuesOfTag(tag, values))
            
            sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.scrolledPanel, wx.ID_ANY, str(tag) ), wx.VERTICAL )
            
            for j in values:
                
                self.m_checkBox = wx.CheckBox(parent = self.scrolledPanel, id = wx.ID_ANY, label = str(j), pos = wx.DefaultPosition, size = wx.DefaultSize, name = str(tag) )
                sbSizer2.Add( self.m_checkBox, 0, wx.EXPAND, 5 )
                self.Bind(wx.EVT_CHECKBOX, self.changeValueTagCheckBoxRight, self.m_checkBox)
                
               
            tagsSizer2.Add( sbSizer2, 0, wx.EXPAND | wx.ALL, 5 )         
         
         
        #INTEGER VALUES        
        if integerValues:
            
               
            #Definition of the Sizer where the checkBoxes will be created
            auxSizer2 = wx.FlexGridSizer( 0, 5, 0, 0 )
            auxSizer2.SetFlexibleDirection( wx.BOTH )
            auxSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
            fgSizer2.Add( auxSizer2, 0,  wx.ALL| wx.EXPAND, 5)
            #self.ListOfAuxSizers.append(auxSizer2)
            
            #self.ListOfAuxSizers.append(auxSizer2)
            
            for i in integerValues:
            
                self.m_checkBox = wx.CheckBox( self.scrolledPanel, wx.ID_ANY, str(i), wx.DefaultPosition, wx.DefaultSize, 0 )
                self.m_checkBox.SetFont( wx.Font( 10, wx.DEFAULT, wx.NORMAL, wx.BOLD, False, wx.EmptyString ) )
                self.Bind(wx.EVT_CHECKBOX, self.changeStatusSpinCtrlRight, self.m_checkBox)
                
                auxSizer2.Add( self.m_checkBox, 0,wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

            
                self.m_staticText11 = wx.StaticText( self.scrolledPanel, wx.ID_ANY, u"From:", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.m_staticText11.Wrap( -1 )
                auxSizer2.Add( self.m_staticText11, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, 5 )
            
                self.m_spinCtrl11 = wx.SpinCtrl( self.scrolledPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 65,-1 ), wx.SP_ARROW_KEYS, minimum, maximum, 0, str(i) + "-LimitInf")
                auxSizer2.Add( self.m_spinCtrl11, 0, wx.ALL, 5 )
                self.m_spinCtrl11.Enable(False)                
                
                self.m_staticText21 = wx.StaticText( self.scrolledPanel, wx.ID_ANY, u"To:", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.m_staticText21.Wrap( -1 )
                auxSizer2.Add( self.m_staticText21, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, 5 )
            
                self.m_spinCtrl21 = wx.SpinCtrl( self.scrolledPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 65,-1 ), wx.SP_ARROW_KEYS, minimum, maximum, 0, str(i) + "-LimitSup")
                auxSizer2.Add( self.m_spinCtrl21, 0, wx.ALL, 5 )
                self.m_spinCtrl21.Enable(False)
                
                self.listOfSpinCtrlRight.append(self.m_spinCtrl11)
                self.listOfSpinCtrlRight.append(self.m_spinCtrl21)    
        
        #TEXT CONTROL
        self.m_textCtrl = rt.RichTextCtrl( self.scrolledPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.VSCROLL | wx.HSCROLL | wx.TE_MULTILINE | wx.TE_READONLY | wx.NO_BORDER)
        self.m_textCtrl.SetMargins((20,20))
        
        self.scrollSizer.Add( self.m_textCtrl, 1,  wx.ALL | wx.EXPAND , 20 )
        
        
        self.scrolledPanel.SetSizerAndFit(self.scrollSizer)
        self.scrolledPanel.Layout()
       
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(self.scrolledPanel, 1, wx.EXPAND)
        
        
        
        okay = wx.Button( self.panel, wx.ID_OK, label = "Show Results" )
        self.Bind(wx.EVT_BUTTON, self.calculateData, okay)
        cancel = wx.Button( self.panel, wx.ID_CANCEL )
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        panelSizer.Add(btns)
        #btn = wx.Button(self.panel, label="Add Widget")
        

        self.panel.SetSizerAndFit(panelSizer)
        panelSizer.Layout()
        self.panel.Layout()
        
        self.Layout()
        
        self.Centre( wx.BOTH )



    def changeStatusSpinCtrlLeft(self, event):
        
        checkBox = event.GetEventObject()
        
        if checkBox.IsChecked():
            
            self.activatedCheckBoxesLeft.append(checkBox.GetLabel().encode("utf-8"))
            
            i = 0
            
            while checkBox.GetLabel().encode("utf-8") != self.listOfSpinCtrlLeft[i].GetName().split("-")[0].encode("utf-8"):
    
                i = i+1
             
             
            if checkBox.GetLabel().encode("utf-8") == self.listOfSpinCtrlLeft[i].GetName().split("-")[0].encode("utf-8"):
                
                self.listOfSpinCtrlLeft[i].Enable()
                self.listOfSpinCtrlLeft[i + 1].Enable()
                        
        else:
            
            self.activatedCheckBoxesLeft.remove(checkBox.GetLabel().encode("utf-8"))
            
            i = 0
            
            while checkBox.GetLabel().encode("utf-8") != self.listOfSpinCtrlLeft[i].GetName().split("-")[0].encode("utf-8"):
    
                i = i+1
            
            if checkBox.GetLabel().encode("utf-8") == self.listOfSpinCtrlLeft[i].GetName().split("-")[0].encode("utf-8"):
                
                self.listOfSpinCtrlLeft[i].Enable(False)
                self.listOfSpinCtrlLeft[i + 1].Enable(False)
    
    
    
    def changeStatusSpinCtrlRight(self, event):
        
        checkBox = event.GetEventObject()
        
        if checkBox.IsChecked():
            
            self.activatedCheckBoxesRight.append(checkBox.GetLabel().encode("utf-8"))
            
            i = 0
            
            while checkBox.GetLabel().encode("utf-8") != self.listOfSpinCtrlRight[i].GetName().split("-")[0].encode("utf-8"):
    
                i = i+1
             
             
            if checkBox.GetLabel().encode("utf-8") == self.listOfSpinCtrlRight[i].GetName().split("-")[0].encode("utf-8"):
                
                self.listOfSpinCtrlRight[i].Enable()
                self.listOfSpinCtrlRight[i + 1].Enable()
                        
        else:
            
            self.activatedCheckBoxesRight.remove(checkBox.GetLabel().encode("utf-8"))
            
            i = 0
            
            while checkBox.GetLabel().encode("utf-8") != self.listOfSpinCtrlRight[i].GetName().split("-")[0].encode("utf-8"):
    
                i = i+1
            
            if checkBox.GetLabel().encode("utf-8") == self.listOfSpinCtrlRight[i].GetName().split("-")[0].encode("utf-8"):
                
                self.listOfSpinCtrlRight[i].Enable(False)
                self.listOfSpinCtrlRight[i + 1].Enable(False)

    
    
    def changeSelectedRadioButtonLeft(self, event):   
        
        radioButton = event.GetEventObject()
        self.clickedRadiobuttonLeft = radioButton.GetLabel().encode("utf-8")
        
            
    
    def changeSelectedRadioButtonRight(self, event):   
        
        radioButton = event.GetEventObject()
        self.clickedRadiobuttonRight = radioButton.GetLabel().encode("utf-8")
        
    

    def changeValueTagCheckBoxLeft(self, event):

        checkBox = event.GetEventObject()
    
        label = checkBox.GetLabel().encode("utf-8")
        nameCheckBox = checkBox.GetName().encode("utf-8")       
                
        if checkBox.IsChecked():
            
            self.selectedVariablesInColumnLeft[nameCheckBox].append(label)
                        
        else:
            
            self.selectedVariablesInColumnLeft[nameCheckBox].remove(label)
    
    
    def changeValueTagCheckBoxRight(self, event):

        checkBox = event.GetEventObject()
    
        label = checkBox.GetLabel().encode("utf-8")
        nameCheckBox = checkBox.GetName().encode("utf-8")       
                
        if checkBox.IsChecked():
            
            self.selectedVariablesInColumnRight[nameCheckBox].append(label)
                        
        else:
            
            self.selectedVariablesInColumnRight[nameCheckBox].remove(label)
            

              
    def getSelectedData(self, activatedCheckBoxes, listOfSpinCtrl, selectedVariablesInColumn):
        
        self.intervalNameAndLimits.clear()
       
        for checkBox in activatedCheckBoxes:
        
            i = 0
            
            while checkBox != listOfSpinCtrl[i].GetName().split("-")[0].encode("utf-8"):
    
                i = i+1
            
            if checkBox == listOfSpinCtrl[i].GetName().split("-")[0].encode("utf-8"):
                
                limitInf = listOfSpinCtrl[i].GetValue()
                limitSup = listOfSpinCtrl[i + 1].GetValue()
                    
                self.intervalNameAndLimits[checkBox] = [limitInf, limitSup]
        
        
        self.wrongInterval = False
        
        for nameVariable, paarList in self.intervalNameAndLimits.iteritems():
            
            if paarList[0] > paarList[1]:
                self.wrongInterval = True 
        
        if self.wrongInterval:
            
            self.wrongIntervalWarning()
            return []
            
        else:
            
            tempList = []
            
            #List of lists
            indices = []
            indicesToReturn = []
    
            for i in selectedVariablesInColumn.values():
                
                tempList.extend(i) 
            
            if not tempList:
                
                auxIndex1 = list(self.dataToAnalyse.index)
                indices.append(auxIndex1)
            
                if self.intervalNameAndLimits:
                    for nameVariable, paarList in self.intervalNameAndLimits.iteritems():
                        
                        auxIndex = []
                        
                        for i in range(len(self.dataToAnalyse.index)):
                            
                            if ( (self.dataToAnalyse.loc[i,nameVariable] >= paarList[0])
                                 and (self.dataToAnalyse.loc[i,nameVariable] <= paarList[1])):
                            
                                auxIndex.append(i+1)
                                
                        indices.append(auxIndex)
                
                #List where all lists are concatenated
                auxIndices2 = []
    
                for i in range(len(indices)):
                    auxIndices2.extend(indices[i])
                
                for i in range(len(indices[0])):
                    
                    if auxIndices2.count(indices[0][i]) == len(indices):# Si es igual a esto quiere decir que cumple todas las condiciones 
                                                                    #seleccionadas en la interfaz gráfica 
                        indicesToReturn.append(indices[0][i])
            
            else:
                auxIndex1 = []
               
                for name, value in selectedVariablesInColumn.items():
                    
                    if value:
                        tagsColumn = self.dataToAnalyse[name]
                        auxIndex1 = [x for x in range(len(tagsColumn)) if tagsColumn[x] in value ]
                        indices.append(auxIndex1)

                        # auxIndex1 = []
                        # for i in range(len(self.dataToAnalyse.index)):
                            
                        #     if (self.dataToAnalyse.loc[i+1,name] in value):
                            
                        #         auxIndex1.append(i+1)
                              
                        # indices.append(auxIndex1)               
                
                if self.intervalNameAndLimits:
                    
                    for nameVariable, paarList in self.intervalNameAndLimits.iteritems():
                        
                        auxIndex = []
                        
                        for i in range(len(self.dataToAnalyse.index)):
                            
                            if ( (self.dataToAnalyse.loc[i,nameVariable] >= paarList[0])
                                 and (self.dataToAnalyse.loc[i,nameVariable] <= paarList[1])):
                            
                                auxIndex.append(i+1)
                                
                        indices.append(auxIndex)
                
                #Se crea una única lista en la que se concatenan las obtenidas anteriormente
                auxIndices2 = []
    
                for i in range(len(indices)):
                    auxIndices2.extend(indices[i])
    
                
                for i in range(len(indices[0])):
                    
                    if auxIndices2.count(indices[0][i]) == len(indices):# Si es igual a esto quiere decir que cumple todas las condiciones 
                                                                    #seleccionadas en la interfaz gráfica 
                        indicesToReturn.append(indices[0][i])
            
             
            return indicesToReturn
        
        
    def resultsSignificanceTests(self):
        
        listIndex1 = self.getSelectedData(self.activatedCheckBoxesLeft, self.listOfSpinCtrlLeft, self.selectedVariablesInColumnLeft)
        listIndex2 = self.getSelectedData(self.activatedCheckBoxesRight, self.listOfSpinCtrlRight, self.selectedVariablesInColumnRight)
                
        #LP means Left Panel
        dataSelectedLP = self.dataToAnalyse.loc[listIndex1, self.clickedRadiobuttonLeft]     
        
        #RP means Right Panel        
        dataSelectedRP = self.dataToAnalyse.loc[listIndex2, self.clickedRadiobuttonRight]

        # print "## dataLP"
        # print dataSelectedLP
        # print "## dataRP"
        # print dataSelectedRP


        if (len(dataSelectedLP) > 0 and len(dataSelectedRP) > 0):
            
            self.m_textCtrl.BeginAlignment(wx.TEXT_ALIGNMENT_CENTER)
            self.m_textCtrl.BeginBold()
            self.m_textCtrl.BeginFontSize(15)
            self.m_textCtrl.WriteText('RESULTS FOR ' + str(self.clickedRadiobuttonLeft) + ' Vs ' + str(self.clickedRadiobuttonRight) + '\n\n')
            self.m_textCtrl.EndAlignment()
            self.m_textCtrl.EndBold()
            self.m_textCtrl.EndFontSize()
            
            #The string to return is created
            toRet = ''            
            
            # print "## d1:\n",dataSelectedLP
            # print "## d2:\n",dataSelectedRP

            temp1, temp2 = ttest_ind(dataSelectedLP, dataSelectedRP, equal_var = False, nan_policy='omit')
            toRet = toRet + 'T-test on TWO INDEPENDENT samples:\n'
            toRet = toRet + 'Statistic: {0}  p-value: {1}\n\n'.format(temp1, temp2)
            
            temp1, temp2 = ks_2samp(dataSelectedLP, dataSelectedRP)
            toRet = toRet + 'Kolmogorov-Smirnov on TWO samples:\n'
            toRet = toRet + 'Statistic: {0}  p-value: {1}\n\n'.format(temp1, temp2)
            
            temp1, temp2 = ranksums(dataSelectedLP, dataSelectedRP)
            toRet = toRet + 'Wilcoxon rank-sum test:\n'
            toRet = toRet + 'Statistic: {0}  p-value: {1}\n\n'.format(temp1, temp2)
            
            return toRet
        else:
            
            wx.MessageBox("There is no data that match the selected filters in one of the variables", "Attention!",
                                   wx.OK | wx.ICON_EXCLAMATION)
            toRet = ''
            return toRet



    def calculateData(self, event):           
        
        self.m_textCtrl.Clear()
        toShow = self.resultsSignificanceTests()
        self.m_textCtrl.AppendText(toShow)

    
    def wrongIntervalWarning(self):
        
        dlg = wx.MessageDialog(self, "The value of the FROM item have to be lower or equal than the TO item", "Attention!",
                               wx.OK | wx.ICON_EXCLAMATION)

        if dlg.ShowModal() == wx.ID_OK:
            
            dlg.Destroy()
        else:
            
            dlg.Destroy()

            

        
class ValidatorForFactors(wx.PyValidator):
    
    def __init__(self, activatedCheckBoxes, listOfSpinCtrl):
        
        wx.PyValidator.__init__(self)
        self.activatedCheckBoxes = activatedCheckBoxes
        self.listOfSpinCtrl = listOfSpinCtrl


    def Clone(self):
        return ValidatorForFactors(self.activatedCheckBoxes, self.listOfSpinCtrl)
    
    def Validate(self, win):
        
        
        
        for checkBox in self.activatedCheckBoxes:
        
            i = 0
            
            while checkBox != self.listOfSpinCtrl[i].GetName().split("-")[0].encode("utf-8"):
    
                i = i+1
            
            if checkBox == self.listOfSpinCtrl[i].GetName().split("-")[0].encode("utf-8"):
                
                limitInf = self.listOfSpinCtrl[i].GetValue()
                limitSup = self.listOfSpinCtrl[i + 1].GetValue()
                    
                self.intervalNameAndLimits[checkBox] = [limitInf, limitSup]
        
        
        self.wrongInterval = False
        
        for paarList in self.intervalNameAndLimits.values():
            
            if paarList[0] > paarList[1]:
                self.wrongInterval = True 
        
        if self.wrongInterval:
            wx.MessageBox("The value of the FROM item have to be lower or equal than the TO item", "Attention!")
            return False
        
        
        else:
            return True
        
    def TransferToWindow(self):
        
        return True
    
    def TransferFromWindow(self):
        return True            



