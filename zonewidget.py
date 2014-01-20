#!/usr/bin/env python
#coding:utf-8
'''
  Author:   --<>
  Purpose:
  Created: 12/10/2013
'''

from PySide.QtCore import *
from PySide.QtGui import *


class ZoneWidget(QWidget):
    '''Main zone widget - holds all other widgets.'''
    def __init__(self, parent, *args, **kwargs):
        super(ZoneWidget, self).__init__(parent)
        self.zoneNumber = None
        self.zoneName = "Zone"


class ZoneIcon(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super(ZoneIcon, self).__init__(parent)
        self.zoneColor = None
        self.zoneImage = None


class ZoneIcon(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super(ZoneIcon, self).__init__(parent)
        self.zoneColor = None
        self.zoneImage = None




