#!/usr/bin/env python

import os
import sys
import shutil
import time
import pytz
import traceback

from pathlib import Path

# import Ska.engarchive.fetch as fetch
from Ska.engarchive import fetch_sci as fetch
import Chandra.Time

import datetime as dt
import matplotlib.dates as mdate
from matplotlib import gridspec

import numpy as np
import pandas as pd
from astropy.table import Table


from tqdm import tqdm as progressbar


fetch.data_source.set('cxc allow_subset=False')


def convert_to_doy(datetime_start):
    '''
    Return a string like '2020:237' that will be passed to start= in fetch.get_telem()
    '''

    year = datetime_start.year
    day_of_year = datetime_start.timetuple().tm_yday
    doystring = '{}:{}'.format(year, day_of_year)

    return doystring


def convert_chandra_time(rawtimes):
    """
    Convert input CXC time (sec) to the time base required for the matplotlib
    plot_date function (days since start of the Year 1 A.D - yes, really).
    :param times: iterable list of times, in units of CXCsec (sec since 1998.0)
    :rtype: plot_date times (days since Year 1 A.D.)
    """

    # rawtimes is in units of CXC seconds, or seconds since 1998.0
    # Compute the Delta T between 1998.0 (CXC's Epoch) and 1970.0 (Unix Epoch)

    seconds_since_1998_0 = rawtimes[0]

    cxctime = dt.datetime(1998, 1, 1, 0, 0, 0)
    unixtime = dt.datetime(1970, 1, 1, 0, 0, 0)

    # Calculate the first offset from 1970.0, needed by matplotlib's plotdate
    # The below is equivalent (within a few tens of seconds) to the command
    # t0 = Chandra.Time.DateTime(times[0]).unix
    delta_time = (cxctime - unixtime).total_seconds() + seconds_since_1998_0

    plotdate_start = mdate.epoch2num(delta_time)

    # Now we use a relative offset from plotdate_start
    # the number 86,400 below is the number of seconds in a UTC day

    chandratime = (np.asarray(rawtimes) -
                   rawtimes[0]) / 86400. + plotdate_start

    return chandratime


def tom_msids():

    msids = ['2P05VAVL', '2N15VAVL', '2P24VAVL', '2DETART', '2SHLDART', '2C05PALV', '2C15PALV', '2C24PALV',
             '2PRBSCR', '2PRBSVL', '2IMHBLV', '2IMHVLV', '2IMHBLV', '2SPHVLV', '2S1HVLV', '2S2HVLV', '2SMOIAST', '2SMOTAST']

    return msids


def main():
    home = str(Path.home())

    data_start = convert_to_doy(dt.datetime(2020, 8, 23, 0, 0))
    data_stop = convert_to_doy(dt.datetime(2020, 8, 29, 0, 0))

    msids = tom_msids()

    dat = fetch.MSIDset(msids, start=data_start, stop=data_stop)

    # data_columns = []

    # # [dat['2CEAHVPT'].times,
    # #                 mdate.num2date(convert_chandra_time(dat['2CEAHVPT'].times))]

    # column_names = []

    # ['Chandra Time',
    #                 'Human-readable time (UTC)']

    for item in progressbar(msids):

        columns = [dat[item].times, dat[item].vals]
        names = [f'{item} Times', f'{item} Values']

        df = pd.DataFrame(data=columns).T
        df.columns = names

        df.to_excel(os.path.join(home, f'Desktop/{item}.xlsx'))


if __name__ == '__main__':
    main()
