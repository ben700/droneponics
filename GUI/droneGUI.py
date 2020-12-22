import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
from math import *
import sys
import os
sys.path.append('/home/pi/droneponics')
from AtlasI2C import (AtlasI2C)

LARGE_FONT= ("Verdana", 12)
f=None
pumpId=None
nutrientMix = []
sensors = []
calibrationEntry=None
calibrationLabel=None
resultLabel=None

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Calibration",
                            command=lambda: controller.show_frame(CalibrationPage))
        button.pack()

        button2 = ttk.Button(self, text="Configuration",
                            command=lambda: controller.show_frame(ConfigurationPage))
        button2.pack()

        button3 = ttk.Button(self, text="Graph Page",
                            command=lambda: controller.show_frame(OperationalDataPage))
        button3.pack()
        
        quitButton = ttk.Button(self, text="Quit",
                            command=quit)
        quitButton.pack()
        
class CalibrationPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Calibration Page!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        DOButton = ttk.Button(self, text="DO Probe",
                            command=lambda: controller.show_frame(DOCalPage))
        ORPButton = ttk.Button(self, text="ORP Probe",
                            command=lambda: controller.show_frame(ORPCalPage))
        TempButton = ttk.Button(self, text="Temp Probe",
                            command=lambda: controller.show_frame(TempCalPage))
        PMPButton = ttk.Button(self, text="Dose Pump",
                            command=lambda: controller.show_frame(PMPCalPage))
        
        
        
        DOButton.pack()
        ORPButton.pack()
        TempButton.pack()
        PMPButton.pack()
        

def pointsCalDO(i):       
    print(i)
    v = i.strip().rstrip('\x00').split(",")[1]
    if(str(v) ==str(1)):
        return "one point calibration"
    elif(str(v) ==str(2)):
        return "two point calibration"
    else:
        return "uncalibrated"
  

def pointsCalTemp(i):       
    print(i)
    v = i.strip().rstrip('\x00').split(",")[1]
    if(str(v) ==str(1)):
        return "Calibrated"
    else:
        return "uncalibrated"
    
class DOCalPage(tk.Frame):

    def __init__(self, parent, controller):
        global sensors
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="DO Probe Calibration Page!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        calibrationLabel = tk.Label(self, text=pointsCalDO(sensors[1].sensor.query("Cal,?")), font=LARGE_FONT)
        calibrationLabel.pack(pady=10,padx=10)
       
        # Cal atmospheric, Cal,0 Zero , Cal,clear
        infoButton = ttk.Button(self, text="Info", command=lambda:infoDO(self))
        infoButton.pack()
        
        clearCalDOButton = ttk.Button(self, text="Reset Calibration", command=lambda:clearCalibrationDOButton(self))
        clearCalDOButton.pack()

        atmosphericCalDOButton = ttk.Button(self, text="Atmospheric", command=lambda:calibrationDOButtonAtmos(self))
        atmosphericCalDOButton.pack()
        
        zeroCalDOButton = ttk.Button(self, text="Zero", command=lambda:calibrationDOButtonZero(self))
        zeroCalDOButton.pack()
        
class ORPCalPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="ORP Probe Calibration Page!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
             
        calibrationLabel = tk.Label(self, text=pointsCalDO(sensors[2].sensor.query("Cal,?")), font=LARGE_FONT)
        calibrationLabel.pack(pady=10,padx=10)
       
        # Cal atmospheric, Cal,0 Zero , Cal,clear
        infoButton = ttk.Button(self, text="Info", command=lambda:infoORP(self))
        infoButton.pack()
        
        clearCalDOButton = ttk.Button(self, text="Reset Calibration", command=lambda:clearCalibrationORPButton(self))
        clearCalDOButton.pack()

        userCalDOButton = ttk.Button(self, text="Calibration", command=lambda:calibrationORPButton(self))
        userCalDOButton.pack()
        
                
        calibrationEntry = ttk.Entry (self, text="ORP Value") 
        calibrationEntry.insert(0, "10.0")
        calibrationEntry.pack()



