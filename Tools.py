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
from pandas import DataFrame
import wx

title_font_size = 12
subtitle_font_size = 11
param_font_size = 10
num_decimals = 3


# Functions to write to text windows
# ----------------------------------

def setFont(results_window):
    font = results_window.GetFont()
    font = wx.Font(font.GetPointSize(), wx.FONTFAMILY_TELETYPE,
                   font.GetStyle(),
                   font.GetWeight(), font.GetUnderlined())
    results_window.SetFont(font)

def writeTitle(results_window, string_text):
    results_window.BeginBold()
    results_window.BeginFontSize(title_font_size)
    results_window.WriteText(string_text)
    results_window.EndFontSize()
    results_window.EndBold()
    results_window.Newline()


def writeSubTitle(results_window, string_text):
    results_window.BeginBold()
    results_window.BeginItalic()
    results_window.BeginFontSize(subtitle_font_size)
    results_window.WriteText(string_text)
    results_window.EndFontSize()
    results_window.EndItalic()
    results_window.EndBold()
    results_window.Newline()


def writeParam(results_window, string_text):
    results_window.Newline()
    results_window.BeginBold()
    results_window.BeginItalic()
    results_window.BeginFontSize(param_font_size)
    results_window.WriteText(string_text)
    results_window.EndFontSize()
    results_window.EndItalic()
    results_window.EndBold()
    results_window.Newline()


def writeResults(results_window, results):
    if type(results) == DataFrame:
        results_window.WriteText(results.to_string(col_space=8, na_rep='--', float_format='%7.3g', justify='right'))
    else:
        results_window.WriteText(results.to_string(na_rep='--', float_format='%7.3g'))
    results_window.Newline()

