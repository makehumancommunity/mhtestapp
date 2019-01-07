#!/usr/bin/python

from PyQt5.QtWidgets import *
from .abstracttest import AbstractTest
from .util import MHLog
from .canvas import Canvas

class InitTest41(AbstractTest):

    def __init__(self, parent):
        super().__init__(parent, "Init opengl 4.1")

        self.log = MHLog("init41.txt")

        self.outputWidget = Canvas(parent, logger=self.log, requestedGLVersion=(4,1))

        self.loadImage("init41.png")

        self.setActualOutputAndAddStretch(self.outputWidget)

        self.log.debug("About to show window")
        self.show()

