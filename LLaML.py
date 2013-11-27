#!/usr/bin/python

"""
Color palette in use:

#112233 -> dark blue
#446699
#6688bb
#5588dd
#bbddff -> light blue

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
    global _lightICON
    global _lightPM

    def __init__(self):
        super(AboutDialog, self).__init__()
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
        self.execUI()

    def execUI(self):
        # Create OK button.
        closeBT = QPushButton("OK")
        closeBT.clicked.connect(self.accept)
        title = QLabel(self.TITLE)
        title.setWordWrap(1)
        body = QLabel(self.ABOUT)
        body.setWordWrap(1)
        pixmap = _lightPM
        pixmap = pixmap.scaled(50, 50)
        image = QLabel(self)
        image.setPixmap(pixmap)

        # Create a top grid for the title and image...
        topGrid = QBoxLayout(QBoxLayout.Direction(0))
        #topGrid.addStretch()
        topGrid.addWidget(image, 0, 0)
        topGrid.addWidget(title, 0, 1)
        topGrid.addStretch()

        # Add bottom grid.
        bottomGrid = QGridLayout()
        bottomGrid.addWidget(body, 0, 0)
        bottomGrid.addWidget(closeBT, 1, 0)

        # Create grid for button placement.
        grid = QGridLayout(self)
        grid.addLayout(topGrid, 0, 0)
        grid.addLayout(bottomGrid, 1, 0)

        self.setWindowTitle("About LLaML")
        self.setFixedWidth(300)
        self.exec_()


class AudioMenu():
    """
    Need to pass in parent Widget and an existing ToolBarWidget.
    """
    def __init__(self, parent, toolbarObj):
        # Make available the images used.
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

        # Setting menu items.
        _openFileM = QAction(QIcon(' '), '&Open Project', self)
        _openFileM.setShortcut('Ctrl+O')
        _openFileM.setStatusTip("Open an existing project file")

        _exitFileM = QAction(QIcon(' '), 'E&xit', self)
        _exitFileM.setShortcut('Ctrl+X')
        _exitFileM.setStatusTip("Exit LLaML")
        _exitFileM.triggered.connect(sys.exit)

        _loadAudioM = QAction(QIcon(''), 'Load &Audio', self)
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

        _settingsAudioM = QAction(QIcon(''), "Settings", self)
        _settingsAudioM.setStatusTip("Modify audio settings")

        _aboutHelpM = QAction(QIcon(''), '&About', self)
        _aboutHelpM.setStatusTip("About LLaLM")
        _aboutHelpM.triggered.connect(AboutDialog)

        _wwwSiteHelpM = QAction(QIcon(''), 'LLaML Website', self)
        _wwwSiteHelpM.setStatusTip("Go to LLaML website")

        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(_openFileM)
        fileMenu.addSeparator()
        fileMenu.addAction(_exitFileM)

        editMenu = menubar.addMenu("&Edit")

        audioMenu = menubar.addMenu("&Audio")
        audioMenu.addAction(_loadAudioM)
        audioMenu.addSeparator()
        audioMenu.addAction(_playAudioM)
        audioMenu.addAction(_pauseAudioM)
        audioMenu.addAction(_stopAudioM)
        audioMenu.addSeparator()
        audioMenu.addAction(_settingsAudioM)

        helpMenu = menubar.addMenu("&Help")
        helpMenu.addAction(_aboutHelpM)
        helpMenu.addSeparator()
        helpMenu.addAction(_wwwSiteHelpM)

        audioToolBar = self.addToolBar('Audio')
        audioControls = AudioMenu(self, audioToolBar)
        audioToolBar.setIconSize(QSize(15, 15))
        audioToolBar.setMovable(False)

        # Create timer widget...
        self.timeLcd = QLCDNumber()
        self.timeLcd.display("00:00")
        audioToolBar.addWidget(self.timeLcd)

        self.setCentralWidget(MainWindowWidget())

        #self.scrollWaveArea = QScrollArea()
        #self.scrollWaveArea.setWidget(self.centralWidget())
        #self.scrollWaveArea.show()

        #self.waveform = DrawAudioWaveForm(self.centralWidget())

        self.statusbar()
        self.setupWindow()

    def statusbar(self):
        self.statusBar().showMessage('Ready')

    def setupWindow(self):
        self.setGeometry(200, 200, 500, 200)
        self.setWindowTitle("Lights, Lights, and More Lights (LLaML)")


class MainWindowWidget(QWidget):
    def __init__(self):
        super(MainWindowWidget, self).__init__()
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
        print("Window Size ->", self.windowSize)
        self.c.updateWidget.emit(self.width, self.height)


class Communicate(QObject):
    '''Setup hook to detect signals emitted from other QWidgets'''
    updateWidget = Signal((int, int))
    print("updateWidget hit with this passed in->", updateWidget)

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
        print("yeah... this drawWave method hit alright!")
        plot.figure(1, figsize=(13, 2))
        plot.plot(self.signal[::480])
        plot.grid()
        plot.axis('off')
        plot.savefig(self._bufferedIMG, format='png')
        # After sending img data to buffer, seek to 0.
        self._bufferedIMG.seek(0)

DrawWave()

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

# Setting up media devices.
mediaDevice = Phonon.Category(Phonon.MusicCategory)
audio = Phonon.MediaSource('new.wav')
newAudio = Phonon.MediaObject()
newAudio.setCurrentSource(audio)
output = Phonon.AudioOutput()
path = Phonon.createPath(newAudio, output)

# Start playing audio -- this is a test.
newAudio.play()

# Close the splash screen if the user has not already closed it out.
# Bring up the main application window after splash screen has closed.
#
# TODO:  Remove window hint that user can close the splash screen.
QTimer().singleShot(2000, splash.close)
QTimer().singleShot(2000, LLaMLWindow.showMaximized)

# Enter Qt application main loop
sys.exit(app.exec_())