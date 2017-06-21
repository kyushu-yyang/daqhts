## derived class from HDaqGuiBase

import time
import datetime
import numpy as np
import visa
import sys
sys.path.append("/Users/yangye/Documents/Experiment/HTS/DAQ/v.2.0")

from PyQt4.Qwt5 import *
import HtsDaqGuiBase
import PyKeithleyHandle
import PyCurrentSupply
import parameter

from PyQt4 import QtGui, QtCore


## marco
TEST  = False
DEBUG = True


##
class HtsMeasurement(QtCore.QThread):

    ## data:
    ##  * voltage of hts
    ##  * voltage of protection
    ##  * voltage of current
    data_sig  = QtCore.pyqtSignal(float, float, float)
    ## current states signal
    ##  * states of the current:
    ##    * True = power on, False = power off
    power_sig = QtCore.pyqtSignal(bool)
    ## current supply value
    ##  * current
    ##  * voltage
    curr_sig  = QtCore.pyqtSignal(float, float)

    ## constructor
    def __init__(self, parent=None):
        super(HtsMeasurement, self).__init__(parent)
        # quit signal
        self.stop = False
        # set data taking instrument
        self.meas_init()
        # set power supply instrument
        self.power_init()

    ## measurement initialization
    def meas_init(self):
        # nanovoltmeter
        self.nano = PyKeithleyHandle.PyKeithley()
        self.nano.SetGpib( parameter.gpib, parameter.add_hts )
        self.nano.Channel(1)
        self.nano.Initialize()
        self.nano.Channel(2)
        self.nano.Initialize()
        if DEBUG==True:
            print " -- check nanovoltmeter: %s" %self.nano.GetInstrInfo()[:-2]
        # multimeter
        self.mult = PyKeithleyHandle.PyKeithley()
        self.mult.SetGpib( parameter.gpib, parameter.add_res )
        self.mult.Initialize()
        if DEBUG==True:
            print " -- check multimeter: %s" %self.mult.GetInstrInfo()[:-2]

    ## power supply initialization
    def power_init(self):
        self.power_state = False
        self.ramp = parameter.ramprate
        self.limI = parameter.upper_I
        self.limV = parameter.upper_V
        self.curr = PyCurrentSupply.PyCurrentSupply()
        self.curr.SetGpib( parameter.gpib, parameter.add_cur )
        self.curr.SetProtectVolt()
        if DEBUG==True:
            print " -- connect instrument: %s" %self.curr.GetInstrInfo()[:-2]
            print " -- set protection voltage: %.2f [V]" %self.curr.GetProtectVolt()
            print " -- set the upper limit of current: %.2f [A]" %self.limI
            print " -- set the upper limit of voltage: %.2f [V]" %self.limV

    ## turn off the power
    def power_off(self):
        self.curr.TurnOff()
        self.power_state = False
        if DEBUG==True:
            print " -- power off."

    ## turn on the power supply
    def power_on(self):
        self.power_state = True
        self.curr.TurnOn()
        if DEBUG==True:
            print " -- power on."

    ## setup the ramp rate
    def ramp_rate(self, ramp):
        self.ramp = ramp
        if DEBUG==True:
            print " -- ramp rate is set to %.4f A/sec" %self.ramp

    ## stop the measurement
    def stop_daq(self):
        self.stop = True
        if DEBUG==True:
            print " -- measurement is stopped."

    ## run the measurement
    def run(self):
        I  = 0.1
        rI = 0.
        rV = 0.
        dt = 1.
        self.curr.SetCurrent(I)
        self.curr.SetVoltage(0.001)
        while True:
            t1 = datetime.datetime.now()
            QtGui.qApp.processEvents()
            # current control
            if self.power_state==True:
                rI = self.curr.GetCurrent()
                rV = self.curr.GetVoltage()
                if rI>self.limI or rV>self.limV:
                    self.power_off()
                    print " -- reached the upper limit."
                    print " -- I: %.4f [A], V: %.4f [V]" %(rI, rV)
                self.curr.SetSmartCurrent(I)
                self.curr_sig.emit(rV, rI)
                time.sleep(0.01)
                I +=  self.ramp * dt
            self.power_sig.emit(self.power_state)
            ## measurement control
            if self.stop==True:
                self.nano.clear()
                self.mult.clear()
                break
            self.nano.Channel(1)
            v1 = self.nano.Read()
            self.nano.Channel(2)
            v2 = self.nano.Read()
            v3 = self.mult.Read()
            time.sleep(0.01)
            self.data_sig.emit(v1, v2, v3)
            t2 = datetime.datetime.now()
            dt = (t2-t1).total_seconds()
        self.stop_daq()
        if self.power_state==True:
            self.power_off()
        self.finished.emit()



