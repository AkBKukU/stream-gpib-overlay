
import time
from gpib_base import GPIBInterface

class GPIB34401A(GPIBInterface):

    def __init__(self,gpib_address,gpib_interface=0,default=True):
        super().__init__(gpib_address,gpib_interface)
        self.device_id = "HP 34401A"
        self.mode_conf={}
        self.mode_conf["VOLT"]="Volts"
        self.mode_conf["CURR"]="Amps"
        self.mode_conf["RES"]="Ohms"
        self.mode_conf["PER"]="Hz"
        self.mode_conf["CONT"]="Continuity"
        self.mode_conf["DIOD"]="Volts"

        if default:
            self.intCreate("Reading",["READ?"],interval=5,conv_float=True)


    def initialize(self):
        """Overload this function with anything you want to run after update()"""
        self.setTimeout("T1s")
        self.gpibWrite("*RST")
        self.gpibLocal()
        self.setTimeout("T100ms")
        self.initialized = True
        print(f"{self.device_id}: Initialized")
        time.sleep(3)
        return

    def configManage(self):
        self.setTimeout("T1s")
        # Query state: "CONF?"
        #conf = self.gpibCommandResponse("CONF?")


        #self.setTimeout("T100ms")

    def update_pre(self):
        """Setup timeout"""
        self.setTimeout("T3s")
        print(f"{self.device_id}: update_pre")
        return


    def update_post(self):
        """Return to local mode"""
        if self.update_change:
            print(f"{self.device_id}: update_change")
            self.setTimeout("T100ms")
            self.gpibLocal()
        print(f"{self.device_id}: update_post")
        return
