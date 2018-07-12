import os
import time
import sys

prefix = os.path.dirname(os.path.realpath(__file__))+"/"

def waiting():
        waiting = True
        while waiting:
                try:
                        with open(prefix+"calibration_last.log","r") as log:
                                l = log.read()
                                log.close()
                                return(l)
                        waiting = False
                except:
                        time.sleep(0.5)
                        pass

def cal(conc):
	sys.stdout=sys.__stdout__
	os.system("rm {}calibration_last.log&>/dev/null".format(prefix))
	print ("Starting UV calibration\n")
	command="python3 {}calibration.py".format(prefix)
	conc_all=[]
	for i in range(6): #number of concentrations
		try:
			value = float(eval("conc.conc_{}".format(i+1)))
			conc_all.append(value)
		except:
			pass
	if not (len(conc_all))==0:
		for k in range(len(conc_all)):
			value = conc_all[k]
			if value>=0:
				command+=" {}".format(value)
	else:
		print("No concentrations provided, running on standard ones")
	os.system("lxterminal -t 'DarX: UV calibration' -e {}".format(command))
	print(waiting())
	print ("Successfully executed\n")
