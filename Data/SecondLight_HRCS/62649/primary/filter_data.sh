dmcopy "hrcf62649N001_evt2.fits.gz[time=720021888.647:720026453.997]" hrcS_arlac_goodtime_evt2.fits
# That worked. GTI is clean and now says: FITS_rec([(7.20021889e+08, 7.20026452e+08)],


specextract "hrcS_arlac_goodtime_evt2.fits[sky=region(source.reg)]" spec bkgfile="hrcS_arlac_goodtime_evt2.fits[sky=region(source.reg)]" grouptype=NONE binspec=NONE