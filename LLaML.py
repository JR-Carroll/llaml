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
import matplotlib.pyplot as plot
import wave
import numpy
import StringIO

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.phonon import *

__version__ = "0.1a"

class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__()

        self.pixmap = None

        # Attributes for the app name and app details to be displayed in the
        # About dialog.
        self.TITLE = """<b><h3>Lights, Lights, and More Lights v{0}</h3></b>""".format(__version__)
        self.ABOUT = """
        <p>LLaML (pronounced "YAML") is a program that was created
        to manage the synchronization of lights and music.
        </p>
        <p>
        <b>Creator</b>: J. R. Carroll, 2013
        <br /><b>Email</b>:  <a href="mailto:jrc.csus@gmail.com">jrc.csus@gmail.com</a>
        </p>
        """

        # Create QLabels from attribute strings.
        self.Qtitle = QLabel(self.TITLE)
        self._toggleWordWrap(self.Qtitle, wrap="yes")
        self.Qbody = QLabel(self.ABOUT)
        self._toggleWordWrap(self.Qbody, wrap="yes")

        # Set window defaults.
        self._setWindowTitle(title="About LLaML {0}".format(__version__))
        self._setAppImage(_lightPM)
        # Lock in the window size.
        #
        # TODO:  Test on smaller/larger resolutions to ensure this won't be a
        # problem.
        self.setFixedSize(300, 200)

        # Build/show the About Dialog.
        self.execUI()
        self.showWindow()

    def execUI(self):
        # Create OK button.
        OKBtn = self._addButton(string="OK")

        # Create Application image used in About Dialog and scale it.
        image = QLabel(self)
        image.setPixmap(self.pixmap.scaled(50, 50))

        # Create a top grid for the title and image.
        topGrid = QGridLayout()
        topGrid.addWidget(image, 1, 1, 1, 1)
        topGrid.addWidget(self.Qtitle, 1, 2, 1, 3)
        #topGrid.addSpacing(80)

        # Add bottom grid.
        bottomGrid = QGridLayout()
        bottomGrid.addWidget(self.Qbody, 0, 0)
        bottomGrid.addWidget(OKBtn, 1, 0)

        # Create grid for button placement.
        grid = QGridLayout(self)
        grid.addLayout(topGrid, 0, 0)
        grid.addLayout(bottomGrid, 1, 0)

    def _setAppImage(self, pixmap):
        '''
        Set the application image used in the About Dialog.

        Args:
            pixmap : a Qt pixmap -- typically a png.  See Qt docs.
        Return:
            None
        '''
        assert isinstance(pixmap, QPixmap)
        self.pixmap = pixmap
        return None

    def _setWindowTitle(self, **kwargs):
        # Explicit str conversion to ensure str type for title!
        title = str(kwargs.get('title', "About LLaML"))
        self.setWindowTitle(title)
        return None

    def _addButton(self, *args, **kwargs):
        '''
        Creates a new button for the dialog window.

        Buttons are assigned to the class itself by string label.

        For instance, a button with the string "OK" assigned to it, has an attribute
        of the class self.OK_button.  Whereas, "sToP" would be self.sToP_button.

        Default behavior with no arguments passed is to create a confrmation "OK"
        button.

        It is up to the implementor to add the button to a layout for display
        purposes.

        kwargs:
            string : the string that goes into the button.
            action : the Qt button behavior on button press.

        Return:
            Button : if successful, returns the button hook.
            False  : if unsuccessful, returns False.
        '''
        result = False
        try:
            # Explicit str conversion here to ensure resulting value is a string.
            # This allows the user to pass whatever silliness they want!
            btnString = str(kwargs.get("string", "OK"))
            btnName = btnString + "_button"
            btnAction = kwargs.get("action", self.accept)
            # Create the button and assigned click behavior.
            _button = QPushButton("{}".format(btnString))
            _button.clicked.connect(btnAction)
            setattr(self, btnName, _button)
            result = _button
        except:
            # PEH-GCA
            #
            # TODO:  Add in logging here and silenting pass else deal with more
            # gracefully.
            raise
        return result


    def _toggleWordWrap(self, label, wrap="no"):
        '''
        Wrapper for toggling word-wrapping within a QLabel object.

        Args:
            label : the QLabel object of interest.
            wrap  : either "yes"/"no" or 0/1; mappings are done internally for
                    consistenancy.
        Return:
            None
        '''
        assert isinstance(label, QLabel)
        wordWrapMap = {'yes' : 1,
                       'no': 2}
        _wrap = wrap

        if wrap.lower() == 'yes':
            _wrap = 1
        elif wrap.lower() == 'no':
            _wrap = 0

        label.setWordWrap(_wrap)
        return None

    def showWindow(self):
        '''
        Wrapped for showing the About Dialog (formerly self.exec_).

        Args:
            None
        Return:
            True | False
        '''
        result = False
        try:
            self.exec_()
            result = True
        except:
            # PEH-GCA
            #
            # TODO:  Add in better exception handling here.
            raise
        return result


