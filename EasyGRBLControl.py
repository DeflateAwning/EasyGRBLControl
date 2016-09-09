#!/usr/bin/env python
"""\
Simple g-code streaming script for grbl
"""
 
import serial
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


# Get filename
try:
	filename = sys.argv[1]
except IndexError:
	# Show open dialog
	root = tk.Tk()
	root.withdraw()
	filename = tkFileDialog.askopenfilename()

print("Loading file: " + str(filename))

openFile = open(filename, 'r')

# Stream g-code to grbl
for line in openFile:
    l = line.strip() # Strip all EOL characters for streaming
    print 'Sending: ' + l,
    serialConnection.write(l + '\n') # Send g-code block to grbl
    grbl_out = serialConnection.readline() # Wait for grbl response with carriage return
    
    if "Grbl" in grbl_out and "for help" in grbl_out:
    	# There was a reset, exit steaming
    	break

    print ' : ' + grbl_out.strip()
 
# Wait here until grbl is finished to close serial port and file.
raw_input("  Press <Enter> to exit and disable grbl.")
 
# Close file and serial port
openFile.close()
serialConnection.close()
