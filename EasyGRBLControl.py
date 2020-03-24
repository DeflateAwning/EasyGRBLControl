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
	print("Cannot open serial port (check location and permissions)")
	sys.exit()

# Wake up grbl
serialConnection.write("\r\n\r\n")
time.sleep(2)   # Wait for grbl to initialize
serialConnection.flushInput()  # Flush startup text in serial input

try:
	filename = sys.argv[1]
	streamFile()
except IndexError:
	filename = ""

probeMacro = """
G0 Z0
"""

def streamFile():
	""" This command can be called from the main prompt, prompts for file location and streams file """

	# Get filename
	if filename == "":
		# Show open dialog
		root = tk.Tk()
		root.withdraw()
		filename = tkFileDialog.askopenfilename()

	if raw_input('Press enter to begin streaming "' + str(filename) + '" or type quit and press enter to go back to prompt.'):
		return 1

	openFile = open(filename, 'r')

	startTime = time.time()

	# Stream g-code to grbl
	for line in openFile:
		l = line.strip() # Strip all EOL characters for streaming
		print 'Sending: ' + l,
		serialConnection.write(l + '\n') # Send g-code block to grbl
		grbl_out = serialConnection.readline() # Wait for grbl response with carriage return
		
		if "Grbl" in grbl_out and "for help" in grbl_out:
			# There was a reset (ie Emergency Stop), exit steaming
			break

		print ' : ' + grbl_out.strip()

	# Close g-code 
	openFile.close()
	filename = ""

	print ("Done streaming file in " + str(round((time.time() - startTime)/60, 2)) + " minutes.")

def sendMacro():
	print("sendMacro not currently implemented")

def sendCommand(l):
	"""
	Sends a single line of GCode to the machine
	"""
	serialConnection.write(l + '\n') # Send g-code block to grbl
	grbl_out = serialConnection.readline() # Wait for grbl response with carriage return
	print ' : ' + grbl_out.strip()

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
	- quit: closes serial connection and quits

Any other command starting with '$' or 'G' will be sent directly to GRBL. Any other command will simply give an error.

Example Commands:
	- help
	- probe 12
	- probe 20 30 5
	- send
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
		sendCommand(command)

	else:
		print("Invalid command. Try again.")





