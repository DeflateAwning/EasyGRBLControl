# EasyGRBLControl
Control GRBL from the command line with a minimalistic interface, while allowing for streaming of massive files.
This program is used to stream GCode files to a GRBL-running CNC machine. It also has a few predefined macros to make life easier.

## Current Help Message
```
Use the following commands:
	- help: displays this help message
	- probe thickness speed=25 maxdepth=10: probes worksurface at current XY position, to a maximum depth of "maxdepth" (default 10) at a speed of "speed" (default 25), moves tool back up, and sets current height to the touchplate's thickness, "thickness"
	- send: prompt for filename and stream that file (prompts for confirmation)
	- quit: closes serial connection and quits

Any other command starting with '$' or 'G' will be sent directly to GRBL. Any other command will simply give an error.

Example Commands:
	- help
	- probe 12
	- probe 20 30 5
	- send
	- quit
```