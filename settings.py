#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<J. R. Carroll>
  Purpose: Settings controller.
  Created: 12/09/2013

  Helps to control all the various settings associated with LLaML.
  Settings include:
      - Recently used files
      - User settings
      -
"""

import cPickle
import os

from PySide.QtCore import *
from PySide.QtGui import *

_applicationPath_ = os.curdir
_application_ = "\LLaML.py"
_fullAppPath_ = _applicationPath_ + _application_


def checkForSettings():
    '''Poor-mans check to make sure we are in the correct directory.'''
    if os.path.exists(_fullAppPath_) and os.path.isfile(_fullAppPath_):
        return True
    else:
        raise ErrorApplicationPath(_fullAppPath_)


def clearSettingsFile():
    pass


class ErrorApplicationPath(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return "While looking for a settings file, it was detected that the LLaML application does not exists in the expected path: {0}".format(self.msg)


class ProjectSettingsFile(object):
    def __init__(self, *args, **kwargs):
        pass

    def createProjectFolder(self):
        pass

    def createProjectFile(self):
        pass

    def _setProjectPath(self):
        pass

    def _validateProjectFile(self):
        pass

    def addNewSong(self, song):
        pass

    def removeSong(self, song):
        pass

    def addNewLightMap(self):
        pass

    def removeLightMap(self):
        pass

    def loadProjectFile(self):
        pass

    def saveProjectFile(self):
        pass

    def saveAsProjectFile(self):
        pass


# TODO:  Add program settings file class.

class ApplicationSettingsFile(object):
    def __init__(self, *args, **kwargs):
        pass

    def createAppSettingsFile(self):
        pass

    def _validateAppSettingsFile(self):
        pass

    def loadAppSettingsFile(self):
        pass

    def saveAppSettingsFile(self):
        pass

    def saveAsAppSettingsFile(self):
        pass


class ProgramSettingsWindow(QDialog):
    def __init__(self):
        super(ProgramSettingsWindow, self).__init__()
        self.exec_()

class ApplicationSettingsWindow(QDialog):
    def __init__(self):
        super(ApplicationSettingsWindow, self).__init__()
        self._hbox = QHBoxLayout()
        self.setGeometry(50, 50, 700, 400)
        self.listView = QListWidget()
        self.listView.setGeometry(0, 0, 150, 200)
        self._general = QListWidgetItem('General')
        self._startup = QListWidgetItem('Start-up')
        self._audio = QListWidgetItem('Audio')
        self._comms = QListWidgetItem('Communications')
        self._restore = QListWidgetItem('Restore Defaults')

        self.listView.addItem(self._general)
        self.listView.addItem(self._startup)
        self.listView.addItem(self._audio)
        self.listView.addItem(self._comms)
        self.listView.addItem(self._restore)

        self._hbox.addWidget(self.listView)
        #self._hbox.addStretch()

        # General form/page
        # Create all the options/widgets
        self._generalGrid = QGridLayout()

        self._colorBasedOnDate = QCheckBox("Default pallet to nearest holiday?")
        self._editHolidays = QPushButton("Edit Holiday Calendar")
        self._forcePallet = QComboBox()
        self._importPallet = QPushButton("Import Pallet")
        self._exportPallet = QPushButton("Export Pallet")
        self._customizePallet = QPushButton("Customize Pallet")
        self._defaultPath = QLineEdit()
        self._defaultPath.setDisabled(bool(True))
        self._defaultPathButton = QPushButton("Browse")
        self._save = QPushButton("Save")
        self._cancel = QPushButton("Cancel")

        self._generalGroupBox = QGroupBox("General Settings")
        self._generalGrid.addWidget(self._colorBasedOnDate, 0, 0)
        self._generalGrid.addWidget(self._editHolidays, 1, 0)
        self._generalGrid.addWidget(self._forcePallet, 2, 0)
        self._generalGrid.addWidget(self._importPallet, 3, 0)
        self._generalGrid.addWidget(self._exportPallet, 3, 1)
        self._generalGrid.addWidget(self._customizePallet, 4, 0)
        self._generalGrid.addWidget(self._defaultPath, 5, 0)
        self._generalGrid.addWidget(self._defaultPathButton, 5, 1)
        self._generalGrid.addWidget(self._cancel, 6, 2)
        self._generalGrid.addWidget(self._save, 6, 3)

        self._generalGroupBox.setLayout(self._generalGrid)
        self._hbox.addWidget(self._generalGroupBox)
        self.setLayout(self._hbox)
        self.exec_()

    def _showGeneral(self):
        pass

if __name__ == '__main__':
    # Not doing anything special here.
    pass