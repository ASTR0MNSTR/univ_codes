import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.odr import ODR, Model, RealData
from scipy.stats import linregress
import os

# Load the data
current_folder = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_folder, 'data', 'ex45a_data.txt')

df = pd.read_csv(data_path, sep='\s+')
x = df['x'].values
y = df['y'].values
sig_x = df['sig_x'].values
sig_y = df['sig_y'].values

# Define linear model for ODR: y = m*x + c
def linear_model_func(p, x):
    return p[0] * x + p[1]

# Setup for plotting fits
x_range = np.linspace(x.min() - 20, x.max() + 20, 100)

plt.figure(figsize=(10, 7))

# 1) Plot data with errorbars (Black dots, size 10)
plt.errorbar(x, y, xerr=sig_x, yerr=sig_y, fmt='o', color='black', markersize=10, 
             label='Data with errorbars', elinewidth=1, capsize=2, zorder=3)

# 2) Linear fit: no uncertainties (OLS) - red dashed line
res_ols = linregress(x, y)
m_ols, c_ols = res_ols.slope, res_ols.intercept
plt.plot(x_range, m_ols * x_range + c_ols, color='red', linestyle='--', label='Fit: no uncertainties')

# 3) Linear fit: uncertainties in y (WLS) - orange dashed line
weights = 1.0 / (sig_y**2)
sum_w = np.sum(weights)
sum_wx = np.sum(weights * x)
sum_wy = np.sum(weights * y)
sum_wxx = np.sum(weights * x**2)
sum_wxy = np.sum(weights * x * y)
m_wls = (sum_w * sum_wxy - sum_wx * sum_wy) / (sum_w * sum_wxx - sum_wx**2)
c_wls = (sum_wxx * sum_wy - sum_wx * sum_wxy) / (sum_w * sum_wxx - sum_wx**2)
plt.plot(x_range, m_wls * x_range + c_wls, color='orange', linestyle='--', label='Fit: y uncertainties')

# 4) Linear fit: uncertainties in x and y (ODR) - blue dashed line
def run_odr(x_data, y_data, sx_data, sy_data, beta0=[1, 1]):
    model = Model(linear_model_func)
    data = RealData(x_data, y_data, sx=sx_data, sy=sy_data)
    my_odr = ODR(data, model, beta0=beta0)
    return my_odr.run()

res_odr1 = run_odr(x, y, sig_x, sig_y, beta0=[m_wls, c_wls])
m_odr1, c_odr1 = res_odr1.beta
plt.plot(x_range, m_odr1 * x_range + c_odr1, color='blue', linestyle='--', label='Fit: x and y uncertainties')

# 5) Refit after removing 2 most distant outliers (lightgreen)
dist1 = np.sqrt((res_odr1.delta / sig_x)**2 + (res_odr1.eps / sig_y)**2)
idx_outliers1 = np.argsort(dist1)[-2:]
mask1 = np.ones(len(x), dtype=bool)
mask1[idx_outliers1] = False

plt.scatter(x[idx_outliers1], y[idx_outliers1], marker='x', color='lightgreen', s=150, 
            label='Outliers (1st pair)', zorder=5, linewidths=2)
res_odr2 = run_odr(x[mask1], y[mask1], sig_x[mask1], sig_y[mask1], beta0=[m_odr1, c_odr1])
plt.plot(x_range, res_odr2.beta[0] * x_range + res_odr2.beta[1], color='lightgreen', 
         linestyle=':', label='Fit: 2 outliers removed')

# 6) Refit after removing next 2 most distant outliers (darkgreen)
dist2 = np.sqrt((res_odr2.delta / sig_x[mask1])**2 + (res_odr2.eps / sig_y[mask1])**2)
idx_rel_outliers2 = np.argsort(dist2)[-2:]
idx_outliers2 = np.where(mask1)[0][idx_rel_outliers2]
mask2 = mask1.copy()
mask2[idx_outliers2] = False

plt.scatter(x[idx_outliers2], y[idx_outliers2], marker='x', color='darkgreen', s=150, 
            label='Outliers (2nd pair)', zorder=5, linewidths=2)
res_odr3 = run_odr(x[mask2], y[mask2], sig_x[mask2], sig_y[mask2], beta0=res_odr2.beta)
plt.plot(x_range, res_odr3.beta[0] * x_range + res_odr3.beta[1], color='darkgreen', 
         linestyle=':', label='Fit: 4 outliers removed')

# Final plot formatting
plt.xlabel('x')
plt.ylabel('y')
plt.title('Linear Regressions and Outlier Analysis')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)
plt.tight_layout()
#plt.savefig('regression_outliers_plot.png')
plt.show()
