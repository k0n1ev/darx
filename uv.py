import logger
import RPi.GPIO as gpio #https://pypi.python.org/pypi/RPi.GPIO more info
import time
import config
import Adafruit_ADS1x15
import sys

import Adafruit_DHT

PIN_relay = 20
PIN_TEMPERATURE = 4
sensor = Adafruit_DHT.DHT22
gpio.setwarnings(False)

bsa_coeff=2.2 #from bsa to mAb

def concentration (x): ##formula for concetration from AU
	conc_bsa=74.892*x**(-0.554)*bsa_coeff
	return round(conc_bsa/bsa_coeff,2)
def uv (timedelay):
	temp() #measuring temperature
	adc = Adafruit_ADS1x15.ADS1115()
	# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
	GAIN = 1

	gpio.setmode(gpio.BCM)
	#turning off all syringe pumps
	gpio.setup(14,gpio.OUT)
	gpio.output(14, False)
	gpio.setup(16,gpio.OUT)
	gpio.output(16, False)
	gpio.setup(24,gpio.OUT)
	gpio.output(24, False)
	gpio.setup(PIN_relay, gpio.OUT)

	print ("Starting UV detector ({} sec)".format(timedelay))

	#starting ADC
	time.sleep(timedelay)
	adc.start_adc(0, gain=GAIN)
	#averaging by multiple measurements
	sum_value = 0
	measurements = 5
	for i in range (measurements):
		time.sleep(0.2)
		value = adc.get_last_result()
		sum_value += value
	avg_value = sum_value/measurements
	if avg_value <= 0:
		avg_value = 1 #in case of false reading
	try:
		conc = concentration(avg_value) ##*.74/1.5 is a conversion from BSA calibration to mAb
	except:
		conc = 0

#	writing to UV log (only AU)

	logname = sys.argv[0].split('.')[0]+".uv"
	with open (logname,"a") as logfile:
		logfile.write("{}\n".format(int(avg_value)))
	with open (logname,"r") as logfile:
		first_value= float(logfile.readline().split("\n")[0])
	first_conc = concentration(first_value) #remember the first concentration
	conversion = round((first_conc-conc)/first_conc*100,1)
	if avg_value > 32760:
		avg_value = 32760
		print ("Measured: < 0.2 mg/mL ({} AU)".format(int(avg_value)))
	else:
		print ("Measured: {} mg/mL ({} AU, {}%, BSA: {})".format(conc, int(avg_value),conversion,round(conc*bsa_coeff,2)))
	adc.stop_adc()
	gpio.cleanup()

def temp():
	humidity,temperature=Adafruit_DHT.read_retry(sensor, PIN_TEMPERATURE)
	if humidity is not None and temperature is not None:
		print('Temperature: {0:0.1f}°C.  Humidity: {1:0.1f}%'.format(temperature, humidity))
	else:
		pass

