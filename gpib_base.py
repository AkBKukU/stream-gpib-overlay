#!/usr/bin/python3

import random
import time

from Gpib import *


class GPIBInterface(object):


    def __init__(self,gpib_address,gpib_interface=0, test=False):
        """Setup GP-IB interface for device

        Keyword arguments:
        gpib_address   -- Address of the device
        gpib_interface -- ID number for the GP-IB interface to use
        """
        self.test=test
        if not self.test:
            self.device = Gpib(gpib_interface,gpib_address)
        else:
            self.device = None
        self.setTimeout("T100ms")
        self.value={}
        self.interval_commands={}
        self.gpib_results={}
        self.device_id = "base"
        self.value = None
        self.active = False
        self.initialized = False
        self.update_change = False

# Overload Functions
    def initialize(self):
        """Overload this function with commands to run once before using device"""
        self.initialized = True
        return

    def update_pre(self):
        """Overload this function with anything you want to run before update()

        Runs once only if a GP-IB command is going to be run
        """
        return

    def update_post(self):
        """Overload this function with anything you want to run after update()

        You can also check self.update_change to see if a GP-IB command was
        sent during the update call.
        """
        return


    def setTimeout(self, timeout):
        """Set the timeout for a GP-IB command

        The Gpib module uses unusual timeout values and the timeout
        parameter must be set to one of the following as a string:
        TNONE, T10us, T30us, T100us, T300us, T1ms, T3ms, T10ms, T30ms,
        T100ms, T300ms, T1s, T3s, T10s, T30s, T100s, T300s, T1000s
        """
        timenames = ["TNONE", "T10us", "T30us", "T100us", "T300us",
                     "T1ms", "T3ms", "T10ms", "T30ms", "T100ms", "T300ms",
                     "T1s", "T3s", "T10s", "T30s", "T100s", "T300s", "T1000s"]
        if timeout not in timenames:
            raise ValueError("An invalid timeout value was given.")
            return

        if not self.test:
            # Set the GP-IB hardware timeout
            self.device.timeout(timenames.index(timeout))


    def read(self,names=None):
        """Return single or multiple stored results"""

        if not bool(self.gpib_results) or not self.active:
            return None

        # If no name given return all
        if names is None:
            names = list(self.gpib_results.keys())

        if not isinstance(names, list):
            names = [names]

        results={}
        for name in names:
            print(f"{name}: {self.gpib_results[name]}")
            results[name] = self.gpib_results[name]
        return results


# GP-IB controls
    def gpibRead(self, read_response=100,conv_float=False):
        """Read a response from GP-IB device

        Keyword arguments:
        read_response -- Bytes to read back after command
        conv_float    -- Converts result to float instead of string (default False)
        """
        try:
            if not self.test:
                result=self.device.read(read_response)
            else:
                result=str(random.random()).encode("ascii")
            print(f"{self.device_id}: Result [{str(result)}]")
            self.active = True
        except:
            self.active = False
            self.initialized = False
            print(f"{self.device_id}: gpibRead initialized = False")
            return None

        if conv_float:
            return float(result)
        else:
            return str(result)


    def gpibWrite(self,command):
        """Write a command to the GP-IB device"""
        try:
            if not self.test:
                self.device.write(str(command))

            print(f"{self.device_id}: Command [{str(command)}]")
            self.active = True
            return True
        except:
            self.active = False
            self.initialized = False
            print(f"{self.device_id}: gpibWrite initialized = False")
            return False


    def gpibCommandResponse(self, command, read_response=100,conv_float=False, result_name=None):
        """Runs a GP-IB command and optionally stores result if name given

        Keyword arguments:
        command       -- GP-IB command to send
        read_response -- Bytes to read back after command
        conv_float    -- Converts result to float instead of string (default False)
        result_name   -- Unique name ID to store response
        """

        if not self.initialized:
            self.initialize()
            if not self.initialized:
                return None

        # If there is a command, send it
        if command is not None:
            if not isinstance(command, list):
                command = [command]

            for cmd in command:
                if not self.gpibWrite(cmd):
                    self.active = False
                    self.initialized = False
                    print(f"{self.device_id}: initialized = False")
                    return
                time.sleep(0.5)

        # Read the response if requested
        if read_response:
            result=self.gpibRead(read_response,conv_float)
            if result is None:
                return None


            # Store response if name given
            if result_name is not None:
                self.gpib_results[result_name]=result

            return result


    def gpibLocal(self):
        """Send GP-IB local command"""
        try:
            if not self.test:
                self.device.ibloc()
            self.active = True
        except:
            self.active = False
            self.initialized = False
            print(f"{self.device_id}: initialized = False")
            return None


# Interval command controls
    def intCreate(self,name,command,read_response=100,conv_float=False,interval=1,repeat=True):
        """Runs a GP-IB command at an interval based on the number of calls
        to self.update()

        Keyword arguments:
        name          -- Unique name ID of command to control later
        command       -- GP-IB command to send
        read_response -- Bytes to read back after command
        conv_float    -- Converts result to float instead of string (default False)
        interval      -- Countdown of updates before running command
        repeat        -- Run indefinitely (default True)
        """
        self.interval_commands[name]={
                    "command":command,
                    "interval":interval,
                    "countdown":interval,
                    "read_response":read_response,
                    "float_response":conv_float,
                    "repeat":repeat
            }
        print(f"Added {name}")
        return


    def intRemove(self,name):
        """Remove interval command using name ID"""
        if name in self.interval_commands:
            del self.interval_commands[name]
        else:
            raise ValueError("An invalid interval name was given")


    def update(self):
        """Process intervals for all commands

        This should not be called asynchronously if multiple GP-IB devices
        are being used on one interface. The underlying driver cannot handle
        concurrent calls.
        """
        # Run custom update
        ran_pre=False
        self.update_change = False
        if not bool(self.interval_commands):
            return
        for name, inter in self.interval_commands.items():
            if inter["countdown"]:
                inter["countdown"]-=1
                continue

            if not ran_pre:
                ran_pre = True
                self.update_pre()
            self.update_change = True

            # Handle command
            self.gpibCommandResponse(
                inter["command"],
                inter["read_response"],
                inter["float_response"],
                name
                )


            if inter["repeat"]:
                inter["countdown"]=inter["interval"]
            else:
                del self.interval_commands[name]

        # Run custom update
        self.update_post()




