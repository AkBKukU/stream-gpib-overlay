#!/usr/bin/python3


from api_http import APIhttp

from gpib_3478a import GPIB3478A
from gpib_6633a import GPIB6633A
from gpib_34401a import GPIB34401A

#from gpib_test import GPIBInterface as GPIB3478A

import asyncio
import signal
import json

data_json = "/tmp/gpib_data.json"

dmm1 = GPIB3478A(12)
dmm2 = GPIB3478A(13)
dmm3 = GPIB34401A(11)
psu1 = GPIB6633A(6)
psu2 = GPIB6633A(7)

global loop_state
loop_state = True

async def main_loop():
    """ Blocking main loop to provide time for async tasks to run"""
    global loop_state
    while loop_state:
        data = {"devices":[]}
        dmm1.update_int()
        dmm2.update_int()
        dmm3.update_int()
        psu1.update_int()
        psu2.update_int()
        if dmm1.read() is not None:
            data["devices"].append({"DMM: 3478A Top":dmm1.read()})
        if dmm2.read() is not None:
            data["devices"].append({"DMM: 3478A Bottom":dmm2.read()})
        if dmm3.read() is not None:
            data["devices"].append({"DMM: 34401A":dmm3.read()})
        if psu1.read() is not None:
            data["devices"].append({"PSU: 6632A":psu1.read()})
        if psu2.read() is not None:
            data["devices"].append({"PSU: 6633A":psu2.read()})


        with open(data_json, 'w', encoding="utf-8") as output:
            output.write(json.dumps(data))

        await asyncio.sleep(1)


async def main():
    """ Start connections to async modules """

    # Setup CTRL-C signal to end programm
    signal.signal(signal.SIGINT, exit_handler)
    print('Press Ctrl+C to exit program')

    # Start async modules
    L = await asyncio.gather(
        http.connect(),
        main_loop()
    )

def exit_handler(sig, frame):
    """ Handle CTRL-C to gracefully end program and API connections """
    global loop_state
    print('You pressed Ctrl+C!')
    loop_state = False


http = APIhttp()


asyncio.run(main())

# Run after CTRL-C
http.disconnect()
