#!/usr/bin/python3


from api_http import APIhttp

#from gpib_3478a import GPIB3478A

from gpib_test import GPIBInterface as GPIB3478A

import asyncio
import signal
import json

data_json = "/tmp/gpib_data.json"

dmm1 = GPIB3478A(12)
dmm2 = GPIB3478A(13)

global loop_state
loop_state = True

async def main_loop():
    """ Blocking main loop to provide time for async tasks to run"""
    global loop_state
    while loop_state:
        data = {"devices":[]}
        dmm1.update()
        dmm2.update()
        if dmm1.read() is not None:
            data["devices"].append({"3478A One":dmm1.read()})
        if dmm2.read() is not None:
            data["devices"].append({"3478A Two":dmm2.read()})
        if dmm1.read() is not None:
            data["devices"].append({"3478A One":dmm1.read()})


        with open(data_json, 'w', encoding="utf-8") as output:
            output.write(json.dumps(data))

        await asyncio.sleep(3)


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
