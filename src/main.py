#!/usr/bin/env python
# -*- coding: utf8 -*-

import signal
import time
import subprocess

from aribox import Aribox, RFIDWrapper

STOPCODE = [233, 241, 62, 141, 171]
DEBUG = False


def main():
    aribox = Aribox()
    rfid = RFIDWrapper(aribox)

    signal.signal(signal.SIGINT, rfid.interrupt_handler)

    while rfid.running:
        try:
            uid = rfid.listen(debug=DEBUG)
            subprocess.Popen(['aplay', './beep.wav'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
            aribox.stop_subprocesses()
            aribox.launch_action(uid)
        except RuntimeWarning as e:
            print("Problem reading RFID Tag", e)

        time.sleep(25)


if __name__ == "__main__":
    main()
