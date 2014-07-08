# !/usr/bin python
# -*- coding: utf-8 -*-

from PySide.QtGui import *
from PySide.QtCore import *
from programmgr import ProgramManager
from scheduler import ScheduleView
import logging

logging.debug("Attempting to load (wait for confirmation).")

class AudioToolBar(QToolBar):
    '''
    Need to pass in parent Widget and an existing ToolBarWidget.
    '''
    def __init__(self, parent, *args, **kwargs):
        super(AudioToolBar, self).__init__(parent)

        # Capture the parent to which this widget is bound.
        self._parent = parent

        # Kwargs passed in can toggle size and movability of this toolbar.
        # Allows user to override.
        _size = kwargs.get('iconSize', QSize(15, 15))
        _movable = kwargs.get('movable', True)

        # Set toolbar parameters.
        self.setIconSize(_size)
        self.setMovable(_movable)
        self.setWindowTitle("Audio Toolbar")
        # Group mappings (overrideable via kwargs) are:
        # 1 = File Menu Group
        # 2 = Meta Control Group
        # 3 = Audio Control group
        self._groups = kwargs.get('groups', [1, 2, 3])


        # List of images avaiable in Qt format.
        self.playIMG = QIcon(QPixmap('images/play_blue.png'))
        self.pauseIMG = QIcon(QPixmap('images/pause_blue.png'))
        self.stopIMG = QIcon(QPixmap('images/stop_blue.png'))
        self.previousSongIMG = QIcon(QPixmap('images/previous_blue.png'))
        self.nextSongIMG = QIcon(QPixmap('images/next_blue.png'))
        self.newProjectIMG = QIcon(QPixmap('images/new_project.png'))
        self.openProjectIMG = QIcon(QPixmap('images/open_doc.png'))
        self.saveProjectIMG = QIcon(QPixmap('images/disk_black.png'))
        self.waveformWidgetIMG = QIcon(QPixmap('images/waveform.png'))
        self.zoneManagerIMG = QIcon(QPixmap('images/table_row.png'))
        self.scheduleWidgetIMG = QIcon(QPixmap('images/calendar_select_none.png'))
        self.editPlaylistIMG = QIcon(QPixmap('images/playlist.png'))
        self.randomizeSongsIMG = QIcon(QPixmap('images/arrow_switch_bluegreen.png'))

        # Create the actual buttons with the images/actions associated.
        self.playSongBT = QAction(self.playIMG, "Play", self)
        self.pauseSongBT = QAction(self.pauseIMG, "Pause", self)
        self.stopSongBT = QAction(self.stopIMG, "Stop", self)
        self.nextSongBT = QAction(self.nextSongIMG, "Next Song", self)
        self.previousSongBT = QAction(self.previousSongIMG, "Previous Song", self)
        self.newProjectBT = QAction(self.newProjectIMG, "Create a New Project", self)
        self.openProjectBT = QAction(self.openProjectIMG, "Open an Existing Project", self)
        self.saveProjectBT = QAction(self.saveProjectIMG, "Save Project", self)
        self.randomizeSongsBT = QAction(self.randomizeSongsIMG, "Randomize Songs in Playlist", self)
        self.waveformWidgetBT = QAction(self.waveformWidgetIMG, "Toggle Waveform Display", self)
        self.zoneManagerBT = QAction(self.zoneManagerIMG, "Toggle Zone Manager", self)
        self.scheduleWidgetBT = QAction(self.scheduleWidgetIMG, "Toggle Scheduler Display", self)
        self.scheduleWidgetBT.triggered.connect(ScheduleView)
        self.editPlaylistBT = QAction(self.editPlaylistIMG, "Edit the Playlist", self)
        self.editPlaylistBT.triggered.connect(ProgramManager)

        self.combobox = QComboBox(self._parent)
        self.combobox.addItem("Im To Sexy For Shit.mp3")
        self.combobox.addItem("Hey Mickey Yo So Fine.wav")
        self.combobox.addItem("Somewhere over the rainbow")
        self.combobox.addItem("I like big BUTTS and I can not lie")
        self.combobox.addItem("HIV Song")
        self.combobox.addItem("Electric Slide")

        # Meta-button groupings.  Used for toggling on/off groups.
        self._fileGroup = [self.newProjectBT, self.openProjectBT, self.saveProjectBT]
        self._audioGroup = [self.editPlaylistBT, self.combobox, self.previousSongBT,
                            self.playSongBT, self.pauseSongBT, self.stopSongBT,
                            self.nextSongBT, self.randomizeSongsBT]
        self._metaControlGroup = [self.waveformWidgetBT, self.zoneManagerBT,
                                  self.scheduleWidgetBT]
        self._groupingManager = {1: self._fileGroup,
                                 2: self._metaControlGroup,
                                 3: self._audioGroup}

        self.addStandardButtons()

        # Configure default values
        self.volumeSlider = QSlider(Qt.Orientation.Horizontal)
        self.volumeSlider.setValue(50)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setMaximumWidth(101)

        self._volumeLabel = QLabel('Vol')
        self._sldMin = QLabel(str(self.volumeSlider.minimum()))
        self._sldMax = QLabel(str(self.volumeSlider.maximum()))
        self._sldValue = QLabel(str(self.volumeSlider.value()))

        #self.addWidget(self._sldMin)
        self.addWidget(self._volumeLabel)
        self.addWidget(self.volumeSlider)
        self.addWidget(self._sldValue)


    def addStandardButtons(self):
        '''
        Adds the standard set of buttons one would expect to see in an
        audio toolbar.
        '''

        for icons in self._groups:
            _tmp = self._groupingManager.get(icons)
            for button in _tmp:
                if button == self.combobox:
                    self.addWidget(self.combobox)
                else:
                    self.addAction(button)
            self.addSeparator()


class SliderWidget(QWidget):
    def __init__(self, parent):
        super(SliderWidget, self).__init__()
        self.volumeSlider = QSlider(Qt.Orientation.Horizontal)
        self._sldMin = QLabel(str(self.volumeSlider.minimum()))
        self._sldMax = QLabel(str(self.volumeSlider.maximum()))
        self._sldValue = QLabel(str(self.volumeSlider.value()))

        # Configure default values
        self.volumeSlider.setValue(50)
        self.volumeSlider.setMaximum(100)

        # Create a layout and add the slider elements to it.
        self._layout = QHBoxLayout(parent)
        self._layout.addWidget(self._sldMin)
        self._layout.addWidget(self.volumeSlider)
        self._layout.addWidget(self._sldMax)

logging.debug("Successfully loaded.")