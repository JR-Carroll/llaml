#!/usr/bin/env python
#coding:utf-8
"""
  Author:   Justin Carroll--<jrc.csus@gmail.com>
  Purpose:  Zone Widget Support for LLaML.
  Created: 12/10/2013
"""

import logging
logging.debug("Attempting to load (wait for confirmation)")

from PySide.QtCore import *
from PySide.QtGui import *

class ZoneWidget(QScrollArea):
    """
    Each instance represents individual zones/channels.

    This is the zone widget in it's proper form.  Everything is wrapped
    up in here.
    """
    def __init__(self, parent, *args, **kwargs):
        super(ZoneWidget, self).__init__(parent)
        self.frameWidget = ZoneFrameContainer(self)
        #self.frameWidget.setFrameStyle(QFrame.Panel)
        #self.frameWidget.setLineWidth(1)
        self.frameWidget.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))
        self.setWidget(self.frameWidget)

class ZoneFrameContainer(QFrame):
    def __init__(self, parent, *args, **kwargs):
        super(ZoneFrameContainer, self).__init__(parent)
        #self.set
        self.generalLayout = QVBoxLayout()
        self.generalLayout.setContentsMargins(0,0,0,0)
        self.zoneWidgetOne = ZoneContainerWidget()
        self.generalLayout.addWidget(self.zoneWidgetOne)
        self.generalLayout.setSpacing(0)
        self.generalLayout.setContentsMargins(0,0,0,0)

        # Dummy code to invoke QScrollArea -- remove later.
        for i in range(0, 60, 1):
            self.generalLayout.addWidget(ZoneContainerWidget())

        self.setLayout(self.generalLayout)

class ZoneContainerWidget(QWidget):
    """Container for the Label and Touch portions of the zone widget"""
    def __init__(self, *args, **kwargs):
        super(ZoneContainerWidget, self).__init__()
        #self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.generalLayout = QHBoxLayout()
        self.labelWidget = ZoneLabelWidget()
        self.blockWidget = ZoneTouchWidget()

        # add the label and touch widget to the layout
        self.generalLayout.setContentsMargins(0,0,0,0)
        self.generalLayout.setSpacing(0)
        self.generalLayout.addWidget(self.labelWidget)
        self.generalLayout.addWidget(self.blockWidget)
        #self.generalLayout.addStretch(1)
        self.setLayout(self.generalLayout)

class ZoneLabelWidget(QPushButton):
    """Container for the Zone Widget Icon, Label, and Color."""
    def __init__(self, *args, **kwargs):
        super(ZoneLabelWidget, self).__init__()
        self.setFlat(True)
        self.setContentsMargins(0,0,0,0)
        self.setFixedWidth(115)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.generalLayout = QHBoxLayout()
        #self.setFr
        self.text = QLabel("2.R.Window")
        _labelFont = QFont("Helvetica", 8)
        self.text.setFont(_labelFont)
        self.colorSqr = QFrame()
        self.colorSqr.setFixedWidth(15)
        self.colorSqr.setFixedHeight(15)
        self.colorSqr.setStyleSheet("QWidget {background-color: #FF0000}")
        #self.setStyleSheet("QWidget {background-color: #FF0000}")
        self.generalLayout.addWidget(self.colorSqr)
        self.generalLayout.addWidget(self.text)
        self.generalLayout.addStretch()
        self.zoneColor = None
        self.zoneImage = None
        self.setLayout(self.generalLayout)
        self.clicked.connect(ZoneInfoDialogWidget)


class ZoneTouchWidget(QFrame):
    '''The scrollable area of the zone widget'''
    def __init__(self, *args, **kwargs):
        super(ZoneTouchWidget, self).__init__()
        #self.setContentsMargins(0,0,0,0)
        self.setFrameStyle(QFrame.Panel)
        self.setLineWidth(1)
        #self.setFixedWidth(500)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("aefaefaefaefaefajeflajfkaelkfjlajkflajelfafjlaeflajefaefaefaefaefaefajeflajfkaelkfjlajkflajelfafjlaeflajefaefaefaefaefaefajeflajfkaelkfjlajkflajelfafjlaeflajefaefaefaefaefaefajeflajfkaelkfjlajkflajelfafjlaeflajef5aefaefaefaefaefajeflajfkaelkfjlajkflajelfafjlaeflajefaefaefaefaefaefajeflajfkaelkfjlajkflajelfafjlaeflajefaefaefaefaefaefajeflajfkaelkfjlajkflajelfafjlaeflajefaefaefaefaefaefajeflajfkaelkfjlajkflajelfafjlaeflajefaefaefaefaefaefajeflajfkaelkfjlajkflajelfafjlaeflajef5aefaefaefaefaefajeflajfkaelkfjlajkflajelfafjlaeflajef"))
        self.setLayout(hbox)

class ZoneInfoDialogWidget(QDialog):
    """The information dialog that pops up when you click on a zone."""
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


logging.debug("Successfully loaded.")