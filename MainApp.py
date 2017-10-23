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

import wx
import os

from MainFrame import MainFrame

MainFrame.params = {}
MainFrame.params['version'] = 0.9
MainFrame.params['dataPresent'] = False
MainFrame.params['configDir'] = os.path.expanduser('~')+os.sep+'.gasatad'
MainFrame.params['configFile'] = MainFrame.params['configDir']+os.sep+"gasatad.cfg"

# Factory options to write in file gasatad.cfg
    # Keys must be lowercase
MainFrame.params['options'] = {}  
MainFrame.params['options']['dirfrom'] = os.getcwd()
MainFrame.params['options']['discardfirstcolumn'] = "True"

# Uncomment the following line before build .deb package
# os.chdir("/usr/share/gasatad")


app = wx.App(False)
mainFrame = MainFrame(None)
mainFrame.Centre()
app.MainLoop()