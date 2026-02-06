from astroquery.sdss import SDSS
from astropy import coordinates as coords
import astropy.units as u
from matplotlib import pyplot as plt  

spec = SDSS.get_spectra(plate=266, fiberID=4, mjd=51630)[0]  # pobranie FITS

data = spec[1].data
wavelength = 10 ** data['loglam']
flux = data['flux']

plt.figure(figsize=(5,3.75))
plt.plot(wavelength, flux, '-k', lw=1)
plt.xlabel('Wavelength [Ă]')
plt.ylabel('Flux')
#plt.title('SDSS Spectrum: Plate=1615, MJD=53166, Fiber=513')
plt.savefig('./figures/4.pdf')
