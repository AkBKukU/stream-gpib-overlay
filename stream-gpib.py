#!/usr/bin/python3


from api_http import APIhttp

from gpib_3478a import GPIB3478A
from gpib_6633a import GPIB6633A
from gpib_34401a import GPIB34401A

#from gpib_test import GPIBTest

import asyncio
import signal
import json

data_json = "/tmp/gpib_data.json"
data_control = "/tmp/gpib_control.json"
devices = []
#devices.append({"name":"Fake Device", "dev":GPIBTest(12)})
#devices.append({"name":"DMM: 3478A Top", "dev":GPIB3478A(12)})
#devices.append({"name":"DMM: 3478A Bottom", "dev":GPIB3478A(13)})
devices.append({"name":"DMM: 34401A", "dev":GPIB34401A(11)})
# devices.append({"name":"PSU: 6632A", "dev":GPIB6633A(6)})
# devices.append({"name":"PSU: 6633A", "dev":GPIB6633A(7)})


global loop_state
loop_state = True

async def main_loop():
    """ Blocking main loop to provide time for async tasks to run"""
    global loop_state
    while loop_state:

        pause=False
        try:
            with open(data_control, 'r') as f:
                config = json.load(f)
                pause = config["pause"]
        except:
            pause=False

        if not pause:
            data = {"devices":[]}
            for dev in devices:
                dev["dev"].update()
                if dev["dev"].read() is not None:
                    data["devices"].append({dev["name"]:dev["dev"].read()})


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
