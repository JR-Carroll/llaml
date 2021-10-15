#!/usr/bin/env python
#coding:utf-8
"""
  Author:   J. R. Carroll
  Purpose: aefaefae
  Created: 12/08/2013
"""
import logging
logging.debug("Attempting to load (wait for confirmation)")

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class ProgramManager(QDialog):
    def __init__(self, *args, **kwargs):
        super(ProgramManager, self).__init__()
        # Build/show the About Dialog.
        #self.execUI()
        self.exec_()
    #def


class ProgramList(object):
    def __init__(self):
        self.audioList = []
        self.totalLength = None
        self.songLengths = {}

    def allSongsList(self):
        '''Return a list of all the songs in the playlist.'''
        return self.audioList

    def playAll(self):
        '''Play all the songs in the list'''

        # Need to be able to check status of the playing song.
        for song in self.audioList:
            song.play()

    def addSongToList(self, song):
        '''Append a song to the list.'''
        if song != "MEDIA OBJECT":
            pass
        else:
            self.audioList.append(song)

    def moveSongInList(self, song):
        '''Move the original position of a song.'''
        pass

    def removeSongFromList(self, song):
        '''Remove song from the playlist'''
        pass

    def returnTotalLength(self):
        '''Return the total length of time for all songs in the playlist.'''
        return self.totalLength

    def returnUniSongLen(self, song):
        '''For a given song, return the calculated length (else, None)'''
        return self.songLengths.get(song, None)

    def returnAllSongLen(self):
        '''Returns a dictionary of all the songs and their lengths
        currently in the playlist'''
        return self.songLength

    def removeAllSongs(self):
        '''Remove all the songs from the playlist.

        Reinitialize the class.'''
        self.__init__()
        return True


logging.debug("Successfully loaded.")