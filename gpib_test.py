#!/usr/bin/python3
from gpib_base import GPIBInterface

import random


class GPIBTest(GPIBInterface):


    def __init__(self,gpib_address,gpib_interface=0,default_interval=True):
        super().__init__(gpib_address,gpib_interface, test=True)
        self.value={}
        self.device_id = "test"
        self.intCreate("Random 1","",interval=1,conv_float=True)
        self.intCreate("Random 2","",interval=3,conv_float=True)
        self.intCreate("Random 3","",read_response=0,interval=3,conv_float=True)




