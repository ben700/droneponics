#!/usr/bin/python3
import sys
import os
sys.path.append('/home/pi/droneponics')
from AtlasI2C import (AtlasI2C)
import drone
import logging

from tkinter import * 			# imports the Tkinter lib


    # tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(logging.DEBUG)


root = Tk()				# create the root object
root.wm_title("GUI")			# sets title of the window
root.configure(bg="#99B898")		# change the background color 
root.attributes("-fullscreen", True) 	# set to fullscreen

sensors = []
sensors = drone.buildAllSensors(sensors, _log)
_log.info("All Monitor Sensors created")


def tempCalClicked():	
    label_1["text"]="Temp Calibration"
    probe = AtlasI2C(102)
    label_info["text"]= probe.query("i").strip().rstrip('\x00')
    label_cal["text"]= probe.query("cal,?").strip().rstrip('\x00')
    label_status["text"]= probe.query("Status").strip().rstrip('\x00')
    readProbeButton["text"]= "Read Temp"
    readProbeButton["command"]= readTempClicked
    calProbeButton["text"]= "Cal Temp"
    calProbeButton["command"]= calTempClicked
    clearReading()
	
def phCalClicked():
    label_1["text"]="pH Calibration"
    probe = AtlasI2C(99)
    label_info["text"]= probe.query("i").strip().rstrip('\x00')	
    label_cal["text"]= probe.query("cal,?").strip().rstrip('\x00')
    label_status["text"]= probe.query("Status").strip().rstrip('\x00')
    readProbeButton["text"]= "Read pH"
    readProbeButton["command"]= readPHClicked
    calProbeButton["text"]= "Cal PH"
    calProbeButton["command"]= calPHClicked
    clearReading()


def ecCalClicked():
    label_1["text"]="EC Calibration"
    probe = AtlasI2C(100)
    label_info["text"]= probe.query("i").strip().rstrip('\x00')	
    label_cal["text"]= probe.query("cal,?").strip().rstrip('\x00')
    label_status["text"]= probe.query("Status").strip().rstrip('\x00')
    readProbeButton["text"]= "Read EC"
    readProbeButton["command"]= readECClicked
    calProbeButton["text"]= "Cal EC"
    calProbeButton["command"]= calECClicked
    clearReading()

def readTempClicked():	
    probe = AtlasI2C(102)
    probeRead_label["text"]= probe.query("R").strip().rstrip('\x00')

def readPHClicked():	
    probe = AtlasI2C(99)
    probeRead_label["text"]= probe.query("R").strip().rstrip('\x00')

def readECClicked():	
    probe = AtlasI2C(100)
    rawReading = probe.query("R").strip().rstrip('\x00')
    v1 = rawReading.split(":")[1].split(",")[0].strip().rstrip('\x00')
    v2 = rawReading.split(":")[1].split(",")[1].strip().rstrip('\x00')
    v3 = rawReading.split(":")[1].split(",")[2].strip().rstrip('\x00')
    v4 = rawReading.split(":")[1].split(",")[3].strip().rstrip('\x00')	
    probeRead_label["text"]= "V1 = " + str(v1) + '\n' + "V2 = " + str(v2)+ '\n' + "V3 = " + str(v3)+ '\n' + "V4 = " + str(v4)

def clearReading():	
    probeRead_label["text"]= ""

	
def calTempClicked():	
    probeRead_label["text"]= "calTempClicked"
def calPHClicked():	
    probeRead_label["text"]= "calPHClicked"
def calECClicked():	
    probeRead_label["text"]= "calECClicked"

def btnExit():
  	root.destroy()

# we can exit when we press the escape key
def end_fullscreen(event):
	root.attributes("-fullscreen", False)


label_1 = Label(root, text="Raspberry Pi Graphical User Interface", font="Verdana 26 bold",
			fg="#000",
			bg="#99B898",
			pady = 1,
			padx = 1)

label_info = Label(root, text="", font="Verdana 26 bold",
			fg="#000",
			bg="#99B898",
			pady = 1,
			padx = 1)
label_cal = Label(root, text="", font="Verdana 26 bold",
			fg="#000",
			bg="#99B898",
			pady = 1,
			padx = 1)
label_status = Label(root, text="", font="Verdana 26 bold",
			fg="#000",
			bg="#99B898",
			pady = 1,
			padx = 1)

calProbeButton = Button(root, text="Calibrate Probe", background = "#C06C84",
      command=btnExit, height=5, width=20, font = "Arial 16 bold")

readProbeButton = Button(root, text="Read Probe", background = "#C06C84",
      command=readTempClicked, height=5, width=20, font = "Arial 16 bold")
		

exitButton = Button(root, text="Exit", background = "#C06C84",
      command=btnExit, height=5, width=20, font = "Arial 16 bold")
	

tempCalButton = Button(root, text="Cal Temp",background = "Black", fg = "White",
      command=tempCalClicked, height=5, width=20, font = "Arial 16 bold")

probeRead_label = Button(root, text="",background = "#C06C84", 
      command=tempCalClicked, height=5, width=20, font = "Arial 16 bold")


phCalButton = Button(root, text="Cal pH",background = "Red", 
      command=phCalClicked, height=5, width=20, font = "Arial 16 bold")


ecCalButton = Button(root, text="Cal EC",background = "Green", 
      command=ecCalClicked, height=5, width=20, font = "Arial 16 bold")

doCalButton = Button(root, text="Cal DO",background = "Yellow", 
      command=ecCalClicked, height=5, width=20, font = "Arial 16 bold")

orpCalButton= Button(root, text="Cal DO",background = "Light Blue", 
      command=ecCalClicked, height=5, width=20, font = "Arial 16 bold")


label_1.grid(row=0, column=0, columnspan=3)
label_info.grid(row=1, column=1, columnspan=2)
label_cal.grid(row=2, column=1, columnspan=2)
label_status.grid(row=3, column=1, columnspan=2)
exitButton.grid(row = 1 ,column = 0, rowspan=3)
tempCalButton.grid(row = 4 ,column = 0)
phCalButton.grid(row = 4 ,column = 1)
ecCalButton.grid(row = 4 ,column = 2)
doCalButton.grid(row = 4 ,column = 3)
orpCalButton.grid(row = 4 ,column = 4)

readProbeButton.grid(row = 5 ,column = 0)
probeRead_label.grid(row = 5 ,column = 1)
calProbeButton.grid(row = 5 ,column = 2)


if(sensors[0].isProbeConnected()):
	tempCalButton["text"]= "Cal Temp (Connected)"
else:
	tempCalButton["text"]= "Cal Temp (Not Connected)"
	

if(sensors[2].isProbeConnected()):
	phCalButton["text"]= "Cal PH (Connected)"
else:
	phCalButton["text"]= "Cal PH (Not Connected)"
	

if(sensors[1].isProbeConnected()):
	ecCalButton["text"]= "Cal EC (Connected)"
else:
	ecCalButton["text"]= "Cal EC (Not Connected)"

if(sensors[3].isProbeConnected()):
	doCalButton["text"]= "Cal DO (Connected)"
else:
	doCalButton["text"]= "DO Not Connected"

if(sensors[4].isProbeConnected()):
	orpCalButton["text"]= "Cal ORP (Connected)"
else:
	orpCalButton["text"]= "ORP Not Connected"
root.bind("<Escape>", end_fullscreen)
root.mainloop()				# starts the GUI loop
