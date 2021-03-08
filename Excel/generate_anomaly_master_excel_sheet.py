#!/usr/bin/env python

import os
import sys
import shutil
import time
import pytz
import traceback

# import Ska.engarchive.fetch as fetch
from Ska.engarchive import fetch_sci as fetch
import Chandra.Time

import datetime as dt
import matplotlib.dates as mdate
from matplotlib import gridspec

import numpy as np
import pandas as pd
from astropy.table import Table

from hrcsentinel import hrccore as hrc

from tqdm import tqdm as progressbar


fetch.data_source.set('cxc')


def convert_to_doy(datetime_start):
    '''
    Return a string like '2020:237' that will be passed to start= in fetch.get_telem()
    '''

    year = datetime_start.year
    day_of_year = datetime_start.timetuple().tm_yday
    doystring = '{}:{}'.format(year, day_of_year)

    return doystring


def msids():

    temperature_msids = [
        "2FE00ATM",  # Front-end Temperature (c)
        "2LVPLATM",  # LVPS Plate Temperature (c)
        "2IMHVATM",  # Imaging Det HVPS Temperature (c)
        "2IMINATM",  # Imaging Det Temperature (c)
        "2SPHVATM",  # Spectroscopy Det HVPS Temperature (c)
        "2SPINATM",  # Spectroscopy Det Temperature (c)
        "2PMT1T",  # PMT 1 EED Temperature (c)
        "2PMT2T",  # PMT 2 EED Temperature (c)
        "2DCENTRT",  # Outdet2 EED Temperature (c)
        "2FHTRMZT",  # FEABox EED Temperature (c)
        "2CHTRPZT",  # CEABox EED Temperature (c)
        "2FRADPYT",  # +Y EED Temperature (c)
        "2CEAHVPT",  # -Y EED Temperature (c)
        "2CONDMXT",  # Conduit Temperature (c)
        "2UVLSPXT",  # Snout Temperature (c)
        # CEA Temperature 1 (c) THESE HAVE FEWER POINTS AS THEY WERE RECENTLY ADDED BY TOM
        "2CE00ATM",
        # CEA Temperature 2 (c) THESE HAVE FEWER POINTS AS THEY WERE RECENTLY ADDED BY TOM
        "2CE01ATM",
        "2FEPRATM",  # FEA PreAmp (c)
        # Selected Motor Temperature (c) THIS IS ALWAYS 5 DEGREES THROUGHOUT ENTIRE MISSION
        "2SMTRATM",
        "2DTSTATT"   # OutDet1 Temperature (c)
    ]

    return temperature_msids


def main():

    data_start = convert_to_doy(dt.datetime(2020, 8, 23, 0, 0))
    data_stop = convert_to_doy(dt.datetime(2020, 8, 29, 0, 0))

    temperature_msids = msids()

    dat = fetch.MSIDset(temperature_msids, start=data_start,
                        stop=data_stop)

    data_columns = [dat['2CEAHVPT'].times,
                    mdate.num2date(hrc.convert_chandra_time(dat['2CEAHVPT'].times))]

    column_names = ['Chandra Time',
                    'Human-readable time (UTC)']

    for item in progressbar(temperature_msids):
        data_columns.append(dat[item].vals)
        column_names.append(f'{item}')

    df = pd.DataFrame(data=data_columns).T
    df.columns = column_names

    df['Human-readable time (UTC)'] = df['Human-readable time (UTC)'].dt.tz_localize(None)

    df.to_excel('/Users/grant/Desktop/master_anomaly_excel.xlsx')


if __name__ == '__main__':
    main()
