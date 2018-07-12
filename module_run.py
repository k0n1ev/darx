import os
import shutil
import streamtologger

def run(parameter):
	name = parameter.name
	prefix = os.path.dirname(os.path.realpath(__file__))+"/"
	prefix_flag = False
	if not "/" in name:
		prefix_flag=True
		name=prefix+name
	cycles = parameter.cycles
	add = parameter.add
	timer = parameter.time
	rvol = parameter.rvol
	coeff = parameter.coeff
	###optional
	speed_in = parameter.speed_in
	speed_out = parameter.speed_out
	speed_reagent = parameter.speed_reagent
	uv_time = parameter.uv_time
	mixing_time = parameter.mixing_time
	onlygenerate = parameter.onlygenerate

	### writing .py
	print ("Generated {}.py file".format(name))
	script_text="""import sys
import RPi.GPIO as gpio
import antibody
import needle
import reagent
import uv
import time

i={add}
rvol = {rvol}
for n in range({cycles}):
	print("Cycle: "+str(n+1)+"/"+str({cycles}))
	needle.move("down")
	reagent.inject("out", i, speed={sr})
	rvol = round(rvol+i,1) ##adjusting volume taking into account the add vol
	if not {mt}==0.0:
		reagent.mix({mt})
	needle.move("up")
	time.sleep({timer})
	antibody.inject("in", rvol, speed={si})
	if not {uv_time}==0.0:
		uv.uv({uv_time})
	antibody.inject("out", rvol, speed={so})
	if not {mt}==0.0:
		reagent.mix({mt})
	antibody.inject("in", rvol, speed={si})
	if not {uv_time}==0.0:
		uv.uv({uv_time})
	antibody.inject("out", rvol, speed={so})
	if not {mt}==0:
		time.sleep({mt})
	i=i*{coeff}
print ("Successfully executed")
print ("")
""".format(add=add, cycles=cycles, sr=speed_reagent, mt=mixing_time, timer=timer, rvol=rvol, si=speed_in, uv_time=uv_time, so=speed_out, coeff=coeff)
	with open(name+".py","w") as py:
		py.write(script_text)
		py.close()

	if not onlygenerate:
		### writing log
#		logname = name+".log"
#		streamtologger.redirect(target=logname,header_format="[{timestamp:%Y-%m-%d %H:%M:%S}] ")
		###starting run
		if not uv_time == 0: ##deleting old darx.uv
			old_uv="darx.uv"
			if prefix_flag:
				old_uv=prefix+old_uv
			with open (old_uv,"w") as f:
				f.write("")
				f.close

		exec(script_text) ##script execution

#copying log from darx.log to exp_name.log
		old_log="darx.log"
		if prefix_flag:
			old_log=prefix+old_log
		shutil.move(old_log,'{}.log'.format(name))
		print ("Generated {}.log file".format(name))

#copying uv from darx.uv
		if not uv_time == 0:
			shutil.move(old_uv,'{}.uv'.format(name))
			print ("Generated {}.uv file".format(name))


def prerun(parameter):
	volume=parameter.volout
	uv=parameter.volout_uv
	script_text="""import sys
import RPi.GPIO as gpio
import antibody
import reagent
import uv
if {uv}==True:
	uv.uv(2)
antibody.inject("out", {volume}, speed=1)
for n in range(2):
	reagent.mix(30)
	antibody.inject("in", {volume}, speed=0.5)
	if {uv}==True:
		uv.uv(2)
	antibody.inject("out", {volume}, speed=1)
reagent.mix(30)
print ("Successfully executed")""".format(uv=uv,volume=volume)
	exec(script_text)

def manual(parameter,a,r,n):
#	import RPi.GPIO as gpio
	mix_time=parameter.manual_mixing
	needle = parameter.manual_needle
	reac = parameter.reac
	reag = parameter.reag
	reac_speed = parameter.reac_speed
	reag_speed = parameter.reag_speed
	reac_dir = parameter.reac_dir
	reag_dir = parameter.reag_dir
	uv = parameter.manual_uv

#	print('Current positions of syringes:\nAntibody: {} steps\nReagent: {} steps\nNeedle position: {}'.format(a,r,n))
	if needle == 'up':
		if n == 'up':
			print('Needle is already in the right position (up)')
		else:
			import needle as needle_module
			needle_module.move('up')
	if needle == 'down':
		if n == 'down':
			print('Needle is already in the right position (down)')
		else:
			import needle as needle_module
			needle_module.move('down')
	try:
		int(reac)
		if reac != 0:
			if (reac_dir == 'in') or (reac_dir == 'out'):
				import antibody
				antibody.inject(reac_dir, reac, speed=reac_speed)
			else:
				print ("Error during reactor move: wrong direction indicated ({})".format(reac_dir))
	except:
		print ("Error during reactor move: wrong volume indicated ({})".format(reac))

	try:
		int(reag)
		if reag != 0:
			if (reag_dir == 'in') or (reag_dir == 'out'):
				import reagent
				reagent.prime(reag_dir, reag, speed=reag_speed)
			else:
				print ("Error during reagent move: wrong direction indicated ({})".format(reag_dir))
	except:
		print ("Error during reactor move: wrong volume indicated ({})".format(reag))

	try:
		int(mix_time)
		if mix_time >0:
			import reagent
			reagent.mix(mix_time)
	except:
		print ("Error during mixing: wrong volume indicated ({})".format(mix_time))
	if uv:
		import uv
		uv.uv(2)
	print ("Successfully executed")


def release(parameter,a,r,n):
	import RPi.GPIO as gpio
	name = parameter.name
	rvol = parameter.rvol
	speed_in = parameter.speed_in
	speed_out = parameter.speed_out
	time = parameter.time
	uv = parameter.uv

	print('Current positions of syringes:\nAntibody: {} steps\nReagent: {} steps\nNeedle position: {}'.format(a,r,n))
	if a!= "0":
		print ('Home syringes first')
		return
	prefix = os.path.dirname(os.path.realpath(__file__))+"/"
	prefix_flag = False
	if not "/" in name:
		prefix_flag=True
		name=prefix+name
	cycles = int(time//((rvol/speed_in+rvol/speed_out)/1000))
	if cycles == 0:
		print("Time is insufficient even for 1 cycle")
		return 0
	else:
		print("Starting {} cycles of release".format(cycles))
	### writing .py
	print ("Generated {}.py file".format(name))
	script_text="""import sys
import RPi.GPIO as gpio
import antibody
import uv
import time

for n in range({cycles}):
	print("Cycle: "+str(n+1)+"/"+str({cycles}))
	antibody.inject("in", {rvol}, speed={si})
	if {uv_on}:
		uv.uv(2)
	antibody.inject("out", {rvol}, speed={so})
print ("Successfully executed")
print ("")
""".format(cycles=cycles, rvol=rvol, si=speed_in, so=speed_out, uv_on=uv)
	with open(name+".py","w") as py:
		py.write(script_text)
		py.close()

	if uv: ##deleting old darx.uv
		old_uv="darx.uv"
		if prefix_flag:
			old_uv=prefix+old_uv
		with open (old_uv,"w") as f:
			f.write("")
			f.close

	exec(script_text) ##script execution

#copying log from darx.log to exp_name.log
	old_log="darx.log"
	if prefix_flag:
		old_log=prefix+old_log
	shutil.move(old_log,'{}.log'.format(name))
	print ("Generated {}.log file".format(name))

#copying uv from darx.uv
	if uv:
		shutil.move(old_uv,'{}.uv'.format(name))
		print ("Generated {}.uv file".format(name))
