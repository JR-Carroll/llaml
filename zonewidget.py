#!/usr/bin/env python
#coding:utf-8
'''
  Author:   Justin Carroll--<jrc.csus@gmail.com>
  Purpose:  Zone Widget Support for LLaML.
  Created: 12/10/2013
'''

from PySide.QtCore import *
from PySide.QtGui import *


class ZoneContainerWidget(QScrollArea):
    '''Main zone widget - holds all other widgets.'''
    def __init__(self, *args, **kwargs):
        super(ZoneContainerWidget, self).__init__()
        self.setWidget(QPushButton("Test"))


class ZoneWidget(QWidget):
    '''Each instance represents individual zones/channels.'''
    def __init__(self, parent, *args, **kwargs):
        super(ZoneIcon, self).__init__(parent)
        self.zoneColor = None
        self.zoneImage = None


class ZoneWidgetLabel(QWidget):
    '''Container for the Zone Widget Icon, Label, and Color.'''
    def __init__(self, parent, *args, **kwargs):
        super(ZoneWidgetIcon, self).__init__(parent)
        self.zoneColor = None
        self.zoneImage = None




