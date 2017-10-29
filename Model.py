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
        # self.informationAdditionalFile = FileInformation() 
        
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

    
    def setInformationFile(self, nCols, nRows):
        
        self.informationFile.setNumberOfCols(nCols)
        self.informationFile.setNumberOfRows(nRows)
        
        
    # def setInformationAdditionalFile(self, nCols, nRows, name):
        
    #     self.informationAdditionalFile.setNumberOfCols(nCols)
    #     self.informationAdditionalFile.setNumberOfRows(nRows)
    #     self.informationAdditionalFile.setNameOfFile(name)

class FileInformation():

    
    def __init__(self, nCols = 0, nRows = 0):
        
        self.numColumns = nCols
        self.numRows = nRows

    
    def setNumberOfCols(self, nCols):
        
        self.numColumns = nCols
        
    def setNumberOfRows(self, nRows):
        
        self.numRows = nRows
        
   
    
       
        
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
