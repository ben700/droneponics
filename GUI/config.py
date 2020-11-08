#!/usr/bin/python3
import sys
import os
sys.path.append('/home/pi/droneponics')
from AtlasI2C import (AtlasI2C)
import drone
import logging

from tkinter import * 			# imports the Tkinter lib
# pip install pillow
from PIL import Image, ImageTk

    # tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(logging.DEBUG)

restartCode = {'P': "Powered Off", 'S':"Software Reset",'B':"Brown Out",'W':"Watchdog",'U':"Unknown"}


root = Tk()				# create the root object
root.wm_title("GUI")			# sets title of the window

load = Image.open("/home/pi/droneponics/pic/store_logo.png")
render = ImageTk.PhotoImage(load)
img = Label(root, image=render)
img.image = render
img.place(x=0, y=0)
root.configure(bg="#99B898")		# change the background color 
root.attributes("-fullscreen", True) 	# set to fullscreen

sensors = []
sensors = drone.buildAllSensors(sensors, _log)
_log.info("All Monitor Sensors created")


def tempCalClicked():	
    probe = AtlasI2C(102)
    deviceInfo = probe.query("i")
    label_info["text"]= "Device : " +deviceInfo.split(":")[1].split(",")[1].strip().rstrip('\x00') + '\nFirmware : ' + deviceInfo.split(":")[1].split(",")[2].strip().rstrip('\x00')
    calInfo = probe.query("cal,?")
    label_cal["text"]= "Device Calibrated to " + calInfo.split(":")[1].split(",")[1].strip().rstrip('\x00') + " point(s)"
    statusInfo=probe.query("Status")
    label_status["text"]= "Reason for restart : " + restartCode[statusInfo.split(":")[1].split(",")[1].strip().rstrip('\x00')] + "\nVoltage : " +  statusInfo.split(":")[1].split(",")[2].strip().rstrip('\x00')
    readProbeButton["text"]= "Read Temp"
    readProbeButton["command"]= readTempClicked        
    readProbeButton["state"] = NORMAL
    calButton1["text"]= "Cal,t"
    calButton1["command"]= tempCalButton1Clicked
    calButton1["state"] = NORMAL
    calButton2["text"]= "Cal,clear"
    calButton2["command"]= tempCalButton2Clicked
    calButton2["state"] = NORMAL

    clearReading()
	
def phCalClicked():
    probe = AtlasI2C(99)
    deviceInfo = probe.query("i")
    label_info["text"]= "Device : " +deviceInfo.split(":")[1].split(",")[1].strip().rstrip('\x00') + '\nFirmware : ' + deviceInfo.split(":")[1].split(",")[2].strip().rstrip('\x00')
    calInfo = probe.query("cal,?")
    label_cal["text"]= "Device Calibrated to " + calInfo.split(":")[1].split(",")[1].strip().rstrip('\x00') + " point(s)"
    statusInfo=probe.query("Status")
    label_status["text"]= "Reason for restart : " + restartCode[statusInfo.split(":")[1].split(",")[1].strip().rstrip('\x00')] + "\nVoltage : " +  statusInfo.split(":")[1].split(",")[2].strip().rstrip('\x00')
    readProbeButton["text"]= "Read pH"
    readProbeButton["command"]= readPHClicked
    readProbeButton["state"] = NORMAL
    calButton1["text"]= "Cal,dry"
    calButton1["command"]= phCalButton1Clicked
    calButton1["state"] = NORMAL
    calButton2["text"]= "Cal,n"
    calButton2["command"]= phCalButton2Clicked
    calButton2["state"] = NORMAL
    calButton3["text"]= "Cal,clear"
    calButton3["command"]= phCalButton3Clicked
    calButton3["state"] = NORMAL
    clearReading()


def ecCalClicked():
    probe = AtlasI2C(100)
    deviceInfo = probe.query("i")
    label_info["text"]= "Device : " +deviceInfo.split(":")[1].split(",")[1].strip().rstrip('\x00') + '\nFirmware : ' + deviceInfo.split(":")[1].split(",")[2].strip().rstrip('\x00')
    calInfo = probe.query("cal,?")
    label_cal["text"]= "Device Calibrated to " + calInfo.split(":")[1].split(",")[1].strip().rstrip('\x00') + " point(s)"
    statusInfo=probe.query("Status")
    label_status["text"]= "Reason for restart : " + restartCode[statusInfo.split(":")[1].split(",")[1].strip().rstrip('\x00')] + "\nVoltage : " +  statusInfo.split(":")[1].split(",")[2].strip().rstrip('\x00')
    readProbeButton["text"]= "Read EC"
    readProbeButton["command"]= readECClicked
    readProbeButton["state"] = NORMAL
    calButton1["text"]= "Cal,dry"
    calButton1["command"]= ecCalButton1Clicked
    calButton1["state"] = NORMAL
    calButton2["text"]= "Cal,n"
    calButton2["command"]= ecCalButton2Clicked
    calButton2["state"] = NORMAL
    calButton3["text"]= "Cal,clear"
    calButton3["command"]= ecCalButton3Clicked
    calButton3["state"] = NORMAL
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
    probeRead_label["text"]= "Conductivity = " + str(v1) + '\n' + "Total Dissolved Solids = " + str(v2)+ '\n' + "Salinity = " + str(v3)+ '\n' + "Specific Gravity = " + str(v4)

