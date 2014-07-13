#!/usr/bin/env python
#coding:utf-8
'''
  Author:   --<>
  Purpose:
  Created: 12/08/2013
'''

# Import Standard Library modules
import logging

logging.debug("Attempting to load (wait for confirmation)")

# Import PySide specific modules
from PySide.QtGui import *
from PySide.QtCore import *
from PySide import *

# import standard libraries
import sys

__llaml_version__ = "0.1a"

class AboutDialog(QDialog):
    '''
    Render the About Dialog on user request.

    Requires an image to run correctly -- images are stored in resources and MUST
    be loaded from the main application after QApplication has been called.
    '''
    def __init__(self, image=None, *args, **kwargs):
        super(AboutDialog, self).__init__()

        self.pixmap = None

        # Attributes for the app name and app details to be displayed in the
        # About dialog.
        self.TITLE = """<b><h3>Lights, Lights, and More Lights v{0}</h3></b>""".format(__llaml_version__)
        self.ABOUT = """
        <p>LLaML (pronounced "YAML") is a program that was created
        to manage the synchronization of lights and music.
        </p>
        <p>
        <b>Creator</b>: J. R. Carroll, 2014
        <br /><b>Email</b>:  <a href="mailto:jrc.csus@gmail.com">jrc.csus@gmail.com</a>
        </p>
        """

        # Create QLabels from attribute strings.
        self.Qtitle = QLabel(self.TITLE)
        self._toggleWordWrap(self.Qtitle, wrap="yes")
        self.Qbody = QLabel(self.ABOUT)
        self._toggleWordWrap(self.Qbody, wrap="yes")

        # Set window defaults.
        self._setWindowTitle(title="About LLaML {0}".format(__llaml_version__))
        self._setAppImage(image)

        # Set up developer information from About dialog.
        # There is nothing secrete here, just random bits of
        # developer information that is useful for debugging.
        #
        # Encourage others to add to this section anything they
        # do not want the users to see, but should be easy enough
        # for developers to jump into (should be all static information).
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        _hiddenInfo = QAction(self)
        _hiddenInfo.setText("Developer Information")
        _hiddenInfo.triggered.connect(ShowDeveloperWindow)
        self.addAction(_hiddenInfo)

        # Lock in the window size.
        #
        # TODO:  Test on smaller/larger resolutions to ensure this won't be a
        # problem.
        self.setFixedSize(300, 200)

        # Build/show the About Dialog.
        self.execUI()
        self.showWindow()

    def execUI(self):
        # Create OK button.
        okBT = self._addButton(string="OK")

        # Create Application image used in About Dialog and scale it.
        image = QLabel(self)
        image.setPixmap(self.pixmap.scaled(50, 50))

        # Create a top grid for the title and image.
        topGrid = QGridLayout()
        topGrid.addWidget(image, 1, 1, 1, 1)
        topGrid.addWidget(self.Qtitle, 1, 2, 1, 3)
        #topGrid.addSpacing(80)

        # Add bottom grid.
        bottomGrid = QGridLayout()
        bottomGrid.addWidget(self.Qbody, 0, 0)
        bottomGrid.addWidget(okBT, 1, 0)

        # Create grid for button placement.
        grid = QGridLayout(self)
        grid.addLayout(topGrid, 0, 0)
        grid.addLayout(bottomGrid, 1, 0)

    def _setAppImage(self, pixmap):
        '''
        Set the application image used in the About Dialog.

        Args:
            pixmap : a Qt pixmap -- typically a png.  See Qt docs.
        Return:
            None
        '''
        assert isinstance(pixmap, QPixmap)
        self.pixmap = pixmap
        return None

    def _setWindowTitle(self, **kwargs):
        # Explicit str conversion to ensure str type for title!
        title = str(kwargs.get('title', "About LLaML"))
        self.setWindowTitle(title)
        return None

    def _addButton(self, *args, **kwargs):
        '''
        Creates a new button for the dialog window.

        Buttons are assigned to the class itself by string label.

        For instance, a button with the string "OK" assigned to it, has an attribute
        of the class self.OK_button.  Whereas, "sToP" would be self.sToP_button.

        Default behavior with no arguments passed is to create a confrmation "OK"
        button.

        It is up to the implementor to add the button to a layout for display
        purposes.

        kwargs:
            string : the string that goes into the button.
            action : the Qt button behavior on button press.

        Return:
            Button : if successful, returns the button hook.
            False  : if unsuccessful, returns False.
        '''
        result = False
        try:
            # Explicit str conversion here to ensure resulting value is a string.
            # This allows the user to pass whatever silliness they want!
            btnString = str(kwargs.get("string", "OK"))
            btnName = btnString + "_button"
            btnAction = kwargs.get("action", self.accept)
            # Create the button and assigned click behavior.
            _button = QPushButton("{}".format(btnString))
            _button.clicked.connect(btnAction)
            setattr(self, btnName, _button)
            result = _button
        except:
            # PEH-GCA
            #
            # TODO:  Add in logging here and silenting pass else deal with more
            # gracefully.
            raise
        return result


    def _toggleWordWrap(self, label, wrap="no"):
        '''
        Wrapper for toggling word-wrapping within a QLabel object.

        Args:
            label : the QLabel object of interest.
            wrap  : either "yes"/"no" or 0/1; mappings are done internally for
                    consistenancy.
        Return:
            None
        '''
        assert isinstance(label, QLabel)
        wordWrapMap = {'yes' : 1,
                       'no': 2}
        _wrap = wrap

        if wrap.lower() == 'yes':
            _wrap = 1
        elif wrap.lower() == 'no':
            _wrap = 0

        label.setWordWrap(_wrap)
        return None

    def showWindow(self):
        '''
        Wrapped for showing the About Dialog (formerly self.exec_).

        Args:
            None
        Return:
            True | False
        '''
        result = False
        try:
            self.exec_()
            result = True
        except:
            # PEH-GCA
            #
            # TODO:  Add in better exception handling here.
            raise
        return result


