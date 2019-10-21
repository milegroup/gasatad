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

import wx
import wx.xrc
import wx.richtext as rt
import wx.lib.scrolledpanel

from pandas.core.frame import DataFrame, Series
from scipy.stats import shapiro, normaltest, gmean, hmean, kstest

import Tools
from numpy import nan as NaN
import numpy as np


class BasicStatisticsInterface(wx.Dialog):

    def __init__(self, parent, namesCheckBox, tagsAndValues, integerValues, dataFrame):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Basic statistics", size=(1024, 600),
                           pos=wx.DefaultPosition)

        self.SetMinSize((640, 480))

        self.dataToAnalyse = dataFrame

        # Inicialización de las listas necesarias para obtener las opciones elegidas por el usuario
        # self.listOfCheckBoxes = []

        # self.checkBoxStatus = {}

        self.listOfSpinCtrl = []

        self.intervalNameAndLimitsLeft = {}

        self.activatedCheckBoxes = []

        # self.checkBoxTagLeft = []

        self.selectedCheckBoxes = []

        self.selectedVariablesInColumn = dict.fromkeys(tagsAndValues.keys())

        # The values of each key in the dictionary are initialized as an empty list
        for key in self.selectedVariablesInColumn.keys():
            self.selectedVariablesInColumn[key] = []

        self.integerValues = integerValues

        # Panel for all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)

        # Definition of the scrolled panel
        self.scrolledPanel = wx.lib.scrolledpanel.ScrolledPanel(self.panel, -1, style=wx.TAB_TRAVERSAL)

        self.scrolledPanel.SetAutoLayout(1)
        self.scrolledPanel.SetupScrolling()

        self.scrollSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.leftSizer = wx.BoxSizer(wx.VERTICAL)

        dataSelectionSizer = wx.StaticBoxSizer(wx.StaticBox(self.scrolledPanel, wx.ID_ANY, u"Data set"), wx.VERTICAL)

        self.leftSizer.Add(dataSelectionSizer, 0, wx.EXPAND | wx.ALL, 10)

        self.scrollSizer.Add(self.leftSizer)

        fgSizer = wx.FlexGridSizer(0, 1, 0, 0)
        fgSizer.SetFlexibleDirection(wx.BOTH)
        fgSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        dataSelectionSizer.Add(fgSizer, 1, wx.ALL | wx.EXPAND, 5)

        # Sizer for checkboxes (numerical columns)
        checkSizer = wx.FlexGridSizer(0, 3, 0, 0)
        checkSizer.SetFlexibleDirection(wx.BOTH)
        checkSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        fgSizer.Add(checkSizer, 0, wx.ALL | wx.EXPAND, 5)

        for i in namesCheckBox:
            self.m_checkBox = wx.CheckBox(self.scrolledPanel, wx.ID_ANY, i, wx.DefaultPosition, wx.DefaultSize, 0)
            checkSizer.Add(self.m_checkBox, 0, wx.LEFT | wx.EXPAND, 5)
            # self.listOfCheckBoxes.append(self.m_checkBox)

            self.Bind(wx.EVT_CHECKBOX, self.changeValueCheckBox, self.m_checkBox)

        # Sizer for tags (text columns)
        tagsSizer = wx.FlexGridSizer(0, 4, 10, 0)
        tagsSizer.SetFlexibleDirection(wx.BOTH)
        tagsSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        fgSizer.Add(tagsSizer, 1, wx.ALL | wx.EXPAND, 5)

        for tag, values in tagsAndValues.items():

            # self.checkBoxTagLeft.append(SelectedValuesOfTag(tag, values))

            sbSizer = wx.StaticBoxSizer(wx.StaticBox(self.scrolledPanel, wx.ID_ANY, tag), wx.VERTICAL)

            for j in values:
                self.m_checkBox = wx.CheckBox(parent=self.scrolledPanel, id=wx.ID_ANY, label=j,
                                              pos=wx.DefaultPosition, size=wx.DefaultSize, name=tag)
                sbSizer.Add(self.m_checkBox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
                self.Bind(wx.EVT_CHECKBOX, self.changeValueTagCheckBox, self.m_checkBox)

            tagsSizer.Add(sbSizer, 0, wx.EXPAND | wx.ALL, 10)

        # INTEGER VALUES
        if integerValues:

            # Sizer for selecting range of numerical values
            auxSizer2 = wx.FlexGridSizer(0, 5, 0, 0)
            auxSizer2.SetFlexibleDirection(wx.BOTH)
            auxSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
            fgSizer.Add(auxSizer2, 0, wx.ALL | wx.EXPAND, 5)

            for i in integerValues:
                minumum = int(min(self.dataToAnalyse[i]))
                maximum = int(max(self.dataToAnalyse[i]))

                self.m_checkBox = wx.CheckBox(self.scrolledPanel, wx.ID_ANY, i, wx.DefaultPosition, wx.DefaultSize, 0)
                self.m_checkBox.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD, False, wx.EmptyString))
                self.Bind(wx.EVT_CHECKBOX, self.changeStatusSpinCtrl, self.m_checkBox)

                auxSizer2.Add(self.m_checkBox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

                self.m_staticText11 = wx.StaticText(self.scrolledPanel, wx.ID_ANY, u"From:", wx.DefaultPosition,
                                                    wx.DefaultSize, 0)
                self.m_staticText11.Wrap(-1)
                auxSizer2.Add(self.m_staticText11, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 5)

                self.m_spinCtrl11 = wx.SpinCtrlDouble(self.scrolledPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                      # wx.DefaultSize,
                                                      wx.Size(130, -1),
                                                      # wx.SP_ARROW_KEYS | wx.ALIGN_RIGHT,
                                                      wx.SPLIT_VERTICAL,
                                                      minumum,
                                                      maximum, minumum, 1, i + "-LimitInf")

                auxSizer2.Add(self.m_spinCtrl11, 0, wx.ALL, 5)
                self.m_spinCtrl11.Enable(False)

                self.m_staticText21 = wx.StaticText(self.scrolledPanel, wx.ID_ANY, u"To:", wx.DefaultPosition,
                                                    wx.DefaultSize, 0)
                self.m_staticText21.Wrap(-1)
                auxSizer2.Add(self.m_staticText21, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 5)

                self.m_spinCtrl21 = wx.SpinCtrlDouble(self.scrolledPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                      wx.Size(130, -1),
                                                      # wx.DefaultSize,
                                                      wx.SP_ARROW_KEYS | wx.ALIGN_RIGHT, minumum,
                                                      maximum, maximum, 1, i + "-LimitSup")
                auxSizer2.Add(self.m_spinCtrl21, 0, wx.ALL, 5)
                self.m_spinCtrl21.Enable(False)

                self.listOfSpinCtrl.append(self.m_spinCtrl11)
                self.listOfSpinCtrl.append(self.m_spinCtrl21)


        self.textResultsWindow = rt.RichTextCtrl(self.scrolledPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                 wx.DefaultSize,
                                                 wx.VSCROLL | wx.HSCROLL | wx.TE_MULTILINE | wx.TE_READONLY | wx.NO_BORDER)
        self.textResultsWindow.SetMargins((20, 20))

        self.scrollSizer.Add(self.textResultsWindow, 1, wx.EXPAND | wx.ALL, 10)

        self.scrolledPanel.SetSizer(self.scrollSizer)

        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(self.scrolledPanel, 1, wx.EXPAND)

        close = wx.Button(self.panel, wx.ID_CANCEL, label="Close")
        showResults = wx.Button(self.panel, wx.ID_ANY, label="Show results")
        self.Bind(wx.EVT_BUTTON, self.calculateData, showResults)
        sizerBtns = wx.BoxSizer(wx.HORIZONTAL)
        sizerBtns.Add(showResults, 1, wx.EXPAND | wx.ALL, 5)
        sizerBtns.Add(close, 1, wx.EXPAND | wx.ALL, 5)
        panelSizer.Add(sizerBtns, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.panel.SetSizer(panelSizer)
        self.Centre(wx.BOTH)
        self.Show(True)

    def changeStatusSpinCtrl(self, event):

        checkBox = event.GetEventObject()

        if checkBox.IsChecked():

            self.activatedCheckBoxes.append(checkBox.GetLabel())

            i = 0

            while checkBox.GetLabel() != self.listOfSpinCtrl[i].GetName().split("-")[0]:
                i = i + 1

            if checkBox.GetLabel() == self.listOfSpinCtrl[i].GetName().split("-")[0]:
                self.listOfSpinCtrl[i].Enable()
                self.listOfSpinCtrl[i + 1].Enable()

        else:

            self.activatedCheckBoxes.remove(checkBox.GetLabel())

            i = 0

            while checkBox.GetLabel() != self.listOfSpinCtrl[i].GetName().split("-")[0]:
                i = i + 1

            if checkBox.GetLabel() == self.listOfSpinCtrl[i].GetName().split("-")[0]:
                self.listOfSpinCtrl[i].Enable(False)
                self.listOfSpinCtrl[i + 1].Enable(False)

                # self.listIntervalNameAndLimits.pop(i)

    def changeValueCheckBox(self, event):

        checkBox = event.GetEventObject()

        if checkBox.IsChecked():

            self.selectedCheckBoxes.append(checkBox.GetLabel())

        else:

            self.selectedCheckBoxes.remove(checkBox.GetLabel())

    def changeValueTagCheckBox(self, event):

        checkBox = event.GetEventObject()

        label = checkBox.GetLabel()
        nameCheckBox = checkBox.GetName()

        if checkBox.IsChecked():

            self.selectedVariablesInColumn[nameCheckBox].append(label)

        else:

            self.selectedVariablesInColumn[nameCheckBox].remove(label)

    def getSelectedData(self):

        self.intervalNameAndLimitsLeft.clear()
        # Obtain values from spinctrl to check them

        for checkBox in self.activatedCheckBoxes:
            i = 0

            while checkBox != self.listOfSpinCtrl[i].GetName().split("-")[0]:
                i = i + 1

            if checkBox == self.listOfSpinCtrl[i].GetName().split("-")[0]:
                limitInf = self.listOfSpinCtrl[i].GetValue()
                limitSup = self.listOfSpinCtrl[i + 1].GetValue()
                self.intervalNameAndLimitsLeft[checkBox] = [limitInf, limitSup]

        self.wrongInterval = False

        for nameVariable, paarList in self.intervalNameAndLimitsLeft.items():
            if paarList[0] > paarList[1]:
                self.wrongInterval = True

        if not self.selectedCheckBoxes:
            self.noCheckBoxSelectedWarning()
            return DataFrame()

        elif self.wrongInterval:
            self.wrongIntervalWarning()
            return DataFrame()

        else:  # Everything is Ok

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
                    for nameVariable, paarList in self.intervalNameAndLimitsLeft.items():

                        auxIndex = []
                        # if -1 not in paarList:
                        for i in range(len(self.dataToAnalyse.index)):
                            if ((self.dataToAnalyse.loc[i, nameVariable] >= paarList[0])
                                    and (self.dataToAnalyse.loc[i, nameVariable] <= paarList[1])):
                                auxIndex.append(i)
                        indices.append(auxIndex)
                        # del auxIndex[:]

                # se crea una única lista en la que se concatenan las obtenidas anteriormente
                auxIndices2 = []

                for i in range(len(indices)):
                    auxIndices2.extend(indices[i])

                for i in range(len(indices[0])):
                    if auxIndices2.count(indices[0][i]) == len(
                            indices):  # Si es igual a esto quiere decir que cumple todas las condiciones seleccionadas en la interfaz gráfica
                        indicesToReturn.append(indices[0][i])

            else:  # tempList (marked discrete variables) is not empty

                auxIndex1 = []

                for name, value in self.selectedVariablesInColumn.items():

                    if value:
                        tagsColumn = self.dataToAnalyse[name]
                        auxIndex1 = [x for x in range(len(tagsColumn)) if tagsColumn[x] in value]
                        indices.append(auxIndex1)

                    # if value:
                    #     auxIndex1 = []
                    #     for i in range(len(self.dataToAnalyse.index)):

                    #         if (self.dataToAnalyse.loc[i+1,name] in value):

                    #             auxIndex1.append(i+1)

                    #     indices.append(auxIndex1)

                if self.intervalNameAndLimitsLeft:
                    for nameVariable, paarList in self.intervalNameAndLimitsLeft.items():

                        auxIndex = []
                        # if -1 not in paarList:

                        for i in range(len(self.dataToAnalyse.index)):

                            if ((self.dataToAnalyse.loc[i, nameVariable] >= paarList[0])
                                    and (self.dataToAnalyse.loc[i, nameVariable] <= paarList[1])):
                                auxIndex.append(i + 1)

                        indices.append(auxIndex)
                        # del auxIndex[:]

                # se crea una única lista en la que se concatenan las obtenidas anteriormente
                auxIndices2 = []

                for i in range(len(indices)):
                    auxIndices2.extend(indices[i])

                for i in range(len(indices[0])):

                    if auxIndices2.count(indices[0][i]) == len(
                            indices):  # Si es igual a esto quiere decir que cumple todas las condiciones
                        # seleccionadas en la interfaz gráfica
                        indicesToReturn.append(indices[0][i])

            return self.dataToAnalyse.loc[indicesToReturn, self.selectedCheckBoxes]

    def calculateData(self, event):

        self.textResultsWindow.Clear()

        data = self.getSelectedData()

        if not data.empty:

            Tools.setFont(self.textResultsWindow)

            Tools.writeTitle(self.textResultsWindow, "BASIC STATISTICS")

            Tools.writeParam(self.textResultsWindow, "No. of values")
            Tools.writeResults(self.textResultsWindow, data.count())

            Tools.writeParam(self.textResultsWindow, "Minimum")
            Tools.writeResults(self.textResultsWindow, data.min())

            Tools.writeParam(self.textResultsWindow, "Maximum")
            Tools.writeResults(self.textResultsWindow, data.max())

            Tools.writeParam(self.textResultsWindow, "Mean")
            Tools.writeResults(self.textResultsWindow, data.mean())

            Tools.writeParam(self.textResultsWindow, "Geometric mean")
            series_data = Series()
            for key in data.columns:
                dd = np.array(data[key].dropna(), dtype='float64')
                if np.amin(dd) < 0:
                    series_data[key] = '--'
                else:
                    series_data[key] = gmean(dd)
            Tools.writeResults(self.textResultsWindow, series_data)

            Tools.writeParam(self.textResultsWindow, "Harmonic mean")
            series_data = Series()
            for key in data.columns:
                dd = np.array(data[key].dropna(), dtype='float64')
                if np.amin(dd) < 0:
                    series_data[key] = '--'
                else:
                    series_data[key] = hmean(dd)
            Tools.writeResults(self.textResultsWindow, series_data)

            Tools.writeParam(self.textResultsWindow, "Median")
            Tools.writeResults(self.textResultsWindow, data.median())

            Tools.writeParam(self.textResultsWindow, "Mode")
            dd = data.mode()
            Tools.writeResults(self.textResultsWindow, dd.head(10))
            numDataMode = dd.count().tolist()
            if any(t > 10 for t in numDataMode):
                Tools.writeComment(self.textResultsWindow, 'Mode data truncated. Number of elements is')
                Tools.writeComment(self.textResultsWindow, dd.count().to_string())

            Tools.writeParam(self.textResultsWindow, "Std Deviation")
            Tools.writeResults(self.textResultsWindow, data.std())

            Tools.writeParam(self.textResultsWindow, "Variance")
            Tools.writeResults(self.textResultsWindow, data.var())

            Tools.writeParam(self.textResultsWindow, "Covariance")
            Tools.writeResults(self.textResultsWindow, data.cov())

            Tools.writeParam(self.textResultsWindow, "Quantile 25%")
            Tools.writeResults(self.textResultsWindow, data.quantile(q=0.25))

            Tools.writeParam(self.textResultsWindow, "Quantile 50%")
            Tools.writeResults(self.textResultsWindow, data.quantile(q=0.5))

            Tools.writeParam(self.textResultsWindow, "Quantile 75%")
            Tools.writeResults(self.textResultsWindow, data.quantile(q=0.75))

            Tools.writeParam(self.textResultsWindow, "Correlation (Pearson)")
            Tools.writeResults(self.textResultsWindow, data.corr(method='pearson'))

            Tools.writeParam(self.textResultsWindow, "Gini coefficient")
            series_data = Series()
            for key in data.columns:
                dd = np.array(data[key].dropna(), dtype='float64')
                if np.amin(dd) < 0:
                    # Values cannot be negative:
                    dd -= np.amin(dd)
                # Values cannot be 0:
                dd += 0.0000001
                # Values must be sorted:
                dd = np.sort(dd)
                # Index per array element:
                index = np.arange(1, len(dd) + 1)
                # Number of array elements:
                n = len(dd)
                # Gini coefficient:
                gini = ((np.sum((2 * index - n - 1) * dd)) / (n * np.sum(dd)))
                series_data[key] = gini
            Tools.writeResults(self.textResultsWindow, series_data)

            Tools.writeParam(self.textResultsWindow, "Kurtosis")
            Tools.writeComment(self.textResultsWindow, "Fisher's kurtosis normalized by N-1 (normal = 0.0)")
            Tools.writeResults(self.textResultsWindow, data.kurtosis())
            if len(data[data.columns[0]])<20:
                Tools.writeComment(self.textResultsWindow, 'Warning: kurtosis test only valid for n>=20')

            Tools.writeParam(self.textResultsWindow, "Skew")
            Tools.writeComment(self.textResultsWindow, "Unbiased skew normalized by N-1")
            Tools.writeResults(self.textResultsWindow, data.skew())

            Tools.writeParam(self.textResultsWindow, "Shapiro-Wilk test")
            Tools.writeComment(self.textResultsWindow, "H0: the sample follows a Gaussian distribution")
            Tools.writeComment(self.textResultsWindow, "H1: the sample does not follow a Gaussian distribution")
            df_aux = DataFrame(columns=['statistic', 'p-value'])
            for key in data.columns:
                try:
                    ss = shapiro(data[key].dropna().tolist())
                    df_aux.loc[key] = [ss[0], ss[1]]
                except ValueError:
                    df_aux.loc[key] = [NaN, NaN]
            Tools.writeResults(self.textResultsWindow, df_aux)

            Tools.writeParam(self.textResultsWindow, "D'Agostino's K-squared test")
            Tools.writeComment(self.textResultsWindow, "H0: the sample follows a Gaussian distribution")
            Tools.writeComment(self.textResultsWindow, "H1: the sample does not follow a Gaussian distribution")
            df_aux = DataFrame(columns=['statistic', 'p-value'])
            for key in data.columns:
                try:
                    ss = normaltest(data[key].dropna().tolist())
                    df_aux.loc[key] = [ss[0], ss[1]]
                except ValueError:
                    df_aux.loc[key] = [NaN, NaN]
            Tools.writeResults(self.textResultsWindow, df_aux)


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
