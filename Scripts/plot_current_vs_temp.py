from kadi import events
from Chandra.Time import DateTime
from Ska.engarchive import fetch_eng as fetch
import numpy as np
import matplotlib.pyplot as plt


msid1 = '2PRBSCR'
msid2 = '2CHTRPZT'

e1_start = '2000:001'
e1_stop = '2020:180'

dwells = events.dwells
dwells.interval_pad = (-300)
dwells.interval_pad
e1_intervals = dwells.intervals(e1_start, e1_stop)

# below gets start and end time for each interval
# also filter on observations greater than 10ks

e1_intervals = [i for i in e1_intervals if np.diff(DateTime(i).secs) >10000]
e1 = DateTime([t[1] for t in e1_intervals]).secs
s1 = DateTime([t[0] for t in e1_intervals]).secs

# now get the data
d1 = fetch.Msidset([msid1,msid2], e1_start, e1_stop)
d1.interpolate()
t1 = np.interp(e1, d1.times, d1[msid2].vals)
c1 = np.interp(e1, d1.times, d1[msid1].vals)

t1_0 = np.interp(s1, d1.times, d1[msid2].vals)
c1_0 = np.interp(s1, d1.times, d1[msid1].vals)

sign1 = np.sign(t1 - t1_0)

pe1 = plt.plot(t1[sign1 < 0], c1[sign1 < 0], 'b.', alpha=0.5, label='cooling')
plt.hold(True)
plt.plot(t1[sign1 > 0], c1[sign1 > 0], 'r.', alpha=0.5, label='warming')
plt.xlabel('Temperature (2CHTRPZT)')
plt.ylabel('Current (2PRBSCR)')
plt.legend()
