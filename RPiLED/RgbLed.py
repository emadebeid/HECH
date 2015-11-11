#!/usr/bin/python

import time, sys, string, logging
import getopt
from threading import Thread
from multiprocessing import Lock
from time import sleep

from RPIO import PWM

log = logging.getLogger(__file__.strip("./").split('.')[0].split('/')[-1])
log.setLevel(logging.DEBUG)

PWM_RES = 1000 # resultion in us
PWM_PRD = 200000 # period in us
PWM_PRD1 = 2000000 # period in us
PWM_DMA = 0 # channels for each pin (0-14)
PWM_DMA1 = 1 # channels for each pin (0-14)

class RgbLed(object):
    """A RGB LED that can be set to: off, on or blinking in either of the colors red, green or blue
    Author: Egon Kidmose""" 

    def __init__(self, pins):
        """Pin configuration. 
        [pins] : List of the the pins to use for R,G and B (GPIO.BCM numbering). """
        pins = [int(pin) for pin in pins.split(',')]
        if not len(pins) == 3:
            raise ValueError("Configuration must contain three pins (pins="+str(pins)+")")
        self._pins = pins
        
        # PWM setup
        PWM.setup(pulse_incr_us=PWM_RES)
        PWM.init_channel(PWM_DMA, subcycle_time_us=PWM_PRD)
        PWM.init_channel(PWM_DMA1, subcycle_time_us=PWM_PRD1)
        
    def __enter__(self): 
        return self

    def __exit__(self, eType, eValue, eTrace):
        """ Clean up routine for context manager (with-statement). 
        Takes care of closing DMA channel - failure to do this breaks OS and a reboot will be needed."""
        log.info("Destroying "+str(self))
        self.set([0, 0, 0])
        sleep(PWM_PRD/1e6) # wait a period to ensure set() has been actioned
        PWM.clear_channel(PWM_DMA)
        PWM.clear_channel(PWM_DMA1)
        PWM.cleanup()
        return False
        
    def set(self, rgb, blink=False, fast=False):
        """Set desired output RGB values. 
        rgb: RGB vector of 0/1 or False/True.
        [blink]: If the LED should blink. 
        """
        if not len(rgb) == 3:
            raise ValueError("RGB vector must have three entries (rgb="+str(rgb)+")")
        PWM.clear_channel(PWM_DMA)
        PWM.clear_channel(PWM_DMA1)
        timing_offset = 0 # cant set both low and high at the same time, using one channel
        for value, pin in zip(rgb, self._pins):
            log.debug("value=%s", str(value))
            if value in (1, True, "HIGH"):
                if blink:
                    if fast:
                        PWM.add_channel_pulse(PWM_DMA, pin, timing_offset, PWM_PRD/PWM_RES/2)
                    else:
                        PWM.add_channel_pulse(PWM_DMA1, pin, timing_offset, PWM_PRD/PWM_RES/2)
                else:
                    PWM.add_channel_pulse(PWM_DMA, pin, timing_offset, PWM_PRD/PWM_RES-1) 
            else:
                PWM.add_channel_pulse(PWM_DMA, pin, timing_offset, PWM_PRD/PWM_RES-1) 
            timing_offset = timing_offset +1

def main(argv):
    _usage = """Command line utility controlling an RGB LED for 5 seconds and exiting. 
Usage: """+__file__+""" [-h|--help] [-[r][g][b][B] {-p|--pins} <R>,<G>,<B>]

-r: Enables red.
-g: Enables green.
-b: Enables blue.
-B: Enables 0.5 Hz blinking. 
{-p|--pins} <R>,<G>,<B>: Pin numbers for the RGB LED in RPi.GPIO.BCM format. 
-h|--help: Displays this message and exits. 
"""
    # Get root logger
    rl = logging.getLogger()
    rl.setLevel(logging.DEBUG)
    # Console logging
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    #cf = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    cf = logging.Formatter('%(levelname)s - %(message)s')
    ch.setFormatter(cf)
    rl.addHandler(ch)

    log.debug("Started as: "+" ".join(argv))
    
    rgb = [0,0,0]
    blink = False
    pins = None
    period = PWM_PRD
    try:
        options, remainder = getopt.getopt(argv[1:],"hrgbBp:",["help", "pins="])
        for opt, arg in options:
            if opt in ('-h', '--help'):
                log.info(_usage)
                sys.exit(0)
            elif opt in ('-r'):
                rgb[0] = 1
            elif opt in ('-g'):
                rgb[1] = 1
            elif opt in ('-b'):
                rgb[2] = 1
            elif opt in ('-B'):
                blink = True
            elif opt in ('-Bslow'):
                blink = True
                period = 100000
            elif opt in ('-Bfast'):
                blink = True
                period = 400000
            elif opt in ('-p', "--pins"):
                pins = arg
    except getopt.GetoptError:
        log.error("Error parsing arguments.")
        log.info(_usage)
        sys.exit(2)

    with RgbLed(pins) as led:
        led.set(rgb, blink, period)
        try:
            sleep(5)
        except (KeyboardInterrupt, SystemExit):
            log.debug("Interupted from keyboard, continuing.")
    
    log.debug("Exiting, with success")
    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv)
        
