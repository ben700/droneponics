import time
import serial
import subprocess
import traceback
import getrpimodel
import struct
import platform
import argparse
import sys
import json
import os.path

# setting
pimodel        = getrpimodel.model
pimodel_strict = getrpimodel.model_strict()

if os.path.exists('/dev/serial0'):
  partial_serial_dev = 'serial0'
elif pimodel == "3 Model B" or pimodel_strict == "Zero W":
  partial_serial_dev = 'ttyS0'
else:
  partial_serial_dev = 'ttyAMA0'

serial_dev = '/dev/%s' % partial_serial_dev

print("serial_dev = " + serial_dev)

ser = serial.Serial(
        port=serial_dev, #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 38400
)
ser.write(str.encode("D0"+'\r'))
ser.write(str.encode("SC"+'\r'))

print("connected to: " + ser.portstr)

ser.write(str.encode("R"+'\r'))
output = ser.read(5)
print("Temprature :" + output.decode())

ser.close()