class AudioToolBar():
    """
    Need to pass in parent Widget and an existing ToolBarWidget.
    """
    def __init__(self, parent, toolbarObj):
        # Make the images avaiable in Qt format.
        self.playIMG = QIcon(QPixmap('images/play_blue.png'))
        self.pauseIMG = QIcon(QPixmap('images/pause_blue.png'))
        self.stopIMG = QIcon(QPixmap('images/stop_blue.png'))

        # Create the menu object and create icons
        self.playMenuBT = QAction(self.playIMG, "Play", parent)
        self.pauseMenuBT = QAction(self.pauseIMG, "Pause", parent)
        self.stopMenuBT = QAction(self.stopIMG, "Stop", parent)
        _play = toolbarObj.addAction(self.playMenuBT)
        toolbarObj.addAction(self.pauseMenuBT)
        toolbarObj.addAction(self.stopMenuBT)


class ParentWindowMgr(QMainWindow):
    global _lightICON
    global _lightPM

    def __init__(self):
        super(ParentWindowMgr, self).__init__()

        # File Menu
        _newProjectFileM = QAction(QIcon(''), '&New Project', self)
        _newProjectFileM.setShortcut('Ctrl+N')
        _newProjectFileM.setStatusTip("Create a new project")

        _openFileM = QAction(QIcon(''), '&Open Project', self)
        _openFileM.setShortcut('Ctrl+O')
        _openFileM.setStatusTip("Open an existing project file")

        _closeProjectFileM = QAction(QIcon(''), '&Close', self)
        _closeProjectFileM.setShortcut('Ctrl+W')
        _closeProjectFileM.setStatusTip("Close the current project")

        # TODO:  Plumb in recent menu correctly!
        _recentProjectFileM = QAction(QIcon(''), 'Recent Projects', self)
        _recentProjectFileM.setStatusTip("Select from a list of previously opened projects")

        _exitFileM = QAction(QIcon(''), 'E&xit', self)
        _exitFileM.setShortcut('Alt+f4')
        _exitFileM.setStatusTip("Exit LLaML")
        _exitFileM.triggered.connect(sys.exit)

        # Edit Menu
        _preferencesEditM = QAction(QIcon(''), 'Preferences', self)
        _preferencesEditM.setStatusTip("Edit LLaML preferences and default behaviors")

        # Audio Menu
        _loadAudioM = QAction(QIcon(''), '&Load Audio', self)
        _loadAudioM.setShortcut('Ctrl+L')
        _loadAudioM.setStatusTip("Load audio file into project")

        _playAudioM = QAction(QIcon(''), '&Play', self)
        _playAudioM.setShortcut('Ctrl+P')
        _playAudioM.setStatusTip("Play audio file from last position")

        _pauseAudioM = QAction(QIcon(''), 'Pa&use', self)
        _pauseAudioM.setShortcut('Ctrl+U')
        _pauseAudioM.setStatusTip("Pause the currently playing audio file")

        _stopAudioM = QAction(QIcon(''), '&Stop', self)
        _stopAudioM.setShortcut('Ctrl+S')
        _stopAudioM.setStatusTip("Stop the currently playing audio file, and rewind")

        _audioInfoAudioM = QAction(QIcon(''), 'Audio &Info', self)
        _audioInfoAudioM.setStatusTip("See any currently available meta information")

        _seePlaylistAudioM = QAction(QIcon(''), 'Pla&ylist', self)
        _seePlaylistAudioM.setStatusTip("See the current list of queued songs")

        _addSongAudioM = QAction(QIcon(''), '&Add Song', self)
        _addSongAudioM.setStatusTip("Select a song from the file-system")

        _removeSongAudioM = QAction(QIcon(''), '&Remove Song', self)
        _removeSongAudioM.setStatusTip("Remove the current song from the playlist")

        _settingsAudioM = QAction(QIcon(''), 'Se&ttings', self)
        _settingsAudioM.setStatusTip("Modify audio settings")

        # View menu
        _waveformWidgetViewM = QAction(QIcon(''), 'View &Waveform', self)
        _waveformWidgetViewM.setStatusTip("Toggle viewing of waveform widget (can help performance)")

        _zoneWidgetViewM = QAction(QIcon(''), 'View &Zone Manager', self)
        _zoneWidgetViewM.setStatusTip("See the Zone Widget")

        _statusBarViewM = QAction(QIcon(''), 'Toggle &Statusbar', self)
        _statusBarViewM.setStatusTip("Toggle the statusbar view")

        # Help menu
        _aboutHelpM = QAction(QIcon(''), '&About', self)
        _aboutHelpM.setStatusTip("About LLaLM")
        _aboutHelpM.triggered.connect(AboutDialog)

        _systemCheckHelpM = QAction(QIcon(''), 'System Check', self)
        _systemCheckHelpM.setStatusTip("Perform a system check to ensure everything is working correclty")

        _wwwSiteHelpM = QAction(QIcon(''), 'LLaML Website', self)
        _wwwSiteHelpM.setStatusTip("Go to LLaML website")

        menubar = self.menuBar()

        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(_newProjectFileM)
        fileMenu.addAction(_openFileM)
        fileMenu.addAction(_closeProjectFileM)
        fileMenu.addAction(_recentProjectFileM)
        fileMenu.addSeparator()
        fileMenu.addAction(_exitFileM)

        editMenu = menubar.addMenu("&Edit")
        editMenu.addAction(_preferencesEditM)

        audioMenu = menubar.addMenu("&Audio")
        audioMenu.addAction(_loadAudioM)
        audioMenu.addSeparator()
        audioMenu.addAction(_playAudioM)
        audioMenu.addAction(_pauseAudioM)
        audioMenu.addAction(_stopAudioM)
        audioMenu.addSeparator()
        audioMenu.addAction(_audioInfoAudioM)
        audioMenu.addSeparator()
        audioMenu.addAction(_seePlaylistAudioM)
        audioMenu.addSeparator()
        audioMenu.addAction(_addSongAudioM)
        audioMenu.addAction(_removeSongAudioM)
        audioMenu.addSeparator()
        audioMenu.addAction(_settingsAudioM)

        viewMenu = menubar.addMenu("&View")
        viewMenu.addAction(_waveformWidgetViewM)
        viewMenu.addAction(_zoneWidgetViewM)
        viewMenu.addAction(_statusBarViewM)

        helpMenu = menubar.addMenu("&Help")
        helpMenu.addAction(_aboutHelpM)
        helpMenu.addAction(_wwwSiteHelpM)
        helpMenu.addSeparator()
        helpMenu.addAction(_systemCheckHelpM)

        audioToolBar = self.addToolBar('Audio')
        audioControls = AudioToolBar(self, audioToolBar)
        audioToolBar.setIconSize(QSize(15, 15))
        audioToolBar.setMovable(False)

        # Create timer widget...
        self.timeLcd = QLCDNumber()
        self.timeLcd.display("00:00")
        audioToolBar.addWidget(self.timeLcd)

        self.setCentralWidget(MainWidget())

        #self.scrollWaveArea = QScrollArea()
        #self.scrollWaveArea.setWidget(self.centralWidget())
        #self.scrollWaveArea.show()

        #self.waveform = DrawAudioWaveForm(self.centralWidget())

        self._statusbar()
        self._setupWindow()

    def _statusbar(self):
        self.statusBar().showMessage('Ready')

    def _setupWindow(self):
        self.setGeometry(200, 200, 500, 200)
        self.setWindowTitle("Lights, Lights, and More Lights (LLaML)")

    def openProject(self):
        pass



