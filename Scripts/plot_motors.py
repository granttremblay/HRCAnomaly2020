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

motor = fetch.get_telem(["2MSDRAMD", ], start='2000:001', sampling='5min')

motor_values = []
motor_register_values = []
for event in motor["2MSDRAMD"].vals:
    if event == 'ENAB':
        motor_values.append(1.0)
    elif event == 'DISA':
        motor_values.append(0.0)

motor_register = fetch.get_telem("2MDRVAST", start='2000:001', sampling='5min')
for event in motor_register["2MDRVAST"].vals:
    if event == 'ENAB':
        motor_register_values.append(1.0)
    elif event == 'DISA':
        motor_register_values.append(0.0)


current = fetch.get_telem("2PRBSCR", start='2000:001', sampling='5min')


fig, ax = plt.subplots(figsize=(12, 6))

ax.plot_date(hrc.convert_chandra_time(
    motor["2MSDRAMD"].times), motor_values, markersize=markersize, label='Motor Drive Enable (0 = DISA, 1 = ENAB)')
ax.plot_date(hrc.convert_chandra_time(
    current["2PRBSCR"].times), current["2PRBSCR"].vals, markersize=markersize, label='S/C Bus Current (2PRBSCR) (A)')

# ax.plot_date(hrc.convert_chandra_time(
#     motor_register["2MDRVAST"].times), motor_register_values, markersize=markersize, label='S/C Bus Current (2PRBSCR) (A)')


# both = fetch.get_telem(["2PRBSCR", "2MSDRAMD"],
#                        start='2000:001', stop='2010:001', sampling='5min')
# motor_values = []
# motor_register_values = []
# for event in both["2MSDRAMD"].vals:
#     if event == 'ENAB':
#         motor_values.append(1.0)
#     elif event == 'DISA':
#         motor_values.append(0.0)


# ax.scatter(motor_values, both["2PRBSCR"].vals)
# # sns.jointplot(x=motor_values, y=both["2PRBSCR"].vals, kind="kde")

ax.legend()

plt.show()
