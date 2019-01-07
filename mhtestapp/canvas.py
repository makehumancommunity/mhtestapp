#/usr/bin/python3

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .util import log

class Canvas(QOpenGLWidget):

    def __init__(self, parent=None, requestedGLVersion=(2,1), logger=log):

        self.log = logger
        
        self.debugMembers = False

        self.requestedVersion = requestedGLVersion
        self.log.debug("About to try to initialize parent (abstract) gl widget")
        super(Canvas, self).__init__(parent)
        self.log.debug("Parent (abstract) gl widget should now have been created")
        self.destroyed.connect(self._on_destroyed)

    def _on_destroyed(self, *args):
        self.log.debug("Canvas is about to be destroyed")
        self.makeCurrent()
        self.closeGL()
        self.doneCurrent()

    # Override if necessary
    def minimumSizeHint(self):
        self.log.debug("minimumSizeHint() is not overridden")
        return QSize(400, 400)

    # Override if necessary
    def sizeHint(self):
        self.log.debug("sizeHint() is not overridden")
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
                self.log.debug("\n" + msg + "!\n")
            else:
                self.log.debug("\n" + msg + " at location \"" + location + "\"!\n")

            currentError = self.gl.glGetError()

        if self.glLog is None:
            return

        messages = self.glLog.loggedMessages()
        if not messages is None and len(messages) > 0:
            if location is None:
                self.log.debug("\n--- LOG MESSAGES ---")
            else:
                self.log.debug("\n--- " + location + " ---")
            for message in messages:
                self.log.debug(message.message())

            print("---\n")

    # Do not override this, instead override setupGL
    def initializeGL(self):

        self.log.debug("About to start general GL initialization")

        self.glLog = QOpenGLDebugLogger(self);
        if not self.glLog.initialize():
            self.log.debug("Unable to initialize GL logging")
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

        self.log.debug("\nGeneral GL information")
        self.log.debug("--------------------------------")
        self.log.debug("PROFILE",self.profile)
        self.log.debug("FUNCTIONS",self.gl)

        self.dumpGLLogMessages("initializeGL()")

        glVer = self.gl.glGetString(self.gl.GL_VERSION)
        glLangVer = self.gl.glGetString(self.gl.GL_SHADING_LANGUAGE_VERSION)
        glVendor = self.gl.glGetString(self.gl.GL_VENDOR)
        glRenderer = self.gl.glGetString(self.gl.GL_RENDERER)

        self.log.debug("GL_VERSION", glVer)
        self.log.debug("GL_SHADING_LANGUAGE_VERSION",glLangVer)
        self.log.debug("GL_VENDOR", glVendor)
        self.log.debug("GL_RENDERER", glRenderer)

        self.log.debug("--------------------------------\n")

        self.setupGL()

    # Override this
    def setupGL(self):
        self.log.debug("setupGL() is not overridden")

    # Override this
    def paintGL(self):
        self.log.debug("paintGL() is not overridden")

    # Override this
    def resizeGL(self, width, height):
        self.log.debug("resizeGL() is not overridden")

    # Override this
    def closeGL(self):
        self.log.debug("resizeGL() is not overridden")

