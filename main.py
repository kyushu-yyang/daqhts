#!/usr/bin/env python2.7

import sys
sys.path.append("/Users/yangye/Documents/Experiment/HTS/DAQ/v.2.0/package")

import HDaqGuiHandle
from PyQt4 import QtGui, QtCore

def run():
    app = QtGui.QApplication(sys.argv)
    form = HDaqGuiHandle.HDaqGuiHandle()
    form.show()
    sys.exit(app.exec_())


if __name__=="__main__":
    run()
