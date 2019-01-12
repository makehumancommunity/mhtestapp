
from .util import *
from .rotatablecanvas import RotatableCanvas
from .abstracttest import AbstractTest

from PyQt5.QtGui import *

import numpy as np
import math

class _RotationCanvas(RotatableCanvas):

    def __init__(self, parent):

        self.vertexShaderSource = testDataAsString("colortri","vertex.glsl")
        self.fragmentShaderSource = testDataAsString("colortri", "fragment.glsl")

        if self.vertexShaderSource is None:
            log.debug("Could not load the source for the vertex shader")
            raise Exception("Could not load the source for the vertex shader")

        if self.fragmentShaderSource is None:
            log.debug("Could not load the source for the fragment shader")
            raise Exception("Could not load the source for the fragment shader")

        super(_RotationCanvas, self).__init__(parent)

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

        # Vertex data
        self.vertices = np.array(
            [-0.5, -0.5, 0.0,
             0.5, 0.5, 0.0,
             0.5, -0.5, 0.0],
            dtype=np.dtype('f4'))

        # Color data
        self.colors = np.array(
            [1.0, 1.0, 0.0, # Yellow
             1.0, 0.0, 1.0, # Purple
             0.0, 1.0, 1.0],# Cyan
            dtype=np.dtype('f4'))

        # Get the number of elements in the array. We can reuse these for both vertices and
        # color data, as they are the same sizes
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
        self.triangleVAO1 = QOpenGLVertexArrayObject()
        self.triangleVAO1.create()
        self.triangleVAO1.bind()

        # Instead of asking GL directly to allocate an array buffer, we ask QT
        # to set up one for us. In GL language we are creating a "VBO" here.
        self.verticesBuffer1 = QOpenGLBuffer()
        self.verticesBuffer1.create()
        self.verticesBuffer1.bind()
        self.verticesBuffer1.setUsagePattern(QOpenGLBuffer.DynamicDraw)
        self.verticesBuffer1.allocate(self.vertices.tobytes(), self.verticesDataLength)

        # Here we specify that there is a program attribute that should get data that is sent
        # to it (by glDraw* operations), and in what form the data will arrive.
        self.program.enableAttributeArray(self.program.attributeLocation("somePosition"))
        self.program.setAttributeBuffer(self.program.attributeLocation("somePosition"), self.gl.GL_FLOAT, 0, 3, 0)

        self.verticesBuffer1.release()

        self.colorBuffer1 = QOpenGLBuffer()
        self.colorBuffer1.create()
        self.colorBuffer1.bind()
        self.colorBuffer1.setUsagePattern(QOpenGLBuffer.StaticDraw)
        self.colorBuffer1.allocate(self.colors.tobytes(), self.verticesDataLength)

        self.program.enableAttributeArray(self.program.attributeLocation("someColor"))
        self.program.setAttributeBuffer(self.program.attributeLocation("someColor"), self.gl.GL_FLOAT, 0, 3, 0)

        self.triangleVAO1.release()

        # Release the program until we need to actually draw something.
        self.program.release()

        self.gl.glClearColor(0.0, 0.0, 0.4, 1.0)

        self.dumpGLLogMessages("setupGL()")

    def paintGL(self):

        self.rotatedVertices = np.copy(self.vertices)

        # We have rotations (in degrees) stored in xRot, yRot and zRot:
        log.trace("Current rotation: " + "(" + str(self.xRot) + ", " + str(self.yRot) + ", " + str(self.zRot) + ")")

        # Rotation matrices are constructed according to "rotation matrix" in https://en.wikipedia.org/wiki/Rotation_matrix (3-dim case)
        # the use of a 4x4 matrix results from the fact that we have to track 3 axis and the origin, rotation will only apply to the 3x3
        # matrix, the value of 1 in the last row will avoid that the rotation modifies the origin
        # but when you move the origin from 0,0,0 you have to take this also into consideration
        # original MH code is in transformations.py, which creates the matrix for only one direction

        # lets calculate the values for multiplication before, we need radians instead of degrees
        rx =    math.radians(self.xRot)
        ry =    math.radians(self.yRot)
        rz =    math.radians(self.zRot)

        sinax = math.sin(rx)
        cosax = math.cos(rx)
        sinay = math.sin(ry)
        cosay = math.cos(ry)
        sinaz = math.sin(rz)
        cosaz = math.cos(rz)

        rx = np.array([
            [1, 0,      0,     0],
            [0, cosax,  sinax, 0],
            [0, -sinax, cosax, 0],
            [0, 0,      0,     1]
            ])

        ry = np.array([
            [cosay, 0, -sinay, 0],
            [0,     1, 0,      0],
            [sinay, 0, cosay,  0],
            [0,     0, 0,      1]
            ])

        rz = np.array([
            [cosaz, -sinaz, 0, 0],
            [sinaz, cosaz,  0, 0],
            [0,     0,      1, 0],
            [0,     0,      0, 1]
            ])

        #
        # rotatedCoordinates = rz * ry * rx * somePosition, where "somePosition" is a the INPUT :-)
        # lets precalculate the complete matrix, maybe not the fastest method ...
        # and don't write rx * ry * rz maybe use @ but I like the old fashioned way
        #
        m = np.matmul (np.matmul (rx, ry), rz)

        # is there a better way?!?! well normally vertices are not packed into a one-dimensional array I guess
        # mostly it is done in a nested array or using tuples (x,y,z combination) :)
        # and my knowlegde is nasty
        #
        for v in  range (0,self.numberOfVertices*3,3):
            nx = np.array ([self.rotatedVertices[v], self.rotatedVertices[v+1], self.rotatedVertices[v+2], 1])
            l = np.dot (nx, m)
            self.rotatedVertices[v:v+2] = l[0:2]

        self.verticesBuffer1.bind()
        self.verticesBuffer1.write(0,self.rotatedVertices.tobytes(), self.verticesDataLength)
        self.verticesBuffer1.release()

        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT | self.gl.GL_DEPTH_BUFFER_BIT)

        # We re-enable the program and use it for all draw operations (both VAOs use
        # this program)
        self.program.bind()

        # Activate the first VAO
        self.triangleVAO1.bind()

        # Draw the VAO. It will remember which VBO was specified for it.
        self.gl.glDrawArrays(self.gl.GL_TRIANGLES, 0, self.numberOfVertices)

        # Release the first VAO
        self.triangleVAO1.release()

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


class RotationTest(AbstractTest):

    def __init__(self, parent):
        super().__init__(parent, "Draw a triangle that can be rotated using the mouse")

        self.outputWidget = _RotationCanvas(parent)

        self.loadImage("rotatable.png")

        self.setActualOutputAndAddStretch(self.outputWidget)

        log.debug("About to show window")
        self.show()
