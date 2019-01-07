#/usr/bin/python3

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .util import log

class Canvas(QOpenGLWidget):

    def __init__(self, parent=None, requestedGLVersion=(2,1)):

        self.debugMembers = False

        self.requestedVersion = requestedGLVersion
        log.debug("About to try to initialize parent (abstract) gl widget")
        super(Canvas, self).__init__(parent)
        log.debug("Parent (abstract) gl widget should now have been created")
        self.destroyed.connect(self._on_destroyed)

    def _on_destroyed(self, *args):
        log.debug("Canvas is about to be destroyed")
        self.makeCurrent()
        self.closeGL()
        self.doneCurrent()

    # Override if necessary
    def minimumSizeHint(self):
        log.debug("minimumSizeHint() is not overridden")
        return QSize(400, 400)

    # Override if necessary
    def sizeHint(self):
        log.debug("sizeHint() is not overridden")
        return QSize(500, 500)

    def dumpGLLogMessages(self, location = None):

        currentError = self.gl.glGetError()
        while currentError != self.gl.GL_NO_ERROR:
            msg = "UNKNOWN GL ERROR"
            if currentError == self.gl.GL_INVALID_OPERATION:
                msg = "GL_INVALID_OPERATION"
            if currentError == self.gl.GL_INVALID_ENUM:
                msg = "GL_INVALID_ENUM"
            if currentError == self.gl.GL_INVALID_VALUE:
                msg = "GL_INVALID_VALUE"
            if currentError == self.gl.GL_OUT_OF_MEMORY:
                msg = "GL_OUT_OF_MEMORY"
            if currentError == self.gl.GL_INVALID_FRAMEBUFFER_OPERATION:
                msg = "GL_INVALID_FRAMEBUFFER_OPERATION"

            if location is None:
                log.debug("\n" + msg + "!\n")
            else:
                log.debug("\n" + msg + " at location \"" + location + "\"!\n")

            currentError = self.gl.glGetError()

        if self.glLog is None:
            return

        messages = self.glLog.loggedMessages()
        if not messages is None and len(messages) > 0:
            if location is None:
                log.debug("\n--- LOG MESSAGES ---")
            else:
                log.debug("\n--- " + location + " ---")
            for message in messages:
                log.debug(message.message())

            print("---\n")

    # Do not override this, instead override setupGL
    def initializeGL(self):

        self.glLog = QOpenGLDebugLogger(self);
        if not self.glLog.initialize():
            log.debug("Unable to initialize GL logging")
            self.glLog = None
        else:
            self.glLog.enableMessages(sources = QOpenGLDebugMessage.AnySource, types = QOpenGLDebugMessage.AnyType, severities = QOpenGLDebugMessage.AnySeverity)

        if self.debugMembers:

            print("\n--- MEMBERS IN CANVAS ---")
            for member in dir(self):
                print(member)
            print ("---\n")
    
            print("\n--- MEMBERS IN CONTEXT ---")
            ctx = self.context()
            for member in dir(ctx):
                print(member)
            print ("---\n")

        self.profile = QOpenGLVersionProfile()
        self.profile.setVersion(self.requestedVersion[0],self.requestedVersion[1])
        self.gl = self.context().versionFunctions(self.profile)
        self.gl.initializeOpenGLFunctions()

        # Enable GL capabilities we need
        self.gl.glEnable(self.gl.GL_DEBUG_OUTPUT_SYNCHRONOUS)
        self.gl.glEnable(self.gl.GL_DEPTH_TEST)
        self.gl.glEnable(self.gl.GL_VERTEX_PROGRAM_POINT_SIZE)

        log.debug("\nGeneral GL information")
        log.debug("----------------------")
        log.debug("PROFILE",self.profile)
        log.debug("FUNCTIONS",self.gl)

        self.dumpGLLogMessages("initializeGL()")

        glVer = self.gl.glGetString(self.gl.GL_VERSION)
        glLangVer = self.gl.glGetString(self.gl.GL_SHADING_LANGUAGE_VERSION)
        glVendor = self.gl.glGetString(self.gl.GL_VENDOR)
        glRenderer = self.gl.glGetString(self.gl.GL_RENDERER)

        log.debug("GL_VERSION", glVer)
        log.debug("GL_SHADING_LANGUAGE_VERSION",glLangVer)
        log.debug("GL_VENDOR", glVendor)
        log.debug("GL_RENDERER", glRenderer)

        log.debug("----------------------")

        self.setupGL()

    # Override this
    def setupGL(self):
        log.debug("setupGL() is not overridden")

    # Override this
    def paintGL(self):
        log.debug("paintGL() is not overridden")

    # Override this
    def resizeGL(self, width, height):
        log.debug("resizeGL() is not overridden")

    # Override this
    def closeGL(self):
        log.debug("resizeGL() is not overridden")

