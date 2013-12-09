# !/usr/bin python
# -*- coding: utf-8 -*-

from PySide.QtGui import *
from PySide.QtCore import *
import playlist

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
        self.editPlaylistBT = QAction(self.editPlaylistIMG, "Edit the Playlist", self)
        self.editPlaylistBT.triggered.connect(playlist.Playlist)

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