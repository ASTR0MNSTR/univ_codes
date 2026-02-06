import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os

# 1. Load Data
current_folder = os.path.dirname(os.path.abspath(__file__))

training_df = pd.read_csv(os.path.join(current_folder, 'data', 'ex39a_training_data.csv'))
test_df = pd.read_csv(os.path.join(current_folder, 'data', 'ex39a_test_data.csv'))
unknown_df = pd.read_csv(os.path.join(current_folder, 'data', 'ex39a_unknown1.csv'))
verification_df = pd.read_csv(os.path.join(current_folder, 'data','ex39a_verification1.csv')).rename(columns={'Star Name': 'star'})

# 2. Fit P-L Relation (Training)
training_df['log_P'] = np.log10(training_df['period_days'])
training_df['M_abs'] = training_df['mV_mean'] + 5 - 5 * np.log10(training_df['distance_pc'])

def pl_relation(log_p, a, b):
    return a * log_p + b

params, _ = curve_fit(pl_relation, training_df['log_P'], training_df['M_abs'])
a, b = params

# 3. Calculate Predictions
# Test Set Predictions
test_df['log_P'] = np.log10(test_df['period_days'])
test_df['M_pred'] = pl_relation(test_df['log_P'], a, b)
test_df['distance_pred'] = 10**((test_df['mV_mean'] - test_df['M_pred'] + 5) / 5)

# Verification Set Predictions (Merging with Gaia RUWE data)
merged_df = pd.merge(unknown_df, verification_df, on='star')
merged_df['distance_gaia'] = 1000.0 / merged_df['Parallax [mas]']
merged_df['log_P'] = np.log10(merged_df['period_days'])
merged_df['M_pred'] = pl_relation(merged_df['log_P'], a, b)
merged_df['distance_pl'] = 10**((merged_df['mV_mean'] - merged_df['M_pred'] + 5) / 5)

# 4. Visualization of Agreement
plt.figure(figsize=(8, 8))

# Plot Test Data
plt.scatter(test_df['distance_pc'], test_df['distance_pred'], 
            color='blue', alpha=0.6, label='Test Data')

# Plot Verification (Unknown) Data with RUWE distinction
ruwe_good = merged_df[merged_df['RUWE'] <= 1.4]
ruwe_bad = merged_df[merged_df['RUWE'] > 1.4]

plt.scatter(ruwe_good['distance_gaia'], ruwe_good['distance_pl'], 
            color='green', marker='s', label='Verification (RUWE $\leq$ 1.4)')
plt.scatter(ruwe_bad['distance_gaia'], ruwe_bad['distance_pl'], 
            color='red', marker='x', label='Verification (RUWE > 1.4)')

# 1:1 Reference Line
max_val = max(test_df['distance_pc'].max(), test_df['distance_pred'].max(), 
              merged_df['distance_gaia'].max(), merged_df['distance_pl'].max())
plt.plot([0, max_val], [0, max_val], 'k--', alpha=0.5, label='1:1 Line (Perfect Agreement)')

plt.xlabel('Known / Gaia Distance [pc]')
plt.ylabel('Predicted (P-L Model) Distance [pc]')
plt.title('Agreement: Predicted vs. Known Distances')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)
plt.axis('equal')
plt.show()
