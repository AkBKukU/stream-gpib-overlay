import time
from gpib_base import GPIBInterface

class GPIB3478A(GPIBInterface):

    def __init__(self,gpib_address,gpib_interface=0,default=True,emu34401A=False):
        super().__init__(gpib_address,gpib_interface)
        self.emu34401A = emu34401A
        if self.emu34401A:
            self.device_id = "HP 34401A (3478A Emulation)"
        else:
            self.device_id = "HP 3478A"

        if default:
            self.intCreate("Reading",None,interval=0,conv_float=True)

    def initialize(self):
        """Overload this function with anything you want to run after update()"""
        if self.emu34401A:
            self.setTimeout("T1s")
            self.gpibWrite("*RST")
            time.sleep(3)
            self.gpibWrite("L2")
            time.sleep(3)
            self.setTimeout("T100ms")
            time.sleep(3)
        self.initialized = True
        return


