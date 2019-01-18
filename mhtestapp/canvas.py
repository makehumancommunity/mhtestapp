#/usr/bin/python3

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtOpenGL import QGLFormat

from .util import log

import sys

class Canvas(QOpenGLWidget):

    def __init__(self, parent=None, requestedGLVersion=(2,1)):

        self.log = log
        
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
        self.log.trace("minimumSizeHint() is not overridden")
        return QSize(400, 400)

    # Override if necessary
    def sizeHint(self):
        self.log.trace("sizeHint() is not overridden")
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
        if self.requestedVersion[0] > 2:
            self.profile.setProfile(QSurfaceFormat.CoreProfile)
        self.profile.setVersion(self.requestedVersion[0],self.requestedVersion[1])

        ctx = None

        log.debug("About to request the GL context from the widget")
        try:
            ctx = self.context()
        except:
            log.debug("The GL layer crashed when trying to read the context object from the widget")

        if ctx is None:
            log.debug("Giving up as we don't have a valid OpenGL context.")
            sys.exit(1)

        self.gl = None
        log.debug("About to request QOpenGLFunctions for OpenGL version " + str(self.requestedVersion))

        try:
            self.gl = ctx.versionFunctions(self.profile)
        except:
            log.debug("A stack trace was thrown when requesting a QOpenGLFunctions object from the GL context. The most likely cause is that we asked for a higher GL version than was available, but it is also possible the GL context as such is faulty.")

        if self.gl is None:
            log.debug("Giving up as we could not get access to a QOpenGLFunctions object for the selected version. We'll do a sys.exit here, in order to avoid cascading error messages, so it is expected that the application closes.")
            sys.exit(1)
            return

        self.gl.initializeOpenGLFunctions()

        # Enable GL capabilities we need
        self.gl.glEnable(self.gl.GL_DEBUG_OUTPUT_SYNCHRONOUS)
        self.gl.glEnable(self.gl.GL_DEPTH_TEST)
        self.gl.glEnable(self.gl.GL_VERTEX_PROGRAM_POINT_SIZE)

        self.log.debug("\nGeneral GL information")
        self.log.debug("--------------------------------")
        self.log.debug("Version profile object",self.profile)
        self.log.debug("GL API compatibility wrapper",str(self.gl) + "  <--  look at instance name to figure out what GL API we work with")

        self.dumpGLLogMessages("initializeGL()")

        glVer = self.gl.glGetString(self.gl.GL_VERSION)
        glLangVer = self.gl.glGetString(self.gl.GL_SHADING_LANGUAGE_VERSION)
        glVendor = self.gl.glGetString(self.gl.GL_VENDOR)
        glRenderer = self.gl.glGetString(self.gl.GL_RENDERER)

        self.log.debug("GL Version used by backend", glVer)
        self.log.debug("Max GLSL version available",glLangVer)
        self.log.debug("GL vendor", glVendor)
        self.log.debug("GL renderer (gfx card)", glRenderer)

        self.log.debug("--------------------------------\n")

        self.setupGL()

    # Override this
    def setupGL(self):
        self.log.trace("setupGL() is not overridden")

    # Override this
    def paintGL(self):
        self.log.trace("paintGL() is not overridden")

    # Override this
    def resizeGL(self, width, height):
        self.log.trace("resizeGL() is not overridden")

    # Override this
    def closeGL(self):
        self.log.trace("resizeGL() is not overridden")

