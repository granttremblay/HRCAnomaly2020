#!/usr/bin/env conda run -n ska3 python
import shutil
import time
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
fetch.data_source.set('maude')

hrc.styleplots()
labelsizes = 8
plt.rcParams['axes.titlesize'] = labelsizes + 2
plt.rcParams['axes.labelsize'] = labelsizes
plt.rcParams['xtick.labelsize'] = labelsizes
plt.rcParams['ytick.labelsize'] = labelsizes


def update_plot(counter):
    plotnum = -1
    for i in range(3):
        for j in range(4):
            ax = plt.subplot2grid((3, 4), (i, j))
            plotnum += 1
            for msid in progressbar(dashboard_msids[plotnum]):
                data = fetch.get_telem(msid, start="2020:245")
                ax.plot_date(hrc.convert_chandra_time(
                    data[msid].times), data[msid].vals, markersize=1, label=msid)
                xmin = dt.datetime(2020, 9, 7, 12)
                xmax = dt.datetime(2020, 9, 8, 12)
                ax.set_xlim(xmin, xmax)
                ax.axvline(time_of_cap_1543, color='gray')
                # ax.format_xdata = mdate.DateFormatter('%m-%d')
                # here you can format your datetick labels as desired
                myFmt = mdate.DateFormatter('%m-%d')
                plt.gca().xaxis.set_major_formatter(myFmt)
                ax.legend(prop={'size': 8}, loc=3)
                ax.set_title('{}'.format(
                    dashboard_tiles[plotnum]), color='slategray', loc='center')
                plt.suptitle('Iteration {} | {}'.format(
                    counter, dt.datetime.now()), color='slategray', size=8)


if __name__ == "__main__":

    fig_save_directory = '/Users/grant/HEAD/data/wdocs/tremblay/HRCOps/plots/'

    plt.ion()
    plt.figure(0, figsize=(16, 7))
    # plt.tight_layout()
    counter = 0
    while True:
        # plt.clf()
        update_plot(counter)
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
