## @package PyKeithleyHandle
#  module handle the keithley voltage meter

import visa
import time

import sys
sys.path.append("/Users/yangye/Documents/Experiment/HTS/DAQ/v.2.0")
import parameter

## base class to connect the device with gpib
#
class PyGpibConnection:

    ## constructor
    def __init__(self):
        self.fRm = visa.ResourceManager()

    ## check gpib port
    def GetGpibPort(self):
        gpib = self.fRm.list_resources()
        return gpib

    ## set gpib port
    def SetGpib(self, gpib, address):
        self.fIst = self.fRm.open_resource("GPIB%i::%i::INSTR" %(gpib,address))

    ## check instrument info
    def GetInstrInfo(self):
        w = self.fIst.write("*IDN?")
        r = self.fIst.read()
        return r

    ## reset the command
    def reset(self):
        w = self.fIst.write("*RST")

    ## clear the register
    def clear(self):
        self.fIst.write(":system:clear")


class PyKeithley(PyGpibConnection):

    ## constructor
    def __init__(self):
        PyGpibConnection.__init__(self)

    ## initialize
    def Initialize(self):
        self.fIst.write(":sense:voltage:nplcycles %.2f" %parameter.sampling)
        self.fIst.write(":sense:voltage:lpass OFF")
        self.fIst.write(":output:relative ON")

    ## change the channel
    def Channel(self, ch):
        self.fIst.write(":sense:channel %i" %ch)

    ## require the current channel
    def ReqChannel(self):
        self.fIst.write(":sense:channel?")
        r = self.fIst.read()
        return int(r)

    ## read data from instrument
    def Read(self):
        w = self.fIst.write(":fetch?")
        r = self.fIst.read()
        return float(r)


