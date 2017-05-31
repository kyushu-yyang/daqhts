## derived class from HDaqGuiBase

import time
import datetime
import numpy as np
import sys
sys.path.append("/Users/yangye/Documents/Experiment/HTS/DAQ/v.2.0")

from PyQt4.Qwt5 import *
import HtsDaqGuiBase
import parameter

from PyQt4 import QtGui, QtCore

##
class HtsDaqSimulator(QtCore.QThread):

    ## signal
    data_sig = QtCore.pyqtSignal(float, float)

    ## constructor
    def __init__(self, parent=None):
        super(HtsDaqSimulator, self).__init__(parent)
        ## self.stopped is the derived parameter from QThread
        self.stopped = False
        self.mutex = QtCore.QMutex()

    ## stop the simulator
    def stop(self):
        with QtCore.QMutexLocker(self.mutex):
            self.stopped = True

    ## run the simulator
    def run(self):
        while True:
            if self.stopped:
                break
            v1 = np.random.random()
            v2 = np.random.random()
            time.sleep(1.)
            self.data_sig.emit(v1, v2)
        self.stop()
        self.finished.emit()


##
class HtsMeasSimulator(QtCore.QThread):

    ## signal: current, protection voltage, hts voltage
    data_sig = QtCore.pyqtSignal(float, float, float)

    ## constructor
    def __init__(self, parent=None):
        super(HtsMeasSimulator, self).__init__(parent)
        ## self.stopped is the derived parameter from QThread
        self.stopped = False
        self.mutex = QtCore.QMutex()

    ## stop the simulator
    def stop(self):
        with QtCore.QMutexLocker(self.mutex):
            self.stopped = True

    ## run the simulator
    def run(self):
        while True:
            if self.stopped:
                break
            v1 = np.random.random()
            v2 = np.random.random()
            v3 = np.random.random()
            time.sleep(1.)
            self.data_sig.emit(v1, v2, v3)
        self.stop()
        self.finished.emit()



##
class HDaqGuiHandle(QtGui.QMainWindow, HtsDaqGuiBase.Ui_Monitor):

    ## constructor
    def __init__(self, parent=None):
        super(HDaqGuiHandle, self).__init__(parent)
        self.setupUi(self)
        self._data = {"time":np.array([]), "hts":np.array([]), "prot":np.array([]), "curr":np.array([])}
        nowtime = datetime.datetime.now()
        self._start = nowtime
        self.setup()
        #self._file = open( parameter.path+"/meas%s.dat" %(nowtime.strftime("%Y%m%d_%H%M%S")), "w" )

    ## setup
    def setup(self):
        self.I_on_but.clicked.connect(self.slp_run)
        self.I_off_but.clicked.connect(self.slp_stop)
        ## setup the current class
        self._sim = HtsDaqSimulator()
        self._sim.data_sig.connect(self.slp_simulator)
        self._sim.finished.connect(self.slp_finish)
        ## setup the measurement class
        self._meas = HtsMeasSimulator()
        self._meas.data_sig.connect(self.meas_sim)
        self._meas.start()
        ## setup plot
        self.ax_Vp = self._fig_tVp.add_subplot(1,1,1)
        self.ax_Vh = self._fig_tVh.add_subplot(1,1,1)
        self.ax_Vc = self._fig_tI.add_subplot(1,1,1)
        self.ax_VI = self._figVI.add_subplot(1,1,1)

    ## run datataking
    @QtCore.pyqtSlot()
    def slp_run(self):
        self._sim.start()
        ## rewrite the warning text after turn on the current
        self.supply_dis.setText("Current Supply: ON")

    ## run simulator
    @QtCore.pyqtSlot(float, float)
    def slp_simulator(self, v1, v2):
        self.supply_dis.setText("Powering up\nI = %.2f A\nV = %.2f V" %(v1,v2))

    ## stop
    @QtCore.pyqtSlot()
    def slp_stop(self):
        ## rewrite the supply display
        self.supply_dis.setText("Current Supply: OFF")
        self._sim.stop()
        self._sim.wait()

    ## finished
    @QtCore.pyqtSlot()
    def slp_finish(self):
        self._sim.wait()

    ## measurement simulator
    @QtCore.pyqtSlot(float, float, float)
    def meas_sim(self, v1, v2, v3):
        now = datetime.datetime.now()
        self._data["time"] = np.append( self._data["time"], (now-self._start).total_seconds() )
        self._data[ "hts"] = np.append( self._data[ "hts"], v1 )
        self._data["curr"] = np.append( self._data["curr"], v2 )
        self._data["prot"] = np.append( self._data["prot"], v3 )
        print "%.2f  %.2f  %.2f" %(v1, v2, v3)
        self.draw()

    ## draw the measurement
    def draw(self):
        QtGui.qApp.processEvents()
        self.ax_Vp.clear()
        self.ax_Vh.clear()
        self.ax_Vc.clear()
        self.ax_VI.clear()

        self.ax_Vp.plot( self._data["time"], self._data["prot"] )
        self.ax_Vh.plot( self._data["time"], self._data[ "hts"] )
        self.ax_Vc.plot( self._data["time"], self._data["curr"] )
        self.ax_VI.plot( self._data["curr"], self._data["hts"] )

        self.plot_tVp.draw()
        self.plot_tVh.draw()
        self.plot_tI.draw()
        self.plotVI.draw()

