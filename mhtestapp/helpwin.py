#!/usr/bin/python

from PyQt5.QtWidgets import *

class HelpWin(QMainWindow):

    def __init__(self, parent):
        super().__init__(parent)

        text = "yada yada yada"

        self.textWidget = QTextEdit()
        self.textWidget.setText(text)
        self.textWidget.setLineWrapMode(QTextEdit.WidgetWidth)

        self.resize(800,600)
        self.move(200,200)

        self.setCentralWidget(self.textWidget)

        self.setWindowTitle("Help window")

        self.show()
