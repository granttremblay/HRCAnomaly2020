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
# import mpld3

import numpy as np
import pandas as pd

import numpy as np
from scipy.interpolate import spline
from scipy.interpolate import interp1d
from scipy.signal import hilbert


from msidlists import *
from event_times import *
from plot_stylers import *


def compute_yearly_average(values, window):

    array = values

    cumulative_sum, moving_aves = [0], []

    for i, x in enumerate(array, 1):
        cumulative_sum.append(cumulative_sum[i-1] + x)
        if i >= window:
            moving_ave = (cumulative_sum[i] - cumulative_sum[i-window])/window
            # can do stuff with moving_ave here
            moving_aves.append(moving_ave)

    # Ensure that this is a Numpy array, so that we can do some proper vector math with it.
    moving_ave_array = np.asarray(moving_aves)
    return moving_ave_array


all_trends = {}

for msidname in temperature_msids:
    moving_aves = compute_yearly_average(
        data["{}_values".format(msidname)], window)
    moving_stds = compute_yearly_average(
        data["{}_stds".format(msidname)], window)
    all_trends["{}_trend".format(msidname)] = moving_aves
    all_trends["{}_stds".format(msidname)] = moving_stds
