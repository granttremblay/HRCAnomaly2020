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


# PLOT DETECTOR RATES OVER MISSION LIFETIME
with fetch.data_source('cxc', 'maude allow_subset={}'.format(allow_subset)):
    dat = fetch.get_telem(
        ['2PRBSVL', '2PRBSCR'], '2020:220')
plt.clf()
dat['2PRBSVL'].plot(label='2PRBSVL', color=red)
dat['2PRBSCR'].plot(label='2PRBSCR', color=blue)


plt.axvline(eventdate, color='gray')
plt.axvline(hrc_poweroff_date, color='gray')
plt.axvline(cap_step_2, color='gray')
plt.axvline(time_of_second_anomaly, color='gray')
plt.axvline(time_of_second_shutdown, color='gray')
plt.axvline(time_of_cap_1543, color='gray')
plt.legend()
plt.tight_layout()
plt.show()

# PLOT DETECTOR RATES OVER MISSION LIFETIME
with fetch.data_source('cxc', 'maude allow_subset={}'.format(allow_subset)):
    dat = fetch.get_telem(
        ['2PRBSVL', '2PRBSCR', '2S2HVST', '2PMT2T', '2S2HVLV', '2SHEV1RT'], '2020:220')
plt.clf()
dat['2PRBSVL'].plot(label='2PRBSVL', color=red, linewidth=2.0)
dat['2PRBSCR'].plot(label='2PRBSCR', color=blue, linewidth=2.0)
dat['2SHEV1RT'].plot(label='Shield Rate', color=purple, linewidth=2.0)
# dat['2S2HVST'].plot(label='2S2HVST', color=yellow, linewidth=2.0)
dat['2PMT2T'].plot(label='2PMT2T', color=yellow, linewidth=2.0)
# dat['2S2HVLV'].plot(label='2S2HVLV', color='black', linewidth=2.0)


plt.axvline(eventdate, color='gray')
plt.axvline(hrc_poweroff_date, color='gray')
plt.axvline(cap_step_2, color='gray')
plt.axvline(time_of_second_anomaly, color='gray')
plt.axvline(time_of_second_shutdown, color='gray')
plt.axvline(time_of_cap_1543, color='gray')
# plt.legend()
plt.tight_layout()
plt.show()


# PLOT DETECTOR RATES OVER MISSION LIFETIME
with fetch.data_source('cxc'):
    dat = fetch.get_telem(['2DETART', '2DETBRT'], '2000:001', sampling='5min')
plt.clf()
dat['2DETART'].plot(label='2DETART', color=red)
dat['2DETBRT'].plot(label='2DETBRT', color=blue)

plt.axvline(eventdate, color='gray')
plt.axvline(hrc_poweroff_date, color='gray')
plt.axvline(cap_step_2, color='gray')
plt.axvline(time_of_second_anomaly, color='gray')
plt.axvline(time_of_second_shutdown, color='gray')
plt.axvline(time_of_cap_1543, color='gray')
plt.legend()
plt.tight_layout()
plt.show()


colors_to_use = [yellow, blue, green, red]

fig, ax = plt.subplots(figsize=(20, 12))

rasterized = True
markersize = 1.8

ax.axvline(eventdate, color='gray')
ax.axvline(hrc_poweroff_date, color='gray')
ax.axvline(cap_step_2, color='gray')
ax.axvline(time_of_second_anomaly, color='gray')
ax.axvline(time_of_second_shutdown, color='gray')
ax.axvline(time_of_cap_1543, color='gray')

for msid, color in zip(voltage_msids, colors_to_use):
    print('Fetching MAUDE MSID {} ... '.format(msid), end="")
    msid = fetch.MSID(msid, start='2020:234')
    print('Done')
    times = hrc.convert_chandra_time(msid.times)
    vals = msid.vals
    cut_aside_mdate = mdate.date2num(time_of_cap_1543)
    stop_aplot_idx = np.where(times > cut_aside_mdate)[0][0]
    ax.plot_date(times[:stop_aplot_idx], vals[:stop_aplot_idx],
                 markersize=markersize, rasterized=rasterized, color=color,  label=msid.MSID)

for msid, color in zip(voltage_msids_b, colors_to_use):
    print('Fetching MAUDE MSID {} ... '.format(msid), end="")
    msid = fetch.MSID(msid, start='2020:244')
    print('Done')
    times = hrc.convert_chandra_time(msid.times)
    vals = msid.vals
    start_bplot_idx = np.where(times < cut_aside_mdate)[0][0]
    ax.plot_date(times[start_bplot_idx:], vals[start_bplot_idx:],
                 markersize=markersize, rasterized=rasterized, color=color,  label=msid.MSID)

ax.set_ylabel('Bus Voltage (V)')
ax.set_xlabel('Date (UTC)')

xmin = dt.datetime(2020, 8, 23, 12)
xmax = end_date
ax.set_xlim(xmin, xmax)
ax.set_ylim(-30, 30)

plt.show()
