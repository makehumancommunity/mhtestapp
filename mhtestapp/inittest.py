#!/usr/bin/python

from PyQt5.QtWidgets import *
from .abstracttest import AbstractTest
from .util import MHLog
from .canvas import Canvas

class InitTest(AbstractTest):

    def __init__(self, parent):
        super().__init__(parent, "No init test")

        self.log = MHLog("init.txt")

        self.outputWidget = Canvas(parent)

        self.loadImage("init.png")

        self.setActualOutputAndAddStretch(self.outputWidget)

        self.log.debug("About to show window")
        self.show()