#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose:
  Created: 12/08/2013
"""

from PySide.phonon import *

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
        self.audio.setCurrentSource(self.audio)

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


class AudioList(object):
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