
# FILTER THE DATA IN TIME
# "Good" time for our AR Lac observation is 2384.14999998 seconds
# GTI start for March2020 osbervation is 7.01314133e+08, so 2384.149999 seconds later is 701316517.15

dmcopy "hrcm62650N000_evt2.fits[time=717738069.608:717740453.758]" newARlac_2384sec.fits
dmcopy "march2020_arlac_evt2.fits[time=701314133:701316517.15]" marchARlac_2384sec.fits

punlearn specextract
specextract "newARlac_2384sec.fits[sky=region(new_source.reg)]" newARlac_ bkgfile="newARlac_2384sec.fits[sky=region(new_bkg.reg)]" grouptype=NONE binspec=NONE
specextract "marchARlac_2384sec.fits[sky=region(march_source.reg)]" marchARlac_ bkgfile="marchARlac_2384sec.fits[sky=region(march_bkg.reg)]" grouptype=NONE binspec=NONE