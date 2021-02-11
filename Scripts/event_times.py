#!/usr/bin/env python

import datetime as dt

import matplotlib.pyplot as plt
import matplotlib.dates as mdate

import numpy as np

# from hrcmonitor import convert_chandra_time




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



# Use today's date, plus 2 days
end_date = dt.date.today() + dt.timedelta(days=2)


sunday_pass = dt.datetime(2020, 8, 24, 2, 30)
sunday_pass_end = dt.datetime(2020, 8, 24, 3, 27, 34)

oneweek_pre_anomaly = dt.datetime(2020, 8, 18, 0)
oneday_pre_anomaly = dt.datetime(2020, 8, 23, 0)

eventdate = mdate.num2date(convert_chandra_time([714627954.9676153660]))
fa6_heater_poweroff = dt.datetime(2020, 8, 24, 14, 38)
hrc_poweroff_date = dt.datetime(2020, 8, 24, 15, 7, 26)
morning_pass_time = dt.datetime(2020, 8, 24, 13, 45)
evening_pass_time = dt.datetime(2020, 8, 24, 21, 20)

tuesday_community_brief = dt.datetime(2020, 8, 25, 13, 0)
wednesday_community_brief = dt.datetime(2020, 8, 26, 13, 0)

a_side_reset = dt.datetime(2020, 8, 27, 0, 13)
cap_step_2 = dt.datetime(2020, 8, 27, 0, 13)
cap_step_5 = dt.datetime(2020, 8, 27, 0, 24)
cap_step_8 = dt.datetime(2020, 8, 27, 0, 40)

# The famous 6am pass in which everything looked fine
thursday_early_pass = dt.datetime(2020, 8, 27, 10, 0)
thursday_early_pass_end = dt.datetime(2020, 8, 27, 11, 0)

# I got the time of second anomaly from the first bad frame in the data. That is the Chandra time stamp below.
time_of_second_anomaly = convert_chandra_time([714916399.97800004])
human_time_of_second_anomaly = mdate.num2date(
    time_of_second_anomaly)  # Just to have a human-readable time

time_of_second_shutdown = convert_chandra_time([714951463.18])
human_time_of_second_shutdown = mdate.num2date(
    time_of_second_shutdown)  # Just to have a human-readable time

time_of_cap_1543 = dt.datetime(2020, 8, 31, 17, 50)

time_of_cap_1545a = dt.datetime(2020, 9, 7, 23, 54)
