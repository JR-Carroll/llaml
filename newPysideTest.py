''' ps_Multimedia_play_sound1.py
explore the PySide QtMultimedia module to play a specified sound
modified PyQT code from:
http://www.diotavelli.net/PyQtWiki/Playing%20a%20sound%20with%20QtMultimedia
PySide is the official LGPL-licensed version of PyQT
for free PySide Windows installers see:
http://developer.qt.nokia.com/wiki/PySide_Binaries_Windows
or
http://www.lfd.uci.edu/~gohlke/pythonlibs/
tested with Python33 and Pyside112  by vegaseat  29jul2013
'''
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtMultimedia import *
from math import pi, sin
import struct
class Window(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(300, 300, 400, 80)
        self.setWindowTitle("Play a specified sound (2 seconds)")
        format = QAudioFormat()
        format.setChannels(1)
        format.setFrequency(22050)
        format.setSampleSize(16)
        format.setCodec("audio/pcm")
        format.setByteOrder(QAudioFormat.LittleEndian)
        format.setSampleType(QAudioFormat.SignedInt)
        self.output = QAudioOutput(format, self)
        self.frequency = 100
        self.volume = 15000
        self.buffer = QBuffer()
        self.data = QByteArray()
        self.pitchSlider = QSlider(Qt.Horizontal)
        self.pitchSlider.setMaximum(2000)
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setMaximum(32767)
        self.volumeSlider.setPageStep(1024)
        self.volumeSlider.setValue(self.volume)
        self.playButton = QPushButton("&Play")
        self.pitch_label = QLabel()
        self.pitchSlider.valueChanged.connect(self.changeFrequency)
        self.volumeSlider.valueChanged.connect(self.changeVolume)
        self.playButton.clicked.connect(self.play)
        # layout managers ...
        formLayout = QFormLayout()
        formLayout.addRow("P&itch:", self.pitchSlider)
        formLayout.addRow("&Volume:", self.volumeSlider)
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.pitch_label)
        buttonLayout.addWidget(self.playButton)
        buttonLayout.addStretch()
        horizontalLayout = QHBoxLayout(self)
        horizontalLayout.addLayout(formLayout)
        horizontalLayout.addLayout(buttonLayout)
        self.changeFrequency()
    def changeFrequency(self, value=0):
        self.frequency = 100 + (value * 2)
        s = "pitch = {} Hz".format(self.frequency)
        self.pitch_label.setText(s)
    def play(self):
        if self.output.state() == QAudio.ActiveState:
            self.output.stop()
        if self.buffer.isOpen():
            self.buffer.close()
        self.createData()
        self.buffer.setData(self.data)
        self.buffer.open(QIODevice.ReadOnly)
        self.buffer.seek(0)
        self.output.start(self.buffer)
    def changeVolume(self, value):
        self.volume = value
    def createData(self):
        '''
        create 2 seconds of data with 22050 samples per second,
        each sample being 16 bits (2 bytes)
        '''
        self.data.clear()
        for k in range(2 * 22050):
            t = k / 22050.0
            value = int(self.volume * sin(2 * pi * self.frequency * t))
            self.data.append(struct.pack("<h", value))
# test the module
if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()