class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.windowSize = self.size()
        self.width = self.windowSize.width()
        self.height = self.windowSize.height()
        self.c = Communicate()
        # Nested waveform widget.
        self.waveform = DrawAudioWaveForm(self)
        self.c.updateWidget[int, int].connect(self.waveform.setDimensions)

    def paintEvent(self, event):
        canvas = QPainter()
        canvas.begin(self)
        canvas.setBrush((QColor("#446699")))
        canvas.drawRect(event.rect())
        canvas.setPen(Qt.red)
        canvas.end()

    def resizeEvent(self, event):
        '''Respond to resize events and adjust geometry of children.

        Add new child widget signal emitters to this method.
        '''
        self.windowSize = self.size()
        self.height = self.windowSize.height()
        self.width = self.windowSize.width()
        self.c.updateWidget.emit(self.width, self.height)


class Communicate(QObject):
    '''Setup hook to detect signals emitted from other QWidgets'''
    updateWidget = Signal((int, int))


class DrawAudioWaveForm(QWidget):
    '''Uses Pyside/Qt to draw audio waveforms.'''
    def __init__(self, parent):
        super(DrawAudioWaveForm, self).__init__(parent)
        # Initialize width/height dimensions attribute.
        self.width, self.height = None, None
        # Handler to parent container/widget.
        self._parent = parent
        # Sample points to draw for polyline
        self.pts = [[0,1], [5, 30], [200, 300]]
        self.AudioImage = DrawWave()
        self._rawData = self.AudioImage._bufferedIMG.getvalue()
        self._rawIMG = QImage.fromData(self._rawData)
        self.pixmap = QPixmap.fromImage(self._rawIMG)
        self.image = QLabel(self)
        self.image.setPixmap(self.pixmap)

    def setDimensions(self, width, height):
        '''Set widget dimensions.

        This is hooked into the Qt signaling system, so as the
        parent widget resizes, new signals are emitted onto this method/handler
        and the widget redrawn.
        '''
        self.width, self.height = width, height
        self.resizeEvent(None)

    def resizeEvent(self, event):
        '''Respond to resize events and adjust the geometry of the widget.'''
        self.scroll(20, 0)
        # At the point of adjusting the geometry of the widget, this assumes that
        # the waveform will occupy the top 1/8th of the available space, and has
        # a width of one less than total (totalWidth - 1).
        self.setGeometry(0, 0, (self.width-1), (self.height/8))

    def paintEvent(self, event):
        '''Draw the waveform.'''
        canvas = QPainter()
        canvas.begin(self)
        canvas.setBrush(Qt.green)
        canvas.drawRect(event.rect())
        canvas.setPen(Qt.red)
        #self.drawWaveAudio(canvas)
        canvas.end()

    #def poly(self, pts):
        #return QPolygonF(map(lambda p: QPointF(*p), pts))

    #def drawWaveAudio(self, canvas):
        #print("This was called...")


