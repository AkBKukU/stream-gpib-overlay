#!/usr/bin/python3
import random


class GPIBInterface(object):


    def __init__(self,gpib_address,gpib_interface=0):
        self.value={}
        self.device_id = "base"

    def update(self):
        self.value = {"Random":random.random()}

    def read(self):
        return self.value


