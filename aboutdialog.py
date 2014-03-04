#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose:
  Created: 12/08/2013
"""

from PySide.QtGui import *
from PySide.QtCore import *

__version__ = "0.1a"

class AboutDialog(QDialog):
    '''Draw the About Dialog on user request.

    Requires an image to run correctly -- images are stored in resources and MUST
    be loaded from the main application after QApplication has been called.
    '''
    def __init__(self, image=None, *args, **kwargs):
        super(AboutDialog, self).__init__()

        self.pixmap = None

        # Attributes for the app name and app details to be displayed in the
        # About dialog.
        self.TITLE = """<b><h3>Lights, Lights, and More Lights v{0}</h3></b>""".format(__version__)
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
        self._setWindowTitle(title="About LLaML {0}".format(__version__))
        self._setAppImage(image)

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