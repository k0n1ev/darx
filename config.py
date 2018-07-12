#!/usr/bin/env python3
import os
import sys
import socket

prefix = os.path.dirname(os.path.realpath(__file__))
ini_name = prefix+"/config_"+socket.gethostname()+".ini"

def writevalue (name, value):
	with open(ini_name,"r") as ini:
		raw_ini = ini.readlines()
		ini.close()
	for i in range (len(raw_ini)):
		if name in raw_ini[i]:
			raw_ini[i] = "{}={}\n".format(name,value)
	with open(ini_name, 'w') as ini:
		ini.writelines(raw_ini)
		ini.close()
def readvalue (name):
	with open(ini_name,"r") as ini:
		raw_ini = ini.readlines()
		ini.close()
	for element in raw_ini:
		if name in element:
			return (element.strip().split("=")[1])
