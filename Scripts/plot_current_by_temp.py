#!/usr/bin/env conda run -n ska3 python

import Ska.engarchive.fetch as fetch
import Chandra.Time

import datetime as dt
import matplotlib.dates as mdate
from matplotlib import gridspec

import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

from msidlists import *
from event_times import *
from plot_stylers import *

from hrcsentinel import hrccore as hrc
hrc.styleplots()

# allow_subset=True will allow Maude queries longer than 7 days, but will subsample data
allow_subset = True
fetch.data_source.set('cxc', 'maude allow_subset={}'.format(allow_subset))


# PLOT RELEVANT TEMPERATURES
with fetch.data_source('maude allow_subset=False'):
    dat = fetch.MSIDset(['2FHTRMZT', '2CHTRPZT', '2PRBSCR'],
                        '2020:245')
dat.interpolate()
# intersection_indices = np.intersect1d(
#     dat['2PRBSCR'].times, dat['2FHTRMZT'].times, return_indices=True)

fig, ax = plt.subplots(figsize=(20, 10))

x = dat['2CHTRPZT'].vals-273.15
y = dat['2PRBSCR'].vals


ax.scatter(x, y)
# Fit a best-fit
m, b = np.polyfit(x, y, 1)
ax.plot(x, m*x + b, color=blue)

ax.set_xlabel('CEA Box Temp 2CHTRPZT (C)')
ax.set_ylabel('S/C Redundant Bus Current 2PRBSCR (A)')
plt.title('Data Following Side B Swap')

ax.text(20, 1.9, 'Slope of best fit is {} mA / C'.format(np.round(m, 4)), color='dimgray')
plt.tight_layout()
plt.show()
