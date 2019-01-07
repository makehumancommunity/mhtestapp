#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import QApplication

from mhtestapp import MainWin, log

if __name__ == '__main__':

    log.debug("About to start QApplication")
    app = QApplication(sys.argv)
    mainwin = MainWin()
    log.debug("About to exit QApplication")
    sys.exit(app.exec_())
