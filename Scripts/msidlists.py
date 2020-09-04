#!/usr/bin/env python

import datetime as dt

import matplotlib.pyplot as plt
import matplotlib.dates as mdate

from hrcsentinel import hrccore as hrc


# MSIDlists

voltage_msids = ['2P24VAVL',  # 24 V bus EED voltage,
                 '2P15VAVL',  # +15 V bus EED voltage
                 '2P05VAVL',  # +05 V bus EED voltage
                 '2N15VAVL'  # +15 V bus EED voltage
                 ]

voltage_msids_b = ['2P24VBVL',  # 24 V bus EED voltage,
                   '2P15VBVL',  # +15 V bus EED voltage
                   '2P05VBVL',  # +05 V bus EED voltage
                   '2N15VBVL'  # +15 V bus EED voltage
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
