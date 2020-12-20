import tkinter as tk
from tkinter import ttk


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
        
        
class ORPCalPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="ORP Probe Calibration Page!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        
class PMPCalPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Dose Pump Calibration Page!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
