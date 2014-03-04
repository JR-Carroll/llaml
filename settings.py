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
        self.setFixedSize(self.size())
        self.setWindowTitle("LLaML Settings")
        self._hbox = QHBoxLayout()
        # Add a layout to the main settings window.
        self._vbox = QVBoxLayout()

        # Add a listview widget that will have a listing of all the child menus.
        self.listView = self.ListViewWidget()
        self.listView.currentItemChanged.connect(self._toggleVisibility)
        self.listView.setMaximumWidth(150)

        self.generalView = self.GeneralViewWidget()
        self.startupView = self.StartupViewWidget()
        self.audioView = self.AudioViewWidget()
        self.commView = self.CommunicationsViewWidget()
        self.adminView = self.AdministrationViewWidget()

        self.startupView.setHidden(True)
        self.audioView.setHidden(True)
        self.commView.setHidden(True)
        self.adminView.setHidden(True)

        self._save = QPushButton("Save")
        self._cancel = QPushButton("Cancel")

        self._allSettingsWidgets = {'General': self.generalView,
                                    'Start-up': self.startupView,
                                    'Audio': self.audioView,
                                    'Communications': self.commView,
                                    'Administration': self.adminView}

        self._allItemsInList = self.listView._buildListViewItems()

        self._hbox.addWidget(self.listView)

        self._vbox.addWidget(self.generalView)
        self._vbox.addWidget(self.startupView)
        self._vbox.addWidget(self.audioView)
        self._vbox.addWidget(self.commView)
        self._vbox.addWidget(self.adminView)
        self._vbox.addStrut(400)

        self._commitCancelLayout = QHBoxLayout()
        self._commitCancelLayout.addStretch()
        self._commitCancelLayout.addWidget(self._cancel)
        self._commitCancelLayout.addWidget(self._save)

        self._hbox.addLayout(self._vbox)
        self._hbox.addStretch()
        self._vbox.addLayout(self._commitCancelLayout)
        self.setLayout(self._hbox)
        self.exec_()


    class ListViewWidget(QListWidget):
        '''ListViewWidget falls under the exclusive parent class of
        ApplicationSettingsWindow.'''

        def _buildListViewItems(self):
            '''Helper function to build a list of mappings of text:memory-ref
            foreach item within the ListViewWidget.'''

            _count = self.count() # Count how many items are currently in the list.
            _dict = {}

            for item in range(0, _count):
                _dict[self.item(item).text()] = None

            return _dict

        def __init__(self, *args, **kwargs):
            QListWidget.__init__(self)

            self.setGeometry(0, 0, 150, 200)
            # List Widget Items -- add here if more setting pannels are needed.
            self._general = QListWidgetItem('General')
            self._startup = QListWidgetItem('Start-up')
            self._audio = QListWidgetItem('Audio')
            self._comms = QListWidgetItem('Communications')
            self._admin = QListWidgetItem('Administration')

            self.addItem(self._general)
            self.addItem(self._startup)
            self.addItem(self._audio)
            self.addItem(self._comms)
            self.addItem(self._admin)


    class AudioViewWidget(QWidget):
        '''AudioViewWidget falls under the exclusive parent class of
        ApplicationSettingsWindow and is a container for the Audio Settings.'''
        def __init__(self, *args, **kwargs):
            QWidget.__init__(self)
            # General form/page
            # Create all the options/widgets
            self._visualSampleRate = QComboBox()

            self._visualSampleRateLabel = QLabel("Adjust the sample rate at which "
                                                 "the visual waveforms are drawn; "
                                                 "lower sample rates can increase "
                                                 "performance.")
            self._visualSampleRateLabel.setWordWrap(True)

            self._visualSampleRate.addItem("Raw Sample Rate (unknown performance)")
            self._visualSampleRate.addItem("Low Sample Rate (best performance)")
            self._visualSampleRate.addItem("Med Sample Rate ('meh' performance)")
            self._visualSampleRate.addItem("High Sample Rate (worst performance)")

            self._cacheWaveForms = QCheckBox("Cache Waveforms (redraw only on demand)")
            self._cacheWaveForms.setChecked(True)

            self._audioLevelLabel = QLabel("Default Audio Level on Startup")
            self._audiolevelSlider = QSlider(Qt.Horizontal)

            self._generalVGrid = QVBoxLayout()
            self._generalVGrid.addWidget(self._visualSampleRateLabel)
            self._generalVGrid.addWidget(self._visualSampleRate)
            self._generalVGrid.addWidget(self._cacheWaveForms)
            self._generalVGrid.addWidget(self._audioLevelLabel)
            self._generalVGrid.addWidget(self._audiolevelSlider)
            self._generalVGrid.addStretch()

            self.setLayout(self._generalVGrid)


    class AdministrationViewWidget(QWidget):
        def __init__(self, *args, **kwargs):
            QWidget.__init__(self)
            self._importBtn = QPushButton("Import Settings")
            self._exportBtn = QPushButton("Export Settings")
            self._restoreBtn = QPushButton("Restore Settings")
            self._logDebug = QCheckBox("Create log/debug-mode")

            self._generalVGrid = QVBoxLayout()
            self._generalVGrid.addWidget(self._importBtn)
            self._generalVGrid.addWidget(self._exportBtn)
            self._generalVGrid.addWidget(self._restoreBtn)
            self._generalVGrid.addWidget(self._logDebug)
            self._generalVGrid.addStretch()

            self.setLayout(self._generalVGrid)


    class GeneralViewWidget(QWidget):
        '''GeneralViewWidget falls under the exclusive parent class of
        ApplicationSettingsWindow and is a container for the General Settings.'''
        def __init__(self, *args, **kwargs):
            QWidget.__init__(self)
            # General form/page
            # Create all the options/widgets
            self._generalGrid = QVBoxLayout()

            # Force pallet/colors select box.
            self._forcePallet = QComboBox()
            self._customizePallet = QPushButton("Edit Pallets")

            # Holiday groupings
            self._holidayGrouping = QGroupBox("Application Colors Based on Holiday")
            self._holidayLayout = QVBoxLayout()
            self._colorBasedOnDate = QCheckBox("Default color pallet to nearest holiday?")
            self._editHolidays = QPushButton("Edit Holiday Calendar")
            #self._editHolidays.connect(QDialog) ## TODO:  Implement connected behavior.
            self._holidayLayout.addWidget(self._colorBasedOnDate)
            self._holidayLayout.addWidget(self._editHolidays)
            self._holidayGrouping.setLayout(self._holidayLayout)

            # Default project path
            self._defaultPathGroupBox = QGroupBox("Default Project Path")
            self._defaultPathLayout = QHBoxLayout()
            self._defaultPath = QLineEdit()
            self._defaultPath.setDisabled(True)
            self._defaultPathButton = QPushButton("Select")
            self._defaultPathLayout.addWidget(self._defaultPath)
            self._defaultPathLayout.addWidget(self._defaultPathButton)
            self._defaultPathGroupBox.setLayout(self._defaultPathLayout)

            self._forcePalletGrouping = QGroupBox("Manually Select Pallet")
            self._forcePalletLayout = QVBoxLayout()
            self._forcePalletLayout.addWidget(self._forcePallet)
            self._forcePalletLayout.addWidget(self._customizePallet)
            self._forcePalletGrouping.setLayout(self._forcePalletLayout)

            # Add to the General Display grid
            self._generalGrid.addWidget(self._holidayGrouping)
            self._generalGrid.addWidget(self._forcePalletGrouping)
            self._generalGrid.addWidget(self._defaultPathGroupBox)

            self.setLayout(self._generalGrid)

    class CommunicationsViewWidget(QWidget):
            '''CommunicatiosViewWidget falls under the exclusive parent class of
            ApplicationSettingsWindow and is a container for the Communication Settings.'''
            def __init__(self, *args, **kwargs):
                QWidget.__init__(self)
                # General form/page
                # Create all the options/widgets
                self._generalGrid = QVBoxLayout()
                self._testLabel = QLabel("Testing this out...")

                self._tabWidget = QTabWidget()

                self._tabWidget.addTab(self.DevicesTab(), "Devices")
                self._tabWidget.addTab(self.EmailTab(), "Email")
                self._tabWidget.addTab(self.ServerTab(), "Server")
                self._tabWidget.addTab(self.ClientTab(), "Client")

                self._generalGrid.addWidget(self._tabWidget)
                self.setLayout(self._generalGrid)

            class EmailTab(QWidget):
                def __init__(self, *args, **kwargs):
                    QWidget.__init__(self)
                    self._generalGrid = QVBoxLayout()

                    self._emailCheckBoxLayout = QVBoxLayout()

                    self._emailOnSchedStartup = QCheckBox("Email on Scheduled Application Start-up")
                    self._emailOnSongChange = QCheckBox("Email on Song Change")
                    self._emailOnSchedClose = QCheckBox("Email on Scheduled Application Close")
                    self._emailOnError = QCheckBox("Email on Error")
                    self._customizeEmail = QPushButton("Customize Email")

                    self._emailCheckBoxLayout.addWidget(self._emailOnSchedStartup)
                    self._emailCheckBoxLayout.addWidget(self._emailOnSongChange)
                    self._emailCheckBoxLayout.addWidget(self._emailOnSchedClose)
                    self._emailCheckBoxLayout.addWidget(self._emailOnError)
                    self._emailCheckBoxLayout.addWidget(self._customizeEmail)

                    self._emailGroupBox = QGroupBox("Email On Event:")
                    self._emailGroupBox.setLayout(self._emailCheckBoxLayout)


                    self._fromLabel = QLabel("Send Email From This Address:")
                    self._fromEmail = QLineEdit()
                    self._toLabel  = QLabel("Send Email To This Address:")
                    self._toEmail = QLineEdit()
                    self._testEmail = QPushButton("Send Test Email")

                    self._generalGrid.addWidget(self._emailGroupBox)
                    self._generalGrid.addWidget(self._fromLabel)
                    self._generalGrid.addWidget(self._fromEmail)
                    self._generalGrid.addWidget(self._toLabel)
                    self._generalGrid.addWidget(self._toEmail)
                    self._generalGrid.addWidget(self._testEmail)

                    self.setLayout(self._generalGrid)


            class ServerTab(QWidget):
                def __init__(self, *args, **kwargs):
                    QWidget.__init__(self)
                    # Basic layout
                    self._generalLayout = QVBoxLayout()
                    # The Server is initialized to off to begin with
                    self.serverStatus = 0
                    self._serverStatusDict = {0 : "UNKNOWN",
                                              1 : "OFF",
                                              2 : "ON",
                                              3 : "ERROR/SEE LOG"}
                    self.serverStatusTxt = self._serverStatusDict.get(\
                        self.serverStatus,
                        "UNKNOWN")

                    self.serverIP = "UNKNOWN"
                    self.serverPort = "UNKNOWN"
                    self.serverMDNS = "UNKNOWN"

                    serverButtonsLayout = self._serverButtons()
                    serverInfoGBox = self._serverInfo()

                    # Add elements to the layout and set layout as default
                    self._generalLayout.addLayout(serverButtonsLayout)
                    self._generalLayout.addWidget(serverInfoGBox)
                    self._generalLayout.addStretch()
                    self.setLayout(self._generalLayout)

                def _serverInfo(self):
                    '''Create/manage the server info grouping box'''
                    grouping = QGroupBox("Server Details")
                    layout = QGridLayout()

                    IPTxt = QLabel("Server IP: ")
                    PortTxt = QLabel("Port: ")
                    MDNSTxt = QLabel("MDNS Name: ")
                    StatusTxt = QLabel("Server Status: ")

                    # Column 0, multi rows
                    layout.addWidget(StatusTxt, 0, 0)
                    layout.addWidget(IPTxt, 1, 0)
                    layout.addWidget(PortTxt, 2, 0)
                    layout.addWidget(MDNSTxt, 3, 0)

                    # Column 1, multi rows
                    layout.addWidget(QLabel(self.serverStatusTxt), 0, 1)
                    layout.addWidget(QLabel(self.serverIP), 1, 1)
                    layout.addWidget(QLabel(self.serverPort), 2, 1)
                    layout.addWidget(QLabel(self.serverMDNS), 3, 1)
                    grouping.setLayout(layout)
                    return grouping

                def _serverButtons(self):
                    '''Create/manage the buttons at the top of the settings screen'''
                    # Update the buttons
                    self.serverStatusTxt = self._serverStatusDict.get(\
                                            self.serverStatus,
                                            "UNKNOWN")

                    # Need various layouts to position all elements
                    layoutVert = QVBoxLayout()
                    layoutHor = QHBoxLayout()

                    # The Server Start/Stop Button (also shows status)
                    self.serverOnOffBtn = QPushButton(
                        "Server Status {}".format(self.serverStatusTxt))
                    self.serverOnOffBtn.setCheckable(True)

                    # Buttons just below the Server Start/Stop
                    self.serverSettingsBtn  = QPushButton("Server Settings")
                    self.testServerBtn = QPushButton("Test Server")

                    # Layout the buttons
                    layoutHor.addWidget(self.serverSettingsBtn)
                    layoutHor.addWidget(self.testServerBtn)

                    layoutVert.addWidget(self.serverOnOffBtn)
                    layoutVert.addLayout(layoutHor)
                    return layoutVert


                def changeServerStatus(self, status=0):
                    '''
                    Change the Server Status Button status, and change the button
                    to notify users.

                    TODO:  Not fully implemented yet -- not connected to the anything
                    '''
                    self.serverStatus = status
                    return self.serverOnOffBtn.setText("Server Status: {0}".format(self.serverStatusTxt.get(
                            self.serverStatus, "UNKNOWN")))

            class ClientTab(QWidget):
                def __init__(self, *args, **kwargs):
                    QWidget.__init__(self)

            class DevicesTab(QWidget):
                '''Sinlgeton for the devices tab of the settings menu.'''
                def __init__(self, *args, **kwargs):
                    QWidget.__init__(self)
                    self._hboxLayout = QHBoxLayout()
                    self._gridLayout = QGridLayout()
                    self._vboxLayout = QVBoxLayout()

                    self._commDeviceList = QListView()

                    self._addDevicesBtn  = QPushButton("Add")
                    self._removeDevicesBtn = QPushButton("Remove")
                    self._editDevicesBtn = QPushButton("Edit")
                    self._exportBtn = QPushButton("Export")
                    self._importBtn = QPushButton("Import")

                    self._vboxLayout.addWidget(self._addDevicesBtn)
                    self._vboxLayout.addWidget(self._removeDevicesBtn)
                    self._vboxLayout.addWidget(self._editDevicesBtn)
                    self._vboxLayout.addWidget(self._importBtn)
                    self._vboxLayout.addWidget(self._exportBtn)
                    self._vboxLayout.addStretch()

                    # Add List Box and Buttons to HBoxLayout
                    self._hboxLayout.addWidget(self._commDeviceList)
                    self._hboxLayout.addLayout(self._vboxLayout)
                    self._hboxLayout.addStretch()
                    # Add to the overall gridded layout
                    self._gridLayout.addLayout(self._hboxLayout, 0, 0)

                    self.setLayout(self._gridLayout)


    class StartupViewWidget(QWidget):
        def __init__(self):
            QWidget.__init__(self)
            # General form/page
            # Create all the options/widgets
            self._startupGrid = QVBoxLayout()

            # Create the various widgets that get added to the Startup View
            self._defaultProjectGrouping = QGroupBox("Default Project to Start-up")
            self._defaultProjectHGrid = QHBoxLayout()
            self._defaultProjectVGrid = QVBoxLayout()
            self._defaultProject = QLineEdit()
            self._defaultProject.setDisabled(True)
            self._defaultProjectBrowseBtn = QPushButton("Select")
            self._defaultProjectHGrid.addWidget(self._defaultProject)
            self._defaultProjectHGrid.addWidget(self._defaultProjectBrowseBtn)
            self._defaultProjectVGrid.addLayout(self._defaultProjectHGrid)
            self._playOnStartCheckBox = QCheckBox("Start playing project on application load.")
            self._defaultProjectVGrid.addWidget(self._playOnStartCheckBox)
            self._defaultProjectGrouping.setLayout(self._defaultProjectVGrid)

            # Toggle widgets GROUP BOX
            self._widgetToggleGroupBox = QGroupBox("Toggle Widgets on Startup")
            self._statusbarCheckBox = QCheckBox("Show Status Bar")
            self._audiobarCheckBox = QCheckBox("Show Audio Bar")
            self._visualWaveFormCheckBox = QCheckBox("Show Visual Wave Form")
            self._widgetToggleLayout = QVBoxLayout()
            self._widgetToggleLayout.addWidget(self._statusbarCheckBox)
            self._widgetToggleLayout.addWidget(self._audiobarCheckBox)
            self._widgetToggleLayout.addWidget(self._visualWaveFormCheckBox)
            self._widgetToggleLayout.addStretch()

            self._widgetToggleGroupBox.setLayout(self._widgetToggleLayout)

            self._startupGrid.addWidget(self._defaultProjectGrouping)
            self._startupGrid.addWidget(self._widgetToggleGroupBox)
            self._startupGrid.addStretch()
            self.setLayout(self._startupGrid)


    def _toggleVisibility(self, current, previous, *args, **kwargs):
        '''Toggle widget visibility.'''
        currentTxt = current.text()

        try:
            previousTxt = previous.text()
        except AttributeError:
            # If previous is not available, set to none; this occurs on first
            # creation.
            previousTxt = None

        try:
            for item in self._allItemsInList:
                if item == currentTxt:
                    # Toggle visibility to TRUE for the widget we want to see.
                    self._allSettingsWidgets.get(currentTxt, None).setHidden(False)
                    continue
                self._allSettingsWidgets.get(previousTxt, None).setHidden(True)
        except AttributeError:
            pass

        return currentTxt, previousTxt


    def _showGeneral(self):
        pass

    def _hideGeneral(self):
        self._colorBasedOnDate.setVisible(bool(False))
        pass

    def _showStartup(self):
        pass

    def _showAudio(self):
        pass

    def _showCommunications(self):
        pass

    def _showAdmin(self):
        pass

if __name__ == '__main__':
    # Not doing anything special here.
    pass