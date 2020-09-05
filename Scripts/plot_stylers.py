#!/usr/bin/env python

import datetime as dt

import matplotlib.pyplot as plt
import matplotlib.dates as mdate

from hrcsentinel import hrccore as hrc


# Colors
# Grab the ggplot colors so you can manually set them if needed
hrc.styleplots()
rasterized = True
markersize = 1.8
colortable = plt.rcParams['axes.prop_cycle'].by_key()['color']
red = colortable[0]
blue = colortable[1]
gggray = colortable[3]
yellow = colortable[4]
green = colortable[5]
pink = colortable[6]
purple = colortable[2]
