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

    colorsPatch = ['cornflowerblue', 'yellowgreen', 'gold', 'tomato', 'lightgreen', 'hotpink', 'tan', 'lightgrey', 'yellow', 'lightcoral', 'darkgrey', 'aqua', 'darkkhaki', 'orchid', 'lightskyblue']
    colorsLine = ['red','blue','green','orange','black','grey']


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
        if self.programState.dataToAnalyse.empty:
            self.resetDataToAnalyse()     

    def deleteRows(self, listOfRowsIndex):
        self.programState.dataToAnalyse.reset_index(drop=True, inplace=True)
        self.programState.dataToAnalyse = self.programState.dataToAnalyse.drop(listOfRowsIndex, axis=0)
        self.recalculateRowsIndexes()
        if self.programState.dataToAnalyse.empty:
            self.resetDataToAnalyse()    


    def renameColumn(self,oldLabel,newLabel):
        self.programState.dataToAnalyse.rename(columns={oldLabel:newLabel},inplace=True)


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

            if str(item) == 'nan':
                arrayToInsert.append(item)
            else:
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

        # No tag selected
        if histogramOptions['secondVarSelected'].encode('utf-8') == 'None'.encode('utf-8'):
            
            dataForChart = self.programState.dataToAnalyse[histogramOptions['firstVarSelected']]
            dataForChart = [ x for x in dataForChart if str(x) != 'nan']

            
            n,bins,patches = plt.hist(dataForChart, histtype='bar', color=self.colorsPatch[0], rwidth=0.75, bins=histogramOptions['numOfBins'])
           
            plt.xlabel(histogramOptions['xAxisName'])
            plt.ylabel(histogramOptions['yAxisName'])
            plt.ylim(0,max(n)*1.1)
            for patch in patches:
                patch.set_edgecolor('white')
            
            
            if (histogramOptions['xAxisGrid'] & histogramOptions['yAxisGrid']):                
                plt.grid()
            
            elif histogramOptions['xAxisGrid']:                
                plt.grid(axis = 'x')
             
            elif histogramOptions['yAxisGrid']:                
                plt.grid(axis = 'y')
                       
            plt.title(histogramOptions['title'], fontsize = 18)
            plt.show()
            
        else: # Some tag has been selected
        
            dataForChart = {}
            selectedCategory = histogramOptions['secondVarSelected']
            tags = self.programState.dataToAnalyse[selectedCategory].unique()
            
            for tag in tags:
                if str(tag) != 'nan':
                    dataForChart[tag] = []

            tagsColumn = self.programState.dataToAnalyse[selectedCategory]
            valuesColumn = self.programState.dataToAnalyse[histogramOptions['firstVarSelected']]

            for i in range(len(valuesColumn)):
                if str(tagsColumn[i]) != 'nan' and str(valuesColumn[i]) != 'nan':
                    dataForChart[tagsColumn[i]].append(valuesColumn[i])

            dataForChart = {k:v for k,v in dataForChart.items() if len(v) != 0}    
            
            colorsTmp = None
            if len(self.colorsPatch)>=len(dataForChart.keys()):
                colorsTmp = self.colorsPatch[0:len(dataForChart)]
            n,bins,patches = plt.hist(dataForChart.values(), histtype='bar',  label=dataForChart.keys(), color=colorsTmp, bins=histogramOptions['numOfBins'])
            
            plt.xlabel(histogramOptions['xAxisName'])
            plt.ylabel(histogramOptions['yAxisName'])

            if type(n[0]) is np.ndarray:            
                n = [data for nl in n for data in nl]
            plt.ylim(0,max(n)*1.1)

            from matplotlib.patches import Rectangle
            if type(patches[0]) is not Rectangle:
                patches = [data for pl in patches for data in pl]
            for patch in patches:
                patch.set_edgecolor('white')
            
            if (histogramOptions['xAxisGrid'] & histogramOptions['yAxisGrid']):                
                plt.grid()
            
            elif histogramOptions['xAxisGrid']:                
                plt.grid(axis = 'x')
             
            elif histogramOptions['yAxisGrid']:                
                plt.grid(axis = 'y')
            
            if histogramOptions['legendPosition'] == "default".encode("utf-8"):
                plt.legend()
            else:
                plt.legend(loc = histogramOptions['legendPosition'])
            
            plt.title(histogramOptions['title'], fontsize = 18)
            plt.show()

    def createScatterPlot(self, scatterOptions):

        if len(scatterOptions['selectedCheckBoxes'])==1:
            xdata = self.programState.dataToAnalyse[scatterOptions['firstVarSelected']]
            ydata = self.programState.dataToAnalyse[scatterOptions['selectedCheckBoxes'][0]]
            plt.scatter(xdata, ydata, s=50)
            xf = 0.05*(max(xdata)-min(xdata))
            yf = 0.05*(max(ydata)-min(ydata))
            xmin = min(xdata)-xf
            xmax = max(xdata)+xf
            plt.xlim(xmin,xmax)
            plt.ylim(min(ydata)-yf,max(ydata)+yf)

            if scatterOptions['linearFit']:
                m,b = np.polyfit(xdata,ydata,1)
                xplotdata = np.array([xmin,xmax])
                plt.plot(xplotdata, m*xplotdata + b, linewidth=2)
                

            
        else:
            for i in range(len(scatterOptions['selectedCheckBoxes'])):
                xdata = self.programState.dataToAnalyse[scatterOptions['firstVarSelected']]
                ydata = self.programState.dataToAnalyse[scatterOptions['selectedCheckBoxes'][i]]
                if i==0:
                    ymin = min(ydata)
                    ymax = max(ydata)
                else:
                    if min(ydata) < ymin:
                        ymin = min(ydata)
                    if max(ydata) > ymax:
                        ymax = max(ydata)

                plt.scatter(xdata, ydata, s=50, color=self.colorsLine[i], label=scatterOptions['selectedCheckBoxes'][i])
            xf = 0.05*(max(xdata)-min(xdata))
            yf = 0.05*(ymax-ymin)
            xmin = min(xdata)-xf
            xmax = max(xdata)+xf
            plt.xlim(xmin,xmax)
            plt.ylim(ymin-yf,ymax+yf)

            if scatterOptions['legendPosition'] == "default".encode("utf-8"):
                plt.legend(scatterpoints=1)
            else:
                plt.legend(loc = scatterOptions['legendPosition'], scatterpoints=1)

            if scatterOptions['linearFit']:
                xplotdata = np.array([xmin,xmax])
                for i in range(len(scatterOptions['selectedCheckBoxes'])):
                    xdata = self.programState.dataToAnalyse[scatterOptions['firstVarSelected']]
                    ydata = self.programState.dataToAnalyse[scatterOptions['selectedCheckBoxes'][i]]
                    m,b = np.polyfit(xdata,ydata,1)
                    plt.plot(xplotdata, m*xplotdata + b, linewidth=2, color=self.colorsLine[i])




        plt.xlabel(scatterOptions['xAxisName'])
        plt.ylabel(scatterOptions['yAxisName'])
        
        if (scatterOptions['xAxisGrid'] & scatterOptions['yAxisGrid']):
            plt.grid()
        elif scatterOptions['xAxisGrid']:
            plt.grid(axis = 'x')
        elif scatterOptions['yAxisGrid']:
            plt.grid(axis = 'y')

        plt.title(scatterOptions['title'], fontsize = 18)
        plt.show()



    def createPieChart(self, pieChartOptions):

        print "##",pieChartOptions['numOfSlices']

        sizes = []
        labels = []
        

        dataForPie = self.programState.dataToAnalyse[pieChartOptions['firstVarSelected']].value_counts() # Number of elements for slice

        numberSamples = self.programState.dataToAnalyse[pieChartOptions['firstVarSelected']].count() # Total of elements

        print dataForPie
        print numberSamples

        explode = None
        if pieChartOptions['offset']:
            explode = []
            for l in dataForPie.index:
                explode.append(0.05)
                    

        for v in dataForPie:
            sizes.append(100.0*v/numberSamples)

        if pieChartOptions['legendPosition'] == "default".encode("utf-8"):
            for l in dataForPie.index:
                labels.append(l)
            patches = plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=self.colorsPatch, explode=explode)
            for patch in patches[0]:
                patch.set_edgecolor('white')
        else:

            for l in dataForPie.index:
                labels.append(l)
            patches = plt.pie(sizes, autopct = '%1.1f%%', startangle=90, colors=self.colorsPatch, explode=explode)
            for patch in patches[0]:
                patch.set_edgecolor('white')
            plt.legend(patches[0], labels, loc = pieChartOptions['legendPosition'])
        
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        plt.axis('equal')
        plt.tight_layout()
        plt.title(pieChartOptions['title'],fontsize=18)                
        plt.show()
        


    def createBoxPlot(self, boxPlotOptions):

        flierprops = dict(marker='o',markerfacecolor='white', markersize=8, linestyle='none')
        # No categorical variable was selected
        if boxPlotOptions.getSecondVarSelected() == 'None':
            
            bplot = self.programState.dataToAnalyse.plot.box(y = boxPlotOptions.getSelectedCheckBoxes(),
                                                    rot=45,grid = boxPlotOptions.getShowGrid(),
                                                    return_type='dict',
                                                    patch_artist=True, flierprops=flierprops)

            for patch, color in zip(bplot['boxes'], self.colorsPatch):
                patch.set_facecolor(color)

        else: # Some categorical value was selected => subplots
            
            
            plotBoxes = boxPlotOptions.getSelectedCheckBoxes()
            result = self.programState.dataToAnalyse

            bplots = result.boxplot(column = boxPlotOptions.getSelectedCheckBoxes(), by=str(boxPlotOptions.getSecondVarSelected()),
                           rot=45,grid = boxPlotOptions.getShowGrid(), return_type='dict', patch_artist=True, flierprops=flierprops)
            
            for key in bplots.keys():
                for patch, color in zip(bplots[key]['boxes'], self.colorsPatch):
                    patch.set_facecolor(color)
            
        plt.suptitle(boxPlotOptions.getChartTitle(),fontsize=18)
        plt.show()    
    


    def createBarChart(self, barChartOptions, operation):

        # No tag selected
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
            
        else: # Some tag has been selected
        
            dataForChart = {}
            selectedCategory = barChartOptions.getSecondVarSelected()
            tags = self.programState.dataToAnalyse[selectedCategory].unique()

            
            for tag in tags:
                if str(tag) != 'nan':
                    dataForChart[tag] = []
    
            tagsColumn = self.programState.dataToAnalyse[selectedCategory]
            valuesColumn = self.programState.dataToAnalyse[barChartOptions.getFirstVarSelected()]

            for i in range(len(valuesColumn)):
                if str(tagsColumn[i]) != 'nan' and str(valuesColumn[i]) != 'nan':
                    dataForChart[tagsColumn[i]].append(valuesColumn[i])

            dataForChart = {k:v for k,v in dataForChart.items() if len(v) != 0}
              
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
    
            plt.xlabel(barChartOptions.getXAxisName())
            plt.ylabel(barChartOptions.getYAxisName())
            
            if (barChartOptions.getXAxisGrid() & barChartOptions.getYAxisGrid()):
                
                plt.grid()
            
            elif barChartOptions.getXAxisGrid():
                
                plt.grid(axis = 'x')
             
            elif barChartOptions.getYAxisGrid():
                
                plt.grid(axis = 'y')
            
            plt.title(barChartOptions.getChartTitle(), fontsize = 18)
            
            plt.show()
    
    

    def nullValuesInFile(self, data): 
         
        return pandas.isnull(data).values.any()
