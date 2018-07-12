#!/usr/bin/env python3
import os
import time
import sys

import sys
prefix = os.path.dirname(os.path.realpath(__file__))+"/"
def waiting():
	waiting = True
	while waiting:
		try:
			with open("{}rvol.log".format(prefix),"r") as log:
				l = log.read()
				log.close()
				return(l)
			waiting = False
		except:
			time.sleep(0.5)
			pass

def volume(parameters):
	speed=parameters.rvol_speed
	os.system("rm {}rvol.log&>/dev/null".format(prefix))
	print ("Starting measuring reactor volume")
	command = "python {}volume.py {}".format(prefix,speed)
	os.system("lxterminal -t 'DarX: Reactor volume' -e {}".format(command))
	sys.stdout=sys.__stdout__
	print (waiting())
	print ("Successfully executed\n")
