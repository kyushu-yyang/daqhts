# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../gui/monitor.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

import matplotlib
from   matplotlib.backends import qt_compat
from   matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from   matplotlib.figure   import Figure

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Monitor(object):
    def setupUi(self, Monitor):
        Monitor.setObjectName(_fromUtf8("Monitor"))
        Monitor.resize(1060, 680)
        self.setrunning(Monitor)
        self.setbutton(Monitor)
        self.setramprate(Monitor)

        # matplotlib canvas
        self._figVI = Figure(facecolor="whitesmoke")
        self.plotVI = FigureCanvas(self._figVI)
        self.plotVI.setGeometry( QtCore.QRect(380, 20, 640, 400) )
        self.plotVI.setObjectName(_fromUtf8("VIshow"))
        self.plotVI.setParent(Monitor)

        self._fig_tI = Figure(facecolor="whitesmoke")
        self.plot_tI = FigureCanvas(self._fig_tI)
        self.plot_tI.setGeometry( QtCore.QRect(40, 450, 300, 200) )
        self.plot_tI.setObjectName(_fromUtf8("tIshow"))
        self.plot_tI.setParent(Monitor)

        self._fig_tVp = Figure(facecolor="whitesmoke")
        self.plot_tVp = FigureCanvas(self._fig_tVp)
        self.plot_tVp.setGeometry( QtCore.QRect(380, 450, 300, 200) )
        self.plot_tVp.setObjectName(_fromUtf8("tVpshow"))
        self.plot_tVp.setParent(Monitor)

        self._fig_tVh = Figure(facecolor="whitesmoke")
        self.plot_tVh = FigureCanvas(self._fig_tVh)
        self.plot_tVh.setGeometry( QtCore.QRect(720, 450, 300, 200) )
        self.plot_tVh.setObjectName(_fromUtf8("tVhshow"))
        self.plot_tVh.setParent(Monitor)

        self.retranslateUi(Monitor)
        #QtCore.QObject.connect(self.exit_but, QtCore.SIGNAL(_fromUtf8("clicked()")), Monitor.close)
        QtCore.QMetaObject.connectSlotsByName(Monitor)

    def retranslateUi(self, Monitor):
        Monitor.setWindowTitle(_translate("Monitor", "Form", None))
        self.supply_dis.setText(_translate("Dialog", "Current Supply: OFF", None))
        self.I_on_but.setText(_translate("Dialog", "ON", None))
        self.I_up_but.setText(_translate("Dialog", "SET RAMP", None))
        self.I_off_but.setText(_translate("Dialog", "OFF", None))
        self.exit_but.setText(_translate("Dialog", "EXIT", None))
        self.meas_but.setText(_translate("Dialog", "MEASURE", None))
        self.ramp_lab.setText(_translate("Dialog", "Ramp Rate [A/sec]:", None))

    def setrunning(self, mainwin):
        self.supply_dis = QtGui.QLabel(mainwin)
        self.supply_dis.setGeometry(QtCore.QRect(30, 30, 310, 80))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Helvetica"))
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.supply_dis.setFont(font)
        self.supply_dis.setAlignment(QtCore.Qt.AlignCenter)
        self.supply_dis.setObjectName(_fromUtf8("supply_dis"))

    def setbutton(self, mainwin):
        self.I_on_but = QtGui.QPushButton(mainwin)
        self.I_on_but.setGeometry(QtCore.QRect(90, 200, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setUnderline(True)
        self.I_on_but.setFont(font)
        self.I_on_but.setAutoFillBackground(False)
        self.I_on_but.setObjectName(_fromUtf8("I_on_but"))
        self.I_up_but = QtGui.QPushButton(mainwin)
        self.I_up_but.setGeometry(QtCore.QRect(90, 250, 200, 40))
        self.I_up_but.setFont(font)
        self.I_up_but.setObjectName(_fromUtf8("I_up_but"))
        self.I_off_but = QtGui.QPushButton(mainwin)
        self.I_off_but.setGeometry(QtCore.QRect(90, 300, 200, 40))
        self.I_off_but.setFont(font)
        self.I_off_but.setObjectName(_fromUtf8("I_off_but"))
        self.meas_but = QtGui.QPushButton(mainwin)
        self.meas_but.setGeometry(QtCore.QRect(90, 360, 200, 40))
        self.meas_but.setFont(font)
        self.meas_but.setObjectName(_fromUtf8("I_off_but"))
        self.exit_but = QtGui.QPushButton(mainwin)
        self.exit_but.setGeometry(QtCore.QRect(90, 410, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(False)
        self.exit_but.setFont(font)
        self.exit_but.setToolTip(_fromUtf8(""))
        self.exit_but.setObjectName(_fromUtf8("exit_but"))

    def setramprate(self, win):
        self.ramp_box = QtGui.QDoubleSpinBox(win)
        self.ramp_box.setEnabled(True)
        self.ramp_box.setGeometry(QtCore.QRect(180, 130, 120, 30))
        self.ramp_box.setProperty("value", 0.1)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.ramp_box.setFont(font)
        self.ramp_box.setAlignment(QtCore.Qt.AlignCenter)
        self.ramp_box.setDecimals(2)
        self.ramp_box.setMaximum(40.0)
        self.ramp_box.setObjectName(_fromUtf8("ramp_box"))
        self.ramp_lab = QtGui.QLabel(win)
        self.ramp_lab.setGeometry(QtCore.QRect(30, 130, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.ramp_lab.setFont(font)
        self.ramp_lab.setObjectName(_fromUtf8("ramp_lab"))


