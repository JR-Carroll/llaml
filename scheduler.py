#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose:
  Created: 12/09/2013
"""

from PySide.QtCore import *
from PySide.QtGui import *


class ScheduleView(QDialog):
    def __init__(self):
        super(ScheduleView, self).__init__()
        self.setWindowTitle("Schedule Viewer")
        self.calendar = QCalendarWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        self.setLayout(layout)
        self.exec_()

