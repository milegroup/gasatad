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


# TODO: reading and writing excel data files
# TODO: adding new text columns

import wx
import os
import sys

from MainFrame import MainFrame

MainFrame.params = {}
MainFrame.params['version'] = 1.6
MainFrame.params['noOfNulls'] = 0
#MainFrame.params['configDir'] = os.path.expanduser('~')+os.sep+'.gasatad'
MainFrame.params['configDir'] = os.path.join(os.path.expanduser('~'),'.gasatad')
MainFrame.params['configFile'] = os.path.join(MainFrame.params['configDir'],"gasatad.cfg")

if sys.platform == 'win32':
    import locale
    loc = locale.getdefaultlocale()
    if loc[1]:
        MainFrame.params['configFile'] = MainFrame.params['configFile'].decode(loc[1],"ignore")

MainFrame.params['upgradable'] = False
MainFrame.params['availableVersionToUpgrade'] = ""

# Factory options to write in file gasatad.cfg
    # Keys must be lowercase

MainFrame.params['optionsdefault'] = {}  
MainFrame.params['optionsdefault']['dirfrom'] = os.getcwd()

MainFrame.params['options'] = {}  
for key in MainFrame.params['optionsdefault'].keys():
    MainFrame.params['options'][key] = MainFrame.params['optionsdefault'][key]


# Uncomment the following line before build .deb package
# os.chdir("/usr/share/gasatad")


app = wx.App(False)
mainFrame = MainFrame(None)
mainFrame.Centre()
app.MainLoop()
