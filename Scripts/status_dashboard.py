#!/usr/bin/env conda run -n ska3 python

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

from hrcsentinel import hrccore as hrc


# allow_subset=True should let us draw more data points
# fetch.data_source.set('maude allow_subset=True')
fetch.data_source.set('maude')

hrc.styleplots()
labelsizes = 8
plt.rcParams['axes.titlesize'] = labelsizes
plt.rcParams['axes.labelsize'] = labelsizes
plt.rcParams['xtick.labelsize'] = labelsizes
plt.rcParams['ytick.labelsize'] = labelsizes


plt.figure(0, figsize=(10, 8))
plots = []
plotnum = -1
for i in range(3):
    for j in range(4):
        ax = plt.subplot2grid((3, 4), (i, j))
        plotnum += 1
        for msid in dashboard_msids[plotnum]:
            data = fetch.get_telem(msid, start="2020:245")
            ax.plot_date(hrc.convert_chandra_time(
                data[msid].times), data[msid].vals, markersize=1, label=msid)
            ax.axvline(time_of_cap_1543, color='gray')
            ax.format_xdata = mdate.DateFormatter('%m-%d')
            ax.legend(prop={'size': 8})
            ax.set_title('{}'.format(
                dashboard_tiles[plotnum]), color='gray', loc='center')

plt.show()
# mpld3.show()
