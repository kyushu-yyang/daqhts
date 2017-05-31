## @package PyCurrentSupply
#  module to handle the power supply for measurement
#

import PyKeithleyHandle
import visa

## class to control the power supply
#
class PyCurrentSupply(PyKeithleyHandle.PyGpibConnection):

    ## constructor
    def __init__(self):
        PyKeithleyHandle.PyGpibConnection.__init__(self)

    ## set protection voltage
    def SetProtectVolt(self, volt=5.):
        self.fIst.write("volt:prot %.2f" %volt)

    ## return the protection voltage
    def GetProtectVolt(self):
        w = self.fIst.write("volt:prot?")
        r = self.fIst.read()
        return float(r)

    ## turn off the power supply
    def TurnOff(self):
        self.fIst.write("outp OFF")

    ## turn on the power supply
    def TurnOn(self):
        self.fIst.write("outp ON")

    ## set input voltage
    def SetVoltage(self, volt):
        self.fIst.write("volt %.4f" %volt)

    ## return the voltage from machine
    def GetVoltage(self):
        w = self.fIst.write("meas:volt?")
        r = self.fIst.read()
        return float(r)

    ## set input current
    def SetCurrent(self, curr):
        self.fIst.write("curr %.2f" %curr)

    ## return the current from machine
    def GetCurrent(self):
        w = self.fIst.write("meas:curr?")
        r = self.fIst.read()
        return float(r)

    ## set current with tuning voltage
    def SetSmartCurrent(self, curr, dV=0.1):
        # get setup voltage
        setvolt = self.GetSetupVolt()

        # measured voltage
        meavolt = self.GetVoltage()

        # voltage tuning
        while True:
            if meavolt>setvolt+0.01 or meavolt<setvolt-0.01:
                break
            setvolt += dV
            self.SetVoltage(setvolt)

        self.SetCurrent(curr)

    ## return set voltage
    def GetSetupVolt(self):
        w = self.fIst.write("volt?")
        r = self.fIst.read()
        return float(r)

    ## return set current
    def GetSetupCurrent(self):
        w = self.fIst.write("curr?")
        r = self.fIst.read()
        return float(r)
