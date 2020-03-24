# EasyGRBLControl
Control GRBL from the command line with a minimalistic interface, while allowing for streaming of massive files.
This program is used to stream GCode files to a GRBL-running CNC machine. It also has a few predefined macros to make life easier.

## Current Help Message
The follow help message describes most of the features/commands present in this program.
```
Use the following commands:
	- help: displays this help message
	- probe <thickness of touch plate=19.25> <speed=25> <maxdepth=10>: probes worksurface at current XY position (default shown), moves tool back up, and sets the appropriate height (touchplate thickness)
	- send: prompt for filename and stream that file (prompts for confirmation)
	- abs/rel: absolute coordinate mode/relative coordinate mode (G90=abs, G91=rel)
	- quit: closes serial connection and quits

Any other command starting with '$' or 'G' will be sent directly to GRBL. Any other command will simply give an error.

Example Commands:
	- help
	- probe
	- probe 12
	- probe 20 30 5
	- send
	- abs/rel
	- G0 X10
	- quit
```

## To Do
* Change to Python3
* Improve readline to readlines system in reading buffer