import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.neighbors import KernelDensity
import os

# 1. Load data from ex26_data.dat
# The file contains headers and some null entries (H=0). 
# We skip the initial header lines and load H, a_prime, and sin_i_prime.

current_folder = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_folder, 'data', 'ex26_data.dat')

try:
    df = pd.read_csv(data_path, sep='\s+', skiprows=5, 
                     names=['H', 'a_prime', 'sin_i_prime'])
except Exception as e:
    print(f"Error reading file: {e}")

# 2. Select only the biggest asteroids (H < 18)
# We also filter out H <= 0 as these represent invalid/missing data in this dataset.
df_filtered = df[(df['H'] < 18) & (df['H'] > 0)]

a = df_filtered['a_prime'].values
sini = df_filtered['sin_i_prime'].values
X = np.column_stack([a, sini])

# 3. Density Estimation Setup
# Create a grid for evaluating the density
a_grid = np.linspace(2.0, 3.6, 100)
sini_grid = np.linspace(0, 0.3, 100)
A, S = np.meshgrid(a_grid, sini_grid)
grid_coords = np.column_stack([A.ravel(), S.ravel()])

# Kernels requested: Gaussian, Top-Hat, Exponential
kernels = ['gaussian', 'tophat', 'exponential']
bandwidth = 0.02  # Heuristic bandwidth for asteroid belt structures
densities = {}

for kernel in kernels:
    kde = KernelDensity(kernel=kernel, bandwidth=bandwidth)
    kde.fit(X)
    # kde.score_samples returns log-density
    log_dens = kde.score_samples(grid_coords)
    densities[kernel] = np.exp(log_dens).reshape(A.shape)

# 4. Plotting the Results
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.subplots_adjust(hspace=0.3, wspace=0.3)

# Subplot 1: Raw Scatter Plot
axes[0, 0].scatter(a, sini, s=0.5, c='black', alpha=0.3)
axes[0, 0].set_title(r'Scatter Plot (Asteroids with $H < 18$)')
axes[0, 0].set_xlim(2.0, 3.6)
axes[0, 0].set_ylim(0, 0.3)
axes[0, 0].set_xlabel("$a'$ (AU)")
axes[0, 0].set_ylabel("$\sin i'$")

# Subplots 2-4: Kernel Density Estimations
titles = ['Gaussian Kernel', 'Top-Hat Kernel', 'Exponential Kernel']
for i, kernel in enumerate(kernels):
    ax = axes.flatten()[i+1]
    im = ax.imshow(densities[kernel], origin='lower', 
                   extent=[2.0, 3.6, 0, 0.3], aspect='auto', cmap='Blues')
    ax.set_title(f'KDE: {titles[i]}')
    ax.set_xlabel("$a'$ (AU)")
    ax.set_ylabel("$\sin i'$")
    plt.colorbar(im, ax=ax, label='Density')

plt.tight_layout()
plt.show()

print(f"Total asteroids processed: {len(df_filtered)}")
