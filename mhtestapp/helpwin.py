#!/usr/bin/python

from PyQt5.QtWidgets import *

class HelpWin(QMainWindow):

    def __init__(self, parent):
        super().__init__(parent)

        text = "These test are intended to test what graphics capabilities can be used on your platform. "
        text += "Each test will show a window with two parts:\n\n"
        text += "* On the left side is a screenshot of how it is supposed to look\n"
        text += "* On the right side is how it looks on your computer\n\n"
        text += "The first few test are supposed to be empty and not show anything in particular.\n\n"
        text += "If a test fails for you, you should find log files in a directory called 'mhtestapp' "
        text += "where you would normally find your makehuman logs. These files should then be attached "
        text += "to a post at the makehuman forums, alongside a screenshot if applicable."

        self.textWidget = QTextEdit()
        self.textWidget.setText(text)
        self.textWidget.setLineWrapMode(QTextEdit.WidgetWidth)

        self.resize(800,600)
        self.move(200,200)

        self.setCentralWidget(self.textWidget)

        self.setWindowTitle("Help window")

        self.show()
