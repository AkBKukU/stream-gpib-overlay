
from gpib_base import GPIBInterface

class GPIB3478A(GPIBInterface):

    def __init__(self,gpib_address,gpib_interface=0):
        super().__init__(gpib_address,gpib_interface)
        self.intCreate("Reading","",interval=1,conv_float=True)

