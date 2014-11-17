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
        self.frameWidget.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))
        self.setWidget(self.frameWidget)

class ZoneFrameContainer(QFrame):
    def __init__(self, parent, *args, **kwargs):
        super(ZoneFrameContainer, self).__init__(parent)
        self.generalLayout = QVBoxLayout()
        self.generalLayout.setContentsMargins(0,0,0,0)
        self.zoneWidgetOne = ZoneContainerWidget()
        self.generalLayout.addWidget(self.zoneWidgetOne)
        self.generalLayout.setSpacing(0)
        self.generalLayout.setContentsMargins(0,0,0,0)
        
        self.setFixedWidth(2000)
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
        self.setLayout(self.generalLayout)

class ZoneLabelWidget(QPushButton):
    """Container for the Zone Widget Icon, Label, and Color."""
    def __init__(self, *args, **kwargs):
        super(ZoneLabelWidget, self).__init__()
        self.setFlat(True)
        self.setContentsMargins(0,0,0,0)
        self.setFixedWidth(115)
        self.generalLayout = QHBoxLayout()
        self.text = QLabel("2.R.Window")
        _labelFont = QFont("Helvetica", 8)
        self.text.setFont(_labelFont)
        self.colorSqr = QFrame()
        self.colorSqr.setFixedWidth(15)
        self.colorSqr.setFixedHeight(15)
        self.colorSqr.setStyleSheet("QWidget {background-color: #FF0000}")
        self.generalLayout.addWidget(self.colorSqr)
        self.generalLayout.addWidget(self.text)
        self.generalLayout.addStretch()
        self.zoneColor = None
        self.zoneImage = None
        self.setLayout(self.generalLayout)
        self.clicked.connect(ZoneInfoDialogWidget)


class ZoneTouchWidget(QFrame):
    """The scrollable area of the zone widget"""
    def __init__(self, *args, **kwargs):
        super(ZoneTouchWidget, self).__init__()
        self.setFrameStyle(QFrame.Panel)
        self.setLineWidth(1)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        hbox = QHBoxLayout()
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.setStyleSheet("QFrame {background-color: \"white\"}")
        self.isPressed = False        
        self.setLayout(hbox)
        self._allLightNodes = []
        # Arbitrary 10000 ceiling.  
        self._allZoneSteps = [a for a in xrange(0,10000, 2)]
    
    def mousePressEvent(self, *args, **kwargs):
        self.isPressed = True
        # The last mouseX and mouseY pressed
        self.mouseX = args[0].x()
        self.mouseY = args[0].y()
        self._allLightNodes.append((self._determine_nearestNodeFloor(), self.mouseY))
        self.update()
    
    def _determine_nearestNodeFloor(self, i=None):
        """
        Calculate the nearest node floor value.
        
        Node floor is calculated by looking at the self._allZoneSteps.
        
        If "x" is < self._allZoneSteps[i], then use i-1.
        If "x" is == self._allZoneSteps[i], then use i.
        If "x" is > self._allZoneSteps[i], then try again!
        
        Args:
            i = value to test.
        """
        if not i:
            i = self.mouseX
        lastStep = None 
        for step in self._allZoneSteps:
            if i < step:
                rtnStep = lastStep
            elif i == step:
                rtnStep = step
            else:
                lastStep = step
                continue
            return rtnStep
        
    def mouseReleaseEvent(self, *args, **kwargs):
        self.isPressed = False
        
    def paintEvent(self, *args, **kwargs):
        """Overloaded paintEvent"""
        self.draw_allLightNodes()
        super(ZoneTouchWidget, self).paintEvent(*args, **kwargs)
    
    def draw_singleLightNode(self):
        """
        Draw a single node on the zone widget.
        """
        pass
    
    def draw_allLightNodes(self):
        """
        Draw all nodes on the zone widget (this has to be called EVERY type update occurs).
        """
        tmpPaint = QPainter()
        tmpPaint.begin(self)
        # Todo -- need to map in the colors from the widget into this portion of the application.
        for node in self._allLightNodes:
            tmpPaint.fillRect(node[0], 0, 2, 26, QColor(122, 122, 122))
        tmpPaint.end()
        tmpPaint.restore()        

    
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