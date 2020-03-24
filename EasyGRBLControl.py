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
G0 Z0
"""

def streamFile(filename=None):
	""" This command can be called from the main prompt, prompts for file location and streams file """

	# Get filename
	if filename is None:
		# Show open dialog
		root = tk.Tk()
		root.withdraw()
		filename = tkFileDialog.askgcodeFilename(initialdir="/home/parker/Dropbox/1Parker/")

	if raw_input('Press enter to begin streaming "' + str(filename) + '" or type quit and press enter to go back to prompt.'):
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

		print 'Sending: ' + l,
		serialConnection.write(l + '\n') # Send g-code block to grbl
		incomingSerialLine = serialConnection.readline() # Wait for grbl response with carriage return
		
		if "Grbl" in incomingSerialLine and "for help" in incomingSerialLine:
			# There was a reset (ie Emergency Stop), exit steaming
			print ("EMERGENCY STOPPING STREAMING, likely an emergency stop or reset")
			break

		print ' : ' + incomingSerialLine.strip() + " : \t\t" + str(curLineNumber) + "/" + str(totalLines) + "=" + str(round(curLineNumber*100/totalLines, 2)) + "% in " + str(round((time.time()-startTime)/60, 2)) + " min"

	# Close g-code 
	gcodeFile.close()

	print("Done streaming file in {:.2f} minutes.".format((time.time() - startTime)/60))

def sendMacro():
	print("sendMacro not currently implemented")

def sendCommand(l):
	"""
	Sends a single line of GCode to the machine, generally from prompt
	"""
	serialConnection.write(l + '\n') # Send g-code block to grbl
	incomingSerialLine = serialConnection.readline() # Wait for grbl response with carriage return
	print ' : ' + incomingSerialLine.strip()

def closeConnections():
	# Close serial port
	serialConnection.close()
	print("Closed serial connection, exiting now.")
	sys.exit()

def printHelp():
	print("""
Use the following commands:
	- help: displays this help message
	- probe thickness speed=25 maxdepth=10: probes worksurface at current XY position, to a maximum depth of "maxdepth" (default 10) at a speed of "speed" (default 25), moves tool back up, and sets current height to the touchplate's thickness, "thickness"
	- send: prompt for filename and stream that file (prompts for confirmation)
	- abs/rel: absolute coordinate mode/relative coordinate mode (G90=abs, G91=rel)
	- quit: closes serial connection and quits

Any other command starting with '$' or 'G' will be sent directly to GRBL. Any other command will simply give an error.

Example Commands:
	- help
	- probe 12
	- probe 20 30 5
	- send
	- abs/rel
	- quit
""")

printHelp()

while True:
	# Prompt for Input
	command = raw_input(">>> ")

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
	elif command.startswith('rel'):
		sendCommand("G91")

	elif command.startswith("probe"):
		commandSplit = command.split(" ")
		try:
			thickness = commandSplit[1]
		except:
			print("No/invalid thickness provided.")
			continue
		try:
			speed = commandSplit[2]
		except:
			speed = 25
		try:
			maxdepth = commandSplit[3]
		except:
			maxdepth = 10
		sendMacro(probeMacro.replace("thickness", thickness).replace("speed", speed).replace("maxdepth", maxdepth))

	elif command[0] == "$" or command[0] == "g" or command[0] == "m":
		# Accept Single G-Codes and M-Codes
		sendCommand(command)

	else:
		print("Invalid command. Try again.")





