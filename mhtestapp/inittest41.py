#!/usr/bin/python

from PyQt5.QtWidgets import *
from .abstracttest import AbstractTest
from .util import log
from .canvas import Canvas

class InitTest41(AbstractTest):

    def __init__(self, parent):
        super().__init__(parent, "Init opengl 4.1")

        self.outputWidget = Canvas(parent, requestedGLVersion=(4,1))

        self.loadImage("init41.png")

        self.setActualOutputAndAddStretch(self.outputWidget)

        log.debug("About to show window")
        self.show()

