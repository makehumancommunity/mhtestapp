#!/usr/bin/python

import sys, re

from PyQt5.QtWidgets import *

from .helpwin import HelpWin

from .dummytest import DummyTest
from .noinittest import NoInitTest
from .inittest21 import InitTest21
from .inittest41 import InitTest41
from .redtest import RedTest
from .triangletest import TriangleTest
from .quadtest import QuadTest
from .colortritest import ColorTriangleTest

class MainWin(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(1000,600)
        self.move(100, 100)
        self.setWindowTitle('MH OpenGL Test Application')

        self.mainLayout = QHBoxLayout()

        self.testList = QListWidget()
        self.testList.addItem("01 (Dummy) -- Show an empty window to test the abstract test class")
        self.testList.addItem("02 (NoInit) -- Show an empty default QOpenGLWidget to test if it can be constructed")
        self.testList.addItem("03 (Init21) -- Show an empty v2.1 QOpenGLWidget with basic initialization performed")
        self.testList.addItem("04 (Init41) -- Show an empty v4.1 Core QOpenGLWidget with basic initialization performed")
        self.testList.addItem("05 (Red) -- Clear background to red, to test if we can work with the GL context")
        self.testList.addItem("06 (Triangle) -- Draw two triangles to test Qt's VBO and VAO wrappers")
        self.testList.addItem("07 (Quad) -- Draw a quad to test if the GL backend supports quads")
        self.testList.addItem("08 (ColorTri) -- Draw a multicolored triangle to test passing both vertex and color data to Qt")

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

        if test == "init21":
            self.inittest21 = InitTest21(self)

        if test == "init41":
            self.inittest41 = InitTest41(self)

        if test == "red":
            self.red = RedTest(self)

        if test == "triangle":
            self.triangle = TriangleTest(self)

        if test == "quad":
            self.quad = QuadTest(self)

        if test == "colortri":
            self.triangle = ColorTriangleTest(self)

    def _helpClick(self):
        helpWin = HelpWin(self)

    def _quitClick(self):
        sys.exit(0)
