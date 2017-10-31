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

import sys
import pandas
from pandas import concat
import numpy as np

import sys
if sys.platform=="darwin":
    import matplotlib
    matplotlib.use('WXAgg')
import matplotlib.pyplot as plt

from Model import  ProgramState


class Controller():
    
    #Main variables    
    programState = ProgramState()

    characterValues = []
    floatValues = []
    integerValues = []


    def ConcatDataFrame(self, dataFrame_1, dataFrame_2):

        dataFrame_1.reset_index(drop=True, inplace=True)
        dataFrame_2.reset_index(drop=True, inplace=True)
               
        nameColumns = list(dataFrame_1.columns)
        
        for column in dataFrame_2.columns:
            
            colIndex=2
            auxColumn = str(column)
            while auxColumn in dataFrame_1.columns:
                auxColumn = str(column) + "_" + str(colIndex)
                colIndex += 1
                    
            nameColumns.append(auxColumn)
            
        self.data = concat([dataFrame_1,dataFrame_2], axis = 1)
        
        self.data.columns = nameColumns
        
        return self.data

   

    def OpenFile (self, data):
         
        self.programState.quantitativeData = data
        self.programState.dataToAnalyse = data
        try:
            self.recalculateRowsIndexes()
        except:
            # print "Error: ", sys.exc_info()[0] 
            None

        self.programState.setInformationFile(len(data.columns), len(data.index))



    def OpenAdditionalFile (self,data):
         
        try:
            sameNumberRows = False
            
            self.programState.qualitativeData = data

            
            if len(data.index) == (self.programState.informationFile.numRows):
                
                sameNumberRows = True
            
            if self.programState.qualitativeData is not None:
                
                self.programState.dataToAnalyse = self.ConcatDataFrame(self.programState.quantitativeData, self.programState.qualitativeData)
                self.programState.quantitativeData = self.programState.dataToAnalyse
                # self.programState.setInformationAdditionalFile(len(data.columns), len(data.index), nameOfFile)
                self.recalculateRowsIndexes()
    
            return sameNumberRows
        
        except:
            
            print "Error: ", sys.exc_info()[0]

    
    
    
    def getDataToAnalyse(self):
        
        return self.programState.dataToAnalyse       



    def getNumberOfColumns(self):
        
        return len(self.programState.dataToAnalyse.columns)


    
    def getNumberOfRows(self):
        
        return len(self.programState.dataToAnalyse.index)


    
    def getLabelsOfColumns(self):
        
        return self.programState.dataToAnalyse.columns



    def deleteColumns(self, listOfColumnsName):
        self.programState.dataToAnalyse = self.programState.dataToAnalyse.drop(labels = listOfColumnsName, axis = 1)
        self.recalculateRowsIndexes()
        if self.programState.dataToAnalyse.empty:
            self.resetDataToAnalyse()     


    def deleteRows(self, listOfRowsIndex):
        self.programState.dataToAnalyse.reset_index(drop=True, inplace=True)
        self.programState.dataToAnalyse = self.programState.dataToAnalyse.drop(listOfRowsIndex, axis=0)
        self.recalculateRowsIndexes()
        if self.programState.dataToAnalyse.empty:
            self.resetDataToAnalyse()    

    def recalculateRowsIndexes(self):
        newIndexes = range(1,len(self.programState.dataToAnalyse.index)+1)
        self.programState.dataToAnalyse.reindex(newIndexes)
        self.programState.dataToAnalyse.reset_index(drop=True, inplace=True)


        
    def sortVariables(self):
       
        '''
        Check  the type of the variables saved on Dataframe: int, float or string
        '''  
        colsDataframe = self.programState.dataToAnalyse.columns      
        
        del self.floatValues[:]
        del self.characterValues[:]
        del self.integerValues[:]
        
        for col in colsDataframe:
                          
            if self.programState.dataToAnalyse[col].dtypes == 'int64':
                
                self.integerValues.append(col)
            
            elif self.programState.dataToAnalyse[col].dtypes == 'float64':
                
                self.floatValues.append(col)
                
            else:
                
                self.characterValues.append(col)
    
    '''
    def initializationComboBox(self):
        
        self.programState.initializationComboBoxStatus(self.characterValues)
    '''
    
    def resetDataToAnalyse(self):
        
        for column in self.programState.dataToAnalyse.columns:
        
            del self.programState.dataToAnalyse[column]


        
    def exportData(self, filePath, exportOptions):
        
        self.programState.dataToAnalyse.to_csv(path_or_buf = filePath, sep = exportOptions.getFieldDelimiter(),
                                               header = exportOptions.getWriteColNames(), index = exportOptions.getWriteRowNames(),
                                               encoding = exportOptions.getCharacterSet(), decimal = exportOptions.getDecimalSeparator())    
        
    

    def addColumn(self, factorsFromInterface, nameRadioButton, tagRestValues, nameOFFactor):
        
        self.isInRange = False
        self.itemAdded = False
        arrayToInsert = []
        dictKeys = factorsFromInterface.keys()
 
        
        for i in (self.programState.dataToAnalyse.index):
            
            item = self.programState.dataToAnalyse.loc[i, nameRadioButton]
            
            for factor in dictKeys:
                
                if ( (item >= factorsFromInterface[factor][0]) and (item <= factorsFromInterface[factor][1])):
                    
                    arrayToInsert.append(factor)
                    self.isInRange = True
                    self.itemAdded = True

                else:
                    if ((factor == dictKeys[-1]) and (self.isInRange == False) and (self.itemAdded == False)): 
                        arrayToInsert.append(tagRestValues)
                self.isInRange = False
                
            self.itemAdded = False

        self.programState.dataToAnalyse.insert(len(self.programState.dataToAnalyse.columns), nameOFFactor, arrayToInsert)
        

    
    def createHistogram(self, histogramOptions):

        if histogramOptions.getSecondVarSelected().encode('utf-8') == 'Not use label'.encode('utf-8'):
            
            dataForChart = self.programState.dataToAnalyse[histogramOptions.getFirstVarSelected()]
            
            plt.hist(dataForChart, 10, normed=1, histtype='bar')
            plt.title(histogramOptions.getChartTitle())
            plt.xlabel(histogramOptions.getXAxisName())
            plt.ylabel(histogramOptions.getYAxisName())
            
            if (histogramOptions.getXAxisGrid() & histogramOptions.getYAxisGrid()):
                
                plt.grid()
            
            elif histogramOptions.getXAxisGrid():
                
                plt.grid(axis = 'x')
             
            elif histogramOptions.getYAxisGrid():
                
                plt.grid(axis = 'y')

            
            if histogramOptions.getLegendPosition() != "by default".encode("utf-8"):
                
                plt.legend(loc = histogramOptions.getLegendPosition())
            
            
            plt.show()
            
        else:
        
            dataForChart = {}
            tags = self.programState.dataToAnalyse[histogramOptions.getSecondVarSelected()].unique()
            
            for tag in tags:
                dataForChart[tag] = []
    
            
            
            for i in range(len(self.programState.dataToAnalyse.index)):
    
                dataForChart[self.programState.dataToAnalyse.loc[i+1, histogramOptions.getSecondVarSelected()]].append(self.programState.dataToAnalyse.loc[i+1, histogramOptions.getFirstVarSelected()])

            labels = []
            for i in tags:
                labels.append(i)
                
            
            tags = np.asarray(tags)
            plt.hist(dataForChart.values(), 10, normed=1, histtype='bar',  label=labels)
            plt.legend()
            plt.title(histogramOptions.getChartTitle())
            plt.xlabel(histogramOptions.getXAxisName())
            plt.ylabel(histogramOptions.getYAxisName())
            
            if (histogramOptions.getXAxisGrid() & histogramOptions.getYAxisGrid()):
                
                plt.grid()
            
            elif histogramOptions.getXAxisGrid():
                
                plt.grid(axis = 'x')
             
            elif histogramOptions.getYAxisGrid():
                
                plt.grid(axis = 'y')
            
            
            if histogramOptions.getLegendPosition() != "by default".encode("utf-8"):
                
                plt.legend(loc = histogramOptions.getLegendPosition())
            
            plt.show()



    def createScatterPlot(self, scatterOptions):
        
        plt.scatter(self.programState.dataToAnalyse[scatterOptions.getFirstVarSelected()], 
                    self.programState.dataToAnalyse[scatterOptions.getSecondVarSelected()])
        plt.title(scatterOptions.getChartTitle())
        plt.xlabel(scatterOptions.getXAxisName())
        plt.ylabel(scatterOptions.getYAxisName())
        
        if (scatterOptions.getXAxisGrid() & scatterOptions.getYAxisGrid()):
            
            plt.grid()
        
        elif scatterOptions.getXAxisGrid():
            
            plt.grid(axis = 'x')
         
        elif scatterOptions.getYAxisGrid():
            
            plt.grid(axis = 'y')
               
        plt.show()

  
    def createPieChart(self, pieChartOptions):

        sizes = []
        explode = []
        labels = []

        dataForPie = self.programState.dataToAnalyse[pieChartOptions.getFirstVarSelected()].value_counts()
        numberSamples = self.programState.dataToAnalyse[pieChartOptions.getFirstVarSelected()].count()

        for v in dataForPie:
            sizes.append(100.0*v/numberSamples)
            explode.append(0.05)


        # colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
        if pieChartOptions.getLegendPosition() == "by default".encode("utf-8"):
            for l in dataForPie.index:
                labels.append(l)
            plt.pie(sizes, labels=labels, explode = explode, autopct='%1.1f%%', shadow=True, startangle=90)
        else:
            for l in range(len(sizes)):
                labels.append('{} ({:.2f}%)'.format(dataForPie.index[l],sizes[l]))
            patches, text = plt.pie(sizes, explode = explode, shadow=True, startangle=90)
            plt.legend(patches, labels, loc = pieChartOptions.getLegendPosition())
        
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        plt.axis('equal')
        plt.tight_layout()
        plt.title(pieChartOptions.getChartTitle())                
        plt.show()
        
        
    def createBoxPlot(self, boxPlotOptions):

        if boxPlotOptions.getSecondVarSelected() == 'None':
            
            self.programState.dataToAnalyse.plot.box(y = boxPlotOptions.getSelectedCheckBoxes(),
                                                    rot = -45, grid = boxPlotOptions.getShowGrid(),
                                                    return_type='dict', title = boxPlotOptions.getChartTitle())
        else:
            
            result = self.programState.dataToAnalyse
                                                    
            result.boxplot(column = boxPlotOptions.getSelectedCheckBoxes(), by=str(boxPlotOptions.getSecondVarSelected()),
                           rot = -45, grid = boxPlotOptions.getShowGrid(), return_type='dict')
        plt.suptitle(boxPlotOptions.getChartTitle())
        plt.show()    
    


    def createBarChart(self, barChartOptions, operation):

        if barChartOptions.getSecondVarSelected().encode('utf-8') == 'None'.encode('utf-8'):
            
            if operation == 'Mean':
                dataForChart = self.programState.dataToAnalyse[barChartOptions.getFirstVarSelected()].mean()
                
            elif operation == 'Median':
                dataForChart = self.programState.dataToAnalyse[barChartOptions.getFirstVarSelected()].median()

            elif operation == 'Variance':
                dataForChart = self.programState.dataToAnalyse[barChartOptions.getFirstVarSelected()].var()

            else:
                dataForChart = self.programState.dataToAnalyse[barChartOptions.getFirstVarSelected()].std()

    
            names = [str(barChartOptions.getFirstVarSelected())]
            y_pos = np.arange(len(names))
            
            plt.bar(y_pos, dataForChart, align='center', alpha=0.5)
            plt.xticks(y_pos, names)
            
            plt.title(barChartOptions.getChartTitle())
            plt.xlabel(barChartOptions.getXAxisName())
            plt.ylabel(barChartOptions.getYAxisName())
            
            if (barChartOptions.getXAxisGrid() & barChartOptions.getYAxisGrid()):
                
                plt.grid()
            
            elif barChartOptions.getXAxisGrid():
                
                plt.grid(axis = 'x')
             
            elif barChartOptions.getYAxisGrid():
                
                plt.grid(axis = 'y')
                
            plt.show()
            
        else:
        
            dataForChart = {}
            tags = self.programState.dataToAnalyse[barChartOptions.getSecondVarSelected()].unique()
            
            for tag in tags:
                dataForChart[tag] = []
    

            for i in range(len(self.programState.dataToAnalyse.index)):
                temp = self.programState.dataToAnalyse.loc[i+1, barChartOptions.getFirstVarSelected()]
        
                dataForChart[self.programState.dataToAnalyse.loc[i+1, barChartOptions.getSecondVarSelected()]].append(temp)
              
            labels = []
            for i in tags:
                labels.append(i)
                
                
            results = []  
            if operation == 'Mean':
                
                for data in dataForChart.values():
                    temp2 = pandas.Series(data)
                    results.append(temp2.mean())

            elif operation == 'Median':
            
                for data in dataForChart.values():
                    temp2 = pandas.Series(data)
                    results.append(temp2.median())

            elif operation == 'Variance':
                for data in dataForChart.values():
                    temp2 = pandas.Series(data)
                    results.append(temp2.var())

            else:
                for data in dataForChart.values():
                    temp2 = pandas.Series(data)
                    results.append(temp2.std())

                
            tags = np.asarray(tags)
            plt.bar(range(len(dataForChart)), results, align='center')
            plt.xticks(range(len(dataForChart)), dataForChart.keys())
    
            plt.title(barChartOptions.getChartTitle())
            plt.xlabel(barChartOptions.getXAxisName())
            plt.ylabel(barChartOptions.getYAxisName())
            
            if (barChartOptions.getXAxisGrid() & barChartOptions.getYAxisGrid()):
                
                plt.grid()
            
            elif barChartOptions.getXAxisGrid():
                
                plt.grid(axis = 'x')
             
            elif barChartOptions.getYAxisGrid():
                
                plt.grid(axis = 'y')
            
            plt.show()
    
    

    def nullValuesInFile(self, data): 
         
        return pandas.isnull(data).values.any()
