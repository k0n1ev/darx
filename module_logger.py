import streamtologger
import os

def logger(parameter):
#	prefix = os.path.dirname(os.path.realpath(__file__))+"/"
	name = parameter.name
#	if not "/" in name:
#		name=prefix+name
	logname = name+".log"
	streamtologger.redirect(target=logname,header_format="[{timestamp:%Y-%m-%d %H:%M:%S}] ")