def setcalibrationEntry(calibrationEntry, value):
    calibrationEntry.delete(0,"end")
    calibrationEntry.insert(0,value)    
    
def reduceUserValue (v):
    global calibrationEntry
    userValue = calibrationEntry.get()
    setcalibrationEntry(calibrationEntry, float(userValue)-1)
#    calibrationEntry.delete(0, "end")
 #   calibrationEntry.insert(0, float(userValue)-1)
    print("calibrationEntry.insert" + str(float(userValue)-1))
    
def increaseUserValue (v):
    global calibrationEntry, calibrationLabel
    userValue = calibrationEntry.get()
    setcalibrationEntry(calibrationEntry, float(userValue)+1)
#    calibrationEntry.delete(0, "end")
#    calibrationEntry.insert(0, float(userValue)+1)
    print("calibrationEntry.insert" + str(float(userValue)+1))

def infoTemp(fr):
    infoDevice(fr,Sensors[0].sensor)
def readDO(fr):
    infoDevice(fr,Sensors[0].sensor)
def readORP(fr):
    infoDevice(fr,Sensors[0].sensor)
    
def infoDevice(fr, device):
    global nutrientMix, resultLabel, calibrationLabel
    resultText = device.query("I")
    if(resultLabel == None):
        resultLabel = tk.Label(fr, text=resultText, font=LARGE_FONT)
        resultLabel.pack(pady=10,padx=10)
    else:
        resultLabel.config(text=resultText)
        
    calibrationLabel.config(text=device.query("Cal,?"))

def readTemp(fr):
    readDevice(fr,Sensors[0].sensor)
def readDO(fr):
    readDevice(fr,Sensors[0].sensor)
def readORP(fr):
    readDevice(fr,Sensors[0].sensor)
    
def readDevice(fr, device):
    global nutrientMix, resultLabel, calibrationLabel
    resultText = device.query("R")
    if(resultLabel == None):
        resultLabel = tk.Label(fr, text=resultText, font=LARGE_FONT)
        resultLabel.pack(pady=10,padx=10)
    else:
        resultLabel.config(text=resultText)
        
    calibrationLabel.config(text=device.query("Cal,?"))

def clearCalibrationTempButton(fr):
    clearCalibrationButton(fr,Sensors[0].sensor)
def clearCalibrationDOButton(fr):
    clearCalibrationButton(fr,Sensors[1].sensor)
def clearCalibrationORPButton(fr):
    clearCalibrationButton(fr,Sensors[2].sensor)
    
def clearCalibrationButton(fr, device):
    global nutrientMix, calibrationEntry, resultLabel, calibrationLabel
    MsgBox = tk.messagebox.askquestion ('Clear Calibration','Are you sure you want to clear calibration' ,icon = 'warning')
    if MsgBox == 'yes':
        device.query("Cal,clear")
        calibrationLabel.config(text=device.query("Cal,?"))
        
    else:
        tk.messagebox.showinfo('Return','You will now return to the calibration screen')

def calibrationTempButton(fr):
    calibrationButton(fr,Sensors[0].sensor, calibrationEntry.get())
def calibrationDOButtonZero(fr):
    calibrationButton(fr,Sensors[1].sensor,0)
def calibrationORPButton(fr):
    calibrationButton(fr,Sensors[2].sensor)
    
def calibrationButton(fr, device, value):
    global nutrientMix, calibrationEntry, resultLabel

    resultText = "Calibrated to " +  str(value)
    MsgBox = tk.messagebox.askquestion ('Save Calibration','Are you sure you want to calibrate using ' + str(value) ,icon = 'warning')
    if MsgBox == 'yes':
        device.query("Cal,"+str(value))
        calibrationLabel.config(text=device.query("Cal,?"))
        if(resultLabel == None):
            resultLabel = tk.Label(fr, text=resultText, font=LARGE_FONT)
            resultLabel.pack(pady=10,padx=10)
        else:
            resultLabel.config(text=resultText)
            calibrationLabel.config(text=device.query("Cal,?"))
    else:
        tk.messagebox.showinfo('Return','You will now return to the calibration screen')


