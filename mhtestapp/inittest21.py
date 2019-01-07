#!/usr/bin/python

from PyQt5.QtWidgets import *
from .abstracttest import AbstractTest
from .util import MHLog
from .canvas import Canvas

class InitTest21(AbstractTest):

    def __init__(self, parent):
        super().__init__(parent, "Init opengl 2.1")

        self.log = MHLog("init21.txt")

        self.outputWidget = Canvas(parent, logger=self.log)

        self.loadImage("init21.png")

        self.setActualOutputAndAddStretch(self.outputWidget)

        self.log.debug("About to show window")
        self.show()