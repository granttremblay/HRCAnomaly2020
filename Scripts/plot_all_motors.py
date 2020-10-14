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

hrc.styleplots()

fetch.data_source.set('maude allow_subset=True')

fig, ax = plt.subplots()
counter = 0


n_lines = len(motor_msids)
color_idx = np.linspace(0, 1, n_lines)


for i, msid in zip(color_idx, motor_msids):
    print('Fetching {}'.format(msid))
    dat = fetch.MSID(msid, start='2020:220')
    # YOU HAVE TO USE RAW_VALS HERE BECAUSE OTHERWISE VALS WILL BEA  STRING LIKE UNACT OR ENAB
    try:
        ax.plot_date(hrc.convert_chandra_time(dat.times),
                     dat.raw_vals + counter, label=dat.msid, color=plt.cm.tab20(i), markersize=0, linestyle='-', linewidth=1.5)
        ax.text(dt.datetime(2020, 8, 10, 0, 0),
                dat.raw_vals[0] + counter + 0.1, dat.msid, color=plt.cm.tab20(i), size=10)
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
