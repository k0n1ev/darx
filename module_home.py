#!/usr/bin/env python3
#from multiprocessing import Process
#import os
#import sys
import antibody #direction in or out and volume to provide
import reagent #same as inject module but for reagent addition
import needle

#sys.stdout=sys.__stdout__ #restore stdout to _no log after imports
#prefix = os.path.dirname(os.path.realpath(__file__))+"/"

def positions(a,r,n):
#	os.system("rm {}darx.log&>/dev/null".format(prefix))
	print('Current positions of syringes:\nAntibody: {} steps\nReagent: {} steps\nNeedle position: {}'.format(a,r,n))
def home(conf):
	antibody.home()
	reagent.home()
	needle.home()
#	Process(target=antibody.home).start()
#	Process(target=reagent.home).start()
#	Process(target=needle.home).start()
#	sys.stdout=old_stdout

