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
    

class ProgramState():
    
    def __init__(self):
                
        self.dataToAnalyse = None
        self.checkBoxStatus = []
        self.comboBoxStatus = {}
        
        self.informationFile = FileInformation()
        
    
    def setInformationFile(self, nCols, nRows):
        self.informationFile.setNumberOfCols(nCols)
        self.informationFile.setNumberOfRows(nRows)
        
        
class FileInformation():

    
    def __init__(self, nCols = 0, nRows = 0):
        self.numColumns = nCols
        self.numRows = nRows
    
    def setNumberOfCols(self, nCols):
        self.numColumns = nCols
        
    def setNumberOfRows(self, nRows):
        self.numRows = nRows
        
   

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
