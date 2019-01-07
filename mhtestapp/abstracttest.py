#!/usr/bin/python

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from .util import *

class AbstractTest(QMainWindow):

    def __init__(self, parent, windowTitle = "Test window"):
        super().__init__(parent)

        self.resize(1040,700)
        self.move(150,150)

        self.mainPanel = QWidget()
        self.mainLayout = QHBoxLayout()
        self.mainPanel.setLayout(self.mainLayout)

        self.leftPanel = QWidget()
        self.leftPanel.setMinimumWidth(500)
        self.leftPanel.setMaximumWidth(502)
        self.leftLayout = QVBoxLayout()
        self.leftPanel.setLayout(self.leftLayout)

        self.imageLabel = QLabel("Expected output:")
        self.leftLayout.addWidget(self.imageLabel)

        self.image = QLabel("-")
        self.image.setMinimumWidth(500)
        self.image.setMaximumWidth(500)
        self.image.setMinimumHeight(500)
        self.image.setMaximumHeight(500)
        self.leftLayout.addWidget(self.image)

        self.leftLayout.addStretch()

        self.rightPanel = QWidget()
        self.rightPanel.setMinimumWidth(500)
        self.rightPanel.setMaximumWidth(500)
        self.rightLayout = QVBoxLayout()
        self.rightPanel.setLayout(self.rightLayout)

        self.glLabel = QLabel("Actual output:")
        self.rightLayout.addWidget(self.glLabel)

        self.mainLayout.addWidget(self.leftPanel)
        self.mainLayout.addStretch()
        self.mainLayout.addWidget(self.rightPanel)

        self.setCentralWidget(self.mainPanel)

        self.setWindowTitle(windowTitle)

    def setActualOutputAndAddStretch(self, actualWidget):
        self.actualWidget = actualWidget

        self.actualWidget.setMinimumWidth(500)
        self.actualWidget.setMaximumWidth(500)
        self.actualWidget.setMinimumHeight(500)
        self.actualWidget.setMaximumHeight(500)
        self.rightLayout.addWidget(self.actualWidget)

        self.rightLayout.addStretch()

    def loadImage(self, imageName):
        path = imagePath("dummy.png")
        self.image.setPixmap(QPixmap(path))