class ShowDeveloperWindow(QDialog):
    def __init__(self, *args, **kwargs):
        super(ShowDeveloperWindow, self).__init__()

        # log that someone has gone into the developer mode.
        logging.debug("Opened developer information window.")

        # Layout to which all elements are added.
        self._hbox = QHBoxLayout()

        # Side menu to which all elements are added.
        self.sideMenu = QListWidget()
        self.sideMenu.setMaximumWidth(150)
        self.sideMenu.currentItemChanged.connect(self._requestInfo)
        # Setup what is in the side menu.
        self.sideMenu.addItem("PySide Version")
        self.sideMenu.addItem("QT Version")
        self.sideMenu.addItem("Python Version")
        self.sideMenu.addItem("TBD")
        self.sideMenu.addItem("TBD")

        # Setup TextEdit on the side of the "sideMenu".
        self.informationBox = QTextEdit()

        # Add all the elements to the hbox.
        self._hbox.addWidget(self.sideMenu)
        self._hbox.addWidget(self.informationBox)

        self.setLayout(self._hbox)
        self.exec_()

    def _requestInfo(self, *args, **kwargs):
        _request = str(args[0].text())
        _currentRequest = str(args[0].text()).replace(" ", "_").lower()

        try:
            request = getattr(self, _currentRequest)
            if not request:
                print "test"
            else:
                returnMessage = request()
        except Exception as e:
            returnMessage = str(RequestDoesNotExist(req=_currentRequest))

        self.informationBox.setText(returnMessage)
        return returnMessage

    @staticmethod
    def python_version():
        """Retrieve the latest Python version."""
        _expecting = "Python 2.7.*"
        _pythonVer = sys.version
        return "<b>Expecting</b>: {0} <br/>" \
               "<b>Installed:</b> {1}".format(_expecting, _pythonVer)

    @staticmethod
    def pyside_version():
        """Retrieve the latest PySide version."""
        from PySide import __version__
        _expecting = "PySide ver 1.1.1"
        _pysideVer = __version__
        return "<b>Expecting</b>: {0} <br/>" \
               "<b>Installed:</b> {1}".format(_expecting, _pysideVer)

    @staticmethod
    def qt_version():
        from PySide.QtCore import __version__
        _expecting = "Qt ver. 4.8.2"
        _qtVersion = __version__
        return "<b>Expecting</b>: {0} <br/>" \
               "<b>Installed:</b> {1}".format(_expecting, _qtVersion)


class RequestDoesNotExist(Exception):
    def __init__(self, *args, **kwargs):
        super(RequestDoesNotExist, self).__init__()
        self.message = "Your request is not valid/implemented"
        logging.warn("User requested \"{0}\" from the dev. dialog, but the "\
                     "info requested isn't working.".format(kwargs.get('req',
                                                                       'Unknown')))
    def __str__(self):
        return self.message

logging.debug("Successfully loaded.")