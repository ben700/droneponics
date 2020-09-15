#import colormap
import matplotlib
from colour import Color
from matplotlib import cm

def getTempColour(Temp):
     #normalize item number values to colormap
     norm = matplotlib.colors.Normalize(vmin=0, vmax=400)

     #colormap possible values = viridis, jet, spectral
     rgba_color = cm.coolwarm(norm(100),bytes=True) 
     print("rgba_color =" + str(rgba_color))

     c = Color(rgb=(rgba_color[0]/255,rgba_color[1]/255,rgba_color[2]/255))
     print("color =" + str(c))
     return c


def getMoistColour(Temp):
     #normalize item number values to colormap
     norm = matplotlib.colors.Normalize(vmin=0, vmax=100)

     #colormap possible values = viridis, jet, spectral
     rgba_color = cm.RdBu(norm(100),bytes=True) 
     print("rgba_color =" + str(rgba_color))

     c = Color(rgb=(rgba_color[0]/255,rgba_color[1]/255,rgba_color[2]/255))
     print("color =" + str(c))
     return c
