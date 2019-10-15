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


# import wx.xrc

class HistogramInterface(wx.Dialog):
    legendPosition = 'default'

    def __init__(self, parent, listOfVariables, listOfTags, histogramOptions):

        self.listOfVariables = listOfVariables

        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Histogram", size=wx.DefaultSize, pos=wx.DefaultPosition)

        gbSizer1 = wx.GridBagSizer(0, 0)
        gbSizer1.SetFlexibleDirection(wx.BOTH)
        gbSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # -------------------------------

        # Histogram options

        fgSizerchartOptions = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizerchartOptions.SetFlexibleDirection(wx.BOTH)
        fgSizerchartOptions.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        fgSizerchartOptions.AddGrowableCol(1)

        self.histogramName = wx.StaticText(self, wx.ID_ANY, u"Histogram title:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.histogramName.Wrap(-1)
        fgSizerchartOptions.Add(self.histogramName, 0, wx.ALIGN_CENTER | wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.histogramNameTextCtrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizerchartOptions.Add(self.histogramNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL, 5)

        self.xAxisName = wx.StaticText(self, wx.ID_ANY, u"X-axis label:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.xAxisName.Wrap(-1)
        fgSizerchartOptions.Add(self.xAxisName, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.xAxisNameTextCtrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizerchartOptions.Add(self.xAxisNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL, 5)

        self.yAxisName = wx.StaticText(self, wx.ID_ANY, u"Y-axis label:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.yAxisName.Wrap(-1)
        fgSizerchartOptions.Add(self.yAxisName, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.yAxisNameTextCtrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizerchartOptions.Add(self.yAxisNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL, 5)

        gbSizer1.Add(fgSizerchartOptions, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.ALL, 5)

        # -------------------------------

        # Display Grid 

        displayGridsSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Display settings"), wx.HORIZONTAL)

        self.xAxischeckBox = wx.CheckBox(self, wx.ID_ANY, "X-axis grid", wx.DefaultPosition, wx.DefaultSize, 0)
        displayGridsSizer.Add(self.xAxischeckBox, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        self.yAxischeckBox = wx.CheckBox(self, wx.ID_ANY, "Y-axis grid", wx.DefaultPosition, wx.DefaultSize, 0)
        displayGridsSizer.Add(self.yAxischeckBox, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        displayGridsSizer.AddStretchSpacer()
        displayGridsSizer.Add(wx.StaticText(self, wx.ID_ANY, u"No. of bins:", wx.DefaultPosition, wx.DefaultSize, 0), 0,
                              wx.CENTER, 5)
        self.numOfBins = wx.SpinCtrl(self, wx.ID_ANY, value='10', size=(130, -1))
        self.numOfBins.SetRange(1, 100)
        displayGridsSizer.Add(self.numOfBins, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)

        gbSizer1.Add(displayGridsSizer, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        # ---------------------------------------   

        # Legend

        positions = ['Upper right', 'Upper left', 'Lower left', 'Lower right', 'Right', 'Center left', 'Center right',
                     'Lower center', 'Upper center', 'Center']

        self.histLegendPosText = wx.StaticBox(self, wx.ID_ANY, u"Legend position")
        legendPosSizer = wx.StaticBoxSizer(self.histLegendPosText, wx.HORIZONTAL)
        self.histLegendPosText.Enable(False)

        fgLegendSizer = wx.FlexGridSizer(0, 4, 0, 0)
        fgLegendSizer.SetFlexibleDirection(wx.BOTH)
        fgLegendSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        legendPosSizer.Add(fgLegendSizer, 1, wx.EXPAND, 5)

        self.histLegendPosDefault = wx.RadioButton(self, wx.ID_ANY, "Default", wx.DefaultPosition, wx.DefaultSize,
                                                   wx.RB_GROUP)
        fgLegendSizer.Add(self.histLegendPosDefault, 0, wx.ALL, 1)
        self.Bind(wx.EVT_RADIOBUTTON, self.updateLegendPosition, self.histLegendPosDefault)
        self.histLegendPosDefault.Enable(False)

        self.histLegendPosOther = []

        for i in range(len(positions)):
            self.histLegendPosOther.append(
                wx.RadioButton(self, wx.ID_ANY, positions[i], wx.DefaultPosition, wx.DefaultSize))
            fgLegendSizer.Add(self.histLegendPosOther[i], 0, wx.ALL, 1)
            self.histLegendPosOther[i].Enable(False)
            self.Bind(wx.EVT_RADIOBUTTON, self.updateLegendPosition, self.histLegendPosOther[i])

        gbSizer1.Add(legendPosSizer, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT | wx.TOP, 10)

        # ---------------------------------------

        # Variables

        sbSizerXVariable = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"X variable"), wx.VERTICAL)
        sbHistTag = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Tag"), wx.VERTICAL)

        fgSizer3 = wx.FlexGridSizer(1, 0, 0, 0)
        fgSizer3.SetFlexibleDirection(wx.BOTH)
        fgSizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # xVariable
        fgSizer5 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer5.SetFlexibleDirection(wx.BOTH)
        fgSizer5.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.radioBtnsXVariable = []
        for i in range(len(listOfVariables)):
            # First element
            if i == 0:
                self.radioBtnsXVariable.append(
                    wx.RadioButton(self, wx.ID_ANY, listOfVariables[i], wx.DefaultPosition, wx.DefaultSize,
                                   wx.RB_GROUP))
                fgSizer5.Add(self.radioBtnsXVariable[i], 0, wx.ALL, 1)
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedVariablesRadioButton, self.radioBtnsXVariable[i])
            else:
                self.radioBtnsXVariable.append(
                    wx.RadioButton(self, wx.ID_ANY, listOfVariables[i], wx.DefaultPosition, wx.DefaultSize))
                fgSizer5.Add(self.radioBtnsXVariable[i], 0, wx.ALL, 1)
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedVariablesRadioButton, self.radioBtnsXVariable[i])

        # Tags
        fgSizer6 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer6.SetFlexibleDirection(wx.BOTH)
        fgSizer6.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.radioBtnDefaultTag = wx.RadioButton(self, wx.ID_ANY, "None", wx.DefaultPosition, wx.DefaultSize,
                                                 wx.RB_GROUP)
        fgSizer6.Add(self.radioBtnDefaultTag, 0, wx.ALL, 1)
        self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedTagsRadioButton, self.radioBtnDefaultTag)

        self.radioBtnsOtherTags = []
        for i in range(len(listOfTags)):
            self.radioBtnsOtherTags.append(
                wx.RadioButton(self, wx.ID_ANY, listOfTags[i], wx.DefaultPosition, wx.DefaultSize))
            fgSizer6.Add(self.radioBtnsOtherTags[i], 0, wx.ALL, 1)
            self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedTagsRadioButton, self.radioBtnsOtherTags[i])

        # As a default the name of the axis are the selected variables
        self.xAxisNameTextCtrl.SetValue(listOfVariables[0])
        self.yAxisNameTextCtrl.SetValue('No. of elements')

        sbSizerXVariable.Add(fgSizer5, 1, wx.EXPAND, 5)
        sbHistTag.Add(fgSizer6, 1, wx.EXPAND, 5)

        fgSizer3.Add(sbSizerXVariable, 1, wx.EXPAND | wx.ALL, 5)
        fgSizer3.Add(sbHistTag, 1, wx.EXPAND | wx.ALL, 5)

        gbSizer1.Add(fgSizer3, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.ALIGN_RIGHT | wx.EXPAND | wx.ALL, 5)

        # --------------------------------------- 

        # Ok and Cancel buttons

        okay = wx.Button(self, wx.ID_OK)
        cancel = wx.Button(self, wx.ID_CANCEL)
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()

        gbSizer1.Add(btns, wx.GBPosition(4, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.TOP | wx.BOTTOM, 10)

        self.SetSizer(gbSizer1)
        gbSizer1.Fit(self)
        self.Layout()
        self.Fit()
        self.Centre(wx.BOTH)

        # Variable to save the selected radiobutton
        self.selectedRadioButtonVariables = listOfVariables[0]
        self.selectedRadioButtonTags = 'None'

        if histogramOptions:
            self.setHistogramOptions(histogramOptions)

        self.Fit()
        self.Show(True)

    def updateLegendPosition(self, event):
        radioButton = event.GetEventObject()
        self.legendPosition = radioButton.GetLabelText()

    def updateSelectedVariablesRadioButton(self, event):
        radioButton = event.GetEventObject()

        self.selectedRadioButtonVariables = radioButton.GetLabelText()
        self.xAxisNameTextCtrl.SetValue(radioButton.GetLabelText())

    def updateSelectedTagsRadioButton(self, event):
        radioButton = event.GetEventObject()
        selectedRadioButton = radioButton.GetLabelText()
        self.selectedRadioButtonTags = radioButton.GetLabelText()

        if selectedRadioButton == 'None':
            self.histLegendPosText.Enable(False)
            self.histLegendPosDefault.Enable(False)
            for otherRadioButton in self.histLegendPosOther:
                otherRadioButton.Enable(False)
            self.histLegendPosDefault.SetValue(True)
        else:
            self.histLegendPosText.Enable()
            self.histLegendPosDefault.Enable()
            for otherRadioButton in self.histLegendPosOther:
                otherRadioButton.Enable()

    def getHistogramOptions(self):
        histogramOptions = dict(
            title=self.histogramNameTextCtrl.GetValue(),
            xAxisName=self.xAxisNameTextCtrl.GetValue(),
            yAxisName=self.yAxisNameTextCtrl.GetValue(),
            xAxisGrid=self.xAxischeckBox.IsChecked(),
            yAxisGrid=self.yAxischeckBox.IsChecked(),
            numOfBins=self.numOfBins.GetValue(),

            legendIsEnabled=self.histLegendPosText.IsEnabled(),
            defaultLegend=self.histLegendPosDefault.GetValue(),
            otherLegends=[self.histLegendPosOther[i].GetValue() for i in range(len(self.histLegendPosOther))],

            xVariable=[self.radioBtnsXVariable[i].GetValue() for i in range(len(self.radioBtnsXVariable))],

            otherTags=[self.radioBtnsOtherTags[i].GetValue() for i in range(len(self.radioBtnsOtherTags))],

            firstVarSelected=self.selectedRadioButtonVariables,
            secondVarSelected=self.selectedRadioButtonTags,
            legendPosition=self.legendPosition.lower(),
            selectedCheckBoxes=[]
        )

        return histogramOptions

    def setHistogramOptions(self, histogramOptions):
        self.histogramNameTextCtrl.SetValue(histogramOptions['title'])
        self.xAxisNameTextCtrl.SetValue(histogramOptions['xAxisName'])
        self.yAxisNameTextCtrl.SetValue(histogramOptions['yAxisName'])
        self.xAxischeckBox.SetValue(histogramOptions['xAxisGrid'])
        self.yAxischeckBox.SetValue(histogramOptions['yAxisGrid'])
        self.numOfBins.SetValue(histogramOptions['numOfBins'])

        self.histLegendPosDefault.SetValue(histogramOptions['defaultLegend'])
        for i in range(len(histogramOptions['otherLegends'])):
            self.histLegendPosOther[i].SetValue(histogramOptions['otherLegends'][i])
        if histogramOptions['legendIsEnabled']:
            self.histLegendPosText.Enable()
            self.histLegendPosDefault.Enable()
            for buttonLegend in self.histLegendPosOther:
                buttonLegend.Enable()
        self.legendPosition = histogramOptions['legendPosition']

        for i in range(len(histogramOptions['xVariable'])):
            self.radioBtnsXVariable[i].SetValue(histogramOptions['xVariable'][i])
            if histogramOptions['xVariable'][i]:
                self.selectedRadioButtonVariables = self.listOfVariables[i]

        self.radioBtnDefaultTag.SetValue(True)
        self.selectedRadioButtonTags = 'None'
        for i in range(len(histogramOptions['otherTags'])):
            self.radioBtnsOtherTags[i].SetValue(histogramOptions['otherTags'][i])
            if histogramOptions['otherTags'][i]:
                self.selectedRadioButtonTags = self.radioBtnsOtherTags[i].GetLabelText()


class ScatterPlotInterface(wx.Dialog):

    def __init__(self, parent, listOfVariables, scatterPlotOptions):

        self.listOfVariables = listOfVariables

        self.selectedCheckBoxes = []
        self.position = 'default'

        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Scatter plot", size=wx.DefaultSize,
                           pos=wx.DefaultPosition)

        gbSizer1 = wx.GridBagSizer(0, 0)
        gbSizer1.SetFlexibleDirection(wx.BOTH)
        gbSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # Scatter Plot Options
        fgSizerchartOptions = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizerchartOptions.SetFlexibleDirection(wx.BOTH)
        fgSizerchartOptions.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        fgSizerchartOptions.AddGrowableCol(1)

        self.scatterName = wx.StaticText(self, wx.ID_ANY, u"Scatter plot title:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.scatterName.Wrap(-1)
        fgSizerchartOptions.Add(self.scatterName, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.scatterNameTextCtrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizerchartOptions.Add(self.scatterNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL, 5)

        self.xAxisName = wx.StaticText(self, wx.ID_ANY, u"X-axis label:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.xAxisName.Wrap(-1)
        fgSizerchartOptions.Add(self.xAxisName, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.xAxisNameTextCtrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizerchartOptions.Add(self.xAxisNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL, 5)

        self.yAxisName = wx.StaticText(self, wx.ID_ANY, u"Y-axis label:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.yAxisName.Wrap(-1)
        fgSizerchartOptions.Add(self.yAxisName, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.yAxisNameTextCtrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizerchartOptions.Add(self.yAxisNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL, 5)

        gbSizer1.Add(fgSizerchartOptions, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.ALL, 5)

        # -------------------------------
        # Display Grid

        displayGridsSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Display settings"), wx.HORIZONTAL)

        self.xAxischeckBox = wx.CheckBox(self, wx.ID_ANY, "X-axis grid", wx.DefaultPosition, wx.DefaultSize, 0)
        displayGridsSizer.Add(self.xAxischeckBox, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        self.yAxischeckBox = wx.CheckBox(self, wx.ID_ANY, "Y-axis grid", wx.DefaultPosition, wx.DefaultSize, 0)
        displayGridsSizer.Add(self.yAxischeckBox, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        displayGridsSizer.AddStretchSpacer()

        self.LFcheckBox = wx.CheckBox(self, wx.ID_ANY, "Plot linear fit", wx.DefaultPosition, wx.DefaultSize)
        displayGridsSizer.Add(self.LFcheckBox, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)

        gbSizer1.Add(displayGridsSizer, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        # ---------------------------------------
        # Legend

        positions = ['Upper right', 'Upper left', 'Lower left', 'Lower right', 'Right', 'Center left', 'Center right',
                     'Lower center', 'Upper center', 'Center']

        self.scatterLegendPosText = wx.StaticBox(self, wx.ID_ANY, u"Legend position")
        legendPosSizer = wx.StaticBoxSizer(self.scatterLegendPosText, wx.HORIZONTAL)
        self.scatterLegendPosText.Enable(False)

        gbSizer1.Add(legendPosSizer, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT | wx.TOP, 10)

        fgLegendSizer = wx.FlexGridSizer(0, 4, 0, 0)
        fgLegendSizer.SetFlexibleDirection(wx.BOTH)
        fgLegendSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        legendPosSizer.Add(fgLegendSizer, 1, wx.EXPAND, 5)

        self.scatterLegendPosDefault = wx.RadioButton(self, wx.ID_ANY, "Default", wx.DefaultPosition, wx.DefaultSize,
                                                      wx.RB_GROUP)
        fgLegendSizer.Add(self.scatterLegendPosDefault, 0, wx.ALL, 1)
        self.Bind(wx.EVT_RADIOBUTTON, self.updateLegendPosition, self.scatterLegendPosDefault)
        self.scatterLegendPosDefault.Enable(False)

        self.scatterLegendPosOther = []

        for position in positions:
            scatterLegendPosOtherTmp = wx.RadioButton(self, wx.ID_ANY, position, wx.DefaultPosition, wx.DefaultSize, 0)
            fgLegendSizer.Add(scatterLegendPosOtherTmp, 0, wx.ALL, 1)
            scatterLegendPosOtherTmp.Enable(False)
            self.Bind(wx.EVT_RADIOBUTTON, self.updateLegendPosition, scatterLegendPosOtherTmp)
            self.scatterLegendPosOther.append(scatterLegendPosOtherTmp)

        # ---------------------------------------

        # Variables
        sbScatterPlotXVar = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"X variable"), wx.VERTICAL)
        sbScatterPlotYVar = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Y variables"), wx.VERTICAL)

        fgSizer3 = wx.FlexGridSizer(1, 0, 0, 0)
        fgSizer3.SetFlexibleDirection(wx.BOTH)
        fgSizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        fgSizer5 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer5.SetFlexibleDirection(wx.BOTH)
        fgSizer5.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # Variable in X axis

        self.radioBtnsXVariable = []

        for i in range(len(listOfVariables)):

            # First element
            if i == 0:
                self.radioBtnsXVariable.append(
                    wx.RadioButton(self, wx.ID_ANY, listOfVariables[i], wx.DefaultPosition, wx.DefaultSize,
                                   wx.RB_GROUP))
                fgSizer5.Add(self.radioBtnsXVariable[i], 0, wx.ALL, 1)
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedVariablesRadioButton, self.radioBtnsXVariable[i])
            else:
                self.radioBtnsXVariable.append(
                    wx.RadioButton(self, wx.ID_ANY, listOfVariables[i], wx.DefaultPosition, wx.DefaultSize, 0))
                fgSizer5.Add(self.radioBtnsXVariable[i], 0, wx.ALL, 1)
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedVariablesRadioButton, self.radioBtnsXVariable[i])

        fgScatterPlotYVar = wx.FlexGridSizer(0, 2, 0, 0)
        fgScatterPlotYVar.SetFlexibleDirection(wx.BOTH)
        fgScatterPlotYVar.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # Variables in Y axis

        self.checkboxesYVariables = []

        for i in range(len(listOfVariables)):

            # First element
            if i == 0:
                self.checkboxesYVariables.append(
                    wx.CheckBox(self, wx.ID_ANY, listOfVariables[i], wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP))
                fgScatterPlotYVar.Add(self.checkboxesYVariables[i], 0, wx.ALL, 1)
                self.Bind(wx.EVT_CHECKBOX, self.updateSelectedTagsCheckBox, self.checkboxesYVariables[i])
            else:
                self.checkboxesYVariables.append(
                    wx.CheckBox(self, wx.ID_ANY, listOfVariables[i], wx.DefaultPosition, wx.DefaultSize, 0))
                fgScatterPlotYVar.Add(self.checkboxesYVariables[i], 0, wx.ALL, 1)
                self.Bind(wx.EVT_CHECKBOX, self.updateSelectedTagsCheckBox, self.checkboxesYVariables[i])

        # The name of the axis by default
        self.xAxisNameTextCtrl.SetValue(listOfVariables[0])
        self.yAxisNameTextCtrl.SetValue('')

        sbScatterPlotXVar.Add(fgSizer5, 1, wx.EXPAND, 5)
        sbScatterPlotYVar.Add(fgScatterPlotYVar, 1, wx.EXPAND, 5)

        fgSizer3.Add(sbScatterPlotXVar, 1, wx.EXPAND | wx.ALL, 5)
        fgSizer3.Add(sbScatterPlotYVar, 1, wx.EXPAND | wx.ALL, 5)

        gbSizer1.Add(fgSizer3, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.ALIGN_RIGHT | wx.EXPAND | wx.ALL, 5)

        # --------------------------------------- 
        # Ok and Cancel buttons   

        okay = wx.Button(self, wx.ID_OK, validator=ValidatorForScatter(self))
        cancel = wx.Button(self, wx.ID_CANCEL)
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()

        gbSizer1.Add(btns, wx.GBPosition(4, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.TOP | wx.BOTTOM, 10)

        self.SetSizer(gbSizer1)
        gbSizer1.Fit(self)
        self.Layout()
        self.Fit()
        self.Centre(wx.BOTH)

        # Radiobutton selected at the beginning
        self.selectedRadioButtonVariables = listOfVariables[0]
        self.selectedCheckBoxes = []

        if scatterPlotOptions:
            self.setScatterPlotOptions(scatterPlotOptions)

        self.Fit()
        self.Show(True)

    def updateSelectedVariablesRadioButton(self, event):
        # X Variable
        radioButton = event.GetEventObject()
        self.selectedRadioButtonVariables = radioButton.GetLabelText()
        self.xAxisNameTextCtrl.SetValue(radioButton.GetLabelText())

    def updateSelectedTagsCheckBox(self, event):
        checkBox = event.GetEventObject()

        if checkBox.IsChecked():
            self.selectedCheckBoxes.append(checkBox.GetLabel())
        else:
            self.selectedCheckBoxes.remove(checkBox.GetLabel())

        if len(self.selectedCheckBoxes) == 1:
            self.yAxisNameTextCtrl.SetValue(self.selectedCheckBoxes[0])
        else:
            self.yAxisNameTextCtrl.SetValue('')

        if len(self.selectedCheckBoxes) >= 2:
            self.scatterLegendPosText.Enable()
            self.scatterLegendPosDefault.Enable()
            for cb in self.scatterLegendPosOther:
                cb.Enable()
        else:
            self.scatterLegendPosText.Enable(False)
            self.scatterLegendPosDefault.Enable(False)
            for cb in self.scatterLegendPosOther:
                cb.Enable(False)

    def updateLegendPosition(self, event):
        radioButton = event.GetEventObject()
        self.position = radioButton.GetLabelText()

    def getScatterPlotOptions(self):
        scatterOptions = dict(
            title=self.scatterNameTextCtrl.GetValue(),
            xAxisName=self.xAxisNameTextCtrl.GetValue(),
            yAxisName=self.yAxisNameTextCtrl.GetValue(),
            xAxisGrid=self.xAxischeckBox.IsChecked(),
            yAxisGrid=self.yAxischeckBox.IsChecked(),
            linearFit=self.LFcheckBox.IsChecked(),
            xVariable=[self.radioBtnsXVariable[i].GetValue() for i in range(len(self.radioBtnsXVariable))],
            yVariables=[self.checkboxesYVariables[i].GetValue() for i in range(len(self.checkboxesYVariables))],

            legendIsEnabled=self.scatterLegendPosText.IsEnabled(),
            defaultLegend=self.scatterLegendPosDefault.GetValue(),
            otherLegends=[self.scatterLegendPosOther[i].GetValue() for i in range(len(self.scatterLegendPosOther))],

            firstVarSelected=self.selectedRadioButtonVariables,
            legendPosition=self.position.lower(),
            selectedCheckBoxes=self.selectedCheckBoxes
        )
        return scatterOptions

    def setScatterPlotOptions(self, scatterPlotOptions):
        self.scatterNameTextCtrl.SetValue(scatterPlotOptions['title'])
        self.xAxisNameTextCtrl.SetValue(scatterPlotOptions['xAxisName'])
        self.yAxisNameTextCtrl.SetValue(scatterPlotOptions['yAxisName'])
        self.xAxischeckBox.SetValue(scatterPlotOptions['xAxisGrid'])
        self.yAxischeckBox.SetValue(scatterPlotOptions['yAxisGrid'])
        self.LFcheckBox.SetValue(scatterPlotOptions['linearFit'])

        for i in range(len(scatterPlotOptions['xVariable'])):
            self.radioBtnsXVariable[i].SetValue(scatterPlotOptions['xVariable'][i])
            if scatterPlotOptions['xVariable'][i]:
                self.selectedRadioButtonVariables = self.listOfVariables[i]
        for i in range(len(scatterPlotOptions['yVariables'])):
            self.checkboxesYVariables[i].SetValue(scatterPlotOptions['yVariables'][i])
            if scatterPlotOptions['yVariables'][i]:
                self.selectedCheckBoxes.append(self.checkboxesYVariables[i].GetLabel())

        self.scatterLegendPosDefault.SetValue(scatterPlotOptions['defaultLegend'])
        for i in range(len(scatterPlotOptions['otherLegends'])):
            self.scatterLegendPosOther[i].SetValue(scatterPlotOptions['otherLegends'][i])
        if scatterPlotOptions['legendIsEnabled']:
            self.scatterLegendPosText.Enable()
            self.scatterLegendPosDefault.Enable()
            for buttonLegend in self.scatterLegendPosOther:
                buttonLegend.Enable()
        self.position = scatterPlotOptions['legendPosition']


class ValidatorForScatter(wx.Validator):

    def __init__(self, object):
        wx.Validator.__init__(self)
        self.object = object

    def Clone(self):
        return ValidatorForScatter(self.object)

    def Validate(self, win):

        if not self.object.selectedCheckBoxes:
            wx.MessageBox("No variables were selected to be plotted in the y-axis", "ERROR",
                          wx.OK | wx.ICON_EXCLAMATION)
            return False
        elif len(self.object.selectedCheckBoxes) > 6:
            wx.MessageBox("No more than 6 variables can be plotted in the y-axis", "ERROR", wx.OK | wx.ICON_EXCLAMATION)
            return False
        else:
            return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True


class PieChartInterface(wx.Dialog):
    legendPosition = 'default'

    def __init__(self, parent, listOfTags, pieChartOptions):

        self.listOfTags = listOfTags

        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Pie chart", size=wx.DefaultSize, pos=wx.DefaultPosition)

        gbSizer1 = wx.GridBagSizer(0, 0)
        gbSizer1.SetFlexibleDirection(wx.BOTH)
        gbSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # -------------------------------

        # Pie Chart Options

        fgSizerchartOptions = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizerchartOptions.SetFlexibleDirection(wx.BOTH)
        fgSizerchartOptions.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        fgSizerchartOptions.AddGrowableCol(1)

        self.pieChartName = wx.StaticText(self, wx.ID_ANY, u"Pie chart title:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.pieChartName.Wrap(-1)
        fgSizerchartOptions.Add(self.pieChartName, 0, wx.ALIGN_CENTER | wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.pieChartNameTextCtrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizerchartOptions.Add(self.pieChartNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL, 5)

        gbSizer1.Add(fgSizerchartOptions, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.ALL, 5)

        # -------------------------------

        # Display Grid 

        displayGridsSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Display settings"), wx.HORIZONTAL)

        self.offsetCheckBox = wx.CheckBox(self, wx.ID_ANY, "Offset slices", wx.DefaultPosition, wx.DefaultSize, 0)
        displayGridsSizer.Add(self.offsetCheckBox, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        displayGridsSizer.AddStretchSpacer()
        displayGridsSizer.Add(
            wx.StaticText(self, wx.ID_ANY, u"No. of slices (0=all):", wx.DefaultPosition, wx.DefaultSize, 0), 0,
            wx.CENTER, 5)
        self.numOfSlices = wx.SpinCtrl(self, wx.ID_ANY, value='0', size=(130, -1))
        self.numOfSlices.SetRange(0, 20)
        displayGridsSizer.Add(self.numOfSlices, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)

        gbSizer1.Add(displayGridsSizer, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        # -------------------------------

        # Legend position

        positions = ['Upper right', 'Upper left', 'Lower left', 'Lower right', 'Right', 'Center left', 'Center right',
                     'Lower center', 'Upper center', 'Center']

        legendPosSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Legend position"), wx.HORIZONTAL)

        fgLegendSizer = wx.FlexGridSizer(0, 4, 0, 0)
        fgLegendSizer.SetFlexibleDirection(wx.BOTH)
        fgLegendSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        legendPosSizer.Add(fgLegendSizer, 1, wx.EXPAND, 5)

        self.pieChartLegendPosDefault = wx.RadioButton(self, wx.ID_ANY, "Default", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP)
        fgLegendSizer.Add(self.pieChartLegendPosDefault, 0, wx.ALL, 1)
        self.Bind(wx.EVT_RADIOBUTTON, self.updateLegendPosition, self.pieChartLegendPosDefault)

        self.pieChartLegendPosOther = []
        for i in range(len(positions)):
            self.pieChartLegendPosOther.append(wx.RadioButton(self, wx.ID_ANY, positions[i], wx.DefaultPosition, wx.DefaultSize, 0))
            fgLegendSizer.Add(self.pieChartLegendPosOther[i], 0, wx.ALL, 1)
            self.Bind(wx.EVT_RADIOBUTTON, self.updateLegendPosition, self.pieChartLegendPosOther[i])

        gbSizer1.Add(legendPosSizer, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        # -------------------------------

        # Discrete variable

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Tag"), wx.VERTICAL)

        fgSizer5 = wx.FlexGridSizer(0, 3, 0, 0)
        fgSizer5.SetFlexibleDirection(wx.BOTH)
        fgSizer5.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # Here the RadioButtons are created

        self.radioBtnsTag = []

        for i in range(len(listOfTags)):

            # First one
            if i == 0:
                self.radioBtnsTag.append(wx.RadioButton(self, wx.ID_ANY, listOfTags[i], wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP))
                fgSizer5.Add(self.radioBtnsTag[i], 0, wx.ALL, 1)
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedVariablesRadioButton, self.radioBtnsTag[i])
            else:
                self.radioBtnsTag.append(wx.RadioButton(self, wx.ID_ANY, listOfTags[i], wx.DefaultPosition, wx.DefaultSize))
                fgSizer5.Add(self.radioBtnsTag[i], 0, wx.ALL, 1)
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedVariablesRadioButton, self.radioBtnsTag[i])

        sbSizer1.Add(fgSizer5, 1, wx.EXPAND, 5)

        gbSizer1.Add(sbSizer1, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        # -------------------------------

        # Buttons OK and Cancel

        okay = wx.Button(self, wx.ID_OK)
        cancel = wx.Button(self, wx.ID_CANCEL)
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()

        gbSizer1.Add(btns, wx.GBPosition(4, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.TOP | wx.BOTTOM, 10)

        self.SetSizer(gbSizer1)
        gbSizer1.Fit(self)
        self.Layout()
        self.Fit()
        self.Centre(wx.BOTH)

        # RadioButton selected by default
        self.selectedRadioButtonTags = listOfTags[0]
        self.pieChartNameTextCtrl.SetValue(listOfTags[0])

        if pieChartOptions:
            self.setPieChartOptions(pieChartOptions)

        self.Fit()
        self.Show(True)

    def updateSelectedVariablesRadioButton(self, event):
        radioButton = event.GetEventObject()
        self.selectedRadioButtonTags = radioButton.GetLabelText()
        self.pieChartNameTextCtrl.SetValue(self.selectedRadioButtonTags)

    def updateLegendPosition(self, event):
        radioButton = event.GetEventObject()
        self.legendPosition = radioButton.GetLabelText()

    def getPieChartOptions(self):
        pieChartOptions = dict(
            title=self.pieChartNameTextCtrl.GetValue(),
            offset=self.offsetCheckBox.IsChecked(),
            numOfSlices=self.numOfSlices.GetValue(),
            defaultLegend=self.pieChartLegendPosDefault.GetValue(),
            otherLegends=[self.pieChartLegendPosOther[i].GetValue() for i in range(len(self.pieChartLegendPosOther))],
            legendPosition=self.legendPosition.lower(),
            tag=[self.radioBtnsTag[i].GetValue() for i in range(len(self.radioBtnsTag))],
            firstVarSelected=self.selectedRadioButtonTags
        )
        return pieChartOptions

    def setPieChartOptions(self, pieChartOptions):
        self.pieChartNameTextCtrl.SetValue(pieChartOptions['title'])
        self.offsetCheckBox.SetValue(pieChartOptions['offset'])
        self.numOfSlices.SetValue(pieChartOptions['numOfSlices'])
        self.pieChartLegendPosDefault.SetValue(pieChartOptions['defaultLegend'])
        for i in range(len(pieChartOptions['otherLegends'])):
            self.pieChartLegendPosOther[i].SetValue(pieChartOptions['otherLegends'][i])
        self.legendPosition=pieChartOptions['legendPosition']
        for i in range(len(pieChartOptions['tag'])):
            self.radioBtnsTag[i].SetValue(pieChartOptions['tag'][i])
            if pieChartOptions['tag'][i]:
                self.selectedRadioButtonTags = self.listOfTags[i]


class BoxPlotInterface(wx.Dialog):

    def __init__(self, parent, listOfVariables, listOfCharacterValues, boxPlotOptions):

        self.selectedCheckBoxes = []

        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Box plot", size=wx.DefaultSize, pos=wx.DefaultPosition)

        gbSizer1 = wx.GridBagSizer(0, 0)
        gbSizer1.SetFlexibleDirection(wx.BOTH)
        gbSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # -----------------------

        # Box plot Options        

        fgSizerchartOptions = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizerchartOptions.SetFlexibleDirection(wx.BOTH)
        fgSizerchartOptions.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        fgSizerchartOptions.AddGrowableCol(1)

        self.histogramName = wx.StaticText(self, wx.ID_ANY, u"Title:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.histogramName.Wrap(-1)
        fgSizerchartOptions.Add(self.histogramName, 0, wx.ALIGN_CENTER | wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.histogramNameTextCtrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizerchartOptions.Add(self.histogramNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL, 5)

        gbSizer1.Add(fgSizerchartOptions, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.ALL, 5)

        # -----------------------

        # Display settings

        displayGridsSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Display settings"), wx.HORIZONTAL)

        self.showGridCheckBox = wx.CheckBox(self, wx.ID_ANY, "Show grid", wx.DefaultPosition, wx.DefaultSize, 0)
        displayGridsSizer.Add(self.showGridCheckBox, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)

        gbSizer1.Add(displayGridsSizer, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        self.showGridCheckBox.SetValue(True)

        # -----------------------

        # Variables

        self.checkBoxesVariables = []

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Variables"), wx.VERTICAL)

        fgSizer5 = wx.FlexGridSizer(0, 3, 0, 0)
        fgSizer5.SetFlexibleDirection(wx.BOTH)
        fgSizer5.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # Here the checkboxes are created
        for i in range(len(listOfVariables)):
            self.checkBoxesVariables.append(
                wx.CheckBox(self, wx.ID_ANY, listOfVariables[i], wx.DefaultPosition, wx.DefaultSize, 0))
            fgSizer5.Add(self.checkBoxesVariables[i], 0, wx.ALL | wx.EXPAND, 1)

            self.Bind(wx.EVT_CHECKBOX, self.updateSelectedCheckBoxes, self.checkBoxesVariables[i])

        sbSizer1.Add(fgSizer5, 1, wx.EXPAND, 0)

        gbSizer1.Add(sbSizer1, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALL, 10)

        # -----------------------

        # Group By

        groupbySizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Group by"), wx.HORIZONTAL)

        fgGroupbySizer = wx.FlexGridSizer(0, 3, 0, 0)
        fgGroupbySizer.SetFlexibleDirection(wx.BOTH)
        fgGroupbySizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        groupbySizer.Add(fgGroupbySizer, 1, wx.EXPAND, 5)

        self.radioBTNoGroup = wx.RadioButton(self, wx.ID_ANY, "None", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP)
        fgGroupbySizer.Add(self.radioBTNoGroup, 0, wx.ALL, 1)

        self.Bind(wx.EVT_RADIOBUTTON, self.updateGroupByOption, self.radioBTNoGroup)

        # Variable to group BoxPlot
        self.groupByOption = 'None'

        self.radioBTsGroupBy = []

        for i in range(len(listOfCharacterValues)):
            self.radioBTsGroupBy.append(
                wx.RadioButton(self, wx.ID_ANY, listOfCharacterValues[i], wx.DefaultPosition, wx.DefaultSize, 0))
            fgGroupbySizer.Add(self.radioBTsGroupBy[i], 0, wx.ALL, 1)
            self.Bind(wx.EVT_RADIOBUTTON, self.updateGroupByOption, self.radioBTsGroupBy[i])

        gbSizer1.Add(groupbySizer, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 10)

        # ---------------------------------------

        # Ok and Cancel buttons

        okay = wx.Button(self, wx.ID_OK, validator=ValidatorForBoxplot(self.selectedCheckBoxes))
        cancel = wx.Button(self, wx.ID_CANCEL)
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()

        gbSizer1.Add(btns, wx.GBPosition(4, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.TOP | wx.BOTTOM, 10)

        self.SetSizer(gbSizer1)
        gbSizer1.Fit(self)
        self.Layout()
        self.Fit()
        self.Centre(wx.BOTH)

        if boxPlotOptions:
            self.setBoxPlotOptions(boxPlotOptions)

        self.Fit()
        self.Show(True)

    def updateGroupByOption(self, event):
        radioButton = event.GetEventObject()
        self.groupByOption = radioButton.GetLabelText()

    def updateSelectedCheckBoxes(self, event):
        checkBox = event.GetEventObject()
        if checkBox.IsChecked():
            self.selectedCheckBoxes.append(checkBox.GetLabel())
        else:
            self.selectedCheckBoxes.remove(checkBox.GetLabel())

    def getBoxPlotOptions(self):
        boxPlotOptions = dict(
            title=self.histogramNameTextCtrl.GetValue(),
            showGrid=self.showGridCheckBox.GetValue(),
            selectedCheckBoxes=self.selectedCheckBoxes,
            variables=[self.checkBoxesVariables[i].GetValue() for i in range(len(self.checkBoxesVariables))],
            secondVarSelected=self.groupByOption,
            noGroupBy=self.radioBTNoGroup.GetValue(),
            groupBys=[self.radioBTsGroupBy[i].GetValue() for i in range(len(self.radioBTsGroupBy))]

        )
        return boxPlotOptions

    def setBoxPlotOptions(self, boxPlotOptions):
        self.histogramNameTextCtrl.SetValue(boxPlotOptions['title'])
        self.showGridCheckBox.SetValue(boxPlotOptions['showGrid'])
        for i in range(len(boxPlotOptions['variables'])):
            self.checkBoxesVariables[i].SetValue(boxPlotOptions['variables'][i])
            if boxPlotOptions['variables'][i]:
                self.selectedCheckBoxes.append(self.checkBoxesVariables[i].GetLabel())
        self.radioBTNoGroup.SetValue(boxPlotOptions['noGroupBy'])
        for i in range(len(boxPlotOptions['groupBys'])):
            self.radioBTsGroupBy[i].SetValue(boxPlotOptions['groupBys'][i])
        self.groupByOption = boxPlotOptions['secondVarSelected']


class ValidatorForBoxplot(wx.Validator):

    def __init__(self, selectedCheckBoxes):
        wx.Validator.__init__(self)
        self.selectedCheckBoxes = selectedCheckBoxes

    def Clone(self):
        return ValidatorForBoxplot(self.selectedCheckBoxes)

    def Validate(self, win):
        if not self.selectedCheckBoxes:
            wx.MessageBox("Please, select at least one checkBox", "ERROR", wx.OK | wx.ICON_EXCLAMATION)
            return False
        else:
            return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True

    def noCheckBoxSelectedWarning(self):

        dlg = wx.MessageDialog(self, "Please, select at least one checkBox", "ERROR", wx.OK | wx.ICON_EXCLAMATION)
        if dlg.ShowModal() == wx.ID_OK:
            dlg.Destroy()
        else:
            dlg.Destroy()


class BarChartInterface(wx.Dialog):

    def __init__(self, parent, listOfVariables, listOfTags, barChartOptions):

        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Bar chart", size=wx.DefaultSize, pos=wx.DefaultPosition)

        self.listOfVariables = listOfVariables

        gbSizer1 = wx.GridBagSizer(0, 0)
        gbSizer1.SetFlexibleDirection(wx.BOTH)
        gbSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # -----------------------------

        # BarChart options

        fgSizerchartOptions = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizerchartOptions.SetFlexibleDirection(wx.BOTH)
        fgSizerchartOptions.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        fgSizerchartOptions.AddGrowableCol(1)

        self.histogramName = wx.StaticText(self, wx.ID_ANY, u"Title:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.histogramName.Wrap(-1)
        fgSizerchartOptions.Add(self.histogramName, 0, wx.ALIGN_CENTER | wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.histogramNameTextCtrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizerchartOptions.Add(self.histogramNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL, 5)

        self.xAxisName = wx.StaticText(self, wx.ID_ANY, u"X-axis label:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.xAxisName.Wrap(-1)
        fgSizerchartOptions.Add(self.xAxisName, 0, wx.ALIGN_CENTER | wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.xAxisNameTextCtrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizerchartOptions.Add(self.xAxisNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL, 5)

        self.yAxisName = wx.StaticText(self, wx.ID_ANY, u"Y-axis label:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.yAxisName.Wrap(-1)
        fgSizerchartOptions.Add(self.yAxisName, 0, wx.ALIGN_CENTER | wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.yAxisNameTextCtrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizerchartOptions.Add(self.yAxisNameTextCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL, 5)

        gbSizer1.Add(fgSizerchartOptions, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.ALL, 5)

        # -------------------------------

        # Display Grid        

        displayGridsSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Display settings"), wx.HORIZONTAL)

        self.xAxischeckBox = wx.CheckBox(self, wx.ID_ANY, "X-axis grid", wx.DefaultPosition, wx.DefaultSize, 0)
        displayGridsSizer.Add(self.xAxischeckBox, 0, wx.ALL, 4)
        self.yAxischeckBox = wx.CheckBox(self, wx.ID_ANY, "Y-axis grid", wx.DefaultPosition, wx.DefaultSize, 0)
        displayGridsSizer.Add(self.yAxischeckBox, 0, wx.ALL, 4)

        gbSizer1.Add(displayGridsSizer, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        # -------------------------------

        # Variables, tags and operations Options

        sbBarChartVarsSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Variable"), wx.VERTICAL)
        sbBarChartTagsSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Tag"), wx.VERTICAL)
        sbBarChartOpsSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Operation"), wx.VERTICAL)

        fgSizer3 = wx.FlexGridSizer(1, 0, 0, 0)
        fgSizer3.SetFlexibleDirection(wx.BOTH)
        fgSizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # xVariable

        fgSizer5 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer5.SetFlexibleDirection(wx.BOTH)
        fgSizer5.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.radioBtnsXVariable = []
        for i in range(len(listOfVariables)):
            if i == 0:
                self.radioBtnsXVariable.append(wx.RadioButton(self, wx.ID_ANY, listOfVariables[i], wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP))
                fgSizer5.Add(self.radioBtnsXVariable[i], 0, wx.ALL, 1)
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedVariablesRadioButton, self.radioBtnsXVariable[i])
            else:
                self.radioBtnsXVariable.append(wx.RadioButton(self, wx.ID_ANY, listOfVariables[i], wx.DefaultPosition, wx.DefaultSize))
                fgSizer5.Add(self.radioBtnsXVariable[i], 0, wx.ALL, 1)
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedVariablesRadioButton, self.radioBtnsXVariable[i])

        # Tag

        fgSizer6 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer6.SetFlexibleDirection(wx.BOTH)
        fgSizer6.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.radioBtnDefaultTag = wx.RadioButton(self, wx.ID_ANY, "None", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP)
        fgSizer6.Add(self.radioBtnDefaultTag, 0, wx.ALL, 1)
        self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedTagsRadioButton, self.radioBtnDefaultTag)

        self.radioBtnsOtherTags = []
        for i in range(len(listOfTags)):
            self.radioBtnsOtherTags.append(wx.RadioButton(self, wx.ID_ANY, listOfTags[i], wx.DefaultPosition, wx.DefaultSize))
            fgSizer6.Add(self.radioBtnsOtherTags[i], 0, wx.ALL, 1)
            self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedTagsRadioButton, self.radioBtnsOtherTags[i])

        # As a default the name of the axis are the selected variables
        self.xAxisNameTextCtrl.SetValue('')

        # Operations
        listOperations = ['Mean', 'Median', 'Std deviation', 'Variance']
        # By default, Mean selected
        self.selectedOperation = str(listOperations[0])

        self.yAxisNameTextCtrl.SetValue(self.selectedOperation.lower() + " (" + listOfVariables[0] + ")")

        fgSizer7 = wx.FlexGridSizer(1, 0, 0, 0)
        fgSizer7.SetFlexibleDirection(wx.BOTH)
        fgSizer7.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.radioBtnsOperations = []
        for i in range(len(listOperations)):
            if i == 0:
                self.radioBtnsOperations.append(wx.RadioButton(self, wx.ID_ANY, listOperations[i], wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP))
                fgSizer7.Add(self.radioBtnsOperations[i], 0, wx.ALL, 1)
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedOperationRadioButton, self.radioBtnsOperations[i])

            else:
                self.radioBtnsOperations.append(wx.RadioButton(self, wx.ID_ANY, listOperations[i], wx.DefaultPosition, wx.DefaultSize))
                fgSizer7.Add(self.radioBtnsOperations[i], 0, wx.ALL, 1)
                self.Bind(wx.EVT_RADIOBUTTON, self.updateSelectedOperationRadioButton, self.radioBtnsOperations[i])

        sbBarChartVarsSizer.Add(fgSizer5, 1, wx.EXPAND, 5)
        sbBarChartTagsSizer.Add(fgSizer6, 1, wx.EXPAND, 5)
        sbBarChartOpsSizer.Add(fgSizer7, 1, wx.EXPAND, 5)

        fgSizer3.Add(sbBarChartVarsSizer, 1, wx.EXPAND | wx.ALL, 5)
        fgSizer3.Add(sbBarChartTagsSizer, 1, wx.EXPAND | wx.ALL, 5)

        gbSizer1.Add(fgSizer3, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALIGN_RIGHT | wx.EXPAND | wx.ALL, 5)

        gbSizer1.Add(sbBarChartOpsSizer, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 10)

        # -------------------------------     

        # Ok and Cancel buttons

        okay = wx.Button(self, wx.ID_OK)
        cancel = wx.Button(self, wx.ID_CANCEL)
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()

        gbSizer1.Add(btns, wx.GBPosition(4, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.TOP | wx.BOTTOM, 10)

        self.SetSizer(gbSizer1)
        gbSizer1.Fit(self)
        self.Layout()
        self.Fit()
        self.Centre(wx.BOTH)

        # Variable to save the selected radiobutton
        self.selectedRadioButtonVariables = listOfVariables[0]
        self.selectedRadioButtonTags = 'None'

        if barChartOptions:
            self.setBarChartOptions(barChartOptions)

        self.Fit()
        self.Show(True)

    def updateSelectedVariablesRadioButton(self, event):
        radioButton = event.GetEventObject()
        self.selectedRadioButtonVariables = radioButton.GetLabelText()
        self.yAxisNameTextCtrl.SetValue(self.selectedOperation.lower() + " (" + self.selectedRadioButtonVariables + ")")

    def updateSelectedTagsRadioButton(self, event):
        radioButton = event.GetEventObject()
        self.selectedRadioButtonTags = radioButton.GetLabelText()
        if self.selectedRadioButtonTags == 'None':
            self.xAxisNameTextCtrl.SetValue('')
        else:
            self.xAxisNameTextCtrl.SetValue(radioButton.GetLabelText())

    def updateSelectedOperationRadioButton(self, event):
        radioButton = event.GetEventObject()
        self.selectedOperation = radioButton.GetLabelText()
        self.yAxisNameTextCtrl.SetValue(self.selectedOperation.lower() + " (" + self.selectedRadioButtonVariables + ")")

    def getBarChartOptions(self):
        barChartOptions = dict(
            title=self.histogramNameTextCtrl.GetValue(),
            xAxisName=self.xAxisNameTextCtrl.GetValue(),
            yAxisName=self.yAxisNameTextCtrl.GetValue(),
            xAxisGrid=self.xAxischeckBox.IsChecked(),
            yAxisGrid=self.yAxischeckBox.IsChecked(),
            xVariable=[self.radioBtnsXVariable[i].GetValue() for i in range(len(self.radioBtnsXVariable))],
            firstVarSelected=self.selectedRadioButtonVariables,

            otherTags=[self.radioBtnsOtherTags[i].GetValue() for i in range(len(self.radioBtnsOtherTags))],
            secondVarSelected=self.selectedRadioButtonTags,


            operation=self.selectedOperation
        )

        return barChartOptions

    def setBarChartOptions(self, barChartOptions):
        self.histogramNameTextCtrl.SetValue(barChartOptions['title'])
        self.xAxisNameTextCtrl.SetValue(barChartOptions['xAxisName'])
        self.yAxisNameTextCtrl.SetValue(barChartOptions['yAxisName'])
        self.xAxischeckBox.SetValue(barChartOptions['xAxisGrid'])
        self.yAxischeckBox.SetValue(barChartOptions['yAxisGrid'])
        for i in range(len(barChartOptions['xVariable'])):
            self.radioBtnsXVariable[i].SetValue(barChartOptions['xVariable'][i])
            if barChartOptions['xVariable'][i]:
                self.selectedRadioButtonVariables = self.listOfVariables[i]

        self.radioBtnDefaultTag.SetValue(True)
        self.selectedRadioButtonTags = 'None'
        for i in range(len(barChartOptions['otherTags'])):
            self.radioBtnsOtherTags[i].SetValue(barChartOptions['otherTags'][i])
            if barChartOptions['otherTags'][i]:
                self.selectedRadioButtonTags = self.radioBtnsOtherTags[i].GetLabelText()

        for i in range(len(self.radioBtnsOperations)):
            if self.radioBtnsOperations[i].GetLabelText()==barChartOptions['operation']:
                self.radioBtnsOperations[i].SetValue(True)
        self.selectedOperation=barChartOptions['operation']

