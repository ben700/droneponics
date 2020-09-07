#!/usr/bin/python

import os, time, sys
sys.path.append('/home/pi/droneponics')
import drone

if __name__ == "__main__":
	addr = 0x20
	if len(sys.argv) == 2:
		if sys.argv[1].startswith("0x"):
			addr = int(sys.argv[1], 16)
		else:
			addr = int(sys.argv[1])
	chirp = drone.Chirp(1, addr)

	print (chirp)
	print ("Moisture\tTemperature\tBrightness")
	while True:
		print ("%d\t%d\t%d" % (chirp.moist(), chirp.temp(), chirp.light()))
		time.sleep(1)
