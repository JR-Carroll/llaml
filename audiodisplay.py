#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose:
  Created: 12/08/2013
"""

from PySide.QtCore import *
from PySide.QtGui import *

import matplotlib.pyplot as plot
import numpy
import wave
import StringIO


class Communicate(QObject):
    '''Setup hook to detect signals emitted from other QWidgets'''
    updateWidget = Signal((int, int))


class DrawAudioWaveForm(QScrollArea):
    '''Uses Pyside/Qt to draw audio waveforms.'''
    def __init__(self, parent, width=0, height=0):
        super(DrawAudioWaveForm, self).__init__()
        # Initialize width/height dimensions attribute.
        self.width, self.height = 50, 50

        # Handler to parent container/widget.
        self._parent = parent

        # set audio image
        self.audioImage = AudioWaveFormDisplay()._getDrawnWave()
        self.pixmap = self._setAudioImage(self.audioImage)

        # Establish top widget
        self.image = QLabel(parent)
        #self.image.setWidget

        #self.image.setPixmap(self.pixmap.scaled(width, (height/8)))

        # Create a layout to start throwing stuff into
        self.generalLayout = QVBoxLayout()
        self.generalLayout.setContentsMargins(0, 0, 0, 0)
        self.generalLayout.addWidget(self.image)
        self.setLayout(self.generalLayout)

    def setDimensions(self, width, height):
        '''Set widget dimensions.

        This is hooked into the Qt signaling system, so as the
        parent widget resizes, new signals are emitted onto this method/handler
        and the widget redrawn.
        '''
        self._rawWidth, self._rawHeight = width, height
        self.width, self.height = width, (height/8)
        self.scaledPixmap = self.pixmap.scaled(self.width, self.height)
        self.image.setPixmap(self.scaledPixmap)
        self.image.setScaledContents(True)
        self.image.resize(self.pixmap.size())

    def resizeEvent(self, *event):
        '''Respond to resize events and adjust the geometry of the widget.

         At the point of adjusting the geometry of the widget, this assumes that
         the waveform will occupy the top 1/8th of the available space, and has
         a width of one less than total (totalWidth - 1).

        '''
        self.setGeometry(0, 0, self.width, self.height)

    def _setAudioImage(self, data):
        return QPixmap.fromImage(QImage.fromData(data))

    #def paintEvent(self, event):
        #'''Draw the waveform.'''
        #canvas = QPainter()
        #canvas.begin(self)
        #canvas.setBrush(Qt.red)
        #canvas.drawRect(QRect(0, 0, self.width, self.height))
        #canvas.setPen(Qt.red)
        #canvas.end()

    #def poly(self, pts):
        #return QPolygonF(map(lambda p: QPointF(*p), pts))

    #def drawWaveAudio(self, canvas):
        #print("This was called...")


class AudioWaveFormDisplay(object):
    def __init__(self, *args, **kwargs):
        '''Constructor of the DrawWave class.

        Responsible for taking WAVE data and turning it into a PNG that is then
        passed to a buffer object.  This buffer object can then be read from for
        the purposes of redrawing wavedata (waveform).
        '''
        # mapped quality values
        self._quality = {'raw': 1,
                         'low': 800,
                         'med': 500,
                         'high': 200}

        # open the wave file.
        self.openedWave = wave.open('new.wav', 'r')
        self.signal = self.openedWave.readframes(-1)
        # convert binary data to an array of int's
        self.signal = numpy.fromstring(self.signal, 'Int16')
        # retrieve the framerate (from the wave header?)
        self.framerate = self.openedWave.getframerate()
        # create a stringio buffer object to store everything.
        self._bufferedIMG = StringIO.StringIO()

    #def otherStuff(self):
        #self.time = numpy.linspace(0, len(self.signal)/self.framerate,
                                   #num=len(self.signal))

    def _getDrawnWave(self, quality='low', width=20, height=5):
        '''Plots the waveform, derived from the audio data.

        Args:
            quality: render quality of wavedata either 'raw', 'low', 'med', or 'high'.
            width:  the width of the graph as measured in inches.
            height: the height of the graph as measured in inches.
        '''
        plot.figure(1, figsize=(width, height))
        # retrieves the wavedata based on the quality setting.  Default is 'high'.
        plot.plot(self.signal[::self._quality.get(quality, 'high')])
        plot.axis('off')
        plot.tight_layout()
        #plot.subplots_adjust(right=1, left=.1)
        # TODO:  add in dpi control rather than point-skipping
        plot.savefig(self._bufferedIMG, format='png', dpi=200, pad_inches=(-0.5), bbox_inches='tight')
        # After sending img data to buffer, seek to 0.
        self._bufferedIMG.seek(0)
        return self._bufferedIMG.getvalue()