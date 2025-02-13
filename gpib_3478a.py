
from gpib_base import GPIBInterface

class GPIB3478A(GPIBInterface):

    def __init__(self,gpib_address,gpib_interface=0,default=True):
        super().__init__(gpib_address,gpib_interface)
        self.device_id = "HP 3478A"

        if default:
            self.intCreate("Reading",None,interval=0,conv_float=True)

