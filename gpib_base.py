#!/usr/bin/python3


import Gpib


class GPIBInterface(object):


    def __init__(self,gpib_address,gpib_interface=0):
        self.device = Gpib.Gpib(gpib_interface,gpib_address)
        self.device.timeout(gpib.T10ms)
        self.value={}
        self.device_id = "base"

    def update(self):
        self.value = {"blank":"Data not set"}

    def read(self):
        print(f"Read Value: {self.value}")
        return self.value


