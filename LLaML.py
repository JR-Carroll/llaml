#!/usr/bin/python

"""
Color palette in use:

#112233 -> dark blue
#446699
#6688bb
#5588dd
#bbddff -> light blue


PEH-GCA = Pokemon Exception Handling - Gotta Catch'um All
"""

# Import PySide classes
from __future__ import print_function
import sys
import time

from PySide.QtCore import *
from PySide.QtGui import *

from audiotoolbar import AudioToolBar
from aboutdialog import AboutDialog
from audiodisplay import *
from audio import *
from programmgr import ProgramManager
from scheduler import ScheduleView
from settings import *
from systemcheck import SystemTest
from zonewidget import *


# Create a Qt application
app = QApplication(sys.argv)
app.setWindowIcon(QIcon('greenLightSM.png'))
app.setApplicationName("LLaML")

# Loading images once to pass around to the various classes
# that need it.  Images HAVE to be loaded AFTER the QApplication
# and need to be passed around to the various Qt widgets as lambdas.
from resources import _lightICON, _lightPM

class ParentWindowMgr(QMainWindow):
    def __init__(self):
        super(ParentWindowMgr, self).__init__()

        # File Menu
        _newProjectFileM = QAction('&New Project', self)
        _newProjectFileM.setShortcut('Ctrl+N')
        _newProjectFileM.setStatusTip("Create a new project")

        _openFileM = QAction('&Open Project', self)
        _openFileM.setShortcut('Ctrl+O')
        _openFileM.setStatusTip("Open an existing project file")
        _openFileM.triggered.connect(self.openFileWindow)
        self._openFileName = None

        _saveFileM = QAction('&Save Project', self)
        _saveFileM.setStatusTip("Save the currently opened project")

        _saveAsFileM = QAction('Save Project As', self)
        _saveAsFileM.setStatusTip("Save the currently project something other " +
                                  "what it is currently saved as.")

        _closeProjectFileM = QAction('&Close Project', self)
        _closeProjectFileM.setShortcut('Ctrl+W')
        _closeProjectFileM.setStatusTip("Close the current project")

        _recentSubmenu = QMenu('Recent Projects', self)
        # XXX: Tempory file objects to through into the recent menu.
        _recentProject1ListFileM = QAction('File1.lam', self)
        _recentProject2ListFileM = QAction('File2.lam', self)

        _preferences = QAction('&Preferences', self)
        _preferences.setStatusTip("Edit application-level settings")
        _preferences.triggered.connect(ApplicationSettingsWindow)

        _exitFileM = QAction('E&xit', self)
        _exitFileM.setShortcut('Ctrl+Q')
        _exitFileM.setStatusTip("Exit LLaML")
        _exitFileM.triggered.connect(sys.exit)

        # Project Menu
        _programManagerProjectM = QAction('Program Manager', self)
        _programManagerProjectM.setStatusTip("Open the Program Manager")
        _programManagerProjectM.triggered.connect(ProgramManager)
        # Separator
        _editSettingsProjectM = QAction('Program Settings', self)
        _editSettingsProjectM.setStatusTip("Edit the current program settings")
        _editSettingsProjectM.triggered.connect(ProgramSettingsWindow)

        # Audio Menu
        _playAudioM = QAction('&Play', self)
        _playAudioM.setShortcut('Ctrl+P')
        _playAudioM.setStatusTip("Play audio file from last position")

        _pauseAudioM = QAction('Pa&use', self)
        _pauseAudioM.setShortcut('Ctrl+U')
        _pauseAudioM.setStatusTip("Pause the currently playing audio file")

        _stopAudioM = QAction('&Stop', self)
        _stopAudioM.setShortcut('Ctrl+T')
        _stopAudioM.setStatusTip("Stop the currently playing audio file, and rewind")

        _audioInfoAudioM = QAction('Audio &Info', self)
        _audioInfoAudioM.setStatusTip("See any currently available meta information")

        # View menu
        _waveformWidgetViewM = QAction('Toggle &Waveform', self)
        _waveformWidgetViewM.setStatusTip("Toggle viewing of waveform widget (can help performance)")
        _waveformWidgetViewM.setCheckable(bool(True))
        _waveformWidgetViewM.setChecked(bool(True))

        _zoneWidgetViewM = QAction('Toggle &Zone Widget', self)
        _zoneWidgetViewM.setStatusTip("See the Zone Widget")
        _zoneWidgetViewM.setCheckable(bool(True))
        _zoneWidgetViewM.setChecked(bool(True))

        _statusBarViewM = QAction('Toggle &Statusbar', self)
        _statusBarViewM.setStatusTip("Toggle the statusbar view")
        _statusBarViewM.setCheckable(bool(True))
        _statusBarViewM.setChecked(bool(True))

        _audioToolbarViewM = QAction('Toggle Audio Toolbar', self)
        _audioToolbarViewM.setStatusTip("Toggle the audio toolbar")
        _audioToolbarViewM.setCheckable(bool(True))
        _audioToolbarViewM.setChecked(bool(True))


        # Help menu
        _instructionsHelpM = QAction('Help Manual', self)
        _instructionsHelpM.setStatusTip("Part of the RTFM process")

        _aboutHelpM = QAction('&About LLaML', self)
        _aboutHelpM.setStatusTip("About LLaLM")
        _aboutHelpM.triggered.connect(lambda: AboutDialog(image=_lightPM))

        _wwwSiteHelpM = QAction('LLaML Website', self)
        _wwwSiteHelpM.setStatusTip("Go to LLaML website")
        _wwwSiteHelpM.triggered.connect(self.openLLaMLWWW)

        _systemCheckHelpM = QAction('System Check', self)
        _systemCheckHelpM.setStatusTip("Perform a system check to ensure everything" +
                                       "is working correclty")
        _systemCheckHelpM.triggered.connect(SystemTest)

        # Create the actual menubar that contains the various menus.
        menubar = self.menuBar()

        # FILE DROPDOWN
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(_newProjectFileM)
        fileMenu.addAction(_openFileM)
        # XXX: Dummy-place holder code for now.
        _recentSubmenu.addAction(_recentProject1ListFileM)
        _recentSubmenu.addAction(_recentProject2ListFileM)
        # XXX: END DUMMY CODE
        fileMenu.addMenu(_recentSubmenu)
        fileMenu.addAction(_closeProjectFileM)

        fileMenu.addSeparator()
        fileMenu.addAction(_preferences)
        fileMenu.addSeparator()
        fileMenu.addAction(_exitFileM)

        # EDIT DROPDOWN
        editMenu = menubar.addMenu('&Program')
        editMenu.addAction(_programManagerProjectM)
        editMenu.addSeparator()
        editMenu.addAction(_editSettingsProjectM)

        # AUDIO DROPDOWN
        audioMenu = menubar.addMenu('&Audio')
        audioMenu.addAction(_playAudioM)
        audioMenu.addAction(_pauseAudioM)
        audioMenu.addAction(_stopAudioM)
        audioMenu.addSeparator()
        audioMenu.addAction(_audioInfoAudioM)

        # VIEW DROPDOWN
        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(_waveformWidgetViewM)
        viewMenu.addAction(_zoneWidgetViewM)
        viewMenu.addAction(_statusBarViewM)
        viewMenu.addAction(_audioToolbarViewM)

        # HELP DROPDOWN
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(_instructionsHelpM)
        helpMenu.addAction(_aboutHelpM)
        helpMenu.addAction(_wwwSiteHelpM)
        helpMenu.addSeparator()
        helpMenu.addAction(_systemCheckHelpM)

        # Create the audio toolbar.
        #audioToolBar = self.addToolBar('Audio')
        self.audioControls = AudioToolBar(self)
        self.addToolBar(self.audioControls)
        self.audioControls.setIconSize(QSize(15, 15))
        self.audioControls.setMovable(False)

        # Create timer widget.
        self.timeLcd = QLCDNumber()
        self.timeLcd.display("00:00")
        #audioControls.addTool(self.timeLcd)

        self.setCentralWidget(MainWidget())

        self._showStatusbar()
        self._setupWindow()

    def _showStatusbar(self):
        self.statusBar().showMessage('Ready')

    def _setupWindow(self):
        self.setGeometry(200, 200, 500, 200)
        self.setWindowTitle("Lights, Lights, and More Lights (LLaML)")

    def openProject(self):
        pass

    @staticmethod
    def openLLaMLWWW():
        QDesktopServices.openUrl("http://www.google.com")
        return None

    def openFileWindow(self):
        '''Opens the standard Qt file dialog window.

        Only permits *.lam file types (that's LAM not One am).'''
        self.openFileName = QFileDialog.getOpenFileName(self,
                                                        "Open LLaML Project",
                                                        "/",
                                                        "Project files (*.lam)")
        return None


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.windowSize = self.size()
        self.width = self.windowSize.width()
        self.height = self.windowSize.height()
        self.c = Communicate()
        self.generalLayout = QVBoxLayout()
        self.generalLayout.setContentsMargins(0, 0, 0, 0)
        # Nested waveform widget.
        self.waveform = DrawAudioWaveForm(self)
        self.zoneTest = ZoneWidget()
        self.generalLayout.addWidget(self.waveform)
        self.generalLayout.addWidget(self.zoneTest)

        # Stretch factor added because stretching only goes so far!  Setting the
        # factor to 5 allows it to be 5x the normal stretch space allowed.
        self.generalLayout.addStretch(1)

        self.setLayout(self.generalLayout)
        self.c.updateWidget[int, int].connect(self.waveform.setDimensions)

    def paintEvent(self, event):
        canvas = QPainter()
        canvas.begin(self)
        canvas.setBrush((QColor("#446699")))
        canvas.drawRect(event.rect())
        canvas.end()

    def resizeEvent(self, event):
        '''Respond to resize events and adjust geometry of children.

        Add new child widget signal emitters to this method.
        '''
        self.windowSize = self.size()
        self.height = self.windowSize.height()
        self.width = self.windowSize.width()
        v = self.generalLayout.update()
        self.c.updateWidget.emit(self.width, self.height)
        self.updateGeometry()
        self.waveform.updateGeometry()
        self.generalLayout.update()
        #_tempWidget = self.generalLayout.takeAt(0)
        #_tempWidget.widget().deleteLater()


# Splash screen setup.
font = QFont('Serif', 30)
#splash = QSplashScreen(_lightPM)
#splash.setFont(font)
#splash.showMessage("LLaML", Qt.AlignCenter, Qt.black)
#splash.show()

# Create main application window.
LLaMLWindow = ParentWindowMgr()

# Close the splash screen if the user has not already closed it out.
# Bring up the main application window after splash screen has closed.
#
# TODO:  Add window hint that user can close the splash screen.
#QTimer().singleShot(1000, splash.close)
QTimer().singleShot(1000, LLaMLWindow.showMaximized)

# Enter Qt application main loop
sys.exit(app.exec_())