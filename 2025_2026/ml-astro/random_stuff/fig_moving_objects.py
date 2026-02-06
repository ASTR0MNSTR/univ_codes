"""
SDSS Moving Object Data
-----------------------
Figure 1.8.

The orbital semimajor axis vs. the orbital inclination angle diagram for the
first 10,000 catalog entries from the SDSS Moving Object Catalog (after
applying several quality cuts). The gaps at approximately 2.5, 2.8, and 3.3 AU
are called the Kirkwood gaps and are due to orbital resonances with Jupiter.
The several distinct clumps are called asteroid families and represent remnants
from collisions of larger asteroids.
"""
# Author: Jake VanderPlas
# License: BSD
#   The figure produced by this code is published in the textbook
#   "Statistics, Data Mining, and Machine Learning in Astronomy" (2013)
#   For more information, see http://astroML.github.com
#   To report a bug or issue, use the following forum:
#    https://groups.google.com/forum/#!forum/astroml-general
from matplotlib import pyplot as plt
from astroML.datasets import fetch_moving_objects
import pandas as pd
import numpy as np
from astroML.density_estimation import KNeighborsDensity
from matplotlib.colors import LogNorm

#----------------------------------------------------------------------
# This function adjusts matplotlib settings for a uniform feel in the textbook.
# Note that with usetex=True, fonts are rendered with LaTeX.  This may
# result in an error if LaTeX is not installed on your system.  In that case,
# you can set usetex to False.
if "setup_text_plots" not in globals():
    from astroML.plotting import setup_text_plots
setup_text_plots(fontsize=8, usetex=True)

#------------------------------------------------------------
# Fetch the moving object data
# data = fetch_moving_objects(Parker2008_cuts=True)

# Use only the first 10000 points
# data = data[:10000]

df = pd.read_csv("asteroids.dat", sep="\s+", header=None, names=['H', 'a', 'sin'])

df = df[(df['H'] > 1.0) & (df['H'] < 18.0)]

a = df['a']
sini = df['sin']

#
#
 
X = np.vstack((a, sini)).T

#------------------------------------------------------------
# Create  the grid on which to evaluate the results
Nx = 50
Ny = 50
xmin, xmax = (2.0, 3.6)
ymin, ymax = (-0.01, 0.31)

#------------------------------------------------------------
# Evaluate for several models
Xgrid = np.vstack(list(map(np.ravel, np.meshgrid(np.linspace(xmin, xmax, Nx),
                                            np.linspace(ymin, ymax, Ny))))).T

#kde = KernelDensity(kernel='gaussian', bandwidth=5)
#log_pdf_kde = kde.fit(X).score_samples(Xgrid).reshape((Ny, Nx))
#dens_KDE = np.exp(log_pdf_kde)

#knn5 = KNeighborsDensity('bayesian', 5)
#dens_k5 = knn5.fit(X).eval(Xgrid).reshape((Ny, Nx))

knn40 = KNeighborsDensity('bayesian', 40)
dens_k40 = knn40.fit(X).eval(Xgrid).reshape((Ny, Nx))

#------------------------------------------------------------
# Plot the results
fig, ax = plt.subplots(figsize=(5, 5))
ax.plot(a, sini, '.', markersize=2, color='black')
ax.imshow(dens_k40.T, origin='lower', norm=LogNorm(),
           extent=(ymin, ymax, xmin, xmax), cmap=plt.cm.binary)
ax.text(0.95, 0.9, "$k$-neighbors $(k=40)$", ha='right', va='top',
         transform=ax.transAxes,
         bbox=dict(boxstyle='round', ec='k', fc='w'))

ax.set_xlim(2.0, 3.6)
ax.set_ylim(-0.01, 0.31)

ax.set_xlabel('Semimajor Axis (AU)')
ax.set_ylabel('Sine of Inclination Angle')

plt.show()
