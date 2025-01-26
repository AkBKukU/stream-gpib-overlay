
from gpib_base import GPIBInterface

class GPIB3478A(GPIBInterface):

    def __init__(self,gpib_address,gpib_interface=0):
        super().__init__(gpib_address,gpib_interface)

    def update(self):
        self.value = {"Reading":float(self.device.read(100))}
