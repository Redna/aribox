import os
import subprocess
import psutil
import sys

from pirc522 import RFID


class Aribox:
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
        self.proc = None
        pass

    def launch_action(self, uid) -> None:
        uid_str = f"{str(uid[0])}_{str(uid[1])}_{str(uid[2])}_{str(uid[3])}"
        action = f"./actions/uid/{uid_str}"

        if not os.path.isfile(action):
            print(f"No action defined for card with UID[{uid_str}]!")
            return

        print(f"Launching {action}")
        self.proc = subprocess.Popen(['/bin/sh', '-c', action])

    def stop_subprocesses(self) -> None:
        if not hasattr(self.proc, 'pid'):
            return

        proc_pid = self.proc.pid
        print(f"Stopping all subprocesses associated with {proc_pid}")
        process = psutil.Process(proc_pid)
        for proc in process.children(recursive=True):
            proc.kill()
        self.proc = None


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
