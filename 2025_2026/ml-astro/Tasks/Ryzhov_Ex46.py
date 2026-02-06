import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import optimize
import os
from astroML.datasets import fetch_hogg2010test

# Load data from the provided file (Hogg et al. 2010 Table 1)

data = fetch_hogg2010test()
x_orig = data['x']
y_orig = data['y']
dy_orig = data['sigma_y']

# --- Regression Functions ---

def squared_loss(m, b, x, y, dy):
    """Standard squared-loss (Ordinary Least Squares weighted by dy)"""
    y_fit = m * x + b
    return np.sum(((y - y_fit) / dy) ** 2)

def huber_loss(m, b, x, y, dy, c=1):
    """Huber loss: robust to outliers"""
    y_fit = m * x + b
    t = np.abs((y - y_fit) / dy)
    flag = t > c
    loss = np.where(flag, c * t - 0.5 * c**2, 0.5 * t**2)
    return np.sum(loss)

def get_fits(x, y, dy):
    """Compute the maximum likelihood for both loss functions"""
    beta0 = (0, 200)  # Initial guess (slope, intercept)
    f_sq = lambda beta: squared_loss(beta[0], beta[1], x, y, dy)
    f_hu = lambda beta: huber_loss(beta[0], beta[1], x, y, dy, c=1)
    
    beta_sq = optimize.fmin(f_sq, beta0, disp=False)
    beta_hu = optimize.fmin(f_hu, beta0, disp=False)
    return beta_sq, beta_hu

# --- Analysis ---

# 1. Identify biggest outlier from original fit (largest normalized residual)
beta_sq_orig, _ = get_fits(x_orig, y_orig, dy_orig)
residuals = np.abs((y_orig - (beta_sq_orig[0] * x_orig + beta_sq_orig[1])) / dy_orig)
outlier_idx = np.argmax(residuals)

# Case A: Original Data
beta_sq_A, beta_hu_A = get_fits(x_orig, y_orig, dy_orig)

# Case B: Biggest outlier uncertainty reduced 3x
dy_mod = dy_orig.copy()
dy_mod[outlier_idx] /= 3.0
beta_sq_B, beta_hu_B = get_fits(x_orig, y_orig, dy_mod)

# Case C: Biggest outlier removed
x_rem = np.delete(x_orig, outlier_idx)
y_rem = np.delete(y_orig, outlier_idx)
dy_rem = np.delete(dy_orig, outlier_idx)
beta_sq_C, beta_hu_C = get_fits(x_rem, y_rem, dy_rem)

# --- Plotting ---

fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharex=True, sharey=True)
x_fit = np.linspace(0, 350, 10)

titles = ["1) Original Data", "2) Outlier Unc. / 3", "3) Outlier Removed"]
datasets = [(x_orig, y_orig, dy_orig), (x_orig, y_orig, dy_mod), (x_rem, y_rem, dy_rem)]
fits = [(beta_sq_A, beta_hu_A), (beta_sq_B, beta_hu_B), (beta_sq_C, beta_hu_C)]

for i, ax in enumerate(axes):
    cx, cy, cdy = datasets[i]
    csq, chu = fits[i]
    
    # Plot data points
    ax.errorbar(cx, cy, cdy, fmt='.k', lw=1, ecolor='gray', alpha=0.5)
    
    # Plot fits
    ax.plot(x_fit, csq[0] * x_fit + csq[1], '--k', 
            label="Squared loss:\n$y=%.2fx + %.1f$" % (csq[0], csq[1]))
    ax.plot(x_fit, chu[0] * x_fit + chu[1], '-k', 
            label="Huber loss:\n$y=%.2fx + %.1f$" % (chu[0], chu[1]))
    
    # Highlight the outlier being discussed in panels 1 and 2
    if i < 2:
        ax.scatter(x_orig[outlier_idx], y_orig[outlier_idx], color='red', s=60, 
                   zorder=5, label='Biggest Outlier')
    
    ax.set_title(titles[i], fontweight='bold')
    ax.set_xlim(0, 350)
    ax.set_ylim(0, 750)
    ax.set_xlabel('$x$')
    if i == 0:
        ax.set_ylabel('$y$')
    ax.legend(loc='lower right', fontsize=8)
    ax.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.show()
