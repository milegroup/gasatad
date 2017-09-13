# -*- coding: utf-8 -*- 

import wx
import wx.lib.agw.floatspin as fs
import os

class FactorsInterface ( wx.Dialog ):
    
    spinControlList = []
    textControlList = []
    sizerList = []
    #List where the application save the BitmapButtons
    plusList = []
    minusList = []
    paarList = []
    
    factorsAndValues = {}
    
    def __init__( self, parent, listOfVariables, namesColumns, minimum, maximum ):
        
        
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Add New Column", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        mainSizer.Add(gbSizer1)
        
        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Select the Variable" ), wx.VERTICAL )
        
        fgVarSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgVarSizer.SetFlexibleDirection( wx.BOTH )
        fgVarSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        #Here the RadioButtons are created   
        for var in listOfVariables:

            self.radioBtn = wx.RadioButton( self, wx.ID_ANY, var, wx.DefaultPosition, wx.DefaultSize, 0 )
            fgVarSizer.Add( self.radioBtn, 0, wx.ALL, 5 )
            self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedRadioButton, self.radioBtn)
        
        sbSizer1.Add( fgVarSizer, 1, wx.EXPAND, 5 )
        gbSizer1.Add( sbSizer1, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.EXPAND|wx.ALL, 10 )
        
        gbSizer2 = wx.GridBagSizer( 0, 0 )
        gbSizer2.SetFlexibleDirection( wx.BOTH )
        gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        
        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.staticTextCol = wx.StaticText( self, wx.ID_ANY, u"Column Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.staticTextCol.Wrap( -1 )
        bSizer2.Add( self.staticTextCol, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.textCtrlCol = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.textCtrlCol, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER|wx.EXPAND, 20 )
        
        
        gbSizer2.Add( bSizer2, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER | wx.ALL, 10 )
        
        
        self.fgSizer9 = wx.FlexGridSizer( 0, 1, 0, 0 )
        self.fgSizer9.SetFlexibleDirection( wx.BOTH )
        self.fgSizer9.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.fgSizer10 = wx.FlexGridSizer( 0, 8, 0, 0 )
        self.fgSizer10.SetFlexibleDirection( wx.BOTH )
        self.fgSizer10.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        
        self.fgSizer9.Add( self.fgSizer10, 0, wx.ALL, 5 )
        
        
        self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"From:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )
        self.fgSizer10.Add( self.m_staticText9, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )

        self.floatSpinCtrl_1 = fs.FloatSpin(self, wx.ID_ANY, pos = wx.DefaultPosition, min_val = None, max_val = None,increment = 0.001,
                                            value = 0.000, agwStyle = fs.FS_LEFT)
        self.floatSpinCtrl_1.SetFormat("%f")
        self.floatSpinCtrl_1.SetDigits(3)
        self.fgSizer10.Add( self.floatSpinCtrl_1, 0, wx.ALL, 5 )
        
        self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"To:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )
        self.fgSizer10.Add( self.m_staticText10, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.floatSpinCtrl_2 = fs.FloatSpin(self, wx.ID_ANY, pos = wx.DefaultPosition, min_val = None, max_val = None,increment = 0.001,
                                            value = 0.000, agwStyle = fs.FS_LEFT)
        self.floatSpinCtrl_2.SetFormat("%f")
        self.floatSpinCtrl_2.SetDigits(3)
        self.fgSizer10.Add( self.floatSpinCtrl_2, 0, wx.ALL, 5 )
        
        self.staticTextNameVar = wx.StaticText( self, wx.ID_ANY, u"Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.staticTextNameVar.Wrap( -1 )
        self.fgSizer10.Add( self.staticTextNameVar, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0, name = "Factor1" )
        self.fgSizer10.Add( self.m_textCtrl1, 0, wx.ALL|wx.EXPAND, 5 )
        
        
        self.plusBmp = wx.Image(str(os.path.dirname(__file__))+"/icons/mas.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.minusBmp = wx.Image(str(os.path.dirname(__file__))+"/icons/menos.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        
        self.m_bpButton2 = wx.BitmapButton( self, wx.ID_ANY, self.plusBmp, wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_AUTODRAW )
        self.fgSizer10.Add( self.m_bpButton2, 0, wx.ALL, 5 )
        
        self.m_bpButton3 = wx.BitmapButton( self, wx.ID_ANY, self.minusBmp, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.m_bpButton3.Hide()
        
        #List to control the plus and minus buttons
        self.plusList.append(self.m_bpButton2)
        self.minusList.append(self.m_bpButton3)
        
        self.fgSizer10.Add( self.m_bpButton3, 0, wx.ALL, 5 )
        
        gbSizer2.Add( self.fgSizer9, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
        
        fgSizer4 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer4.AddGrowableCol( 1 )
        fgSizer4.SetFlexibleDirection( wx.HORIZONTAL )
        fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.staticTextDefaultValue = wx.StaticText( self, wx.ID_ANY, u"Default Value:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.staticTextDefaultValue.Wrap( -1 )
        fgSizer4.Add( self.staticTextDefaultValue, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.textCtrlDefaultVal = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0, ValidatorForFactors(self.spinControlList, self.textControlList, self.textCtrlCol, namesColumns) )
        fgSizer4.Add( self.textCtrlDefaultVal, 0, wx.ALL|wx.EXPAND, 5 )
        
        
        gbSizer2.Add( fgSizer4, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

        okay = wx.Button( self, wx.ID_OK )
        cancel = wx.Button( self, wx.ID_CANCEL )
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        
        mainSizer.Add( btns, 0, wx.ALIGN_CENTER | wx.ALL, 5 )
        gbSizer1.Add( gbSizer2, wx.GBPosition( 0, 1 ), wx.GBSpan( 2, 1 ), wx.EXPAND|wx.LEFT, 5 )
        
        
        self.SetSizer( mainSizer )
        mainSizer.Fit(self)
        self.Layout()
        self.Fit()
        self.Centre( wx.BOTH )   
        
        #List to control sizers
        self.sizerList.append(self.fgSizer10)
        
        
        #Add the spinContrl to a list to have all of them controlled and to gain access to them
        self.spinControlList.append(self.floatSpinCtrl_1)
        self.spinControlList.append(self.floatSpinCtrl_2)
        
        #Text field where the name of the field is written
        self.textControlList.append(self.m_textCtrl1)

        #Variable to save the selected Radiobutton
        self.selectedRadioButton = listOfVariables[0]

        #Necesitamos un índice para controlar os valores dos distintos combos numéricos e así poder diferencialos
        self.indiceSpinCtrl = 1
        
        #Bindings
        self.Bind(wx.EVT_BUTTON, self.createNewFactor, self.m_bpButton2)
        self.Bind(wx.EVT_BUTTON, self.deleteFactor, self.m_bpButton3)
  
        self.Fit()
        self.Show(True)


        
    def updateSelectedRadioButton(self, event):
        
        radioButton = event.GetEventObject()
        self.selectedRadioButton = radioButton.GetLabelText()
            
        
    def createNewFactor(self, event):
        
        # Aumentamos el índice para así poder diferenciar los diferentes spinCtrl
        
        if self.indiceSpinCtrl is 5:
            
            self.showWarningTooManyIntervals()
            
        else:
        
            self.indiceSpinCtrl += 1
            
            fgSizer = wx.FlexGridSizer( 0, 8, 0, 0 )
            fgSizer.SetFlexibleDirection( wx.BOTH )
            fgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
            self.fgSizer9.Add( fgSizer, 0, wx.ALL, 5 )
            
            self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"From:", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.m_staticText9.Wrap( -1 )
            fgSizer.Add( self.m_staticText9, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
            
            self.floatSpinCtrl_3 = fs.FloatSpin(self, wx.ID_ANY, pos = wx.DefaultPosition, min_val = None, max_val = None,increment = 0.001,
                                            value = 0.000, agwStyle = fs.FS_LEFT)
            self.floatSpinCtrl_3.SetFormat("%f")
            self.floatSpinCtrl_3.SetDigits(3)
            fgSizer.Add( self.floatSpinCtrl_3, 0, wx.ALL, 5 )
            
            self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"To:", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.m_staticText10.Wrap( -1 )
            fgSizer.Add( self.m_staticText10, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
            
            self.floatSpinCtrl_4 = fs.FloatSpin(self, wx.ID_ANY, pos = wx.DefaultPosition, min_val = None, max_val = None,increment = 0.001,
                                            value = 0.000, agwStyle = fs.FS_LEFT)
            self.floatSpinCtrl_4.SetFormat("%f")
            self.floatSpinCtrl_4.SetDigits(3)
            fgSizer.Add( self.floatSpinCtrl_4, 0, wx.ALL, 5 )
            
            self.staticTextNameVar = wx.StaticText( self, wx.ID_ANY, u"Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.staticTextNameVar.Wrap( -1 )
            fgSizer.Add( self.staticTextNameVar, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
            
            self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
            fgSizer.Add( self.m_textCtrl1, 0, wx.ALL|wx.EXPAND, 5 )
            
            self.m_bpButton2 = wx.BitmapButton( self, wx.ID_ANY, self.plusBmp, wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_AUTODRAW )
            fgSizer.Add( self.m_bpButton2, 0, wx.ALL, 5 )
        
            self.m_bpButton3 = wx.BitmapButton( self, wx.ID_ANY, self.minusBmp, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
            fgSizer.Add( self.m_bpButton3, 0, wx.ALL, 5 )
            
            
            #Se deshabilitan los últimos bitmapbutton antes de introducir los que se han creado
            self.plusList[-1].Enable(False)
            self.minusList[-1].Enable(False)
            
            #Se añaden los nuevos
            self.plusList.append(self.m_bpButton2)
            self.minusList.append(self.m_bpButton3)
            
            self.Bind(wx.EVT_BUTTON, self.createNewFactor, self.m_bpButton2)
            self.Bind(wx.EVT_BUTTON, self.deleteFactor, self.m_bpButton3)
            
            #Se añade a la lista de sizers
            self.sizerList.append(fgSizer)
            
            #Añadios los spinCotrl a una lista para tener un control de todos los que tenemos creados y así acceder a ellos
            self.spinControlList.append(self.floatSpinCtrl_3)
            self.spinControlList.append(self.floatSpinCtrl_4)
            
            #Se añade el recuadro de texto dode se escribe el nombre que tendrá el factor
            self.textControlList.append(self.m_textCtrl1)
            
            self.Fit()
            self.Layout()



    def deleteFactor(self, event):
        
        if self.indiceSpinCtrl is 1:
            
            self.showWarning()
            
        else:
            
            self.indiceSpinCtrl -= 1
            
            self.sizerList.pop().DeleteWindows()
            self.fgSizer9.Layout()
            del self.spinControlList[(len(self.spinControlList) -2) : ]
            self.textControlList.pop()
            
            #Se eliminan los dos bitmapbutton de la lista
            self.plusList.pop()
            self.minusList.pop()
            
            #Se habilitan los dos anteriores
            self.plusList[-1].Enable()
            self.minusList[-1].Enable()
            
            self.Layout()
            self.Fit()
    
    
    '''
    This function creates a dictionary where the key is a name and the value is a list of two numbers.(Example Old:(75,90))
    The name is the string that have to be taken for each row which value (of the column selected previouly in the interface)
    is in the interval defined by the two values that are passed as a list.
    '''    
    def createVarWithInterval(self):
        
        self.firstValue = -1
        self.secondValue = -1
        
        self.factorsAndValues.clear()

        for i in range(len(self.spinControlList)):
            
            #Se agrupa el valor inicial y final de cada etiqueta para posteriormente comprobar si hay algún solapamiento
            if i % 2 is 0:
                        
                self.firstValue = self.spinControlList[i].GetValue()
                self.secondValue = self.spinControlList[i + 1].GetValue()
                
                self.paarList.append([self.firstValue, self.secondValue])
                
        
        index = 0
        
        for textControl in self.textControlList:
            
            '''
            Se crea un diccionario cuya clave es el nombre del factor y el valor es el par compuesto por el 
            límite superior e inferior del intervalo
            ''' 
            self.factorsAndValues[textControl.GetValue().encode("utf-8")] = self.paarList[index]
            
            index += 1
        
        del self.spinControlList [:]
        del self.textControlList[:]
        del self.paarList[:]
    
    
    def returnFactors(self):
        
        self.createVarWithInterval()
        
        nameOfFactor = self.textCtrlCol.GetValue()
        nameRestValues = self.textCtrlDefaultVal.GetValue()
               
        return self.factorsAndValues, self.selectedRadioButton, nameRestValues, nameOfFactor


    def showWarningTooManyIntervals(self):
        
        dlg = wx.MessageDialog(self, "You can not create more Intervals", "Attention!", wx.OK | wx.ICON_EXCLAMATION)
        
        if dlg.ShowModal() == wx.ID_OK:
            
            dlg.Destroy()

            

class ValidatorForFactors(wx.PyValidator):
    
    def __init__(self, spinControlList, textControlList, textCtrlNameCol, listNamesCol):
        
        wx.PyValidator.__init__(self)
        self.spinControlList = spinControlList
        self.textControlList = textControlList
        self.textCtrlNameCol = textCtrlNameCol
        self.listNamesCol = listNamesCol

    def Clone(self):
        return ValidatorForFactors(self.spinControlList, self.textControlList, self.textCtrlNameCol, self.listNamesCol)
    
    def Validate(self, win):
        
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()
        existOverlap = False
        erroneousInterval = False
        emptyField = False
        repeatedName = False
        sortedPaarList = []
        
        
        #Check if the name of the columns is already used
        
        if self.textCtrlNameCol.GetValue() in self.listNamesCol:
            
            repeatedName = True
            
        for i in range(len(self.spinControlList)):
            
            #Se agrupa el valor inicial y final de cada etiqueta para posteriormente comprobar si hay algún solapamiento
            if i % 2 is 0:
                        
                firstValue = self.spinControlList[i].GetValue()
                secondValue = self.spinControlList[i + 1].GetValue()
                sortedPaarList.append([firstValue, secondValue])

        #Se crea una lista ordenada para comprobar si existe solapamiento entre los intervalos        
        sortedPaarList.sort()
        if len(sortedPaarList) != 1:
        
            for i in range(len(sortedPaarList) - 1):
                
                lowLimit, hightLimit = sortedPaarList[i]
                lowLimit2, hightLimit2 = sortedPaarList[i + 1]

                if hightLimit >= lowLimit2:
                    
                    existOverlap = True
                
                if (lowLimit > hightLimit) or (lowLimit2 > hightLimit2):
                    
                    erroneousInterval = True        
        else:
             
            lowLimit, hightLimit = sortedPaarList[0]
             
            if (lowLimit > hightLimit):
                    
                    erroneousInterval = True
        
        for textCtrl in self.textControlList:
            
            if not textCtrl.GetValue():
                emptyField = True
        
        if not self.textCtrlNameCol.GetValue():
            emptyField = True
        
        if not text:
            emptyField = True
        
        if repeatedName:
            wx.MessageBox("This name already exists! Please, change it", "Repeated Column Name")
            
            emptyField = False
            existOverlap = False
            erroneousInterval = False
            repeatedName = False
            sortedPaarList = []
            return False     
        
        
        elif emptyField:
            wx.MessageBox("You must fill in all the fields", "Empty Field")
            
            emptyField = False
            existOverlap = False
            erroneousInterval = False
            repeatedName = False
            sortedPaarList = []
            return False
        
        elif existOverlap:
            wx.MessageBox("OverLap in one of the SpinControls", "OverLap")
            
            emptyField = False
            existOverlap = False
            erroneousInterval = False
            repeatedName = False
            sortedPaarList = []
            return False
            
        elif erroneousInterval:
            wx.MessageBox("The value of the FROM item have to be lower or equal than the TO item", "Attention!")
            
            emptyField = False
            existOverlap = False
            erroneousInterval = False
            repeatedName = False
            sortedPaarList = []
            return False
        
        else:
            return True
        
    def TransferToWindow(self):
        
        return True
    
    def TransferFromWindow(self):
        return True            
