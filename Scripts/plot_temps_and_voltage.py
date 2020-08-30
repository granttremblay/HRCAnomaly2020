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
fetch.data_source.set('maude allow_subset=True')

hrc.styleplots()

temp_alpha = 1.0  # set the opacity of the voltage plot.
voltage_alpha = 0.0  # set the opacity of the voltage plot.

# Grab the ggplot colors so you can manually set them if needed
colortable = plt.rcParams['axes.prop_cycle'].by_key()['color']
red = colortable[0]
blue = colortable[1]
yellow = colortable[4]
green = colortable[5]
pink = colortable[6]
purple = colortable[2]

sunday_pass = dt.datetime(2020, 8, 24, 2, 30)
sunday_pass_end = dt.datetime(2020, 8, 24, 3, 27, 34)

eventdate = mdate.num2date(hrc.convert_chandra_time([714627954.9676153660]))
fa6_heater_poweroff = dt.datetime(2020, 8, 24, 14, 38)
hrc_poweroff_date = dt.datetime(2020, 8, 24, 15, 7, 26)
morning_pass_time = dt.datetime(2020, 8, 24, 13, 45)
evening_pass_time = dt.datetime(2020, 8, 24, 21, 20)

tuesday_community_brief = dt.datetime(2020, 8, 25, 13, 0)
wednesday_community_brief = dt.datetime(2020, 8, 26, 13, 0)

cap_step_2 = dt.datetime(2020, 8, 27, 0, 13)
cap_step_5 = dt.datetime(2020, 8, 27, 0, 24)
cap_step_8 = dt.datetime(2020, 8, 27, 0, 40)

# The famous 6am pass in which everything looked fine
thursday_early_pass = dt.datetime(2020, 8, 27, 10, 0)
thursday_early_pass_end = dt.datetime(2020, 8, 27, 11, 0)

# I got the time of second anomaly from the first bad frame in the data. That is the Chandra time stamp below.
time_of_second_anomaly = hrc.convert_chandra_time([714916399.97800004])
human_time_of_second_anomaly = mdate.num2date(
    time_of_second_anomaly)  # Just to have a human-readable time

time_of_secont_shutdown = hrc.convert_chandra_time([714951463.18])
human_time_of_second_shutdown = mdate.num2date(
    time_of_secont_shutdown)  # Just to have a human-readable time

voltage_msids = ['2P24VAVL',  # 24 V bus EED voltage,
                 '2P15VAVL',  # +15 V bus EED voltage
                 '2P05VAVL',  # +05 V bus EED voltage
                 '2N15VAVL'  # +15 V bus EED voltage
                 ]

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


rate_msids = ['2TLEV1RT',  # The Total Event Rate
              '2VLEV1RT',  # VAlie Event Rate
              '2SHEV1RT',  # Shield Event Rate
              ]


all_relevant_hrc_msids = ["2SHEV1RT",  # HRC AntiCo Shield Rates (1)
                          "2TLEV1RT",  # HRC Detector Event Rates (c/s) (1)
                          "2PRBSVL",   # Primary Bus Voltage (V)
                          "2PRBSCR",   # Primary Bus Current (amps)
                          "2C05PALV",  # +5V Bus Monitor
                          "2C15NALV",  # -15V Bus Monitor
                          "2C15PALV",  # +15V Bus Monitor
                          "2C24PALV",  # +24V Bus Monitor
                          "2FE00ATM",  # Front-end Temperature (c)
                          "2LVPLATM",  # LVPS Plate Temperature (c)
                          "2IMHVATM",  # Imaging Det HVPS Temperature (c)
                          "2IMINATM",  # Imaging Det Temperature (c)
                          # Spectroscopy Det HVPS Temperature (c)
                          "2SPHVATM",
                          "2SPINATM",  # Spectroscopy Det Temperature (c)
                          "2PMT1T",    # PMT 1 EED Temperature (c)
                          "2PMT2T",    # PMT 2 EED Temperature (c)
                          "2DCENTRT",  # Outdet2 EED Temperature (c)
                          "2FHTRMZT",  # FEABox EED Temperature (c)
                          "2CHTRPZT",  # CEABox EED Temperature (c)
                          "2FRADPYT",  # +Y EED Temperature (c)
                          "2CEAHVPT",  # -Y EED Temperature (c)
                          "2CONDMXT",  # Conduit Temperature (c)
                          "2UVLSPXT",  # Snout Temperature (c)
                          "2CE00ATM",  # CEA Temperature 1 (c)
                          "2CE01ATM",  # CEA Temperature 2 (c)
                          "2FEPRATM",  # FEA PreAmp (c)
                          "2SMTRATM",  # Selected Motor Temperature (c)
                          "2DTSTATT"  # OutDet1 Temperature (c)
                          ]