##
class HDaqGuiHandle(QtGui.QMainWindow, HtsDaqGuiBase.Ui_Monitor):

    ## constructor
    def __init__(self, parent=None):
        super(HDaqGuiHandle, self).__init__(parent)
        self.setupUi(self)
        self._data = {"time":np.array([]), "hts":np.array([]), "prot":np.array([]), "curr":np.array([])}
        nowtime = datetime.datetime.now()
        self._prot = 1.
        self._start = nowtime
        self.setup()
        #self._file = open( parameter.path+"/meas%s.dat" %(nowtime.strftime("%Y%m%d_%H%M%S")), "w" )

    ## setup
    def setup(self):
        ## setup buttom
        self.I_on_but.clicked.connect( self.poweron )
        self.I_off_but.clicked.connect( self.poweroff )
        self.I_up_but.clicked.connect( self.rampchange )
        self.meas_but.clicked.connect( self.measure )
        self.exit_but.clicked.connect( self.daq_quit )
        ## setup the measurement class
        self._meas = HtsMeasurement()
        self._meas.data_sig.connect(self.datataking)
        self._meas.curr_sig.connect(self.warning)
        self._meas.power_sig.connect(self.states)
        self._meas.finished.connect(self.finish)
        ## setup plot
        self.ax_Vp = self._fig_tVp.add_subplot(1,1,1)
        self.ax_Vh = self._fig_tVh.add_subplot(1,1,1)
        self.ax_Vc = self._fig_tI.add_subplot(1,1,1)
        self.ax_VI = self._figVI.add_subplot(1,1,1)

    ## run datataking
    @QtCore.pyqtSlot()
    def poweron(self):
        self.I_on_but.setEnabled(False)
        self.I_off_but.setEnabled(True)
        self._meas.power_on()
        ## rewrite the warning text after turn on the current
        self.supply_dis.setText("Current Supply: ON")
        self._meas.wait()

    ## stop the power
    @QtCore.pyqtSlot()
    def poweroff(self):
        self.I_off_but.setEnabled(False)
        self.I_on_but.setEnabled(True)
        self._meas.power_off()
        self.supply_dis.setText("Current Supply: OFF")
        self._meas.wait()

    ## update the ramp rate
    @QtCore.pyqtSlot()
    def rampchange(self):
        ramp = self.ramp_box.value()
        self._meas.ramp_rate(ramp)
        self._meas.wait()

    ## check the states of power supply
    @QtCore.pyqtSlot(bool)
    def states(self, state):
        if state==False:
            self.I_off_but.setEnabled(False)
            self.I_on_but.setEnabled(True)

    ## run simulatorr
    @QtCore.pyqtSlot(float, float)
    def warning(self, v1, v2):
        #QtGui.qApp.processEvents()
        self.supply_dis.setText("Powering up\nI = %.2f A\nV = %.2f V" %(v2,v1))

    ## finished
    @QtCore.pyqtSlot()
    def finish(self):
        self._meas.wait()

    ## quit the daq
    @QtCore.pyqtSlot()
    def daq_quit(self):
        self._meas.stop_daq()
        self._meas.wait()
        self.close()

    ## run the measurement daq
    @QtCore.pyqtSlot()
    def measure(self):
        self.meas_but.setEnabled(False)
        self._meas.run()

    ## data measurement
    @QtCore.pyqtSlot(float, float, float)
    def datataking(self, v1, v2, v3):
        #QtGui.qApp.processEvents()
        now = datetime.datetime.now()
        self._data["time"] = np.append( self._data["time"], (now-self._start).total_seconds() )
        self._data[ "hts"] = np.append( self._data[ "hts"], v1 )
        self._data["prot"] = np.append( self._data["prot"], v2 )
        self._data["curr"] = np.append( self._data["curr"], v3/parameter.shuntres )
        self._prot = v2
        #print "%.2f  %.2f  %.2f" %(v1, v2, v3)
        self.draw()

    ## draw the measurement
    def draw(self):
        #QtGui.qApp.processEvents()
        self.ax_Vp.clear()
        self.ax_Vh.clear()
        self.ax_Vc.clear()
        self.ax_VI.clear()

        self.ax_Vp.plot( self._data["time"], self._data["prot"], "ob", markeredgewidth=0.)
        self.ax_Vh.plot( self._data["time"], self._data[ "hts"], "^g", markeredgewidth=0.)
        self.ax_Vc.plot( self._data["time"], self._data["curr"], "vr", markeredgewidth=0.)
        self.ax_VI.plot( self._data["curr"], self._data["hts"], "sk" )

        self.ax_Vp.set_xlabel("Time [sec]")
        self.ax_Vp.set_ylabel("Voltage [V]")
        self.ax_Vh.set_xlabel("Time [sec]")
        self.ax_Vh.set_ylabel("Voltage [V]")
        self.ax_Vc.set_xlabel("Time [sec]")
        self.ax_Vc.set_ylabel("Current [A]")
        self.ax_VI.set_xlabel("Current [A]")
        self.ax_VI.set_ylabel("Voltage [V]")

        self.plot_tVp.draw()
        self.plot_tVh.draw()
        self.plot_tI.draw()
        self.plotVI.draw()
        self._fig_tVp.tight_layout()
        self._fig_tVh.tight_layout()
        self._fig_tI.tight_layout()
        self._figVI.tight_layout()

