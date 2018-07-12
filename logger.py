#!/usr/local/bin/python3
# coding: utf-8
import sys
import os
import streamtologger

prefix = os.path.dirname(os.path.realpath(__file__))+"/"
logname = sys.argv[0].split('.')[0]+".log"
if not "/" in logname:
	logname=prefix+logname
	
streamtologger.redirect(target=logname,header_format="[{timestamp:%Y-%m-%d %H:%M:%S}] ")