spacecraft_orbit_pseudomsids = ["Dist_SatEarth",  # Chandra-Earth distance (from Earth Center) (m)
                                # Pointing-Solar angle (from center) (deg)
                                "Point_SunCentAng"
                                ]

# Times flagged as Secondary Science Corruption
secondary_science_corruption = ["HRC_SS_HK_BAD"]

mission_events = ["obsids",
                  "orbits",
                  "dsn_comms",
                  "dwells",
                  "eclipses",
                  "rad_zones",
                  "safe_suns",
                  "scs107s",
                  "major_events"]


fetch.data_source.set('maude')
fig, ax = plt.subplots(figsize=(20, 12))

rasterized = True
markersize = 2


# ax.axvline(sunday_pass, color='gray')
# ax.axvline(sunday_pass_end, color='gray', linestyle='dashed')
ax.axvline(eventdate, color='red')
# ax.axvline(hrc_poweroff_date, color='gray')
# ax.axvline(cap_step_2, color='gray')
# ax.axvline(thursday_early_pass, color='gray')
# ax.axvline(thursday_early_pass_end, color='gray', linestyle='dashed')
ax.axvline(time_of_second_anomaly, color=red)

n_lines = len(temperature_msids)
color_idx = np.linspace(0, 1, n_lines)


for i, msid in zip(color_idx, temperature_msids):
    print('MAUDE FETCH...', end="")
    msid = fetch.MSID(msid, start='2020:225')
    print('DONE')

    times = hrc.convert_chandra_time(msid.times)

    if msid.unit == 'K':
        vals = msid.vals - 273.15
    else:
        vals = msid.vals

    if msid.content == 'hrc5eng':
        ax.plot_date(times, vals, markersize=markersize,
                     rasterized=rasterized, color=plt.cm.tab20(i), alpha=temp_alpha, label=msid.MSID)

vmsid = fetch.MSID('2P15VAVL', start='2020:225')
vtimes = hrc.convert_chandra_time(vmsid.times)
ax.plot_date(vtimes, vmsid.vals, color=blue, markersize=markersize,
             rasterized=rasterized, label='+15 V Bus (2P15VAVL)', alpha=voltage_alpha)


vmsid = fetch.MSID('2N15VAVL', start='2020:225')
vtimes = hrc.convert_chandra_time(vmsid.times)
ax.plot_date(vtimes, vmsid.vals + 7, color=red, markersize=markersize,
             rasterized=rasterized, label='-15 V Bus + 30 V (2N15VAVL)', alpha=voltage_alpha)

vmsid = fetch.MSID('2P24VAVL', start='2020:225')
vtimes = hrc.convert_chandra_time(vmsid.times)
ax.plot_date(vtimes, vmsid.vals - 20, color=yellow, markersize=markersize,
             rasterized=rasterized, label='+24 V Bus (2P25VAVL)', alpha=voltage_alpha)


# ax.text(mdate.num2date(time_of_second_anomaly - 3600), 15.2,
#         '+15 V Bus (V)', size=12, color=blue)

lgnd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
for i in range(len(lgnd.legendHandles)):
    lgnd.legendHandles[i]._legmarker.set_markersize(20)

ax.set_ylabel('Temperature (C)')
ax.set_xlabel('Date (UTC)')

xmin = dt.datetime(2020, 8, 23, 12)
xmax = dt.datetime(2020, 8, 30, 12)
ax.set_xlim(xmin, xmax)

ax.set_ylim(-20, 50)


plt.show()
