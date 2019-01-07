#!/usr/bin/python

from PyQt5.QtWidgets import *
from .abstracttest import AbstractTest

class DummyTest(AbstractTest):

    def __init__(self, parent):
        super().__init__(parent, "Dummy test")

        self.outputWidget = QWidget()

        self.loadImage("dummy.png")

        self.setActualOutputAndAddStretch(self.outputWidget)

        self.show()
