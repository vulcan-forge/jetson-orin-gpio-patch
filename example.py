#!/usr/bin/python3
# Expected result: 3.3 volts using a volt meter on pin 7 
import Jetson.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.output(7, True)
# GPIO.output(7, False)
