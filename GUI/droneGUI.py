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
        PMPButton = ttk.Button(self, text="Dose Pump",
                            command=lambda: controller.show_frame(PMPCalPage))
        
        
        
        DOButton.pack()
        ORPButton.pack()
        PMPButton.pack()
        


class DOCalPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="DO Probe Calibration Page!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        
class ORPCalPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="ORP Probe Calibration Page!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
def pointsCalPump(i):       
    v = i.strip().rstrip('\x00').split(",")[1]
    if(v ==1):
        return "fixed volume"
    elif(v ==2):
        return "volume/time"
    elif(v ==3):
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
        
    calibrationLabel.config(text="New:"+pointsCalPump(nutrientMix[0].pump.query("Cal,?")))
    
def clearCalibrationButton(fr):
    global nutrientMix, calibrationEntry, resultLabel, calibrationLabel
    
    MsgBox = tk.messagebox.askquestion ('Save Calibration','Are you sure you want to clear calibration' ,icon = 'warning')
    if MsgBox == 'yes':
        print(nutrientMix[0].pump.query("Cal,clear"))
        label2Text = pointsCalPump(nutrientMix[0].pump.query("Cal,?"))
        calibrationLabel.config(text=label2Text)
        
    else:
        tk.messagebox.showinfo('Return','You will now return to the calibration screen')
   
def calibrationButton(fr):
    global nutrientMix, calibrationEntry, resultLabel
    userValue= calibrationEntry.get()
    resultText = "Calibrated to " +  str(userValue)
    MsgBox = tk.messagebox.askquestion ('Save Calibration','Are you sure you want to calibrate pump using ' + str(userValue) + 'ml' ,icon = 'warning')
    if MsgBox == 'yes':
        print("Cal,"+str(userValue))
        print(nutrientMix[0].pump.query("Cal,"+str(userValue)))
        label2Text = pointsCalPump(nutrientMix[0].pump.query("Cal,?"))
        calibrationLabel.config(text=label2Text)

        if(resultLabel == None):
            resultLabel = tk.Label(fr, text=resultText, font=LARGE_FONT)
            resultLabel.pack(pady=10,padx=10)
        else:
            resultLabel.config(text=resultText)
            calibrationLabel.config(text=nutrientMix[0].pump.query("Cal,?").strip().rstrip('\x00'))
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
        label2Text = pointsCalPump(nutrientMix[0].pump.query("Cal,?"))
        calibrationLabel = tk.Label(self, text=label2Text, font=LARGE_FONT)
        calibrationLabel.pack(pady=10,padx=10)
        
        doseButton = ttk.Button(self, text="Dose 10ml", command=lambda:dosePump(self))
        doseButton.pack()
        
        doseOverTimeButton = ttk.Button(self, text="Dose 10ml/Min", command=lambda:doseOverTimePump(self))
        doseOverTimeButton.pack()#
        
        stopButton = ttk.Button(self, text="Stop", command=lambda:stopPump(self))
        stopButton.pack()
        
        
        infoButton = ttk.Button(self, text="Info", command=lambda:infoPump(self))
        infoButton.pack()
        
        clearCalPumpButton = ttk.Button(self, text="Reset Calibration", command=lambda:clearCalibrationButton(self))
        clearCalPumpButton.pack()

        calPumpButton = ttk.Button(self, text="Calibration", command=lambda:calibrationButton(self))
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
