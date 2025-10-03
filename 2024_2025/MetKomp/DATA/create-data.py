import pandas as pd
import numpy as np
import random

# Parameters
num_lines = 1000
nan_ratio = 0.1  # 10% of the cells in each file will contain "NAN"
outlier_ratio = 0.05  # 5% of values will be outliers

# Generate unique IDs for objects, ensuring some overlap between files
ids_file1 = set(range(1000, 2000))  # IDs unique to file 1
ids_file2 = set(range(1500, 2500))  # IDs unique to file 2, with some intersection with file 1
ids_file1 = list(ids_file1)
ids_file2 = list(ids_file2)

# Helper function to insert outliers in a specific column
def add_outliers(data, outlier_ratio, outlier_low, outlier_high):
    outlier_indices = np.random.choice(len(data), int(len(data) * outlier_ratio), replace=False)
    for idx in outlier_indices:
        data[idx] = random.choice([outlier_low, outlier_high])
    return data

# Generate data for File 1
data_file1 = {
    'ObjectID': [random.choice(ids_file1) for _ in range(num_lines)],
    'RA': np.random.uniform(0, 360, num_lines),  # Right Ascension
    'Dec': np.random.uniform(-90, 90, num_lines),  # Declination
    'Brightness': np.random.uniform(10, 20, num_lines),  # Example Brightness
    'Distance': np.random.uniform(0.1, 10, num_lines)  # Example Distance in light years
}

# Apply outliers to file 1 columns
for col, low_outlier, high_outlier in [('RA', -1000, 1000), ('Dec', -500, 500), ('Brightness', -50, 100), ('Distance', -10, 100)]:
    data_file1[col] = add_outliers(data_file1[col], outlier_ratio, low_outlier, high_outlier)

df_file1 = pd.DataFrame(data_file1)

# Generate data for File 2 with additional columns and matching structure
data_file2 = {
    'ObjectID': [random.choice(ids_file2) for _ in range(num_lines)],
    'RA': np.random.uniform(0, 360, num_lines),
    'Dec': np.random.uniform(-90, 90, num_lines),
    'Brightness': np.random.uniform(10, 20, num_lines),
    'Distance': np.random.uniform(0.1, 10, num_lines),
    'Velocity': np.random.uniform(0, 300, num_lines),  # New column in file 2
    'Temperature': np.random.uniform(200, 2000, num_lines)  # New column in file 2
}

# Apply outliers to file 2 columns
for col, low_outlier, high_outlier in [('RA', -1000, 1000), ('Dec', -500, 500), ('Brightness', -50, 100), ('Distance', -10, 100), ('Velocity', -500, 1500), ('Temperature', -1000, 5000)]:
    data_file2[col] = add_outliers(data_file2[col], outlier_ratio, low_outlier, high_outlier)

df_file2 = pd.DataFrame(data_file2)

# Introduce "NAN" values in random cells across the dataframe, targeting 10% of the cells
def add_nans_randomly(df, nan_ratio):
    total_cells = df.size
    num_nans = int(total_cells * nan_ratio)
    nan_indices = [(random.randint(0, df.shape[0] - 1), random.randint(1, df.shape[1] - 1)) for _ in range(num_nans)]
    for row, col in nan_indices:
        df.iat[row, col] = "NAN"
    return df

# Add NaN values randomly to each file
df_file1 = add_nans_randomly(df_file1, nan_ratio)
df_file2 = add_nans_randomly(df_file2, nan_ratio)

# Ensure both files have the same columns by adding missing columns filled with actual data where necessary
df_file1['Velocity'] = np.random.uniform(0, 300, num_lines)
df_file1['Temperature'] = np.random.uniform(200, 2000, num_lines)

# Apply NaN values in 10% of cells, including last two columns, consistently
df_file1 = add_nans_randomly(df_file1, nan_ratio)
df_file2 = add_nans_randomly(df_file2, nan_ratio)

# Rearrange columns to maintain the same order in both files
df_file1 = df_file1[['ObjectID', 'RA', 'Dec', 'Brightness', 'Distance', 'Velocity', 'Temperature']]
df_file2 = df_file2[['ObjectID', 'RA', 'Dec', 'Brightness', 'Distance', 'Velocity', 'Temperature']]

# Save the files
df_file1.to_csv('astronomical_data_file1.csv', index=False)
df_file2.to_csv('astronomical_data_file2.csv', index=False)

print("Files generated: 'astronomical_data_file1.csv' and 'astronomical_data_file2.csv'")
