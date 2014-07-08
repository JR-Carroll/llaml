#!/usr/bin/env python
#coding:utf-8
'''
  Author:   --<>
  Purpose:
  Created: 12/10/2013
'''

import logging
logging.debug("Attempting to load (wait for confirmation)")

from PySide.QtCore import *
from PySide.QtGui import *


class SystemTest(QDialog):
    def __init__(self):
        super(SystemTest, self).__init__()
        self.exec_()


logging.debug("Successfully loaded.")