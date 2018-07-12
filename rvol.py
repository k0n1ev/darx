#!/usr/bin/env python3
import sys
import RPi.GPIO as gpio
import time
import datetime
import curses
import config
import os

PIN_DIR = 12
PIN_STEP = 16

startmessage = "[{}] Reactor volume measurement started".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

dir = "in"
speed = 1

prefix = os.path.dirname(os.path.realpath(__file__))+"/"

def main(win):
	global dir
	global speed
	WaitTime = 0.0055/speed #wait between steps to make 1mL/min spead
	sul10 = 10.71/0.976698/1.038 #number of steps in 1 uL
	maxsteps = 12000*sul10 ##max volume of 15 mL
	gpio.setmode(gpio.BCM)
	gpio.setup(PIN_DIR, gpio.OUT)
	gpio.setup(PIN_STEP, gpio.OUT)
	if dir == "in" or dir == "IN":
		gpio.output(PIN_DIR, False)
		homeinc = 1 #for config (direction of steps)
	elif dir == "out" or dir == "OUT":
		gpio.output(PIN_DIR, True)
		homeinc = -1
	else:
		print("Wrong direction provided (should be IN or OUT). Starting IN direction.")
		dir = "IN"
		gpio.output(PIN_DIR, False)
		homeinc = 1
	win.nodelay(True)
	key=""
	win.clear()
	outmessage = "Measuring reactor volume (press C to measure or E to stop). Direction: {}.\n".format(dir)
	win.addstr(outmessage)
	StepCounter = 0
	while StepCounter < maxsteps:
		try:
			key = win.getkey()
			win.clear()
			win.addstr(outmessage)
			if key == "c" or key == "C":
				win.clear()
				outmessage += "[{}] Current volume: {}uL\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(int(StepCounter/sul10)))
				win.addstr(outmessage)
			if key == "e" or key == "E":
				outmessage += "[{}] Final volume: {}uL".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(int(StepCounter/sul10)))
				break
		except Exception as e:
				pass
		gpio.output(PIN_STEP, True)
		gpio.output(PIN_STEP, False)
		StepCounter += 1
		time.sleep(WaitTime)
	gpio.cleanup()
	lastvalue = int(config.readvalue('antibody')) #reading last position in steps
	newvalue = lastvalue + homeinc*StepCounter
	config.writevalue('antibody',str(newvalue))
	return outmessage

def rvol(direction, sp):
	global dir
	global speed
	dir = direction
	speed = sp
	finalmessage = curses.wrapper(main)
	print (startmessage)
	print (finalmessage)
	with open("{}rvol.log".format(prefix),"w") as log:
		log.write(finalmessage)
		log.close()
