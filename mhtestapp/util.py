#!/usr/bin/python

import os, sys

from .xdg_parser import XDG_PATHS

__home_path = None

def pathToUnicode(path):
    """
    Unicode representation of the filename.
    Bytes is decoded with the codeset used by the filesystem of the operating
    system.
    Unicode representations of paths are fit for use in GUI.
    """

    if isinstance(path, bytes):
        # Approach for bytes string type
        try:
            return str(path, 'utf-8')
        except UnicodeDecodeError:
            pass
        try:
            return str(path, sys.getfilesystemencoding())
        except UnicodeDecodeError:
            pass
        try:
            return str(path, sys.getdefaultencoding())
        except UnicodeDecodeError:
            pass
        try:
            import locale
            return str(path, locale.getpreferredencoding())
        except UnicodeDecodeError:
            return path
    else:
        return path

def formatPath(path):
    if path is None:
        return None
    path = pathToUnicode(os.path.normpath(path).replace("\\", "/"))
    path = os.path.abspath(os.path.realpath(path))
    return path

def rootDir():
    mypath = os.path.abspath( os.path.realpath(__file__) )
    parentpath = os.path.join(mypath, "..")
    return formatPath(parentpath)

def imagePath(fileName):

    imageDir = os.path.join(rootDir(), "images")
    imageFile = os.path.join(imageDir, fileName)

    return formatPath(imageFile)

def getHomePath():
    """
    Find the user home path.
    Note: If you are looking for MakeHuman data, you probably want getPath()!
    """
    # Cache the home path
    global __home_path

    # The environment variable MH_HOME_LOCATION will supersede any other settings for the home folder.
    alt_home_path = os.environ.get("MH_HOME_LOCATION", '')
    if os.path.isdir(alt_home_path):
        __home_path = formatPath(alt_home_path)

    if __home_path is not None:
        return __home_path

    # Windows
    if sys.platform.startswith('win'):
        import winreg
        keyname = r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders'
        #name = 'Personal'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, keyname) as k:
            value, type_ = winreg.QueryValueEx(k, 'Personal')
            if type_ == winreg.REG_EXPAND_SZ:
                __home_path = formatPath(winreg.ExpandEnvironmentStrings(value))
                return __home_path
            elif type_ == winreg.REG_SZ:
                __home_path = formatPath(value)
                return __home_path
            else:
                raise RuntimeError("Couldn't determine user folder")

    # Linux
    elif sys.platform.startswith('linux'):
        doc_folder = XDG_PATHS.get('DOCUMENTS', '')
        if os.path.isdir(doc_folder):
            __home_path = doc_folder
        else:
            __home_path = pathToUnicode(os.path.expanduser('~'))

    # Darwin
    else:
        __home_path = os.path.expanduser('~')

    return __home_path

def mhDir():
    homePath = getHomePath()
    mhdir = os.path.join(homePath, "makehuman", "v1py3")
    mhdir = formatPath(mhdir)
    os.makedirs(mhdir, exist_ok=True)
    return mhdir

def logDir():
    logDir = formatPath(os.path.join(mhDir(),"mhtestapp"))
    os.makedirs(logDir, exist_ok=True)
    return logDir

class MHLog:

    def __init__(self, fileName = "mainlog.txt"):

        self.logFile = formatPath( os.path.join(logDir(), fileName) )

        with open(self.logFile, "w") as f:
            f.write("Starting new log\n")
            f.write("----------------\n")

    def debug(self, message, obj = None):

        if not obj is None:
            message = message.ljust(30,'.')
            message = message + " : " + str(obj)

        print(message)
        with open(self.logFile, "a") as f:
            f.write(message)
            f.write("\n")

log = None

if log is None:
    log = MHLog()

