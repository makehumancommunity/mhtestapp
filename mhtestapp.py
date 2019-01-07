#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import QApplication

from mhtestapp import MainWin

if __name__ == '__main__':

    app = QApplication(sys.argv)
    mainwin = MainWin()
    sys.exit(app.exec_())
