#!/usr/bin/env python
# -*- coding: utf8 -*-

import signal
import time
import subprocess
import alsaaudio

from alsaaudio import ALSAAudioError

from gpiozero import Button

from aribox import Aribox, RFIDWrapper

STOPCODE = [233, 241, 62, 141, 171]
DEBUG = False
PLAY_SOUNDS = True

DISABLE_WIFI = True
DISABLE_WIFI_ACTION = './actions/uid/20_175_34_51'

MAXIMUM_ALSA_VOLUME = 40
MINIMUM_ALSA_VOLUME = 10

mixer = alsaaudio.Mixer()
aribox = Aribox()

    
def blue_button_handler():
    volume = int(mixer.getvolume()[0])
    newvolume = volume - 5

    if newvolume >= MINIMUM_ALSA_VOLUME:
        mixer.setvolume(newvolume)


def yellow_button_handler():
    volume = int(mixer.getvolume()[0])
    newvolume = volume + 5
    
    if newvolume <= MAXIMUM_ALSA_VOLUME:
        mixer.setvolume(newvolume)


def red_button_handler():
    aribox.toggle_pause()


def red_button_held_handler():
    print("Shutting down ...")
    
    if PLAY_SOUNDS:
        subprocess.Popen(['aplay', './songs/stop.wav'])
        time.sleep(5)

    subprocess.Popen(['/bin/sh', '-c', 'sudo systemctl poweroff'])

def disable_wifi():
    subprocess.Popen(['/bin/sh', '-c', DISABLE_WIFI_ACTION])

def main():    
        
    if PLAY_SOUNDS:
        subprocess.Popen(['aplay', './songs/start.wav'])
    
    if DISABLE_WIFI:
        disable_wifi()
    
    rfid = RFIDWrapper(aribox)

    signal.signal(signal.SIGINT, rfid.interrupt_handler)
    
    blue_button = Button(21)
    red_button = Button(13, hold_time=3)
    yellow_button = Button(5)
    blue_button.when_pressed = blue_button_handler
    red_button.when_pressed = red_button_handler
    red_button.when_held = red_button_held_handler 
    
    yellow_button.when_pressed = yellow_button_handler
    
    while rfid.running:
        try:
            uid = rfid.listen(debug=DEBUG)
            action_id = f"{str(uid[0])}_{str(uid[1])}_{str(uid[2])}_{str(uid[3])}"
            
            if aribox.is_action_running(action_id):
                continue
            
            subprocess.Popen(['/bin/sh', '-c', "aplay ./beep.wav"])
            aribox.stop_subprocesses()
            aribox.launch_action(action_id)
        except RuntimeWarning as e:
            print("Problem reading RFID Tag", e)
        except Exception as e:
            print("Error occured: ", e)

        time.sleep(1)
        if(DEBUG):
            time.sleep(22)


if __name__ == "__main__":
    main()
