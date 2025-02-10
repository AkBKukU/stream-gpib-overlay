
from gpib_base import GPIBInterface

class GPIB34401A(GPIBInterface):

    def __init__(self,gpib_address,gpib_interface=0):
        super().__init__(gpib_address,gpib_interface)
        self.intCreate("Reading","READ?",interval=0,conv_float=True)


    def initialize(self):
        """Overload this function with anything you want to run after update()"""
        self.setTimeout("T1s")
        self.gpibWrite("*RST")
        self.gpibLocal()
        self.setTimeout("T100ms")
        self.initialized = True
        return


    def update_pre(self):
        """Setup timeout"""
        self.setTimeout("T3s")
        return


    def update_post(self):
        """Return to local mode"""
        if self.update_change:
            self.setTimeout("T100ms")
            self.gpibLocal()
        return
