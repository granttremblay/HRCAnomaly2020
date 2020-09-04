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
with fetch.data_source('maude'):
    dat = fetch.MSIDset(['2FHTRMZT', '2CHTRPZT', '2PRBSCR'],
                        '2020:232')
dat.interpolate()
# intersection_indices = np.intersect1d(
#     dat['2PRBSCR'].times, dat['2FHTRMZT'].times, return_indices=True)

fig, ax = plt.subplots()

ax.plot(dat['2PRBSCR'].vals, dat['2FHTRMZT'].vals,
        color=yellow, markersize=markersize)
# ax.plot_date(hrc.convert_chandra_time(
#     dat['2CHTRPZT'].times), dat['2CHTRPZT'].vals/20, label='2CHTRPZT', color=purple, markersize=markersize)
# ax.plot_date(hrc.convert_chandra_time(
#     dat['2PRBSCR'].times), dat['2PRBSCR'].vals, label='2PRBSCR', color=blue, markersize=markersize)
ax.legend()
# dat['2FHTRMZT'].plot(label='2FHTRMZT', color=yellow)
# dat['2CHTRPZT'].plot(label='2CHTRPZT', color=purple)
# dat['2PRBSCR'].plot(label='2PRBSCR', color=blue)

# ax.axvline(eventdate, color='gray')
# ax.axvline(hrc_poweroff_date, color='gray')
# ax.axvline(cap_step_2, color='gray')
# ax.axvline(time_of_second_anomaly, color='gray')
# ax.axvline(time_of_second_shutdown, color='gray')
# ax.axvline(time_of_cap_1543, color='gray')
ax.legend()
plt.tight_layout()
plt.show()
