## @package PyKeithleyHandle
#  module handle the keithley voltage meter

import visa
import time

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
    def SetGpib(self, address):
        self.fIst = self.fRm.open_resource( address )

    ## check instrument info
    def GetInstrInfo(self):
        w = self.fIst.write("*IDN?")
        r = self.fIst.read()
        return r


class PyKeithley(PyGpibConnection):

    ## constructor
    def __init__(self):
        PyGpibConnection.__init__(self)

    ## initialize
    def Initialize(self):
        pass

    ## read data from instrument
    def Read(self):
        w = self.fIst.write(":sense:data:fetch?")
        r = self.fIst.read()
        return float(r)