def calibrationDOButtonAtmos(fr, device, value):
    global nutrientMix, calibrationEntry, resultLabel

    resultText = "Calibrated to " +  str(value)
    MsgBox = tk.messagebox.askquestion ('Save Calibration','Are you sure you want to calibrate using Atmos' ,icon = 'warning')
    if MsgBox == 'yes':
        device.query("Cal"))
        calibrationLabel.config(text=device.query("Cal,?"))
        if(resultLabel == None):
            resultLabel = tk.Label(fr, text=resultText, font=LARGE_FONT)
            resultLabel.pack(pady=10,padx=10)
        else:
            resultLabel.config(text=resultText)
            calibrationLabel.config(text=device.query("Cal,?"))
    else:
        tk.messagebox.showinfo('Return','You will now return to the calibration screen')
   
    
class TempCalPage(tk.Frame):

    def __init__(self, parent, controller):
        global nutrientMix, calibrationEntry, resultLabel, calibrationLabel
  
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Temp Probe Calibration Page!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
             
        calibrationLabel = tk.Label(self, text=pointsCalTemp(sensors[0].sensor.query("Cal,?")), font=LARGE_FONT)
        calibrationLabel.pack(pady=10,padx=10)
    
        # Cal atmospheric, Cal,0 Zero , Cal,clear
        infoButton = ttk.Button(self, text="Info", command=lambda:infoTemp(self))
        infoButton.pack()
        
        readButton = ttk.Button(self, text="Info", command=lambda:readTemp(self))
        readButton.pack()
        
        clearCalDOButton = ttk.Button(self, text="Reset Calibration", command=lambda:clearTempCalibrationButton(self))
        clearCalDOButton.pack()

        userCalDODownButton = ttk.Button(self, text="-", command=lambda:reduceUserValue(self))
        userCalDODownButton.pack()
        
        userCalDOButton = ttk.Button(self, text="Calibration", command=lambda:calibrationTempButton(self))
        userCalDOButton.pack()
        
        userCalDOUpButton = ttk.Button(self, text="+", command=lambda:increaseUserValue(self))
        userCalDOUpButton.pack()
        
        calibrationEntry = ttk.Entry (self, text="Temp Value") 
        setcalibrationEntry(calibrationEntry, "25.0")
        calibrationEntry.pack()
        setcalibrationEntry(calibrationEntry, "10.0")
        
        
    
        
def pointsCalPump(i):       
    print(i)
    v = i.strip().rstrip('\x00').split(",")[1]
    print("[" + str(v) + "]")
    if(str(v) ==str(1)):
        print("fixed volume")
        return "fixed volume"
    elif(str(v) ==str(2)):
        return "volume/time"
    elif(str(v) ==str(3)):
        return "Both"
    else:
        return "uncalibrated"
    
    
def dosePump(fr):
    global nutrientMix
    resultText = nutrientMix[0].pump.query("D,10")
    resultLabel = tk.Label(fr, text=resultText, font=LARGE_FONT)
    resultLabel.pack(pady=10,padx=10)
 
def doseOverTimePump(fr):
    global nutrientMix
    resultText = nutrientMix[0].pump.query("D,10,1")
    resultLabel = tk.Label(fr, text=resultText, font=LARGE_FONT)
    resultLabel.pack(pady=10,padx=10)

def stopPump(fr):
    global nutrientMix
    resultText = nutrientMix[0].pump.query("X")
    resultLabel = tk.Label(fr, text=resultText, font=LARGE_FONT)
    resultLabel.pack(pady=10,padx=10)

