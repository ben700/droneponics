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
        baudrate = 38400,
#        parity=serial.PARITY_NONE,
#        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
ser.write(str.encode("DO"+'\r'))
ser.write(str.encode("SC"+'\r'))

print("connected to: " + ser.portstr)
count=1

while True:
  try:
    ser.write(str.encode("R" + '\r'))
    output = ser.readline().decode('utf-8')
    print("----------------------------------START--------------------------------------------------------")
    print(output)
    print(isinstance(output, numbers.Real))
    print(isinstance(output,Float))
    print("----------------------------------END--------------------------------------------------------")
    if (output is not None):
      print('Temprature : ' + output)
      print("NO CR --------------")
  except:
    pass
ser.close()