class DrawWave(object):
    def __init__(self):
        self.openedWave = wave.open('new.wav', 'r')
        self.signal = self.openedWave.readframes(-1)
        self.signal = numpy.fromstring(self.signal, 'Int16')
        self.framerate = self.openedWave.getframerate()
        self._bufferedIMG = StringIO.StringIO()
        self.otherStuff()
        # Create a buffer for the PNG image data from matplotlib.

    def otherStuff(self):
        self.Time = numpy.linspace(0, len(self.signal)/self.framerate, num=len(self.signal))
        self.drawWave()

    def drawWave(self):
        plot.figure(1, figsize=(13, 2))
        plot.plot(self.signal[::480])
        plot.grid()
        plot.axis('off')
        plot.savefig(self._bufferedIMG, format='png')
        # After sending img data to buffer, seek to 0.
        self._bufferedIMG.seek(0)

# Create a Qt application
app = QApplication(sys.argv)
app.setWindowIcon(QIcon('greenLightSM.png'))
app.setApplicationName("LLaML")

#ex = DrawAudioWaveForm(app)

# Loading images once to pass around to the various classes
# that need it.
_lightICON = QIcon('greenLight.png')
_lightPM = QPixmap('greenLight.png')

# Splash screen setup.
font = QFont('Serif', 30)
splash = QSplashScreen(_lightPM)
splash.setFont(font)
splash.showMessage("LLaML", Qt.AlignCenter, Qt.black)
splash.show()

# Create main application window.
LLaMLWindow = ParentWindowMgr()


class LoadAudioWAV(object):
    '''Set up the audio - platform independent.'''
    def __init__(self):
        # Set the nominal priority with the system.
        mediaDevice = Phonon.Category(Phonon.MusicCategory)
        # Set up the audio object/handler
        self.audio = Phonon.MediaObject()
        self.output = Phonon.AudioOutput()
        path = Phonon.createPath(self.audio, self.output)
        # The audio file.
        self.audio = None
        # If not playing (aka stopped) then False
        self.playing = False

    def confirmValidWAV(self):
        '''Confirm that the audio file is a valid WAVE format.'''

    def setAudioFile(self):
        self.audio = Phonon.MediaSource('new.wav')
        self.audio.setCurrentSource(audio)

    def playWAV(self):
        # Start playing audio -- this is a test.
        self.audio.play()

    def stopWAV(self):
        '''Stop playing the WAVE file and return True.

        If no WAVE file is playing, this returns False'''
        stopped = False
        if self.playing:
            self.audio.stop()
            stopped = True
            # Reset playing state
            self.playing = False
        else:
            # Do nothing... once stopped it resets to position 0 anyways.
            pass
        return stopped

    def pauseWAV(self):
        '''Pause the currently playing WAVE file and return True.

        If no WAVE file is playing, this returns False.'''
        paused = False
        if self.playing:
            self.audio.pause()
            paused = True
            # Reset playing state
            self.playing = False
        else:
            self.audio.pause()

        return paused


# Close the splash screen if the user has not already closed it out.
# Bring up the main application window after splash screen has closed.
#
# TODO:  Add window hint that user can close the splash screen.
QTimer().singleShot(1000, splash.close)
QTimer().singleShot(1000, LLaMLWindow.showMaximized)

# Enter Qt application main loop
sys.exit(app.exec_())