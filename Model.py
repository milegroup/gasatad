# -*- coding: utf-8 -*- 

#from pandas.core.frame import DataFrame


'''
This class stores the data that comes from the first file
'''

class QuantitativeData():    
    
    def __init__(self):
        
        #It stores the data that comes from the first file
        self.quantitativeData = None
        
        
    def setQuantitativeData (self, data):
        
        self.quantitativeData = data    
        
    def getQuantitativeData(self):
        
        return self.quantitativeData   
        


class QualitativeData():

    def __init__(self):
        
        #It stores the data that comes from the second file
        self.qualitativeData = None
     
        
    def setQualitativeData (self, data):
        
        self.qualitativeData = data
        
    def getQualitativeData(self):
        
        return self.qualitativeData
    
    
    

class ProgramState():
    
    
    def __init__(self):
        
        self.fileIsOpen = False
        self.additionalFileIsOpen = False
        
        
        self.quantitativeData = QuantitativeData()
        self.qualitativeData = QualitativeData()
        
        
        self.dataToAnalyse = None
        self.result = None
        self.checkBoxStatus = []
        self.comboBoxStatus = {}
        self.additionalFileOpened = False
        
        self.informationFile = FileInformation()
        self.informationAdditionalFile = FileInformation() 
        
    def getDataToAnalyse(self):
        
        return self.dataToAnalyse
    
    
    
    def getQuatitativeData(self):
        
        return self.quantitativeData
    
    
    
    def getQualitativeData(self):
        
        return self.qualitativeData
    
    
    
    def setDataToAnalyse(self, newData):
        
        self.dataToAnalyse = newData
    
    
    
    def setQuantitativeData(self, newData):
        
        self.quantitativeData = newData
    
    
        
    def SetQualitativeData(self, newData):
        
        self.qualitativeData = newData
    
    
    def changeStatusCheckBox(self, nameCheckBox, status):
        
        self.checkBoxStatus[nameCheckBox] = status
            

           
    def initializationComboBoxStatus(self, characterValues):
        
        self.comboBoxStatus = dict.fromkeys(characterValues)
        
        '''
        All the values of the dictionary are initialized into False, because at first, none of the
        checkBox will be checked
        '''
        
        for i in characterValues:
            
            self.comboBoxStatus[i] = ""
            

    def changeStatusComboBox(self, nameComboBox, status):
        
        self.comboBoxStatus[nameComboBox] = status

    
    def setInformationFile(self, nCols, nRows, name):
        
        self.informationFile.setNumberOfCols(nCols)
        self.informationFile.setNumberOfRows(nRows)
        self.informationFile.setNameOfFile(name)
        
        
    def setInformationAdditionalFile(self, nCols, nRows, name):
        
        self.informationAdditionalFile.setNumberOfCols(nCols)
        self.informationAdditionalFile.setNumberOfRows(nRows)
        self.informationAdditionalFile.setNameOfFile(name)

class FileInformation():

    
    def __init__(self, nCols = 0, nRows = 0, name = ''):
        
        self.numColumns = nCols
        self.numRows = nRows
        self.nameOfFile = name

    
    def setNumberOfCols(self, nCols):
        
        self.numColumns = nCols
        
    def setNumberOfRows(self, nRows):
        
        self.numRows = nRows
        
    def setNameOfFile(self, name):
        
        self.nameOfFile = name
    
    
       
        
class ChartOptions():
    
    def __init__(self, title = '', xAxisName = '', yAxisName = '', showGrid = True, xAxisGrid = False, yAxisGrid = False, firstVarSelected = '', secondVarSelected = '', legendPosition = '', selectedCheckBoxes = [] ):
        
        self.chartTitle = title
        self.xAxisName = xAxisName
        self.yAxisName = yAxisName
        
        self.showGrid = showGrid
        self.xAxisGrid = xAxisGrid
        self.yAxisGrid = yAxisGrid
        
        self.legendPosition = legendPosition
        
        self.firstVarSelected = firstVarSelected
        self.secondVarSelected = secondVarSelected
        self.selectedCheckBoxes = selectedCheckBoxes
        
    def getChartTitle(self):
        
        return self.chartTitle
    
    def getXAxisName(self):
        
        return self.xAxisName
    
    def getYAxisName(self):
        
        return self.yAxisName
    
    def getShowGrid(self):
        
        return self.showGrid
    
    def getXAxisGrid(self):
        
        return self.xAxisGrid
    
    def getYAxisGrid(self):
        
        return self.yAxisGrid
    
    def getFirstVarSelected(self):
        
        return self.firstVarSelected
    
    def getSecondVarSelected(self):
        
        return self.secondVarSelected
    
    def getLegendPosition(self):
        
        return self.legendPosition.lower().encode("utf-8")
    
    def getSelectedCheckBoxes(self):
        
        return self.selectedCheckBoxes
    
    def setChartTitle(self, title):
        
        self.chartTitle = title
    
    def setXAxisName(self, xAxisName):
        
        self.xAxisName = xAxisName
    
    def setYAxisName(self, yAxisName):
        
        self.yAxisName = yAxisName
    
    def setShowGrid(self, showGrid):
        
        self.showGrid = showGrid
    
    def setXAxisGrid(self, xAxisGrid):
        
        self.xAxisGrid = xAxisGrid
    
    def setYAxisGrid(self, yAxisGrid):
        
        self.yAxisGrid = yAxisGrid
        
    def setLegendPosition(self, pos):
        
        self.legendPosition = pos
        
    def setSelectedCheckBoxes(self, listCheckBoxes):
        
        self.selectedCheckBoxes = listCheckBoxes    



class OptionsInExportInterface():
    
    def __init__(self, characterSet = "utf-8", fieldDelimiter = ",", decimalSeparator = ".", wColNames = True, wRowNames = True):
        
        self.characterSet = characterSet
        self.fieldDelimiter = fieldDelimiter
        self.decimalSeparator = decimalSeparator
        self.wColNames = wColNames
        self.wRowNames = wRowNames
        
    
    def setCharacterSet(self, characterSet):
        
        self.characterSet = characterSet
        
    
    def setFieldDelimiter(self, fieldDelimiter):
        
        self.fieldDelimiter = fieldDelimiter
        
    
    def setdecimalSeparator(self, decimalSeparator):
        
        self.decimalSeparator = decimalSeparator
    
        
    def setWriteColNames(self, wColNames):
        
        self.wColNames = wColNames
    
    
    def setWriteRowNames(self, wRowNames):
        
        self.wRowNames = wRowNames
    
    
    def getCharacterSet(self):
        
        return self.characterSet
        
    
    def getFieldDelimiter(self):
        
        return self.fieldDelimiter
        
    
    def getDecimalSeparator(self):
        
        return self.decimalSeparator
    
        
    def getWriteColNames(self):
        
        return self.wColNames
    
    
    def getWriteRowNames(self):
        
        return self.wRowNames     
