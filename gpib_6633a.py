
from gpib_base import GPIBInterface

class GPIB6633A(GPIBInterface):

    def __init__(self,gpib_address,gpib_interface=0):
        super().__init__(gpib_address,gpib_interface)
        self.update_interval=10

    def update(self):
        try:
            # 6633/6632 can have it's outputs queried
            self.device.write("VOUT?")
            volts = float(self.device.read(100))
            self.device.write("IOUT?")
            amps = float(self.device.read(100))
            self.value = {
                "Volts":volts,
                "Amps":amps,
                }
            self.device.ibloc()
        except:
            self.value = None
