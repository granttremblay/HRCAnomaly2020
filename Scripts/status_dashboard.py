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
import mpld3

import numpy as np
import pandas as pd

from msidlists import *
from event_times import *
from plot_stylers import *

from tqdm import tqdm as progressbar

from hrcsentinel import hrccore as hrc


# allow_subset=True should let us draw more data points
# fetch.data_source.set('maude allow_subset=True')
# fetch.data_source.set('cxc', 'maude allow_subset=True')
# Be careful if you mix cxc and maude telemetry. There is an offset between the DN-->count conversion.
fetch.data_source.set('maude')

hrc.styleplots()
labelsizes = 8
plt.rcParams['axes.titlesize'] = labelsizes + 2
plt.rcParams['axes.labelsize'] = labelsizes
plt.rcParams['xtick.labelsize'] = labelsizes
plt.rcParams['ytick.labelsize'] = labelsizes


def convert_to_doy(datetime_start):
    '''
    Return a string like '2020:237' that will be passed to start= in fetch.get_telem()
    '''

    year = datetime_start.year
    day_of_year = datetime_start.timetuple().tm_yday
    doystring = '{}:{}'.format(year, day_of_year)

    return doystring


def update_plot(counter, plot_start=dt.datetime(2020, 8, 31, 00), plot_end=dt.date.today() + dt.timedelta(days=2)):
    plotnum = -1
    for i in range(3):
        for j in progressbar(range(4)):
            ax = plt.subplot2grid((3, 4), (i, j))
            plotnum += 1
            for msid in dashboard_msids[plotnum]:

                # Make the fetch silent on command line
                # print("Fetching {}".format(msid), end="")
                sys.stdout = open(os.devnull, "w")
                # Fetch the telemetry
                data = fetch.get_telem(msid, start=convert_to_doy(plot_start))
                # Allow printing again
                sys.stdout = sys.__stdout__

                ax.plot_date(hrc.convert_chandra_time(
                    data[msid].times), data[msid].vals, markersize=1, label=msid)

                ax.set_xlim(plot_start, plot_end)
                ax.axvline(time_of_cap_1543, color='gray')
                ax.axvline(dt.datetime.now(pytz.utc), color='gray', alpha=0.5)

                myFmt = mdate.DateFormatter('%d %H')
                plt.gca().xaxis.set_major_formatter(myFmt)
                ax.legend(prop={'size': 8}, loc=3)
                ax.set_title('{}'.format(
                    dashboard_tiles[plotnum]), color='slategray', loc='center')
                plt.suptitle('Iteration {} | {}'.format(
                    counter, dt.datetime.now()), color='slategray', size=8)


if __name__ == "__main__":

    # Must be a DATETIME object! Beware, anything like datetime.now() will return local time, not UTC!
    plot_start = dt.datetime(2020, 9, 7, 12)
    plot_end = dt.date.today() + dt.timedelta(days=2)

    fig_save_directory = '/Users/grant/HEAD/data/wdocs/tremblay/HRCOps/plots/'

    plt.ion()
    plt.figure(0, figsize=(16, 7))
    # plt.tight_layout()
    counter = 0
    while True:
        print("Refreshing dashboard (iteration {}) at {}".format(
            counter, dt.datetime.now()))
        update_plot(counter, plot_start, plot_end)
        counter += 1
        plt.tight_layout()
        plt.draw()
        try:
            plt.savefig(fig_save_directory + 'status.png', dpi=300)
            print("Updated plot: {}status.png".format(fig_save_directory))
        except Exception as ex:
            print('Error: Cannot reach HEAD Network. Try MOUNTEAD?')
            print(ex)

        plt.pause(120)
