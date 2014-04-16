#!/usr/bin/env python
#coding:utf-8
'''
  Author:   Justin Carroll--<jrc.csus@gmail.com>
  Purpose:  Zone Widget Support for LLaML.
  Created: 12/10/2013
'''

from PySide.QtCore import *
from PySide.QtGui import *

class ZoneWidget(QScrollArea):
    '''Each instance represents individual zones/channels.'''
    def __init__(self, *args, **kwargs):
        super(ZoneWidget, self).__init__()
        self.generalLayout = QVBoxLayout()
        self.setContentsMargins(0,0,0,0)
        self.zoneWidgetOne = ZoneContainerWidget()
        self.generalLayout.addWidget(self.zoneWidgetOne)
        self.setLayout(self.generalLayout)


class ZoneContainerWidget(QWidget):
    '''Container for the Label and Touch portions of the zone widget'''
    def __init__(self, *args, **kwargs):
        super(ZoneContainerWidget, self).__init__()
        self.setContentsMargins(0,0,0,0)
        self.generalLayout = QHBoxLayout()
        self.labelWidget = ZoneLabelWidget()
        self.blockWidget = ZoneTouchWidget()

        # add the label and touch widget to the layout
        self.generalLayout.addWidget(self.labelWidget)
        #self.generalLayout.addWidget(self.blockWidget)
        #self.generalLayout.addStretch(1)

        self.setLayout(self.generalLayout)

class ZoneLabelWidget(QPushButton):
    '''Container for the Zone Widget Icon, Label, and Color.'''
    def __init__(self, *args, **kwargs):
        super(ZoneLabelWidget, self).__init__()
        self.setContentsMargins(0,0,0,0)
        self.setFixedWidth(125)
        self.generalLayout = QHBoxLayout()
        self.text = QLabel("2.R.Window")
        self.colorSqr = QFrame()
        self.colorSqr.setFixedWidth(20)
        self.colorSqr.setStyleSheet("QWidget { background-color: #FF0000}")
        self.generalLayout.addWidget(self.colorSqr)
        self.generalLayout.addWidget(self.text)
        self.generalLayout.addStretch()
        self.zoneColor = None
        self.zoneImage = None
        self.setLayout(self.generalLayout)

        self.clicked.connect(ZoneInfoDialogWidget)


class ZoneTouchWidget(QScrollArea):
    '''The scrollable area of the zone widget'''
    def __init__(self, *args, **kwargs):
        super(ZoneTouchWidget, self).__init__()
        self.setContentsMargins(0,0,0,0)


class ZoneInfoDialogWidget(QDialog):
    def __init__(self, *args, **kwargs):
        super(ZoneInfoDialogWidget, self).__init__()
        self.zoneFullNameTXT = "2nd Floor BedRoom"
        self.zonePartialNameTXT = "2ndFlr BR"
        self.setWindowTitle("Zone Information:  {0}".format(self.zoneFullNameTXT,
                                                            "NULL"))

        self.generalLayout = QGridLayout()

        self.zoneFullNameLBL = QLabel("Zone Full Name:")
        self.zoneFullNameTXTField = QLineEdit()
        self.zoneFullNameLBL.setBuddy(self.zoneFullNameTXTField)

        self.generalLayout.addWidget(self.zoneFullNameLBL, 0, 0)
        self.setLayout(self.generalLayout)
        self.exec_()



