# importing Image class from PIL package  
from PIL import Image  
  
# creating a object  
im = Image.open("/home/pi/droneponics/pic/dronePonics_Logo.jpeg")  
  
im.show() 
print("Method 1 completed")

import os
os.system("/home/pi/droneponics/pic/dronePonics_Logo.jpeg")

print("Method 2 completed")
