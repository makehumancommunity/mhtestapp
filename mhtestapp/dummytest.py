#!/usr/bin/python

from PyQt5.QtWidgets import *
from .abstracttest import AbstractTest
from .util import MHLog

class DummyTest(AbstractTest):

    def __init__(self, parent):
        super().__init__(parent, "Dummy test")

        self.log = MHLog("dummy.txt")

        self.outputWidget = QWidget()

        self.loadImage("dummy.png")

        self.setActualOutputAndAddStretch(self.outputWidget)

        self.log.debug("About to show window")
        self.show()
