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
fetch.data_source.set('cxc')


fig, ax1 = plt.subplots()

dat = fetch.MSIDset(['2PRBSCR', '2S2HVST', '2SHEV1RT', '2CHTRPZT'], '2016:001', stat='5min')

ax1.plot_date(hrc.convert_chandra_time(
    dat['2PRBSCR'].times), dat['2PRBSCR'].midvals, color=purple, markersize=2, linewidth=0, label='Bus Current')

# ax2 = ax1.twinx()
# ax2.plot_date(hrc.convert_chandra_time(
#     dat['2CHTRPZT'].times), dat['2CHTRPZT'].midvals,  color=blue, linewidth=2.0, label='CEA Temp')


ax1.grid('off', axis='y')
# ax2.grid('off', axis='y')
ax1.grid(False)
# ax2.grid(False)
plt.show()


fetch.data_source.set('cxc')

rasterized = True
markersize = 1.2
labelsizes = 28
plt.rcParams['axes.titlesize'] = labelsizes
plt.rcParams['axes.labelsize'] = labelsizes - 4
plt.rcParams['xtick.labelsize'] = labelsizes - 4
plt.rcParams['ytick.labelsize'] = labelsizes - 4


dat = fetch.get_telem(['2PRBSCR'], start='2020:235')

fig, ax1 = plt.subplots(figsize=(20, 12))


ax1.axvline(eventdate, color='gray')
ax1.axvline(hrc_poweroff_date, color='gray')
ax1.axvline(cap_step_2, color='gray')
ax1.axvline(time_of_second_anomaly, color='gray')
ax1.axvline(time_of_second_shutdown, color='gray')
ax1.axvline(time_of_cap_1543, color='gray')


ax1.set_xlabel('Date (UTC)')
ax1.set_ylabel('S/C Bus Current (A)')

ax1.plot_date(hrc.convert_chandra_time(
    dat['2PRBSCR'].times), dat['2PRBSCR'].vals, color=blue, rasterized=True)
# ax1.tick_params(axis='y', labelcolor=red)
xmin = dt.datetime(2020, 8, 31, 0)
xmax = dt.datetime(2020, 9, 7, 18)
ax1.set_xlim(xmin, xmax)
ax1.set_ylim(1.0, 3.0)
# ax1.legend(loc=2)
# ax1.grid('off', axis='y')


# ax2 = ax1.twinx()
# ax2.set_ylabel('S/C Redundant Bus Current (A)', color=blue)
# ax2.tick_params(axis='y', labelcolor=blue)
# ax2.plot_date(hrc.convert_chandra_time(dat['2PRBSCR'].times), dat['2PRBSCR'].vals, color=blue, label='S/C Redundant Bus Current (2PRBSCR)',  rasterized=True)

# ax2.set_xlim(xmin, xmax)

# # ax2.legend(loc=1)
# ax1.axvline(time_of_cap_1543, color='gray')

# fig.tight_layout()
plt.show()
