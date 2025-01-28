#!/usr/bin/python3


from Gpib import *


class GPIBInterface(object):


    def __init__(self,gpib_address,gpib_interface=0):
        self.device = Gpib(gpib_interface,gpib_address)
        self.device.timeout(gpib.T100ms)
        self.value={}
        self.device_id = "base"
        self.update_interval=0
        self.update_countdown=0
        self.value = None

    def update(self):
        self.value = {"blank":"Data not set"}

    def update_int(self):
        if self.update_countdown:
            self.update_countdown-=1
            return
        else:
            self.update_countdown=self.update_interval
            self.update()

    def read(self):
        print(f"Read Value: {self.value}")
        return self.value


