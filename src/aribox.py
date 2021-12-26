import os
import subprocess
import psutil
import sys

from time import time
from psutil import NoSuchProcess
from pirc522 import RFID


CARD_REMOVED_THRESHOLD = 1  # seconds
    

class Aribox:
    
    
    process = None
    action_id = ""    
        
    def __init__(self):
        # Welcome message
        print("    _____")
        print("   |     |")
        print("   | | | |")
        print("   |_____|")
        print("   __|_|__ ")
        print("Welcome to Aribox")
        print("RFID reader started... beep beep beep...")
        print("")
        print("Press Ctrl-C to stop.")
        print("Waiting for a card...")
        pass

    def launch_action(self, id) -> None:
        action = f"./actions/uid/{id}"

        if not os.path.isfile(action):
            print(f"No action defined for card with UID[{id}]!")
            return

        print(f"Launching {action}")
        proc = subprocess.Popen(['/bin/sh', '-c', action])
        self.process = psutil.Process(proc.pid)
        self.action_id = id
        self.start_time = time()

    def stop_subprocesses(self) -> None:
        if not hasattr(self.process, 'pid'):
            return

        print(f"Stopping all subprocesses associated with {self.process.pid}")
        
        try:
            for subprocess in self.process.children(recursive=True):
                subprocess.kill()
        except NoSuchProcess:
            pass

        self.process = None

    def toggle_pause(self) -> None:
        if not hasattr(self.process, 'pid'):
            return

        if is_subprocess_sleeping(self.process):            
            print(f"Resuming all subprocesses associated with {self.process.pid}")
            deep_resume(self.process)
        else:            
            print(f"Suspending all subprocesses associated with {self.process.pid}")
            deep_suspend(self.process)

    def is_action_running(self, id) -> bool:        
        action_running = (self.action_id == id
                          and self.process is not None 
                          and self.process.status() != 'zombie'
                          and time() - self.start_time < CARD_REMOVED_THRESHOLD)
        
        self.start_time = time()
        return action_running  


class RFIDWrapper:
    def __init__(self, aribox: Aribox) -> None:
        self.rdr = RFID()
        self.util = self.rdr.util()
        self.util.debug = True
        self.running = True
        self.aribox = aribox

    def listen(self, debug=False) -> bytearray:
        if debug:
            return [119, 162, 108, 178]

        self.rdr.wait_for_tag()
        (error, data) = self.rdr.request()

        if error:
            raise RuntimeWarning(
                "Not able to read RFID tag. Maybe tag was removed too fast")

        print("\nDetected Card: " + format(data, "02x"))
        (error, uid) = self.rdr.anticoll()

        if error:
            raise RuntimeWarning(
                "Not able extract UID and run anti collision. Maybe tag was removed too fast")

        return uid

    def interrupt_handler(self, signal, frame) -> None:
        self.running = False
        print("\nCtrl+C captured, ending read.")
        self.aribox.stop_subprocesses()
        self.rdr.cleanup()
        sys.exit()



def deep_suspend(process):
    for subprocess in process.children(recursive=True):
        deep_suspend(subprocess)
        subprocess.suspend()


def deep_resume(process):
    for subprocess in process.children(recursive=True):
        deep_resume(subprocess)
        subprocess.resume()


def is_subprocess_sleeping(process) -> bool:
    sleeping = True

    for subprocess in process.children(recursive=True):
        sleeping = is_subprocess_sleeping(
            subprocess) and subprocess.status() == 'stopped'

    return sleeping
