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
labelsizes = 12
plt.rcParams['axes.titlesize'] = labelsizes
plt.rcParams['axes.labelsize'] = labelsizes
plt.rcParams['xtick.labelsize'] = labelsizes
plt.rcParams['ytick.labelsize'] = labelsizes


# allow_subset=True should let us draw more data points
fetch.data_source.set('cxc', 'maude allow_subset=True')


def update_plot():

    rasterized = True
    markersize = 1.0
    colors_to_use = [yellow, blue, green, red]

    ax1.axvline(eventdate, color='gray')
    ax1.axvline(hrc_poweroff_date, color='gray')
    ax1.axvline(cap_step_2, color='gray')
    ax1.axvline(time_of_second_anomaly, color='gray')
    ax1.axvline(time_of_second_shutdown, color='gray')
    ax1.axvline(time_of_cap_1543, color='gray')

    print('Maude Fetch')
    for msid, color in zip(voltage_msids, colors_to_use):
        msid = fetch.MSID(msid, start='2020:234')
        times = hrc.convert_chandra_time(msid.times)
        vals = msid.vals
        cut_aside_mdate = mdate.date2num(time_of_cap_1543)
        stop_aplot_idx = np.where(times > cut_aside_mdate)[0][0]
        ax1.plot_date(times[:stop_aplot_idx], vals[:stop_aplot_idx],
                      markersize=markersize, rasterized=rasterized, color=color,  label=msid.MSID)

    for msid, color in zip(voltage_msids_b, colors_to_use):
        msid = fetch.MSID(msid, start='2020:244')
        times = hrc.convert_chandra_time(msid.times)
        vals = msid.vals
        start_bplot_idx = np.where(times < cut_aside_mdate)[0][0]
        ax1.plot_date(times[start_bplot_idx:], vals[start_bplot_idx:],
                      markersize=markersize, rasterized=rasterized, color=color,  label=msid.MSID)

    ax1.set_ylabel('Bus Voltage (V)')
    xmin = dt.datetime(2020, 8, 30, 12)
    xmax = end_date
    ax1.set_xlim(xmin, xmax)
    ax1.set_ylim(-30, 30)

    ax2.axvline(eventdate, color='gray')
    ax2.axvline(hrc_poweroff_date, color='gray')
    ax2.axvline(cap_step_2, color='gray')
    ax2.axvline(time_of_second_anomaly, color='gray')
    ax2.axvline(time_of_second_shutdown, color='gray')
    ax2.axvline(time_of_cap_1543, color='gray')

    ax2.axhline(-20, color='gray')
    ax2.axhline(-40, color=red)

    n_lines = len(temperature_msids)
    color_idx = np.linspace(0, 1, n_lines)

    for i, msid in zip(color_idx, temperature_msids):
        msid = fetch.MSID(msid, start='2020:234')

        times = hrc.convert_chandra_time(msid.times)

        if msid.unit == 'K':
            vals = msid.vals - 273.15
        else:
            vals = msid.vals

        if msid.content == 'hrc5eng':
            ax2.plot_date(times, vals, markersize=markersize,
                          rasterized=rasterized, color=plt.cm.tab20(i), label=msid.MSID)

    # lgnd = ax2.legend()
    # for i in range(len(lgnd.legendHandles)):
    #     lgnd.legendHandles[i]._legmarker.set_markersize(20)

    ax2.set_ylabel('Temperature (C)')

    ax2.set_xlim(xmin, xmax)

    ax2.set_ylim(-50, 50)

    current = fetch.get_telem(['2PRBSVL', '2PRBSCR'], '2020:220')
    current_times = hrc.convert_chandra_time(current['2PRBSCR'].times)
    ax3.plot_date(
        current_times, current['2PRBSCR'].vals, color=blue, markersize=markersize)

    ax3.axvline(eventdate, color='gray')
    ax3.axvline(hrc_poweroff_date, color='gray')
    ax3.axvline(cap_step_2, color='gray')
    ax3.axvline(time_of_second_anomaly, color='gray')
    ax3.axvline(time_of_second_shutdown, color='gray')
    ax3.axvline(time_of_cap_1543, color='gray')

    ax3.set_ylim(0, 3)
    ax3.set_ylabel('Redundant Bus Current (A)')

    ax3.set_xlabel('Date (UTC)')
    ax1.text(xmin, 32, 'Bus Voltages', color='slategray', fontsize=12)
    ax2.text(xmin, 51, 'Temperatures', color='slategray', fontsize=12)
    ax3.text(xmin, 3.1, 'S/C Redundant Bus Current',
             color='slategray', fontsize=12)


if __name__ == "__main__":
    plt.ion()
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    # plt.tight_layout()
    counter = 0
    while True:
        # plt.clf()
        update_plot()
        counter += 1
        # plt.suptitle("Iteration {} | {}".format(counter, dt.datetime.now()))
        plt.pause(60)
        plt.draw()
