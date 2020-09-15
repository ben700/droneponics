#! /usr/bin/env python3
import matplotlib
import numpy as np 

vmin = 0.1
vmax = 1000

norm = matplotlib.colors.Normalize(np.log10(vmin), np.log10(vmax))
lognum = norm(np.log10([.5, 2., 10, 40, 150,1000]))

cdict = {
    'red':
    (
        (0., 0, 0),
        (lognum[0], 0, 0),
        (lognum[1], 0, 0),
        (lognum[2], 1, 1),
        (lognum[3], 0.8, 0.8),
        (lognum[4], .7, .7),
    (lognum[5], .7, .7)
    ),
    'green':
    (
        (0., .6, .6),
        (lognum[0], 0.8, 0.8),
        (lognum[1], 1, 1),
        (lognum[2], 1, 1),
        (lognum[3], 0, 0),
        (lognum[4], 0, 0),
    (lognum[5], 0, 0)
    ),
    'blue':
    (
        (0., 0, 0),
        (lognum[0], 0, 0),
        (lognum[1], 0, 0),
        (lognum[2], 0, 0),
        (lognum[3], 0, 0),
        (lognum[4], 0, 0),
    (lognum[5], 1, 1)
    )
}


mycmap = matplotlib.colors.LinearSegmentedColormap('my_colormap', cdict, 256)   
norm = matplotlib.colors.LogNorm(vmin, vmax)
colors = {}
count = 0
step_size = 10
for value in np.arange(vmin, vmax+step_size, step_size):
    count += 1
    print("%d/%d %f%%" % (count, vmax*(1./step_size), 100.*count/(vmax*(1./step_size))))
    rgba = mycmap(norm(value), bytes=True)
    color = (rgba[0], rgba[1], rgba[2])
    if color not in colors.values():
        colors[value] = color

print ("value, red, green, blue")
for value in range(1, 100):
    print("value = " + str(value))
    rgb = colors[value]
    print("%s, %s, %s, %s" % (round(value,1), rgb[0], rgb[1], rgb[2]))
    value = value +10