def clearReading():	
    probeRead_label["text"]= ""
 
def tempCalButton1Clicked():	
    calResult_label["text"]= "calButton1TempClicked Completed"	
def tempCalButton2Clicked():	
    calResult_label["text"]= "calButton2TempClicked Completed"
def phCalButton1Clicked():	
    calResult_label["text"]= "Completed"
def phCalButton1Clicked():	
    calResult_label["text"]= "Completed"
def phCalButton1Clicked():	
    calResult_label["text"]= "Completed"
def ecCalButton1Clicked():	
    calResult_label["text"]= "ecButton1TempClicked Completed"
def ecCalButton2Clicked():	
    calResult_label["text"]= "ecButton2TempClicked Completed"
def ecCalButton3Clicked():	
    calResult_label["text"]= "ecButton3TempClicked Completed"

def btnExit():
  	root.destroy()

# we can exit when we press the escape key
def end_fullscreen(event):
	root.attributes("-fullscreen", False)


label_1 = Label(root, text="Droneponics Calibration Interface", font="Verdana 26 bold",
			fg="Black",
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
      command=btnExit, height=5, width=15, font = "Arial 16 bold")

		

exitButton = Button(root, text="Exit", background = "#C06C84",
      command=btnExit, height=5, width=15, font = "Arial 16 bold")
	


phCalButton = Button(root, text="Cal pH",background = "Red", 
      command=phCalClicked, height=5, width=15, font = "Arial 16 bold")

tempCalButton = Button(root, text="Cal EC",background = "Black", fg="White", 
      command=tempCalClicked, height=5, width=15, font = "Arial 16 bold")

ecCalButton = Button(root, text="Cal EC",background = "Green", 
      command=ecCalClicked, height=5, width=15, font = "Arial 16 bold")

doCalButton = Button(root, text="Cal DO",background = "Yellow", 
      command=ecCalClicked, height=5, width=15, font = "Arial 16 bold")

orpCalButton= Button(root, text="Cal DO",background = "Light Blue", 
      command=ecCalClicked, height=5, width=15, font = "Arial 16 bold")

readProbeButton = Button(root, text="Read Probe", background = "#C06C84",
      command=readTempClicked, height=5, width=15, font = "Arial 16 bold")

probeRead_label = Label(root, text="", font="Verdana 26 bold",
			fg="#000",
			bg="#99B898",
			pady = 1,
			padx = 1)

calEntryBox= Entry(root)

calResult_label = Label(root, text="", font="Verdana 26 bold",
			fg="#000",
			bg="#99B898",
			pady = 1,
			padx = 1)


calButton1 = Button(root, text="calButton1",background = "#C06C84", 
       height=5, width=15, font = "Arial 16 bold")

calButton2 = Button(root, text="calButton2",background = "#C06C84", 
       height=5, width=15, font = "Arial 16 bold")

calButton3 = Button(root, text="calButton3",background = "#C06C84",
       height=5, width=15, font = "Arial 16 bold")



label_1.grid(row=0, column=1, columnspan=4)
label_info.grid(row=1, column=1, columnspan=3)
label_cal.grid(row=2, column=1, columnspan=3)
label_status.grid(row=3, column=1, columnspan=3)
exitButton.grid(row = 1,column = 0, rowspan=3)
tempCalButton.grid(row = 4 ,column = 0)
phCalButton.grid(row = 4 ,column = 1)
ecCalButton.grid(row = 4 ,column = 2)
doCalButton.grid(row = 4 ,column = 3)
orpCalButton.grid(row = 4 ,column = 4)

readProbeButton.grid(row = 5 ,column = 0)
probeRead_label.grid(row = 5 ,column = 1, columnspan=3)

calButton1.grid(row = 6 ,column = 0)
calButton2.grid(row = 6 ,column = 1)
calButton3.grid(row = 6 ,column = 2)

calResult_label.grid(row = 7 ,column = 0)

readProbeButton["state"] = DISABLED
calButton1["state"] = DISABLED
calButton2["state"] = DISABLED
calButton3["state"] = DISABLED


if(sensors[0].isProbeConnected()):
	tempCalButton["text"]= "Cal Temp \nConnected"
else:
	tempCalButton["text"]= "Cal Temp \nNot Connected"
	tempCalButton["state"] = DISABLED
	
	

if(sensors[2].isProbeConnected()):
	phCalButton["text"]= "Cal PH \nConnected"
else:
	phCalButton["text"]= "Cal PH \nNot Connected"
	phCalButton["state"] = DISABLED
	
	

if(sensors[1].isProbeConnected()):
	ecCalButton["text"]= "Cal EC "+'\n'+"Connected"
else:
	ecCalButton["text"]= "Cal EC "+'\n'+"Not Connected"
	ecCalButton["state"] = DISABLED
	

if(sensors[3].isProbeConnected()):
	doCalButton["text"]= "Cal DO "+'\n'+"Connected"
else:
	doCalButton["text"]= "DO "+'\n'+"Not Connected"
	doCalButton["state"] = DISABLED
	

if(sensors[4].isProbeConnected()):
	orpCalButton["text"]= "Cal ORP "+'\n'+"Connected"
else:
	orpCalButton["text"]= "ORP "+'\n'+"Not Connected"
	orpCalButton["state"] = DISABLED
	
root.bind("<Escape>", end_fullscreen)
root.mainloop()				# starts the GUI loop
