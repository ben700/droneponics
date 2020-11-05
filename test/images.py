#!/usr/bin/env python3

import pygame
import sys
import time
import glob
import random
from decimal import *
from pygame.locals import *

import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode (GPIO.BOARD)

# set GPIO output pin
OP = 26

GPIO.setup(OP, GPIO.OUT)
GPIO.output(OP,GPIO.HIGH)

# MAXIMUM picture display sizes
max_width = 1600
max_height = 960

# display time in seconds
display = 20

# randomise pictures, 0 = NO, 1 = YES
pic_rand = 1

# Directory name
dir_name ="/home/pi/droneponics/pic"

# Normal or Fullscreen, 0 = normal, 1 = fullscreen
fscreen = 1

# Stretch small images to MAXIMUM display size, 0 = NO, 1 = YES
stretch = 0
print(dir_name)
#find .jpg files in directory
pic_list = glob.glob(dir_name + '*.jpg') 
num_pics =len(pic_list)


while True:
   for num in range (0,num_pics):
      if pic_rand == 0:
         imagefile = pic_list[num]
      else:
         imagefile = pic_list[int(random.random()*num_pics)]
      image = pygame.image.load(imagefile)
      size = image.get_rect()
      width = size[2]
      height = size[3]
      if width < max_width and stretch == 1:
         height = height * (Decimal(max_width)/Decimal(width))
         width = max_width
         image = pygame.transform.scale(image,(width,height))
      if height < max_height and stretch == 1:
         width = width * (Decimal(max_height)/Decimal(height))
         height = max_height
         image = pygame.transform.scale(image,(width,height))
      if width > max_width:
         height = height * (Decimal(max_width)/Decimal(width))
         width = max_width
         image = pygame.transform.scale(image,(width,height))
      if height > max_height:
         width = width * (Decimal(max_height)/Decimal(height))
         height = max_height
         image = pygame.transform.scale(image,(width,height))
      if fscreen == 1:
         windowSurfaceObj = pygame.display.set_mode((width,height),pygame.FULLSCREEN)
      else:
         windowSurfaceObj = pygame.display.set_mode((width,height))
         pygame.display.set_caption('Slideshow')
      windowSurfaceObj.blit(image,(0,0))
      pygame.display.update()
      GPIO.output(OP,GPIO.HIGH)
      t = time.time()
      while t > time.time()- display:
         for event in pygame.event.get():
            if event.type == QUIT:
               pygame.quit()
               sys.exit()
           
            elif event.type == KEYDOWN:
               # press N for normal screen
               if event.key == K_n:
                  windowSurfaceObj = pygame.display.set_mode((width,height))
                  windowSurfaceObj.blit(image,(0,0))
                  pygame.display.update()
                  fscreen = 0
               # press F for fullscreen
               if event.key == K_f:
                  windowSurfaceObj = pygame.display.set_mode((width,height),pygame.FULLSCREEN)
                  windowSurfaceObj.blit(image,(0,0))
                  pygame.display.update()
                  fscreen = 1
               # press X to EXIT
               if event.key == K_x or event.key == K_ESCAPE:
                  pygame.quit()
                  sys.exit()
      GPIO.output(OP,GPIO.LOW)

