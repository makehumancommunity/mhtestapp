#!/usr/bin/python

import os

def rootDir():
    mypath = os.path.abspath( os.path.realpath(__file__) )
    parentpath = os.path.join(mypath, "..")
    return os.path.abspath( os.path.realpath(parentpath) )

def imagePath(fileName):

    imageDir = os.path.join(rootDir(), "images")
    imageFile = os.path.join(imageDir, fileName)

    return os.path.abspath(os.path.realpath(imageFile))
