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


from hrcsentinel import hrccore as hrc


# allow_subset=True should let us draw more data points
# fetch.data_source.set('maude allow_subset=True') fetch.data_source.set('cxc',
# 'maude allow_subset=True') Be careful if you mix cxc and maude telemetry.
# There is an offset between the DN-->count conversion.
# fetch.data_source.set('maude')

hrc.styleplots()
labelsizes = 8
plt.rcParams['axes.titlesize'] = labelsizes + 2
plt.rcParams['axes.labelsize'] = labelsizes
plt.rcParams['xtick.labelsize'] = labelsizes
plt.rcParams['ytick.labelsize'] = labelsizes


def convert_chandra_time(rawtimes):
    """
    Convert input CXC time (seconds since 1998.0) to the time base required for
    the matplotlib plot_date function (days since start of the Year 1 A.D).
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


def convert_to_doy(datetime_start):
    '''
    Return a string like '2020:237' that will be passed to start= in
    fetch.get_telem() and fetch.MSID(). Note that you have to zero-pad the day
    number e.g. 2020:002 instead of 2020:2, otherwise the pull will fail.
    '''

    year = datetime_start.year
    day_of_year = datetime_start.timetuple().tm_yday

    # you have to zero-pad the day number!
    doystring = '{}:{:03d}'.format(year, day_of_year)

    return doystring


def update_plot(counter, plot_start=dt.datetime(2020, 8, 31, 00), plot_end=dt.date.today() + dt.timedelta(days=2), sampling='full', current_hline=False, date_format=mdate.DateFormatter('%d %H')):
    plotnum = -1
    for i in range(3):
        for j in range(4):
            ax = plt.subplot2grid((3, 4), (i, j))
            plotnum += 1
            for msid in dashboard_msids[plotnum]:

                data = fetch.get_telem(
                    msid, start=convert_to_doy(plot_start), sampling=sampling, max_fetch_Mb=100000, max_output_Mb=100000, quiet=True)

                print('Fetched {} from {} at {} resolution.'.format(
                    msid, convert_to_doy(plot_start), sampling.upper()), end='\r', flush=True)
                # Clear the
                sys.stdout.write("\033[K")
                # Plot 12 is Pitch. That's a mess of points over the mission lifetime. So plot shield instead.
                # if plotnum == 11:
                #     data = fetch.get_telem(
                #         '2SHEV1RT', start=plot_start, sampling='daily', max_fetch_Mb=100000, max_output_Mb=100000)

                ax.plot_date(convert_chandra_time(
                    data[msid].times), data[msid].vals, markersize=1, label=msid)

                # Plot a HORIZONTAL line at location of last data point. Useful
                # for showing where we are w.r.t. the mission lifetime
                if current_hline is True:
                    ax.axhline(data[msid].vals[-1], color=green)

                ax.set_xlim(plot_start, plot_end)
                ax.set_ylabel(dashboard_units[plotnum])

                # if missionwide is True and plotnum == 11:
                #     ax.set_ylabel(r"Counts s$^{-1}$")

                ax.axvline(eventdate, color=red)
                ax.axvline(time_of_second_anomaly, color=red)
                ax.axvline(time_of_cap_1543, color='gray')
                ax.axvline(dt.datetime.now(pytz.utc),
                           color='gray', alpha=0.5)

                if plotnum == 0:
                    ax.text(dt.datetime.now(pytz.utc), 27,
                            'Now', fontsize=8, color='slategray')

                plt.gca().xaxis.set_major_formatter(date_format)
                ax.legend(prop={'size': 8}, loc=3)
                ax.set_title('{}'.format(
                    dashboard_tiles[plotnum]), color='slategray', loc='center')
                plt.suptitle('Iteration {} | Updated as of {} EST'.format(
                    counter, dt.datetime.now().strftime("%Y-%b-%d %H:%M:%S")), color='slategray', size=8)


def main():
    '''
    The main event loop. Sets plotting parameters and data sources, and makes
    both plots. Saves them to preferred directories. Pauses the loop for a few
    minutes of sleep to avoid overwhelming MAUDE and wasting cycles. 
    '''

    fig_save_directory = '/Users/grant/HEAD/data/wdocs/tremblay/HRCOps/plots/'
    # fig_save_directory = '/Users/grant/Desktop/'

    plt.ion()
    plt.figure(0, figsize=(16, 7))

    counter = 0

    while True:

        fetch.data_source.set('maude')

        print("Refreshing dashboard (Iteration {}) at {}".format(
            counter, dt.datetime.now().strftime("%Y-%b-%d %H:%M:%S")), flush=True)

        # Must be a DATETIME object! Beware, anything like datetime.now() will
        # return local time, not UTC!
        plot_end_today = dt.date.today() + dt.timedelta(days=2)

        update_plot(counter, plot_start=dt.datetime(2020, 9, 8, 12),
                    plot_end=plot_end_today, sampling='full')

        counter += 1

        plt.tight_layout()
        plt.draw()
        plt.savefig(fig_save_directory + 'status.png', dpi=300)

        fetch.data_source.set('cxc')

        update_plot(counter, plot_start=dt.datetime(
            2000, 1, 1), plot_end=None, sampling='daily', date_format=mdate.DateFormatter('%y-%m'), current_hline=True)

        plt.tight_layout()
        plt.draw()
        plt.savefig(fig_save_directory + 'status_wide.png', dpi=300)

        # try:
        #     plt.savefig(fig_save_directory + 'status_wide.png', dpi=300)
        #     print("Updated plots at {}".format(
        #         fig_save_directory),  flush=True)
        # except Exception as ex:
        #     print('Error: Cannot reach HEAD Network. Try MOUNTEAD?')
        #     print(ex)

        sleep_period_seconds = 120
        for i in range(0, sleep_period_seconds):
            # Normally output to a file or the console is buffered, with text
            # output at least until you print a newline. The flush makes sure
            # that any output that is buffered goes to the destination.
            print('Refreshing plots in {} seconds...'.format(
                sleep_period_seconds-i), end="\r", flush=True)
            time.sleep(1)


if __name__ == "__main__":
    main()
