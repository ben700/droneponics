from colour import Color
import blynklib

def displaySensor(blynk, VP, VALUE, NAME , LOW, HIGH):
 print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
 red = Color("red")
 print("loaded color class")
 colors = list(red.range_to(Color("green"),10))
 print("done colour list")
 print(colors)
 print("Going to update blynk")
 blynk.virtual_write(VP,VALUE)
 blynk.set_property(VP, "label", NAME)
 print("Going to update blynk colors")
 blynk.set_property(VP, "color", colors[round((HIGH-LOW)/10,0)])
 print("####################################################")
 return

