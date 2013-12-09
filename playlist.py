#!/usr/bin/env python
#coding:utf-8
"""
  Author:   Justin Carroll
  Purpose: aefaefae
  Created: 12/08/2013
"""

from PySide.QtCore import *
from PySide.QtGui import *


class Playlist(QDialog):
    def __init__(self, *args, **kwargs):
        super(Playlist, self).__init__()
        # Build/show the About Dialog.
        #self.execUI()
        self.exec_()
    #def