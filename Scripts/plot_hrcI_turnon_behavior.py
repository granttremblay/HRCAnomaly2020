#!/usr/bin/env conda run -n ska3 python

# import seaborn as sns
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
markersize = 2.0
# allow_subset=True will allow Maude queries longer than 7 days, but will subsample data
allow_subset = True
fetch.data_source.set('cxc')


hrci_msids = ['2IMTPAST', '2IMBPAST', '2IMHBLV', '2IMHVLV', '2PRBSCR']


dat_hrci = fetch.get_telem(hrci_msids, sampling='full', start='2018:001')
dat_temps = fetch.get_telem(
    critical_anomaly_temps, sampling='full', start='2018:001', max_fetch_Mb=1000000, max_output_Mb=1000000)

fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.plot_date(hrc.convert_chandra_time(
    dat_hrci['2IMTPAST'].times), dat_hrci['2IMTPAST'].vals, color=red, markersize=0, linewidth=2.0, linestyle='-', label='2IMTPAST')
ax1.plot_date(hrc.convert_chandra_time(
    dat_hrci['2IMHBLV'].times), dat_hrci['2IMHBLV'].vals, color=purple, markersize=0, linewidth=2.0, linestyle='-', label='2IMHBLV')
ax1.plot_date(hrc.convert_chandra_time(
    dat_hrci['2PRBSCR'].times), dat_hrci['2PRBSCR'].vals, color=blue, markersize=0, linewidth=2.0, linestyle='-', label='2PRBSCR')

ax1.grid('off', axis='y')
# ax1.legend()

ax2 = plt.twinx(ax1)


# n_lines = len(critical_anomaly_temps)
# color_idx = np.linspace(0, 1, n_lines)


# for i, msid in zip(color_idx, critical_anomaly_temps):
#     times = hrc.convert_chandra_time(dat_temps[msid].times)
#     vals = dat_temps[msid].vals

#     ax2.plot_date(times, vals, markersize=1.4,
#                   rasterized=rasterized, color=plt.cm.tab20(i), label=msid)

ax2.plot_date(hrc.convert_chandra_time(dat_temps['2FHTRMZT'].times), dat_temps['2FHTRMZT'].vals, markersize=1.4,
              rasterized=rasterized, color=green, label='FEA Temperature (2FHTRMZT)')

ax2.plot_date(hrc.convert_chandra_time(dat_temps['2IMHVATM'].times), dat_temps['2IMHVATM'].vals, markersize=1.4,
              rasterized=rasterized, color=purple, label='Imaging Det HVPS Temperature (c)')

ax2.plot_date(hrc.convert_chandra_time(dat_temps['2IMINATM'].times), dat_temps['2IMINATM'].vals, markersize=1.4,
              rasterized=rasterized, color=yellow, label='Imaging Det Temperature (c)')

# ax2.legend()

ax2.set_ylim(0, 50)

plt.show()
