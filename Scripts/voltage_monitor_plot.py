#!/usr/bin/env conda run -n ska3 python

import Ska.engarchive.fetch as fetch
import Chandra.Time

import datetime as dt
import matplotlib.dates as mdate
from matplotlib import gridspec

import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

from anomaly_variables import *

from hrcsentinel import hrccore as hrc
hrc.styleplots()


# allow_subset=True should let us draw more data points
fetch.data_source.set('cxc', 'maude allow_subset=False')


fig, ax = plt.subplots(figsize=(20, 12))
i = 0
while True:
    i += 1
    plt.pause(1)

    rasterized = True
    markersize = 1.8
    colors_to_use = [yellow, blue, green, red]

    ax.axvline(eventdate, color='gray')
    ax.axvline(hrc_poweroff_date, color='gray')
    ax.axvline(cap_step_2, color='gray')
    ax.axvline(time_of_second_anomaly, color='gray')
    ax.axvline(time_of_second_shutdown, color='gray')

    ax.axvline(time_of_cap_1543, color='gray')

    for msid, color in zip(voltage_msids, colors_to_use):
        msid = fetch.MSID(msid, start='2020:234')
        times = hrc.convert_chandra_time(msid.times)
        vals = msid.vals
        cut_aside_mdate = mdate.date2num(time_of_cap_1543)
        stop_aplot_idx = np.where(times > cut_aside_mdate)[0][0]
        ax.plot_date(times[:stop_aplot_idx], vals[:stop_aplot_idx],
                     markersize=markersize, rasterized=rasterized, color=color,  label=msid.MSID)

    for msid, color in zip(voltage_msids_b, colors_to_use):
        msid = fetch.MSID(msid, start='2020:244')
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
    # ax.set_ylim(-20, 50)
    ax.set_ylim(-30, 30)

    ax.title('Iteration: {}'.format(i))

    plt.draw()
    print('REGENERATING PLOT')
