#!/usr/bin/env python
#coding:utf-8
"""
  Author:   Justin Carroll--<jrcarroll@jrcresearch.net>
  Purpose:  LLaML Schedule Creater
  Created: 12/09/2013
"""

from PySide.QtCore import *
from PySide.QtGui import *

class ScheduleView(QDialog):
    def __init__(self):
        super(ScheduleView, self).__init__()
        header = ['Timez', 'Program/Song', 'Length', 'test']
        data = [('12AM', 'Too Sexy for my shirt', '4min', 'test'),
                ('12AM', 'Dancing in the street', '3min', 'tst'),
                ('12AM', 'Too many candies', '8min', 'test'),
                ('12AM', 'Crazy Mothers Truckin', '18min', 'tst'),
                ('12AM', 'Everyday is a hard day', '2min', 'test'),
                ('12AM', 'I hate this life', '9min', 'test'),
                ('12AM', 'Drama for your momma', '5min', 'test')]
        self.setWindowTitle("Schedule Viewer")
        self.generalLayout = QHBoxLayout()
        self.generalLayout.setSizeConstraint(self.generalLayout.SetFixedSize)
        self.vertLayout = QVBoxLayout()
        self.vertLayout.setSizeConstraint(QLayout.SetFixedSize)

        # Add calendar to the dialog
        self.calendar = QCalendarWidget()

        self.eventName = QLineEdit("Name")
        self.timeStart = QTimeEdit()
        self.stopOnSong = QCheckBox("Stop after: ")
        self.selectStop = QComboBox()
        self.timeEnd   = QTimeEdit()
        self.projectSelect = QLineEdit()
        self.programSelect = QComboBox()

        self.vertLayout.addWidget(self.calendar)
        self.vertLayout.addWidget(self.eventName)
        self.vertLayout.addWidget(self.timeStart)
        self.vertLayout.addWidget(self.stopOnSong)
        self.vertLayout.addWidget(self.selectStop)
        self.vertLayout.addWidget(self.timeEnd)
        self.vertLayout.addWidget(self.projectSelect)
        self.vertLayout.addWidget(self.programSelect)
        self.vertLayout.addStretch()

        self._dailyDataforCalendar = CalendarTimeSlots(self, data, header)
        self.table = QTableView()
        self.table.setModel(self._dailyDataforCalendar)
        self.table.setShowGrid(False)
        self.table.setFixedWidth(550)

        self.generalLayout.addLayout(self.vertLayout)
        self.generalLayout.addSpacing(10)
        self.generalLayout.addWidget(self.table)
        self.setLayout(self.generalLayout)
        self.exec_()


class CalendarTimeSlots(QAbstractTableModel):
    def __init__(self, parent, data, header, *args, **kwargs):
        QAbstractTableModel.__init__(self, parent, *args, **kwargs)
        self.dailyData = data
        self.header = header

    def columnCount(self, parent):
        return len(self.header)

    def rowCount(self, parent):
        return len(self.dailyData)

    def data(self, index, role):
        if not index.isValid():
            _val = None
        elif role != Qt.DisplayRole:
            _val = None
        else:
            if index.column() < len(self.header):
                _val =  self.dailyData[index.row()][index.column()]
            else:
                _val = None
        return _val

    def headerData(self, column, orientiation, role):
        if orientiation == Qt.Horizontal and role == Qt.DisplayRole and column < len(self.header):
            _val = self.header[column]
        else:
            _val = None
        return _val

    def sort(self, column, order):
        self.emit(SIGNAL('layoutAboutToBeChanged()'))
        self.sortedList = sorted(self.sortedList, key=operator.intemgetter(col))
        if order == Qt.DescendingOrder:
            self.sortedList.reverse()
        self.emit(SIGNAL('layoutChanged()'))

header = ['Time', 'Program/Song', 'Length', 'test']
data = [('10AM', 'Too Sexy for my shirt', '4min'),
        ('11AM', 'Dancing in the street', '3min'),
        ('12AM', 'Too many candies', '8min'),
        ('13AM', 'Crazy Mothers Truckin', '18min'),
        ('14AM', 'Everyday is a hard day', '2min'),
        ('15AM', 'I hate this life', '9min'),
        ('16AM', 'Drama for your momma', '5min')]


