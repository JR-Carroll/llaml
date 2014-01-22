#!/usr/bin/env python
#coding:utf-8
"""
  Author:   Justin Carroll--<jrcarroll@jrcresearch.net>
  Purpose:  LLamL Schedule Creater
  Created: 12/09/2013
"""

from PySide.QtCore import *
from PySide.QtGui import *

class ScheduleView(QDialog):
    def __init__(self):
        super(ScheduleView, self).__init__()
        self.setWindowTitle("Schedule Viewer")
        self.layout = QVBoxLayout()

        # Add calendar to the dialog
        self.calendar = QCalendarWidget()

        self.eventName = QLineEdit("Name")
        self.timeStart = QTimeEdit()
        self.stopOnSong = QCheckBox("Stop after: ")
        self.selectStop = QComboBox()
        self.timeEnd   = QTimeEdit()
        self.projectSelect = QLineEdit()
        self.programSelect = QComboBox()

        self.layout.addWidget(self.calendar)
        self.layout.addWidget(self.eventName)
        self.layout.addWidget(self.timeStart)
        self.layout.addWidget(self.stopOnSong)
        self.layout.addWidget(self.selectStop)
        self.layout.addWidget(self.timeEnd)
        self.layout.addWidget(self.projectSelect)
        self.layout.addWidget(self.programSelect)

        self._dailyDataforCalendar = CalendarTimeSlots()
        self.table = QTableView()
        self.table.setShowGrid(True)

        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        self.exec_()


class CalendarTimeSlots(QAbstractTableModel):
    def __init__(self, parent, data, header, *args, **kwargs):
        super(CalendarTimeSlots, self).__init__(self, parent, *args, **kwargs)
        self.dailyData = data
        self.header = header

    def columnCount(self):
        return len(self.dailyData)

    def rowCount(self):
        return len(self.header)

    def data(self, index, role):
        if not index.isValid():
            _val = None
        elif role != Qt.DisplayRole:
            _val = None
        else:
            _val =  self.dailyData[index.row()][index.column()]
        return _val

    def headerData(self, column, orientiation, role):
        if orientiation == Qt.Horizontal and role == Qt.DisplayRole:
            _val = self.header[column]
        else:
            _val = None
        return _val
