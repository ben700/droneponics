#!/usr/bin/python	
from tkinter import * 			# imports the Tkinter lib
root = Tk()				# create the root object
root.wm_title("GUI")			# sets title of the window
root.configure(bg="#99B898")		# change the background color 
root.attributes("-fullscreen", True) 	# set to fullscreen
ledB= False


def btnClicked():
  global ledB    
  if(ledB):
    ledButton["text"]="LED OFF"
    ledB= False
  else:
    ledButton["text"]="LED ON"
    ledB= True

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
exitButton = Button(root, text="Exit", background = "#C06C84",
      command=btnExit, height=10, width=20, font = "Arial 16 bold")
	

ledButton = Button(root, text="LED OFF",background = "#C06C84", 
      command=btnClicked, height=10, width=20, font = "Arial 16 bold")

tempCalButton = Button(root, text="Cal Temp",background = "#C06C84", 
      command=btnClicked, height=10, width=20, font = "Arial 16 bold")


phCalButton = Button(root, text="Cal pH",background = "#C06C84", 
      command=btnClicked, height=10, width=20, font = "Arial 16 bold")


ecCalButton = Button(root, text="Cal EC",background = "#C06C84", 
      command=btnClicked, height=10, width=20, font = "Arial 16 bold")


label_1.grid(row=0, column=0, columnspan=3)
exitButton.grid(row = 1 ,column = 0)
tempCalButton.grid(row = 2 ,column = 0)
phCalButton.grid(row = 2 ,column = 1)
ecCalButton.grid(row = 2 ,column = 2)

root.bind("<Escape>", end_fullscreen)
root.mainloop()				# starts the GUI loop
