#!/usr/bin/python3
from gpib_base import GPIBInterface

import random


class GPIBTest(GPIBInterface):


    def __init__(self,gpib_address,gpib_interface=0):
        self.value={}
        self.device_id = "test"
        self.update_interval=0
        self.update_countdown=0

    def update(self):
        self.value = {"Random":random.random()}



