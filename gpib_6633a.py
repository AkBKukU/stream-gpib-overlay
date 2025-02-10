
from gpib_base import GPIBInterface

class GPIB6633A(GPIBInterface):

    def __init__(self,gpib_address,gpib_interface=0,default=True):
        super().__init__(gpib_address,gpib_interface)
        self.update_interval=10
        self.device_id = "HP 663X"

        if default:
            self.intCreate("Volts","VOUT?",interval=3,conv_float=True)
            self.intCreate("Amps","IOUT?",interval=3,conv_float=True)


    def update_post(self):
        """Return to local mode"""
        if self.update_change:
            self.gpibLocal()
        return

