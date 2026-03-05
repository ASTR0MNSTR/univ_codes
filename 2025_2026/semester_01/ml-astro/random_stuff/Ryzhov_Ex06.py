from astroML.datasets import fetch_imaging_sample
data=fetch_imaging_sample()
objtype = data['type']
stars = data[objtype == 6][:5]
stars_r = stars['rRawPSF']
stars_err_r = stars['rpsfErr']

for i, item in enumerate(stars_r):
    print("{:3f} +/- {:3f}".format(item, stars_err_r[i]))
