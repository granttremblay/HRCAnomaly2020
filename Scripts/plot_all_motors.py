#!/usr/bin/env conda run -n ska3 python
import os
import sys
import shutil
import time
import pytz
import traceback

import Ska.engarchive.fetch as fetch
import Chandra.Time

import datetime as dt
import matplotlib.dates as mdate
from matplotlib import gridspec

import matplotlib.pyplot as plt
# import mpld3

import numpy as np
import pandas as pd

from msidlists import *
from event_times import *
from plot_stylers import *

from hrcsentinel import hrccore as hrc


plt.style.use('ggplot')
labelsizes = 8
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.size'] = labelsizes


plt.rcParams['axes.titlesize'] = labelsizes
plt.rcParams['axes.labelsize'] = labelsizes
plt.rcParams['xtick.labelsize'] = labelsizes-2
plt.rcParams['ytick.labelsize'] = labelsizes

fetch.data_source.set('maude allow_subset=True')


counter = 0


n_lines = len(motor_msids)
color_idx = np.linspace(0, 1, n_lines)

fig, ax = plt.subplots()
for i, msid in zip(color_idx, motor_msids):
    print('Fetching {}'.format(msid))
    dat = fetch.MSID(msid, start='2020:220')
    # YOU HAVE TO USE RAW_VALS HERE BECAUSE OTHERWISE VALS WILL BEA  STRING LIKE UNACT OR ENAB
    try:
        ax.plot_date(hrc.convert_chandra_time(dat.times),
                     dat.raw_vals + counter, label=dat.msid, color=plt.cm.viridis(i), markersize=0, linestyle='-', linewidth=1.5)
        ax.text(dt.datetime(2020, 8, 10, 0, 0),
                dat.raw_vals[0] + counter + 0.1, dat.msid, color=plt.cm.viridis(i), size=10)
    except Exception as inst:
        print('ERROR on {}: '.format(msid, inst))

    counter += 1

# ax.legend()

ax.axvline(eventdate, color='gray')
ax.axvline(hrc_poweroff_date, color='gray')
ax.axvline(a_side_reset, color='gray')

ax.axvline(time_of_second_anomaly, color='gray')
ax.axvline(time_of_second_shutdown, color='gray')

ax.axvline(time_of_cap_1543, color='gray')


plt.show()

for i, msid in zip(color_idx, motor_msids):
    fig, ax = plt.subplots()
    print('Fetching {}'.format(msid))
    dat = fetch.MSID(msid, start='2020:220')
    # YOU HAVE TO USE RAW_VALS HERE BECAUSE OTHERWISE VALS WILL BEA  STRING LIKE UNACT OR ENAB

    ax.axvline(eventdate, color='gray')
    ax.axvline(hrc_poweroff_date, color='gray')
    ax.axvline(a_side_reset, color='gray')

    ax.axvline(time_of_second_anomaly, color='gray')
    ax.axvline(time_of_second_shutdown, color='gray')

    ax.axvline(time_of_cap_1543, color='gray')
    try:
        ax.plot_date(hrc.convert_chandra_time(dat.times),
                     dat.raw_vals, label=dat.msid, color=plt.cm.viridis(i), markersize=0, linestyle='-', linewidth=1.5)
        ax.text(dt.datetime(2020, 8, 10, 0, 0),
                dat.raw_vals[0] + 0.1, dat.msid, color=plt.cm.viridis(i), size=10)
    except Exception as inst:
        print('ERROR on {}: '.format(msid, inst))

    # ax.set_ylim(-2, 2)
    ax.set_xlim(dt.datetime(2020, 8, 22, 0, 0), dt.datetime(2020, 9, 2, 0, 0))
    ax.set_title('{}'.format(msid))

    fig.savefig('/Users/grant/Desktop/{}.png'.format(msid), dpi=300)
    plt.close()
