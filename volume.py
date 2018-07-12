import rvol #initial volume measurement
import sys

try:
	speed=float(sys.argv[1])
except:
	speed=0.5

rvol.rvol("in", speed)
