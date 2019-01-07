#!/usr/bin/python

from PyQt5.QtWidgets import *
from .abstracttest import AbstractTest
from .util import MHLog

class NoInitTest(AbstractTest):

    def __init__(self, parent):
        super().__init__(parent, "No init test")

        self.log = MHLog("noinit.txt")

        self.outputWidget = QOpenGLWidget()

        self.loadImage("noinit.png")

        self.setActualOutputAndAddStretch(self.outputWidget)

        self.log.debug("About to show window")
        self.show()