import logger
import RPi.GPIO as gpio #https://pypi.python.org/pypi/RPi.GPIO more info
import time
import config

PIN_DIR = 23
PIN_STEP = 24

PIN_MIX = 21

#gpio.setwarnings(False)
post_inj_mix = 0.3

def inject (direction, volume, **params):
	WaitTime = 0.00324 #wait between steps to make 100uL/min speed
	if "speed" in params:
		coeff = float(params['speed']) #speed in 0.1mL/min
		WaitTime = WaitTime/coeff
	sul10 = 182.14/1.495*0.985 #number of steps in 1 uL
	steps = int(float(volume)*sul10)

	print("Mixing started")
	print("Starting reagent {} injection ({}uL, {} steps)".format(direction,round(volume,1),steps))

	gpio.setmode(gpio.BCM)
	gpio.setup(PIN_DIR, gpio.OUT)
	gpio.setup(PIN_STEP, gpio.OUT)

	##routine of mixing + stopping all other motors
	gpio.setup(14,gpio.OUT)
	gpio.output(14, False)
	gpio.setup(16,gpio.OUT)
	gpio.output(16, False)
	#strating agitation
	gpio.setup(PIN_MIX, gpio.OUT)

	if direction == 'out':
		gpio.output(PIN_DIR, True)
		homeinc = -1
	elif direction == 'in':
		homeinc = 1
		gpio.output(PIN_DIR, False)
	StepCounter = 0
	while StepCounter < steps:
		gpio.output(PIN_STEP, True)
		gpio.output(PIN_STEP, False)
		StepCounter += 1
		time.sleep(WaitTime)
	lastvalue = int(config.readvalue('reagent')) #reading last position in steps
	newvalue = lastvalue + homeinc*StepCounter
	config.writevalue('reagent',str(newvalue))

	time.sleep(post_inj_mix)
	print("Mixing ended")
	gpio.cleanup()

def prime (direction, volume, **params): #same as inject, but without stirring
	WaitTime = 0.0055 #wait between steps to make 1mL/min spead
	if "speed" in params:
		coeff = float(params['speed']) #speed in mL/min
		WaitTime = WaitTime/coeff
	sul10 = 182.14/1.495*0.985 #number of steps in 1 uL
	steps = int(float(volume)*sul10)
	gpio.setmode(gpio.BCM)
	gpio.setup(PIN_DIR, gpio.OUT)
	gpio.setup(PIN_STEP, gpio.OUT)

	if direction == 'out':
		gpio.output(PIN_DIR, True)
		homeinc = -1
	elif direction == 'in':
		gpio.output(PIN_DIR, False)
		homeinc = 1
	StepCounter = 0
	print("Starting reagent {} prime ({}uL, {} steps)".format(direction,int(volume),steps))
	while StepCounter < steps:
		gpio.output(PIN_STEP, True)
		gpio.output(PIN_STEP, False)
		StepCounter += 1
		time.sleep(WaitTime)
	lastvalue = int(config.readvalue('reagent')) #reading last position in steps
	newvalue = lastvalue + homeinc*StepCounter
	config.writevalue('reagent',str(newvalue))
	gpio.cleanup()

def mix (timemix):
	time.sleep(0.5) #delay after reagent addition
	print("Mixing started ({} sec)".format(timemix))
	gpio.setmode(gpio.BCM)
	gpio.setup(14,gpio.OUT)
	gpio.output(14, False)
	gpio.setup(16,gpio.OUT)
	gpio.output(16, False)
	gpio.setup(24,gpio.OUT)
	gpio.output(24, False)
#strating agitation
	gpio.setup(PIN_MIX, gpio.OUT)
	time.sleep(timemix)
	gpio.cleanup()
	print("Mixing ended")

def home(**params):
	WaitTime = 0.00324/5 #wait between steps to make 5mL/min speed
	if "speed" in params:
		coeff = float(params['speed']) #speed in mL/min
		WaitTime = WaitTime/coeff
	steps = int(config.readvalue('reagent'))
	print("Started homing reagent syringe ({} steps)".format(steps))
	config.writevalue('reagent','0')
	gpio.setmode(gpio.BCM)
	gpio.setup(PIN_DIR, gpio.OUT)
	gpio.setup(PIN_STEP, gpio.OUT)
	if steps >= 0:
		gpio.output(PIN_DIR, True) ##in direction
	else:
		steps = steps * (-1)
		gpio.output(PIN_DIR, False) ##out direction
	StepCounter = 0
	while StepCounter < steps:
		gpio.output(PIN_STEP, True)
		gpio.output(PIN_STEP, False)
		StepCounter += 1
		bufferSteps = StepCounter
		time.sleep(WaitTime)
#	print("Ended homing reagent syringe")
	gpio.cleanup()
