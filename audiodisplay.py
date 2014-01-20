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
        self.resizeEvent()

    def resizeEvent(self, *event):
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
        self.Time = numpy.linspace(0,
                                   len(self.signal)/self.framerate,
                                   num=len(self.signal))
        self.drawWave()

    def drawWave(self):
        plot.figure(1, figsize=(19, 1.5))
        plot.plot(self.signal[::480])
        plot.grid()
        plot.axis('off')
        plot.savefig(self._bufferedIMG, format='png')
        # After sending img data to buffer, seek to 0.
        self._bufferedIMG.seek(0)