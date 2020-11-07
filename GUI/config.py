#!/usr/bin/python	
from tkinter import * 			# imports the Tkinter lib
root = Tk()				# create the root object
root.wm_title("GUI")			# sets title of the window
root.configure(bg="#99B898")		# change the background color 
root.attributes("-fullscreen", True) 	# set to fullscreen


def btnClicked():
  if(ledButton["text"]=="LED ON")
    ledButton["text"]="LED OFF"
  else:
    ledButton["text"]="LED ON"

def btnExit():
  	root.destroy()

# we can exit when we press the escape key
def end_fullscreen(event):
	root.attributes("-fullscreen", False)


label_1 = Label(root, text="Raspberry Pi Graphical User Interface", font="Verdana 26 bold",
			fg="#000",
			bg="#99B898",
			pady = 60,
			padx = 100)
exitButton = Button(root, text="Exit", background = "#C06C84",
      command=btnExit, height=10, width=40, font = "Arial 16 bold")
	

ledButton = Button(root, text="LED OFF",background = "#C06C84", 
      command=btnClicked, height=10, width=40, font = "Arial 16 bold")


label_1.grid(row=0, column=0)
exitButton.grid(row = 1 ,column = 0)
ledButton.grid(row = 1 ,column = 1)


root.bind("<Escape>", end_fullscreen)
root.mainloop()				# starts the GUI loop
