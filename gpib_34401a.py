
from gpib_base import GPIBInterface

class GPIB34401A(GPIBInterface):

    def __init__(self,gpib_address,gpib_interface=0):
        super().__init__(gpib_address,gpib_interface)

    def update(self):
        data = None
        try:
            # 34401A can read the current display but must be put back into
            # local after reading the data from the buffer.
            device.write("READ?")
            data=float(device.read(100))
            device.ibloc()
            self.value = {"Reading":data}
        except:
            self.value = None
