## Push buttons configuration. ##

**Objective**

Connecting two switches to the Raspberry Pi so that when the switch is pressed, some Python code is run and post the color to a web server.

**Solution**

Connect the switches to a GPIO pin and use the RPi.GPIO library in your Python program to detect the button press.

In our Pi, right switch is connected with GPIO 23 and left switch is connected with GPIO 22.

![](./media/image1.png)

Open an editor (nano or IDLE) and paste in the following code. As with all the program examples in this book, you can also download the program from the Code section of the [*Raspberry Pi Cookbook* website](http://www.raspberrypicookbook.com/), where it is called *switch.py*.

This example code displays a message when the button is pressed and turn on Red if the right button is pressed and turn on green if the left button is pressed. Moreover, it stores the LED color in a RPi web server **http://10.24.15.144/LED\_Color.txt**:

	import RPi.GPIO as GPIO
	import time
	
	GPIO.setmode(GPIO.BCM)
	
	GPIO.setup(20, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
	
	GPIO.setup(21, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
	
	GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	
	GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	
	while True:
	    input_state_R = GPIO.input(23)
	    input_state_L = GPIO.input(22)    
	    if input_state_R == True:
	        print('Right Button Pressed')
	        file = open("/var/www/LED_Color.txt", 'w+')
		file.truncate()
		file.write("red")
		file.close()
		GPIO.output(20,1)       
	    if input_state_L == True:   
	        print('Left Button Pressed')
		file = open("/var/www/LED_Color.txt", 'w+')
		file.truncate()
		file.write("green")
		file.close()
		GPIO.output(21,1)
	    time.sleep(0.2)
	    GPIO.output(20,0)
	    GPIO.output(21,0)
	GPIO.cleanup() 


You will need to run the program as superuser:

> pi@raspberrypi ~ $ sudo python push.py
>
> Right Button Pressed
>
> Left Button Pressed

**Discussion**

You will notice that the switch is wired so that when it is pressed, it will connect pin 22 configured as an input to VDD (3V, Pin 17). The input pin is normally pulled down to GND by the optional argumentpull\_up\_down=GPIO.PUD\_DOWN in GPIO.setup. This means that when you read the input value using GPIO.input, True will be returned if the button is pressed. This is a little counterintuitive.

Each GPIO pin has software configurable pull-up and pull-down resistors. When using a GPIO pin as an input, you can configure these resistors so that one or either or neither of the resistors is enabled, using the optional pull\_up\_down parameter to GPIO.setup. If this parameter is omitted, then neither resistor will be enabled. This leaves the input *floating*, which means that its value cannot be relied upon and it will drift between high and low depending on what it picks up in the way of electrical noise.

If it is set to GPIO.PUD\_UP, the pull-up resistor is enabled; if it is set to GPIO.PUD\_DOWN, the pull-down resistor is enabled.
