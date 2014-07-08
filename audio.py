#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose:
  Created: 12/08/2013
"""
import logging
logging.debug("Attempting to load (wait for confirmation)")

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


logging.debug("Successfully loaded.")

