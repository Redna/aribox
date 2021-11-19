#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import signal
import time
import os.path
import subprocess
import os
import psutil

from pirc522 import RFID

from reader import Aribox

STOPCODE=[233, 241, 62, 141, 171]

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()
    sys.exit()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class RFID
run = True
rdr = RFID()
util = rdr.util()
util.debug = True
active_subproc = None

aribox = Aribox()

root = os.path.abspath(os.curdir)

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while run:
    
    rdr.wait_for_tag()
    (error, data) = rdr.request()

    if not error:
        print("\nDetected Card: " + format(data, "02x"))
        subprocess.Popen(['aplay', '/home/pi/pi-rc522/AFK/beep.wav'])

        (error, uid) = rdr.anticoll()
    if not error:        
        if hasattr(active_subproc, 'pid'):
            aribox.stop_subprocesses()
        
        print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

        print("./.AFK/actions/uid/"+str(uid[0])+"_"+str(uid[1])+"_"+str(uid[2])+"_"+str(uid[3]))

        action = "./AFK/actions/uid/"+str(uid[0])+"_"+str(uid[1])+"_"+str(uid[2])+"_"+str(uid[3])
        if os.path.isfile(action):
            print("Found predefined action for UID!")
            aribox.launch_subprocess(action)
        else:
            print("No action defined for card!!")
        time.sleep(1)

