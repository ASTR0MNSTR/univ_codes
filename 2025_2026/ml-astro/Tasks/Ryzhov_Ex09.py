from astroML.datasets import fetch_sdss_sspp
import matplotlib.pyplot as plt
data = fetch_sdss_sspp()

use = data[:10000]

print(use.dtype.names)

logg = use["logg"]
teff = use["Teff"]

fig, ax = plt.subplots(1, 1, figsize=(12, 6))

ax.scatter(teff, logg, color='k', marker='.')

ax.set_xlabel('teff')
ax.set_ylabel('logg')

plt.savefig('logg_teff.pdf')
