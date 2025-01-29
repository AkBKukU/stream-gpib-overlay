# Web GPIB Overlay

This is a tool for mirroring the display of different GPIB test gear in a web browser. This can be captured as video or used as an overlay in OBS.

This specifically does not configure the devices and goes out of its way to make sure the front panels are as usable as possible.

## Readings Per Device

There is no magic bullet solution for reading data from different GPIB devices, even ones from the same manufacture from the same model line. Three devices are currently implemented here, each have their own quirks.

### HP 3478A

This multimeter lets you just read its buffer directly without sending any commands. This is the ideal for how this should work, but this is the only devices I've seen like this so far.

### HP 34401A

This multimeter uses SCPI and as such needs the `READ?` command sent to get the value of the display. This puts the multimeter into remote mode which locks the front panel. This requires the `ibloc` command be sent to unlock the front panel again.

### HP 6633A

This power supply predates SCIP but does need either `IOUT?` or `VOUT?` to read the current or voltage outputs respectively. These both put it into remote mode as well which locks the front panel. This, again, requires the `ibloc` to unlock the front panel. But unlike the multimeters, this device requires you to do more complex interactions when using the front panel to configure it. If it is put into remote mode while you are trying to change a setting, it will cancel it and lock the front panel. As a workaround, this device's code waits 10 seconds between reads to give you time to change settings.



## Web Overlay

This program uses `flask` to create web display of the readings. The goal though is to only have the display when the device is on. Data from the devices is communicated to the web front end using JSON both as a workaround for async issues and an easy way to load data with Javascript.
  
At all times the program is trying to read from all devices, but when they don't respond the are omitted from the JSON data.

