#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose:
  Created: 12/08/2013
"""
import logging
logging.debug("Attempting to load (wait for confirmation)")

from PySide.QtCore import *
from PySide.QtGui import *

import matplotlib.pyplot as plot
import numpy
import wave
import StringIO


class Communicate(QObject):
    """Setup hook to detect signals emitted from other QWidgets"""
    updateWidget = Signal((int, int))


class DrawAudioWaveForm(QScrollArea):
    """Uses Pyside/Qt to draw audio waveforms."""
    def __init__(self, parent, width=0, height=0):
        super(DrawAudioWaveForm, self).__init__()
        # Initialize width/height dimensions attribute.
        self.width, self.height = 0, 0
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        # Handler to parent container/widget.
        self._parent = parent

        # set audio image
        self.audioImage = AudioWaveFormDisplay()._getDrawnWave()
        self.pixmap = self._setAudioImage(self.audioImage)

        # Establish top widget
        self.image = QLabel(parent)
        self.image.setGeometry(0, 0, 20, 20)
        # Create a layout to start throwing stuff into
        self.generalLayout = QVBoxLayout()
        self.generalLayout.setContentsMargins(0, 0, 0, 0)
        self.generalLayout.addWidget(self.image)
        self.setLayout(self.generalLayout)

    def setDimensions(self, width, height):
        """
        Set widget dimensions.

        This is hooked into the Qt signaling system, so as the
        parent widget resizes, new signals are emitted onto this method/handler
        and the widget redrawn.
        """
        self._rawWidth, self._rawHeight = width, height

        # adjust the height of the layout in addition to the height of the
        # waveform widget
        self.width, self.height = width, (height/20)
        self.image.setPixmap(self.pixmap)
        self.image.setScaledContents(True)

    def resizeEvent(self, *event):
        """
        Respond to resize events and adjust the geometry of the widget.

        At the point of adjusting the geometry of the widget, this assumes that
        the waveform will occupy the top 1/8th of the available space, and has
        a width of one less than total (totalWidth - 1).
        """
        # NOTE: all of the resizing events were removed because they werne't
        # needed once a factor was added to the mainWidget (LLaML.py) with a
        # addSpacing factor greater than 0.  If, after adding additional widgets,
        # this starts to muck up, consider replacing various scaling calls here.
        pass

    def _setAudioImage(self, data):
        return QPixmap.fromImage(QImage.fromData(data))

    #def paintEvent(self, event):
        #'''Draw the waveform.'''
        #print(event)
        #canvas = QPainter()
        #canvas.begin(self)
        #canvas.setBrush(Qt.red)
        #canvas.drawRect(event.rect())
        #canvas.drawRect(QRect(0, 0, self.width, self.height))
        #canvas.setPen(Qt.red)
        #canvas.end()

    #def poly(self, pts):
        #return QPolygonF(map(lambda p: QPointF(*p), pts))

    #def drawWaveAudio(self, canvas):
        #print("This was called...")


class AudioWaveFormDisplay(object):
    def __init__(self, *args, **kwargs):
        """
        Constructor of the DrawWave class.

        Responsible for taking WAVE data and turning it into a PNG that is then
        passed to a buffer object.  This buffer object can then be read from for
        the purposes of redrawing wavedata (waveform).
        """
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

    def _getDrawnWave(self, quality='low', width=50, height=20):
        """
        Plots the waveform, derived from the audio data.

        Args:
            quality: render quality of wavedata either 'raw', 'low', 'med', or 'high'.
            width:  the width of the graph as measured in inches.
            height: the height of the graph as measured in inches.
        """
        plot.figure(1, figsize=(width, height))
        # retrieves the wavedata based on the quality setting.  Default is 'high'.
        plot.plot(self.signal[::self._quality.get(quality, 'med')])
        plot.axis('off')
        plot.tight_layout()
        # TODO:  add in dpi control rather than point-skipping
        plot.savefig(self._bufferedIMG, format='png', dpi=30, pad_inches=(4.0), bbox_inches='tight')
        # After sending img data to buffer, seek to 0.
        self._bufferedIMG.seek(0)
        return self._bufferedIMG.getvalue()


logging.debug("Successfully loaded.")