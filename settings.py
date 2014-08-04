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

from __future__ import print_function

import logging
logging.debug("Attempting to load (wait for confirmation)")

import json
import os
import sys
import utilities as util

from PySide.QtCore import *
from PySide.QtGui import *

###################################################
##      APPLICATION SETTINGS - DO NOT MODIFY     ##
###################################################

from rawSettings import settings

###################################################
##      END OF APPLICATION SETTINGS              ##
###################################################

def clearSettingsFile():
    pass


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
        # Check for existance of settings file - if none exists, create one.
        if not self.check_settingsExistance():
            save_appSettingsFile()

    def create_appSettingsFile(self):
        pass

    def check_settingsExistance(self):
        """
        Check to see if the application file exists.

        If the file does not exist then create one.
        """
        settingsFile = ".llamlSettings"
        state = None

        if os.path.isfile(settingsFile):
            logging.info("A pre-existing settings file was found.")
            self.load_appSettingsFile()
            state = True
        else:
            logging.info("No pre-existing settings file located.  Creating a " \
                         "new settings file.")
            state = False
        return state

    def validate_appSettingsFile(self):
        """
        Validate the application settings file.

        This only compares the keys of the JSON structure.  If the keys
        are the same, regardless of the values, then the structures are
        considered to be equivalent.
        """
        state = False
        _allFileKeys = util.explode_dictKeys(settings)

        try:
            with open('.llamlSettings', 'r') as mySettingsFile:
                _allSettingKeys = util.explode_dictKeys(json.loads(mySettingsFile.read()))

            if _allFileKeys == _allSettingKeys:
                logging.info("Verified the integrity of the settings file.")
                state = True
            else:
                logging.info("The settings file is not valid (unknown reason).")
        except:
            # doesn't matter what the error is, the validation failed.
            pass
        return state

    def load_appSettingsFile(self):
        global settings
        state = None
        _validateAttempt = 0

        is_valid = self.validate_appSettingsFile()

        if not is_valid:
            logging.info("Saving a new settings file & destroying the old one!")
            # TODO - save the OLD settings file -- prompt the user to destroy/keep.s
            self.save_appSettingsFile()

            if _validateAttempt == 0:
                logging.info("Attempting to revalidate the new settings file!")
                is_valid = self.validate_appSettingsFile()
                _validateAttempt += 1
            else:
                logging.debug("Unable to create a new settings file - the "\
                              "sentinel variable reached its max value due "\
                              "to an unknown reason.  No settings file was "\
                              "created in-place or to replace the old file.")
                is_valid = False

        if is_valid:
            try:
                logging.info("Attempting to load the previously identified settings file.")
                with open('.llamlSettings', 'r') as settingsFile:
                    settings = json.loads(settingsFile.read())
                state = True
            except:
                logging.error("Loading of the settings file failed for an unknown " \
                              "reason: {0}".format(sys.exc_info()))
                state = False
        else:
            logging.info("Unable to verify the integrity of the settings file.")

        return state


    def save_appSettingsFile(self):
        try:
            with open('.llamlSettings', 'w') as setFile:
                setFile.write(json.dumps(settings, indent=4, separators=(',', ': ')))
            logging.info("Wrote out settings to settings file.")
        except:
            logging.warn("Unable to save settings file for unknown reason.")

    def saveAs_appSettingsFile(self):
        pass


class ProgramSettingsWindow(QDialog):
    def __init__(self):
        super(ProgramSettingsWindow, self).__init__()
        self.exec_()


