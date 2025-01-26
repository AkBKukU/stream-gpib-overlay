#!/usr/bin/python3


import Gpib


class GPIBInterface(object):


    def __init__(self,gpib_address,gpib_interface=0):
        self.device = Gpib.Gpib(gpib_interface,gpib_address)
        self.value={}
        self.device_id = "base"

    def update(self):
        self.value = {"blank":"Data not set"}

    def read(self):
        return self.value


