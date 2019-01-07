#!/usr/bin/python3

from mhtestapp import log

log.debug("About to start testing imports")

log.debug("About to import PyQt5")
try:
    from PyQt5 import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
except:
    log.debug("Could not import all PyQt5 related files. Things will crash later on.")

log.debug("About to import numpy")
try:
    import numpy
except:
    log.debug("Could not import all numpy related files. Things will crash later on.")

log.debug("Finished testing imports")

log.debug("\nQt and NumPy Version information")
log.debug("--------------------------------")
log.debug("Effective QT version", QT_VERSION_STR)
log.debug("Effective numpy version", numpy.version.full_version)
log.debug("--------------------------------\n")

log.debug("Entering main script")

import sys
from PyQt5.QtWidgets import *

from mhtestapp import MainWin

if __name__ == '__main__':

    log.debug("About to start QApplication")
    app = QApplication(sys.argv)
    mainwin = MainWin()
    log.debug("About to exit QApplication")
    sys.exit(app.exec_())