class ApplicationSettingsWindow(QDialog):

    def __init__(self):
        super(ApplicationSettingsWindow, self).__init__()
        self.setMaximumWidth(600)
        self.setFixedSize(self.size())
        self.setWindowTitle("LLaML Settings")
        # This layout is the listview and the submenu selection.
        self._hbox = QHBoxLayout()
        # This layout contains the the various submenu's content paines.
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
        self._save.clicked.connect(self._pushed_savedBtn)
        self._cancel = QPushButton("Cancel")
        #Close the modal dialog and return to the application
        self._cancel.clicked.connect(self.reject)

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
        self._vbox.addLayout(self._commitCancelLayout)
        self.setLayout(self._hbox)

        # Set Settings Atributes here - JSON format for easy export/import.
        self.defaultProjectPath = ""

        # Show the application window.
        self.exec_()

    def _pushed_savedBtn(self):
        """
        This is the default behavior for when you press the 'save' button
        on the application settings dialog.

        This will save the current settings (and cause to modify the entire
        application instance where the settings should be applied).
        """
        settingsFile.save_appSettingsFile()
        self.close()

    class ListViewWidget(QListWidget):
        """
        ListViewWidget falls under the exclusive parent class of
        ApplicationSettingsWindow.
        """

        def _buildListViewItems(self):
            """
            Helper function to build a list of mappings of text:memory-ref
            foreach item within the ListViewWidget.
            """

            # Count how many items are currently in the list.
            _count = self.count()
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
            # Global is not needed, but it is explicit
            global settings
            self._settings = settings['ApplicationSettings']['AudioTab']

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
            self._sampleRateDict = {0 : 'raw',
                                    1: 'low',
                                    2: 'med',
                                    3: 'high'}
            #setattr(self._visualSampleRate, 'rateMap', sampleRateDict)
            self._visualSampleRate.currentIndexChanged.connect(
                lambda x: self._update_sampleRate(x))

            # Cache waveforms and redraw only on demand (this can be performance
            # enhancing!).
            self._cacheWaveForms = QCheckBox("Cache Waveforms (redraw only on demand)")
            self._cacheWaveForms.setChecked(True)
            setattr(self._cacheWaveForms, 'nameSetting', 'cacheWaveforms')
            self._cacheWaveForms.stateChanged.connect(
                lambda: self._set_setting(self._cacheWaveForms))

            # Default startup volume level.
            self._audioLevelLabel = QLabel("Default Audio Level on Startup")
            self._audioLevelSlider = QSlider(Qt.Horizontal)
            self._rawAudioSliderValue = "{0}%".format(self._audioLevelSlider.value()+1)
            self._audioLevelValue = QLabel(self._rawAudioSliderValue)
            setattr(self._audioLevelSlider, 'nameSetting', 'defaultAudioLevelOnStartup')
            self._audioLevelSlider.valueChanged.connect(self._update_audioLevel)

            self._generalVGrid = QVBoxLayout()
            self._generalVGrid.addWidget(self._visualSampleRateLabel)
            self._generalVGrid.addWidget(self._visualSampleRate)
            self._generalVGrid.addWidget(self._cacheWaveForms)
            self._generalVGrid.addWidget(self._audioLevelLabel)
            self._audioSliderHGrid = QHBoxLayout()
            self._audioSliderHGrid.addWidget(self._audioLevelValue)
            self._audioSliderHGrid.addWidget(self._audioLevelSlider)
            self._generalVGrid.addLayout(self._audioSliderHGrid)
            self._generalVGrid.addStretch()

            self.setLayout(self._generalVGrid)

        def _update_audioLevel(self, level):
            """
            Updates the audio level percentage.

            This is a helper function.
            """
            self._rawAudioSliderValue = "{0}%".format(level+1)
            self._audioLevelValue.setText(self._rawAudioSliderValue)
            self._settings['defaultAudioLevelOnStartup'] = level + 1
            print(settings)

        def _update_sampleRate(self, level):
            self._settings['rawSampleRate'] = self._sampleRateDict[level]
            print(settings)

        def _set_setting(self, option, value=None, *args, **kwargs):
            if isinstance(option, QCheckBox) and option.nameSetting:
                self._settings[str(option.nameSetting)] = option.isChecked()
                print(settings)
            elif option.nameSetting:
                self._settings[str(option.nameSetting)] = value
            else:
                logging.debug("User attempted to change an application setting " \
                              "and the setting doesn't have a 'nameSetting' " \
                              "attribute.  No settings were changed.")
                # TODO add in custom error logic to present user with an error.
                # TODO add in additional logging messages that are more verbose.
                return False


    class AdministrationViewWidget(QWidget):
        def __init__(self, *args, **kwargs):
            QWidget.__init__(self)
            self._importBtn = QPushButton("Import Settings")
            self._exportBtn = QPushButton("Export Settings")
            self._exportBtn.clicked.connect(settingsFile.save_appSettingsFile)
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
            # Pull-in global setttings.
            global settings
            self._settings = settings['ApplicationSettings']['GeneralTab']

            QWidget.__init__(self)
            # General form/page
            # Create all the options/widgets
            self._generalGrid = QVBoxLayout()

            # Force pallet/colors select box.
            self._forcePallet = QComboBox()
            self._customizePallet = QPushButton("Edit Pallets")

            # Holiday groupings
            self._holidayGrouping = QGroupBox("Application Colors Based on " \
                                              "Holiday")
            self._holidayLayout = QVBoxLayout()
            self._colorBasedOnDate = QCheckBox("Default color pallet to " \
                                               "nearest holiday?")
            setattr(self._colorBasedOnDate, "nameSetting", "colorPalletByDate")
            self._colorBasedOnDate.stateChanged.connect(
                lambda: self._set_setting(self._colorBasedOnDate))
            self._editHolidays = QPushButton("Edit Holiday Calendar")
            # Dummy fn to call/see current settings...
            self._editHolidays.clicked.connect(lambda: print(settings))

            self._holidayLayout.addWidget(self._colorBasedOnDate)
            self._holidayLayout.addWidget(self._editHolidays)
            self._holidayGrouping.setLayout(self._holidayLayout)

            # Default project path
            self._defaultPathGroupBox = QGroupBox("Default Project Path")
            self._defaultPathLayout = QHBoxLayout()
            self._defaultPath = QLineEdit()
            self._defaultPath.setDisabled(True)

            self._defaultPathButton = QPushButton("Select")
            self._defaultPathButton.clicked.connect(lambda:
                                                    ApplicationSettingsWindow._SelectDirectoryPath(self))

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

        def _set_setting(self, option, value=None, *args, **kwargs):
            if isinstance(option, QCheckBox) and option.nameSetting:
                self._settings[str(option.nameSetting)] = option.isChecked()
            elif option.nameSetting:
                self._settings[str(option.nameSetting)] = value
            else:
                logging.debug("User attempted to change an application setting " \
                              "and the setting doesn't have a 'nameSetting' " \
                              "attribute.  No settings were changed.")
                # TODO add in custom error logic to present user with an error.
                # TODO add in additional logging messages that are more verbose.
                return False

        def _changeProjectDirectory(self, directory, *args, **kwargs):
            self._defaultPath.setText(directory)
            logging.info("Default project path changed, but not yet saved, "
                         "to {0}.".format(directory))

    class _SelectDirectoryPath(QObject):
        def __init__(self, *args, **kwargs):
            self.defaultProjectDirectory = None
            self._parent = args[0]
            self.nameSetting = "defProjectPath"
            self._show_existingDir()

        def _show_existingDir(self, *args, **kwargs):
            logging.debug("User requested to opent he " \
                          "QFileDialog.getExistingDirectory()")
            _directory = QFileDialog.getExistingDirectory()
            if _directory != None:
                self._change_existingDir(_directory)
            else:
                logging.debug("User didn't select a default proj. directory "\
                              "- they cancelled out.")
        def _change_existingDir(self, directory, *args, **kwargs):
            if directory != None:
                self.defaultProjectDirectory = self._parent._set_setting(self, directory)
                self._parent._changeProjectDirectory(directory)
            else:
                # Doesn't need changing!
                pass


    class CommunicationsViewWidget(QWidget):
            '''
            CommunicatiosViewWidget falls under the exclusive parent class of
            ApplicationSettingsWindow and is a container for the Communication
            Settings.
            '''
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
                    return self.serverOnOffBtn.setText("Server Status: " \
                                                       "{0}".format(self.serverStatusTxt.get(
                            self.serverStatus, "UNKNOWN")))

            class ClientTab(QWidget):
                def __init__(self, *args, **kwargs):
                    QWidget.__init__(self)

                    # The local machine information
                    self.thisAvahi = "NA"
                    self.thisIP = "0.0.0.0"
                    self.thisPort = 0

                    # The target server information
                    self.servUsername = None
                    self.servPassword = None
                    self.servIP = "0.0.0.0"
                    self.servAvahi = "NA"
                    self.servPort = 0

                    self.serverInfoGroupBox = QGroupBox("Server Info")
                    self.clientGeneralLayout = QVBoxLayout()
                    self.serverColOne = QGridLayout()

                    # Add Username text field
                    _serverIPLbl = QLabel("Server IP:")
                    self.servIP =  QLineEdit()
                    self.serverColOne.addWidget(_serverIPLbl, 0, 0)
                    self.serverColOne.addWidget(self.servIP, 0, 1)

                    # Add Username text field
                    _serverPort = QLabel("Server Port:")
                    self.servPort =  QLineEdit()
                    self.serverColOne.addWidget(_serverPort, 1, 0)
                    self.serverColOne.addWidget(self.servPort, 1, 1)

                    # Add Username text field
                    _userLbl = QLabel("Username:")
                    self.username =  QLineEdit()
                    self.serverColOne.addWidget(_userLbl, 2, 0)
                    self.serverColOne.addWidget(self.username, 2, 1)

                    # Add Password text field
                    _passwordLbl = QLabel("Password:")
                    self.password = QLineEdit()
                    self.password.setEchoMode(QLineEdit.Password)
                    self.serverColOne.addWidget(_passwordLbl, 3, 0)
                    self.serverColOne.addWidget(self.password, 3, 1)

                    # Add "Connect" button
                    self.connectBtn = QPushButton("Connect with Server")
                    self.installCert = QPushButton("Certificate Management")

                    self.serverColOne.addWidget(self.connectBtn, 4, 0)
                    self.serverColOne.addWidget(self.installCert, 4, 1)

                    self.serverInfoGroupBox.setLayout(self.serverColOne)
                    self.clientGeneralLayout.addWidget(self.serverInfoGroupBox)

                    self.commInfoGroupBox = QGroupBox("Test Communications")
                    self.commVBoxMainLayout = QVBoxLayout()
                    self.commHBoxLayout = QHBoxLayout()
                    self.commVBoxLayout = QVBoxLayout()

                    self._startComm = QPushButton("Start Test")
                    self._stopComm = QPushButton("Stop Test")
                    self._exportCommLog = QPushButton("Export Log")

                    self._logDataTextField = QTextEdit()
                    self._logDataTextField.setReadOnly(True)

                    self.commHBoxLayout.addWidget(self._startComm)
                    self.commHBoxLayout.addWidget(self._stopComm)

                    self.commVBoxLayout.addLayout(self.commHBoxLayout)
                    self.commVBoxLayout.addStretch()
                    self.commVBoxLayout.addWidget(self._logDataTextField)
                    self.commVBoxLayout.addWidget(self._exportCommLog)
                    self.commVBoxLayout.addStretch()

                    self.commVBoxMainLayout.addLayout(self.commHBoxLayout)
                    self.commVBoxMainLayout.addLayout(self.commVBoxLayout)
                    self.commVBoxMainLayout.addStretch()

                    self.commInfoGroupBox.setLayout(self.commVBoxMainLayout)

                    self.clientGeneralLayout.addWidget(self.commInfoGroupBox)
                    self.clientGeneralLayout.addStretch()

                    self.setLayout(self.clientGeneralLayout)

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
                    self._exportBtn.clicked.connect(lambda: print('test'))
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
            # Global is not necessary here, but it's explicit.
            global settings
            self._settings = settings['ApplicationSettings']['StartupTab']

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

            # Start playing on application load.
            self._playOnStartCheckBox = QCheckBox("Start auto playing project "\
                                                  "on application load.")
            setattr(self._playOnStartCheckBox, 'nameSetting', 'startOnLoad')
            self._playOnStartCheckBox.stateChanged.connect(
                lambda: self._set_setting(self._playOnStartCheckBox))
            self._defaultProjectVGrid.addWidget(self._playOnStartCheckBox)
            self._defaultProjectGrouping.setLayout(self._defaultProjectVGrid)

            # Toggle widgets GROUP BOX
            self._widgetToggleGroupBox = QGroupBox("Toggle Widgets on Startup")

            # Show status bar on startup behavior.  If true, it will show
            # the statusbar - else the statusbar is hidden.
            self._statusbarCheckBox = QCheckBox("Show Status Bar")
            setattr(self._statusbarCheckBox, 'nameSetting', 'showStatusBarOnStartup')
            self._statusbarCheckBox.stateChanged.connect(
                lambda: self._set_setting(self._statusbarCheckBox))

            # Show the audio bar at the top of the screen (the audio menu bar).
            # If true, then this will show the audio controls at the top of the
            # screen.  If false, it will show nothing/be hidden on startup.
            self._audiobarCheckBox = QCheckBox("Show Audio Bar")
            setattr(self._audiobarCheckBox, 'nameSetting', 'showAudioBarOnStartup')
            self._audiobarCheckBox.stateChanged.connect(
                lambda: self._set_setting(self._audiobarCheckBox))

            # Show the audio waveform bar at the top of the application.  If true,
            # this will show the processor-intensive waveform at the top.  False,
            # will hide it - thus, saving some overhead on application load.
            self._visualWaveFormCheckBox = QCheckBox("Show Visual Wave Form")
            setattr(self._visualWaveFormCheckBox, 'nameSetting', 'showVisualWaveOnStartup')
            self._visualWaveFormCheckBox.stateChanged.connect(
                lambda: self._set_setting(self._visualWaveFormCheckBox))

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

        def _set_setting(self, option, value=None, *args, **kwargs):
            if isinstance(option, QCheckBox) and option.nameSetting:
                self._settings[str(option.nameSetting)] = option.isChecked()
                print(settings)
            elif option.nameSetting:
                self._settings[str(option.nameSetting())] = value
            else:
                logging.debug("User attempted to change an application setting " \
                              "and the setting doesn't have a 'nameSetting' " \
                              "attribute.  No settings were changed.")
                # TODO add in custom error logic to present user with an error.
                # TODO add in additional logging messages that are more verbose.
                return False

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

settingsFile = ApplicationSettingsFile()

if __name__ == '__main__':
    # Not doing anything special here.
    pass

logging.debug("Successfully loaded.")