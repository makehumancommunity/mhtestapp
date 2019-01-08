#!/usr/bin/python3

from .util import log
from .canvas import Canvas
from .abstracttest import AbstractTest

class _RedCanvas(Canvas):

    def __init__(self, parent):
        super(_RedCanvas,self).__init__(parent)

    def setupGL(self):
        log.debug("About to run local GL setup")
        # Tell GL that whenever we run glClear, this is the color that
        # should be used. We only need to do this once.
        self.gl.glClearColor(1.0, 0.0, 0.0, 1.0)
        self.dumpGLLogMessages("setupGL()")

    def paintGL(self):
        log.debug("About to repaint GL widget")
        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT | self.gl.GL_DEPTH_BUFFER_BIT)
        self.dumpGLLogMessages("paintGL()")

class RedTest(AbstractTest):

    def __init__(self, parent):
        super().__init__(parent, "Clear background to red")

        self.outputWidget = _RedCanvas(parent)

        self.loadImage("red.png")

        self.setActualOutputAndAddStretch(self.outputWidget)

        log.debug("About to show window")
        self.show()
