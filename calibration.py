import uv
import sys
import os

prefix = os.path.dirname(os.path.realpath(__file__))+"/"

arg=sys.argv
#sys.stdout=sys.__stdout__

if len(arg) == 1:
	conc=["9.1140","4.638","3.762","2.844","1.95","0.963","0"]
else:
	conc=arg[1:]
startmes = "Start calibration with following concentration set: "

i=1
for c in conc:
	startmes+="\n{}: {} mg/ml".format(i,c)
	i+=1
startmes+="\nPress 'Enter' when the sample is inserted"
print (startmes)
for i in range(len(conc)):
	input()
	print("Concentration {} mg/ml:".format(conc[i]))
	uv.uv(2)
os.system("mv {0}calibration.log {0}calibration_last.log".format(prefix))
