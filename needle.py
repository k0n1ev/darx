import logger
import RPi.GPIO as gpio #https://pypi.python.org/pypi/RPi.GPIO more info
import time
import config

PIN_STEP = 14
PIN_DIR = 15

def move(direction):
	if not (direction == 'up' or direction == 'down'):
		print("ATTENTION: wrong parameter for needle movement (only 'up' and 'down' are allowed; your input: "+direction)
		input()
	WaitTime = 0.0005
	steps = 200*30 #1mm = 200 steps; 40 mm overall
	current_position = config.readvalue('needle')
	if direction == current_position:
		inp = ""
		while not (inp == "OK"):
			print ("ATTENTION: needle seems to be already in {} position (Ctrl+C to stop execution)".format (direction))
			inp = input()
	print("Needle move ({})".format(direction.capitalize()))
	gpio.setmode(gpio.BCM)
	gpio.setup(PIN_STEP, gpio.OUT) #steps
	gpio.setup(PIN_DIR, gpio.OUT) #direction
	config.writevalue('needle',direction)
	if direction == 'down':
		gpio.output(PIN_DIR, False)
	elif direction == 'up':
		gpio.output(PIN_DIR, True)

	StepCounter = 0
	while StepCounter < steps:
		gpio.output(PIN_STEP, True)
		gpio.output(PIN_STEP, False)
		StepCounter += 1
		time.sleep(WaitTime)
	gpio.cleanup()

def home():
	current_position = config.readvalue('needle')
	if current_position == 'down':
		print("Started homing needle")
		move('up')
	else:
		print("Needle is already in the right position (Up)")
