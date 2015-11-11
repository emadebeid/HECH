#!/usr/bin/python

import sys, string, logging
from time import sleep

import requests
import RgbLed
import httplib as http
import re
import getopt
import json

log = logging.getLogger(__file__.strip("./").split('.')[0].split('/')[-1])
log.info("Created logger: "+str(log))
log.setLevel(logging.DEBUG)

# Valid indicator values
HIGH = "high" # Price is high
LOW = "low" # Price is low
GREEN = "green" # Green Color
RED = "red" # Red Color
NONE = "none" # Price is unspecified, server is reachable
NA = "na" # Price is not available, server cannot be reached. 
UNKNOWN = None # Initialisation value, server connection has not been attempted
GSLOW = "gslow" # green slow blinking
GFAST = "gfast" # green fast blinking
RSLOW = "rslow" # red slow blinking
RFAST = "rfast" # red fast blinking
IND_GOOD = {HIGH, LOW, NONE, GSLOW, GFAST, RSLOW, RFAST, RED, GREEN}
IND_ALL = IND_GOOD.union({NA, UNKNOWN})
    
class RPiLED(object):
    """Polls an URL for DAPP price indicator and sets a RGB LED accordingly.

Author: Egon Kidmose"""

    def __init__(self, led, url):
        """Initialises an instance off the class
        url: HTTP address to obtain price indicator from. 
        led: RGB LED used to express price policy. """

        if not isinstance(url, str):
            raise ValueError("Expected %s, passed %s" % (str.__name__, url.__class__.__name__))
        self._url = url

        if not isinstance(led, RgbLed.RgbLed):
            raise ValueError("Expected %s, passed %s" % (RgbLed.RgbLed.__name__, led.__class__.__name__))
        self._led = led

        self.set_led(UNKNOWN)

    def get_indicator(self):
        """Retrieves price indicator via HTTP"""
        log.debug("get_indicator() called")
        r = requests.get(self._url)
        if r.status_code is not http.OK:
            log.error("Unable to get indicator from %s, HTTP status code: %i", self._url, r.status_code)
        ind = re.sub(re.compile('\W+'), '', r.text.lower()) # lowercase, remove anything but alphanumeric
        log.debug("Canonicalised indicator: %s", ind)
        if ind in IND_GOOD:
            return ind
        else:
            log.error("Price indicator not recognised: %s", r.text)
            return NA

    def set_led(self, indicator):
        """Sets the RGB LED according to an indicator value"""
        if indicator == HIGH or indicator == RED:
            log.info("High indicator, red.")
            self._led.set([1, 0, 0])
<<<<<<< HEAD
        elif indicator == LOW or Green:
=======
        elif indicator == LOW or indicator == GREEN:
>>>>>>> origin/develop
            log.info("Low indicator, green.")
            self._led.set([0, 1, 0]) 
        elif indicator == NONE:
            log.info("\"none\" indicator, blink green.")
            self._led.set([0, 1, 0], True) 
        elif indicator == NA:
            log.error("Indicator not available, blue.")
            self._led.set([0, 0, 1])
        elif indicator == UNKNOWN:
            log.info("Indicator is not yet known, blink blue")
            self._led.set([0, 0, 1], True)
        elif indicator == GSLOW:
            self._led.set([0, 1, 0], True, False)
        elif indicator == GFAST:
            self._led.set([0, 1, 0], True, True )
        elif indicator == RSLOW:
            self._led.set([1, 0, 0], True, False)
        elif indicator == RFAST:
            self._led.set([1, 0, 0], True, True )
        else:
            log.error("Unimplemented indicator: %s, blinking red,", indicator)
            self._led.set([1, 0, 0], True)

            
def main(argv):
    _usage = """Commandline script polling a DAPP service for a price indicator and setting a RGB LED according to the indicator. 
Usage: """+__file__+""" {-T|--period} <minutes> {-u|--url} <dapp-address> {-p|--pins} <R>,<G>,<B>

{-T|--period} <minutes>: Polling period in minutes. 
{-u|--url} <dapp-address>: URL of the DAPP to poll. 
{-p|--pins} <R>,<G>,<B>: Pin numbers for the RGB LED in RPi.GPIO.BCM format. 
-h|--help: Displays this message and exits."""

    # Get root logger
    rl = logging.getLogger()
    rl.setLevel(logging.DEBUG)
    # Console logging
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    #cf = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    cf = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(cf)
    rl.addHandler(ch)

    log.debug("Started as: "+" ".join(argv))

    url = None
    period = None
    pins = None

    try:
        options, remainder = getopt.getopt(argv[1:],"T:u:p:h",["help", "period=", "url=", "pins="])
        for opt, arg in options:
            if opt in ('-h', '--help'):
                log.info(_usage)
                sys.exit(0)
            elif opt in ('-T', "--period"):
                period = int(arg)
            elif opt in ('-p', "--pins"):
                pins = arg
            elif opt in ('-u', "--url"):
                url = arg
    except getopt.GetoptError as e:
        log.error("Error parsing arguments: %s", str(e))
        log.info(_usage)
        sys.exit(2)
    if url is None or period is None or pins is None:
        log.error("Missing one or more arguments, they are all mandatory.")
        log.info(_usage)
        sys.exit(2)

    # Dummy http request. 
    # Has to be made before importing RgbLed (RPIO.PWM?) or maybe before using/initialising. 
    # otherwise script fails silently and exits on first requests.get(...)
    try:
        requests.get("http://127.0.0.1")
    except:
        None

    with RgbLed.RgbLed(pins) as led: 
        try: 
            led = RPiLED(led, url)
            log.info("Going into polling loop")
            while True:
                ind = led.get_indicator()
                led.set_led(ind)
                
                log.info("Sleeping for %i minutes", period)
                sleep(period*60)
        except (KeyboardInterrupt, SystemExit):
            log.info("Caught signal, exiting.")
            
    log.debug("Exiting, with success")
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)
