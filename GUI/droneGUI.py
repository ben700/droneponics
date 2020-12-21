import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import tkinter as tk
from tkinter import ttk
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
        
        
class PMPCalPage(tk.Frame):

    def dosePump(self):
            resultText = pump1.query("D,10")
            resultLabel = tk.Label(self, text=resultText, font=LARGE_FONT)
            resultLabel.pack(pady=10,padx=10)
            
    def __init__(self, parent, controller):
        global pumpId
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Dose Pump Calibration Page!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        pump1=AtlasI2C(nutrientMix[0].pumpId)
        label2Text = pump1.query("Cal,?").strip().rstrip('\x00')
        label = tk.Label(self, text=label2Text, font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        doseButton = ttk.Button(self, text="Dose 10ml", command=dosePump)
        doseButton.pack()
        

        
        
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
