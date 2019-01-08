#!/usr/bin/python

from PyQt5.QtWidgets import *
from .abstracttest import AbstractTest
from .util import log

class NoInitTest(AbstractTest):

    def __init__(self, parent):
        super().__init__(parent, "No init test")

        self.outputWidget = QOpenGLWidget()

        self.loadImage("noinit.png")

        self.setActualOutputAndAddStretch(self.outputWidget)

        log.debug("About to show window")

        self.show()