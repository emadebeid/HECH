README LED Poller
==================
This folder contains a prototype implementation which enables the HECH to retrieve price indicators through a RESTfull interface and express the current price through a RGB LED.

The prototype is built and tested on Raspberry Pi model B+ (40 GPIO pins) running 2014-09-09-wheezy-raspbian. It is expected to be compatible with other Raspberry Pi models. 

The actual LED is outside the scope of this module. It is assumed that a LED is available on the Internet and follows the interface described below. 

Folder contents
========
* README.md: This file. Provides an overview and setup instructions.
* requirements.txt: Requirements formatted for easy installation with PIP. 
* RPiLED
* .py: CLI. The central part of the prototype. Polls for a price policy and uses a RGB LED.
* RgbLed.py: Module encapsulating RGB LED/low level hardware. Also a CLI.
* RgbLed.config: Default pin configuration used by RgbLed.py.

RESTfull Interface
==================
In the current implementation the following assumptions have been made about the interface:

* The HECH is a RESTfull client.
* The LED is a RESTfull server.
* The price indicators are: `low`, `high` and `none`. 

LED Colour codes
================
* Red, constant: Price is `high`.
* Green, constant: Price is `low`.
* Blue, constant: Price is not available. **fault**
* Red, blinking: Invalid price indicator retrieved. **fault**
* Green, blinking: No price(`none`) was specified. 
* Blue, blinking: Price is not yet known. 

Setup
=====
It is assumed that:

* a LED
*  is available on the Internet. 
* the HECH is running 2014-09-09-wheezy-raspbian on Raspberry Pi B+.
* the HECH can connect to the Internet. 

The setup process consist of the following steps:

1. Install dependencies:

		pi@raspberrypi ~ $ sudo apt-get install git python python-pip python-dev

2. Obtain source:

		pi@raspberrypi ~ $ git clone https://bitbucket.org/smarthg/hech.git

3. Install python requirements: 

		pi@raspberrypi ~ $ cd hech/RPiLED/
		pi@raspberrypi ~/hech/RPiLED $ sudo pip install -r requirements.txt

4. Add a crontab entry on reboot for root (root in order to access hardware):

		pi@raspberrypi ~/hech/RPiLED $ sudo crontab -e

	Add a line like the following, make sure there is an empty line at the very bottom, save and exit:

		@reboot /home/pi/hech/RPiLED/RPiLED.py --period <minutes> --url <LED-url> --pins <R>,<G>,<B>

	Example:
	
		@reboot /home/pi/hech/RPiLED/RPiLED.py --period 5 --url http://radagast4.netlab.eng.au.dk/led/ --pins 20,21,26

	For logging use:

		@reboot /home/pi/RPiLED/RPiLED.py --period <minutes> --url <led-url> --pins <R>,<G>,<B> > /home/pi/LEDPoller.log 2>&1
		
6. Restart and verify:

		sudo reboot

