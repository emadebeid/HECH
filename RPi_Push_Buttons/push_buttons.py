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
