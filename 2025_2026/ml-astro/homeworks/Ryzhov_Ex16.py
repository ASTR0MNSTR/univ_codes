import numpy as np
import matplotlib.pyplot as plt
import os

# CHANGE FOR YOUR PATH HERE
current_folder = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_folder, 'data', 'ex16_data.txt')
data = np.loadtxt(data_path)
ra = data[:, 0]  # 1st column (index 0)
dec = data[:, 1] # 2nd column (index 1)

# Convert RA from degrees to radians and shift by 120 deg (to the left)
ra_shifted = np.deg2rad(ra - 120)
dec_rad = np.deg2rad(dec)

# Prepare grid for projections
fig, axs = plt.subplots(2, 2, figsize=(8, 8), subplot_kw={'projection': 'aitoff'})
projections = ['aitoff', 'hammer', 'mollweide', 'lambert']

for ax, proj in zip(axs.flat, projections):
    ax.remove()  # Remove default Aitoff axes
    ax = fig.add_subplot(2, 2, list(axs.flat).index(ax)+1, projection=proj)
    ax.scatter(ra_shifted, dec_rad, s=10, color='red', alpha=0.7, marker='.')
    ax.set_title(proj.capitalize())
    # Grid with 30 deg step
    ax.grid(True, which='minor')
    ax.xaxis.set_minor_locator(plt.FixedLocator(np.pi / 6 * np.linspace(-1, 9, 11)))
    xlab = ['330','0','30','60','90','120','150','180','210','240','270']
    ax.set_xticklabels(xlab)
    ax.set_xlabel('RA')
    ax.set_ylabel('DEC')

plt.tight_layout()
plt.show()