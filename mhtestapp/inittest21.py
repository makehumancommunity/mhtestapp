#!/usr/bin/python

from PyQt5.QtWidgets import *
from .abstracttest import AbstractTest
from .util import log
from .canvas import Canvas

class InitTest21(AbstractTest):

    def __init__(self, parent):
        super().__init__(parent, "Init opengl 2.1")

        self.outputWidget = Canvas(parent)

        self.loadImage("init21.png")

        self.setActualOutputAndAddStretch(self.outputWidget)

        log.debug("About to show window")
        self.show()