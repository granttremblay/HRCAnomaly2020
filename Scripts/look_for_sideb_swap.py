#!/usr/bin/env conda run -n ska3 python

import Ska.engarchive.fetch as fetch
import Chandra.Time

import datetime as dt
import matplotlib.dates as mdate
from matplotlib import gridspec

import matplotlib.pyplot as plt

import numpy as np

from hrcsentinel import hrccore as hrc

# allow_subset=True should let us draw more data points
fetch.data_source.set('cxc')
# fetch.data_source.set('maude')

hrc.styleplots()


fig, ax = plt.subplots()

msid = fetch.MSID('2P05VBVL', start=1999)
