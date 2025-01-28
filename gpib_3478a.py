
from Gpib import *
from gpib_base import GPIBInterface

class GPIB3478A(GPIBInterface):

    def __init__(self,gpib_address,gpib_interface=0):
        super().__init__(gpib_address,gpib_interface)

    def update(self):
        try:
            # Just reading the buffer will give the current display value
            self.value = {"Reading":float(self.device.read(100))}
        except:
            self.value = None
