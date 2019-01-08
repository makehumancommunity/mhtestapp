
from .util import *
from .canvas import Canvas
from .abstracttest import AbstractTest

from PyQt5.QtGui import *

import numpy as np

class _QuadCanvas(Canvas):

    def __init__(self, parent):

        self.vertexShaderSource = testDataAsString("quad","vertex.glsl")
        self.fragmentShaderSource = testDataAsString("quad", "fragment.glsl")

        if self.vertexShaderSource is None:
            log.debug("Could not load the source for the vertex shader")
            raise Exception("Could not load the source for the vertex shader")

        if self.fragmentShaderSource is None:
            log.debug("Could not load the source for the fragment shader")
            raise Exception("Could not load the source for the fragment shader")

        super(_QuadCanvas, self).__init__(parent)

    def setupGL(self):

        self.program = QOpenGLShaderProgram(self.context())
        log.debug("PROGRAM", self.program)

        # addShaderFromSourceCode() only returns a bool telling whether everything went well

        if self.program.addShaderFromSourceCode(QOpenGLShader.Vertex, self.vertexShaderSource):
            log.debug("Managed to load and parse the vertex shader")

        if self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, self.fragmentShaderSource):
            log.debug("Managed to load and parse the fragment shader")

        # Compile and bind the shader program to the current context
        self.program.link()
        self.program.bind()

        # Use numpy to specify vertices for a quad
        self.vertices = np.array([
            -0.5, -0.5, 0.0,
            0.5, -0.5, 0.0,
            0.5, 0.5, 0.0,
            -0.5, 0.5, 0.0
        ], dtype=np.dtype('f4'))

        # Get the number of elements in the array
        self.verticesLength = self.vertices.size
        log.debug("Array length", self.verticesLength)

        # Size in bytes for each element
        self.verticesItemSize = self.vertices.itemsize
        log.debug("Array cell size", self.verticesItemSize)

        # Total size in bytes for entire array
        self.verticesDataLength = self.verticesLength * self.verticesItemSize
        log.debug("Array size in bytes", self.verticesDataLength)

        # Number of vertices in the array
        self.numberOfVertices = int(self.verticesLength / 3)
        log.debug("Number of vertices", self.numberOfVertices)

        # Start specifying the first Vertex Array Object (VAO). The upside of this approach
        # is that we can keep all settings pertaining to the Vertex Buffer Object (VBO) specified
        # here and not have to specify them again at draw time. This will make it a lot easier
        # to keep multiple conceptual graphical objects around.
        #
        # The VAO will remember all that was specified for its VBOs between the VAOs bind() and
        # its close()
        self.quadVAO = QOpenGLVertexArrayObject()
        self.quadVAO.create()
        self.quadVAO.bind()

        # Instead of asking GL directly to allocate an array buffer, we ask QT
        # to set up one for us. In GL language we are creating a "VBO" here.
        self.verticesBuffer = QOpenGLBuffer()
        self.verticesBuffer.create()
        self.verticesBuffer.bind()
        self.verticesBuffer.setUsagePattern(QOpenGLBuffer.StaticDraw)
        self.verticesBuffer.allocate(self.vertices.tobytes(), self.verticesDataLength)

        # Here we specify that there is a program attribute that should get data that is sent
        # to it (by glDraw* operations), and in what form the data will arrive.
        self.program.enableAttributeArray(self.program.attributeLocation("somePosition"))
        self.program.setAttributeBuffer(self.program.attributeLocation("somePosition"), self.gl.GL_FLOAT, 0, 3, 0)

        # Once we have set up everything related to the VBO, we can release that and the
        # related VAO.
        self.verticesBuffer.release()
        self.quadVAO.release()

        # Release the program until we need to actually draw something.
        self.program.release()

        self.gl.glClearColor(0.0, 0.0, 0.4, 1.0)

        self.dumpGLLogMessages("setupGL()")

    def paintGL(self):
        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT | self.gl.GL_DEPTH_BUFFER_BIT)

        # We re-enable the program and use it for all draw operations (both VAOs use
        # this program)
        self.program.bind()

        # Activate the first VAO
        self.quadVAO.bind()

        # Draw the VAO. It will remember which VBO was specified for it.
        self.gl.glDrawArrays(self.gl.GL_QUADS, 0, self.numberOfVertices)

        # Release the first VAO
        self.quadVAO.release()

        # Release the program
        self.program.release()

        self.dumpGLLogMessages("paintGL()")

    def closeGL(self):
        # We need to explicitly destroy VAOs, VBOs and programs. Otherwise we'll get a
        # segfault or another similar crash.
        self.triangleVAO1.destroy()
        self.verticesBuffer1.destroy()
        self.triangleVAO2.destroy()
        self.verticesBuffer2.destroy()
        del self.program


class QuadTest(AbstractTest):

    def __init__(self, parent):
        super().__init__(parent, "Draw a quad")

        self.outputWidget = _QuadCanvas(parent)

        self.loadImage("quad.png")

        self.setActualOutputAndAddStretch(self.outputWidget)

        log.debug("About to show window")
        self.show()
