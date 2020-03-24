#!/usr/bin/env python

# Control GRBL from the command line with a minimalistic interface, while allowing for streaming of massive files
# Written for Python 2
 
import serial # sudo pip install pyserial
import time
import sys

import Tkinter as tk
import tkFileDialog

# Open grbl serial port
try:
	serialConnection = serial.Serial('/dev/ttyUSB0', 115200)
except serial.serialutil.SerialException:
	print("Cannot open serial port 'ttyUSB0' (check location and permissions)")
	sys.exit()

# Wake up grbl
serialConnection.write("\r\n\r\n")
time.sleep(2)   # Wait for grbl to initialize
serialConnection.flushInput()  # Flush startup text in serial input

# Stream the command line argument file, generally not used
if len(sys.argv) == 2:
	filename = sys.argv[1]
	streamFile(filename)

probeMacro = """
G90
G38.2 Z-{0[maxdepth]} F{0[speed]}
G92 Z{0[thickness]}
G91
G0 Z8
"""
# Probes, stop on contact. Sets the current height to the thickness. Sets to relative movement. Raises 8mm to get plate out.

promptTemplate = "({mode}) >>> "
modeOptions = {"abs/rel": "abs"}


def getIncomingSerial():
	"""
	Gets all currently waiting incoming serial data from the serial connection.

	If it's just an 'ok', it puts it on the same line. Otherwise, it puts it on a new line.
	"""
	out = ""
	while serialConnection.in_waiting == 0:
		#print("Delaying while the machine sends an output")
		time.sleep(0.05)

	while serialConnection.in_waiting > 0:
		out += serialConnection.read_until().strip() + "\n"
	out = out.strip()
	return out


def streamFile(filename=None):
	""" This command can be called from the main prompt, prompts for file location and streams file """

	# Get filename
	if filename is None:
		# Show open dialog
		root = tk.Tk()
		root.withdraw()
		filename = tkFileDialog.askgcodeFilename(initialdir="/home/parker/Dropbox/1Parker/")

	if raw_input('Press enter to begin streaming "' + str(filename) + '" or type quit and press enter to go back to prompt.'):
		print("Cancelled streaming.")
		return 1

	# Count the number of lines in the file (for estimation purposes)
	# In the future, also calculate distance from this info
	gcodeFile = open(filename, 'r')
	totalLines = 0
	for line in gcodeFile:
		totalLines += 1
	gcodeFile.close()

	startTime = time.time()
	curLineNumber = 0
	gcodeFile = open(filename, 'r')

	# Stream g-code to grbl
	for line in gcodeFile:
		l = line.strip() # Strip all EOL characters for streaming
		curLineNumber += 1

		print('Sending: ' + l)
		serialConnection.write(l + '\n') # Send g-code block to grbl
		incomingSerial = getIncomingSerial()
		
		if "Grbl" in incomingSerial and "for help" in incomingSerial:
			# There was a reset (ie Emergency Stop), exit steaming
			print("EMERGENCY STOPPING STREAMING, likely an emergency stop or reset")
			break

		print('Received: ' + incomingSerial + " : \t\t" + str(curLineNumber) + "/" + str(totalLines) + "=" + str(round(curLineNumber*100/totalLines, 2)) + "% in " + str(round((time.time()-startTime)/60, 2)) + " min")

	# Close g-code 
	gcodeFile.close()

	print("Done streaming file in {:.2f} minutes.".format((time.time() - startTime)/60))

def sendMacro(commandLines):
	"""
	Sends a command with multiple lines
	"""

	for line in commandLines.split('\n'):
		if len(line) == 0:
			continue

		line = line.strip()
		print("Send: " + line)
		sendCommand(line)

def sendCommand(l):
	"""
	Sends a single line of GCode to the machine, generally from prompt.

	Also, sets the current movement mode (G90/G91 for abs vs. rel movement)
	"""
	l = l.strip()

	if l.lower() == "g90":
		modeOptions["abs/rel"] = "abs"
	elif l.lower() == "g91":
		modeOptions["abs/rel"] = "rel"

	serialConnection.write(l + '\n') # Send g-code block to grbl
	#incomingSerial = serialConnection.readline() # Wait for grbl response with carriage return
	incomingSerial = getIncomingSerial()
	print("\tReceived: " + incomingSerial)

def closeConnections():
	# Close serial port
	serialConnection.close()
	print("Closed serial connection, exiting now.")
	sys.exit()

def printHelp():
	print("""
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
""")

printHelp()

while True:
	# Prompt for Input
	command = raw_input(promptTemplate.format(mode=','.join(modeOptions.values())))

	# Convert to Lower Case, Strip leading/trailing whitespaces
	command = command.lower().strip()

	if command == "help":
		printHelp()

	elif command == "quit" or command == "exit":
		closeConnections()

	elif command == "send":
		streamFile()

	elif command.startswith('abs'):
		sendCommand("G90")
		modeOptions["abs/rel"] = "abs"
	elif command.startswith('rel'):
		sendCommand("G91")
		modeOptions["abs/rel"] = "rel"

	elif command.startswith("probe"):
		commandSplit = command.split(" ")
		probeOptions = {"thickness": 19.25, "speed": 25, "maxdepth": 10}
		try:
			probeOptions["thickness"] = float(commandSplit[1])
		except:
			pass
		try:
			probeOptions["thickness"] = float(commandSplit[2])
		except:
			pass
		try:
			probeOptions["thickness"] = float(commandSplit[3])
		except:
			pass
		if not raw_input("Press enter to confirm sending probe with options: {} >>> ".format(probeOptions)):
			sendMacro(probeMacro.format(probeOptions))
			print("Probing Complete.")
		else:
			print("Cancelled Probe.")

	elif command.startswith("$") or command.startswith("g") or command.startswith("m"):
		# Accept Single G-Codes and M-Codes
		sendCommand(command)

	else:
		print("Invalid command. Try again.")