def infoPump(fr):
    global nutrientMix, resultLabel, calibrationLabel
    resultText = nutrientMix[0].pump.query("I")
    if(resultLabel == None):
        resultLabel = tk.Label(fr, text=resultText, font=LARGE_FONT)
        resultLabel.pack(pady=10,padx=10)
    else:
        resultLabel.config(text=resultText)
        
    calibrationLabel.config(text=pointsCalPump(nutrientMix[0].pump.query("Cal,?")))
    
def clearCalibrationPMPButton(fr):
    global nutrientMix, calibrationEntry, resultLabel, calibrationLabel
    
    MsgBox = tk.messagebox.askquestion ('Save Calibration','Are you sure you want to clear calibration' ,icon = 'warning')
    if MsgBox == 'yes':
        nutrientMix[0].pump.query("Cal,clear")
        calibrationLabel.config(text=pointsCalPump(nutrientMix[0].pump.query("Cal,?")))
        
    else:
        tk.messagebox.showinfo('Return','You will now return to the calibration screen')
   
def calibrationPMPButton(fr):
    global nutrientMix, calibrationEntry, resultLabel
    userValue= calibrationEntry.get()
    resultText = "Calibrated to " +  str(userValue)
    MsgBox = tk.messagebox.askquestion ('Save Calibration','Are you sure you want to calibrate pump using ' + str(userValue) + 'ml' ,icon = 'warning')
    if MsgBox == 'yes':
        nutrientMix[0].pump.query("Cal,"+str(userValue))
        calibrationLabel.config(text=pointsCalPump(nutrientMix[0].pump.query("Cal,?")))

        if(resultLabel == None):
            resultLabel = tk.Label(fr, text=resultText, font=LARGE_FONT)
            resultLabel.pack(pady=10,padx=10)
        else:
            resultLabel.config(text=resultText)
            calibrationLabel.config(text=pointsCalPump(nutrientMix[0].pump.query("Cal,?")))
    else:
        tk.messagebox.showinfo('Return','You will now return to the calibration screen')
   

    
        
    
class PMPCalPage(tk.Frame):

            
    def __init__(self, parent, controller):
        global pumpId, calibrationEntry, calibrationLabel,resultLabel
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Dose Pump Calibration Page!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        nutrientMix[0].pump=AtlasI2C(nutrientMix[0].pumpId)
        calibrationLabel = tk.Label(self, text=pointsCalPump(nutrientMix[0].pump.query("Cal,?")), font=LARGE_FONT)
        calibrationLabel.pack(pady=10,padx=10)
        
        doseButton = ttk.Button(self, text="Dose 10ml", command=lambda:dosePump(self))
        doseButton.pack()
        
        doseOverTimeButton = ttk.Button(self, text="Dose 10ml/Min", command=lambda:doseOverTimePump(self))
        doseOverTimeButton.pack()#
        
        stopButton = ttk.Button(self, text="Stop", command=lambda:stopPump(self))
        stopButton.pack()
        
        
        infoButton = ttk.Button(self, text="Info", command=lambda:infoPump(self))
        infoButton.pack()
        
        clearCalPumpButton = ttk.Button(self, text="Reset Calibration", command=lambda:clearCalibrationPMPButton(self))
        clearCalPumpButton.pack()

        calPumpButton = ttk.Button(self, text="Calibration", command=lambda:calibrationPMPButton(self))
        calPumpButton.pack()

        
        calibrationEntry = ttk.Entry (self, text="Pumped Volume") 
        calibrationEntry.insert(0, "10.0")
        calibrationEntry.pack()
        
        
class ConfigurationPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Configuration Page!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home",
        command=lambda: controller.show_frame(StartPage))
        button1.pack()

class OperationalDataPage(tk.Frame):

    def __init__(self, parent, controller):
        global f        
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Operational Data Page!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home",
        command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
