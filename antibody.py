#!/usr/local/bin/python3
# coding: utf-8

import logger
import RPi.GPIO as gpio #https://pypi.python.org/pypi/RPi.GPIO more info
import time
import config
import Adafruit_DHT

PIN_TEMPERATURE = 4
sensor = Adafruit_DHT.DHT11

PIN_STEP = 16
PIN_DIR = 12

#gpio.setwarnings(False)

def inject (direction, volume, **params):
	WaitTime = 0.0055 #wait between steps to make 1mL/min spead
	if "speed" in params:
		coeff = float(params['speed']) #speed in mL/min
		WaitTime = WaitTime/coeff
	sul10 = 10.71/0.976698/1.038 #number of steps in 1 uL
	steps = int(float(volume)*sul10)
	print("Starting {} ({}ul, {} steps)".format(direction, volume, steps))

	gpio.setmode(gpio.BCM)
	gpio.setup(PIN_STEP, gpio.OUT)
	gpio.setup(PIN_DIR, gpio.OUT)

	if direction == 'out':
		homeinc = -1 #increment coefficient to modify home positions
		gpio.output(PIN_DIR, True)
	elif direction == 'in':
		homeinc = 1
		gpio.output(PIN_DIR, False)
	else:
		print("Attention: wrong direction")
	StepCounter = 0
	while StepCounter < steps:
		gpio.output(PIN_STEP, True)
		gpio.output(PIN_STEP, False)
		StepCounter += 1
		bufferSteps = StepCounter
		time.sleep(WaitTime)
	gpio.cleanup()

	#temp() ##measuring temperature in the end of a cycle

	lastvalue = int(config.readvalue('antibody'))
	newvalue = lastvalue + homeinc*StepCounter
	config.writevalue('antibody',str(newvalue))

def home(**params):
	WaitTime = 0.0055/5 #wait between steps to make 5mL/min spead
	if "speed" in params:
		coeff = float(params['speed']) #speed in mL/min
		WaitTime = WaitTime/coeff
	steps = int(config.readvalue('antibody'))

	print("Started homing antibody syringe ({} steps)".format(steps))
	config.writevalue('antibody','0')
	gpio.setmode(gpio.BCM)
	gpio.setup(PIN_STEP, gpio.OUT)
	gpio.setup(PIN_DIR, gpio.OUT)
	gpio.output(PIN_DIR, True) #always out syringe press
	StepCounter = 0
	if steps<=0:
		steps*=-1 #if negative, do in
		gpio.output(PIN_DIR, False)
	else:
		gpio.output(PIN_DIR, True)
	while StepCounter < steps:
		gpio.output(PIN_STEP, True)
		gpio.output(PIN_STEP, False)
		StepCounter += 1
		bufferSteps = StepCounter
		time.sleep(WaitTime)
	gpio.cleanup()
#	print("Ended homing antibody syringe")

def temp():
        humidity,temperature=Adafruit_DHT.read_retry(sensor, PIN_TEMPERATURE)
        if humidity is not None and temperature is not None:
                print('Temperature: {0:0.1f}°C.  Humidity: {1:0.1f}%'.format(temperature, humidity))
        else:
                pass
