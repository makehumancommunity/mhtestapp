#!/usr/bin/python

import sys, re

from PyQt5.QtWidgets import *

from .helpwin import HelpWin

from .dummytest import DummyTest
from .noinittest import NoInitTest

class MainWin(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(1000,600)
        self.move(100, 100)
        self.setWindowTitle('MH OpenGL Test Application')

        self.mainLayout = QHBoxLayout()

        self.testList = QListWidget()
        self.testList.addItem("01 (Dummy) -- Show an empty window to test the abstract test class")
        self.testList.addItem("02 (NoInit) -- Show a default QOpenGLWidget to test if it can be constructed")

        self.mainLayout.addWidget(self.testList)

        self.buttonPanel = QWidget()
        self.buttonPanel.setMaximumWidth(220)
        self.buttonPanel.setMinimumWidth(210)

        self.buttonLayout = QVBoxLayout()

        self.btnTest = QPushButton("Run selected test")
        self.btnTest.clicked.connect(self._runClick)
        self.buttonLayout.addWidget(self.btnTest)

        self.btnHelp = QPushButton("Show instructions")
        self.btnHelp.clicked.connect(self._helpClick)
        self.buttonLayout.addWidget(self.btnHelp)

        self.btnQuit = QPushButton("Exit application")
        self.btnQuit.clicked.connect(self._quitClick)
        self.buttonLayout.addWidget(self.btnQuit)

        self.buttonLayout.addStretch()

        self.buttonPanel.setLayout(self.buttonLayout)

        self.mainLayout.addWidget(self.buttonPanel)

        self.setLayout(self.mainLayout)
        self.show()

    def _runClick(self):
        item = str(self.testList.currentItem().text())
        match = re.search(r"\d\d\s+\(([^)]+).*", item)
        test = match.group(1).lower()

        if test == "dummy":
            self.dummy = DummyTest(self)

        if test == "noinit":
            self.noinit = NoInitTest(self)

    def _helpClick(self):
        helpWin = HelpWin(self)

    def _quitClick(self):
        sys.exit(0)
