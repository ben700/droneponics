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


class AtlasTemp:
   def __init__(self):
      self.rawOutput = None
      # setting
      pimodel        = getrpimodel.model
      pimodel_strict = getrpimodel.model_strict()

      if os.path.exists('/dev/serial0'):
         partial_serial_dev = 'serial0'
      elif pimodel == "3 Model B" or pimodel_strict == "Zero W":
         partial_serial_dev = 'ttyS0'
      else:
         partial_serial_dev = 'ttyAMA0'

      self.serial_dev = '/dev/%s' % partial_serial_dev
      self.ser = serial.Serial(
           port=self.serial_dev, #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
           baudrate = 38400
      )
      #set the default units on probe 
      self.ser.write(str.encode("D0"+'\r'))
      self.ser.write(str.encode("SC"+'\r'))

    
   def __del__(self):
      self.ser.close()

   def getTemp(self):
         self.ser.write(str.encode("R"+'\r'))
         self.rawOutput = self.ser.read(5)
         o = self.rawOutput.decode()
         
         try :  
             float(o) 
             print("is float = " + str(o))
         except : 
             self.getTemp()
             print("Not a float") 
             
         return o

      
atlasTemp = AtlasTemp()
while True:
   print("Temprature is " + atlasTemp.getTemp())
