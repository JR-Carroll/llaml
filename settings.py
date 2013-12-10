#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<J. R. Carroll>
  Purpose: Settings controller.
  Created: 12/09/2013

  Helps to control all the various settings associated with LLaML.
  Settings include:
      - Recently used files
      - User settings
      -
"""

import cPickle
import os

_applicationPath_ = os.curdir()
_application_ = "\LLaML.py"
_fullAppPath_ = _applicationPath_ + _application_

class ErrorApplicationPath(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return "While looking for a settings file, it was detected that the LLaML"
    "application does not exists in the expected path: {0}".format(self.msg)


def checkForSettings():
    '''Poor-mans check to make sure we are in the correct directory.'''
    if os.path.exists(_fullAppPath_) and os.path.isfile(_fullAppPath_):
        return True
    else:
        raise ErrorApplicationPath(_fullAppPath_)


def clearSettingsFile():
    pass


class ProjectSettingsFile(object):
    def __init__(self, *args, **kwargs):
        pass

    def createProjectFolder(self):
        pass

    def createProjectFile(self):
        pass

    def _setProjectPath(self):
        pass

    def _validateProjectFile(self):
        pass

    def addNewSong(self, song):
        pass

    def removeSong(self, song):
        pass

    def addNewLightMap(self):
        pass

    def removeLightMap(self):
        pass

    def loadProjectFile(self):
        pass

    def saveProjectFile(self):
        pass

    def saveAsProjectFile(self):
        pass



class ApplicationSettingsFile(object):
    def __init__(self, *args, **kwargs):
        pass

    def createAppSettingsFile(self):
        pass

    def _validateAppSettingsFile(self):
        pass

    def loadAppSettingsFile(self):
        pass

    def saveAppSettingsFile(self):
        pass

    def saveAsAppSettingsFile(self):
        pass
