
import asyncio
from Gpib import *
from gpib_base import GPIBInterface

class GPIB34401A(GPIBInterface):

    def __init__(self,gpib_address,gpib_interface=0):
        super().__init__(gpib_address,gpib_interface)
        self.device.timeout(gpib.T1s)
        self.device.write("*RST")
        self.device.ibloc()
        self.device.timeout(gpib.T100ms)
        self.update_interval=0

    def update(self):
        data = None
        try:
            # 34401A can read the current display but must be put back into
            # local after reading the data from the buffer.
            #
            # The 34401A requires a 1 second timeout or it will error.
            self.device.timeout(gpib.T3s)
            self.device.write("READ?")
            data=float(self.device.read(100))
            self.device.ibloc()
            self.device.timeout(gpib.T100ms)
            self.value = {"Reading":data}
        except:
            self.value = None
