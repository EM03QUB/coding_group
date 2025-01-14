# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 13:22:27 2024

@author: 40254336
"""

# -*- coding: utf-8 -*-
"""
Modified from P278488 - Part 1 & 2 of original script.

Changelog:
Values in csv separated by , instead of ;, and decimals changed from , to .
Preprocessing changed to allow user designated change in wavelength looked at
Changed plot type from pcolormesh to plot_surface for better visualisation
Added colour bar to accurately show intensity values

"""
#%% 1) Importing data, and preprocessing
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib
from mpl_toolkits.mplot3d import Axes3D

# Make the x-axis and y-axis ticks a certain size for the whole .py file.
matplotlib.rc('xtick', labelsize=13) 
matplotlib.rc('ytick', labelsize=13)
plt.style.use('default')  # default plot style

# Importing data using pandas from user inputs allowing customization
fn = input("File name? (include .csv): ")
dat = pd.read_csv(fn, sep=",", header=None, decimal=".", skiprows=0)

# Convert all data except the first column to numeric type
dat.iloc[:, 1:] = dat.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
time = dat.loc[0, 1:] / 60  # Convert time from seconds to minutes
dat = dat.loc[1:, :]  # Remove the first row which contains the time data

# Ask the user for the start and end wavelength
swv = int(input("Enter start wavelength: "))
ewv = int(input("Enter end wavelength: "))

# Filter the rows where the wavelength values are within the specified range
dat_wv = dat.loc[(dat[0] >= swv) & (dat[0] <= ewv)]

# Drop rows with NaN values in the data
dat_wv = dat_wv.dropna(axis=0)

# Extract the filtered wavelength values and corresponding data
wv = dat_wv[0]
dat_wv = dat_wv.iloc[:, 1:]

# Ensure that the time and data are numeric as well
time = pd.to_numeric(time, errors='coerce')
dat_wv = dat_wv.apply(pd.to_numeric, errors='coerce')

# Drop rows with NaN values from time and data as well
dat_wv = dat_wv.dropna(axis=0)
time = time.dropna()

# Check if any NaN values exist before plotting
if dat_wv.isnull().values.any() or time.isnull().any():
    print("Warning: Data contains NaN values. The plot may not display correctly.")

print("Filename for plotted data?")
nfn = input()


#%% 2) Plotting of the data to visualize in 3D

# Create a meshgrid for the 3D plot
X, Y = np.meshgrid(wv, time)  # Create the grid for X (wavelength) and Y (time)
Z = dat_wv.T.values  # Transpose the data so that Z corresponds to the correct axes

# Creating a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plotting the 3D surface
surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')

# Adding axis labels
ax.set_xlabel('Raman shift (cm-1)')
ax.set_ylabel('Time (minutes)')
ax.set_zticks([])  # Remove z-axis ticks, this is shown by colour bar below

# Adding a colour bar for intensity
cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
cbar.set_label('Intensity', rotation=270, labelpad=20)  # Vertical label

# Title and save the plot
ax.set_title('3D Plot of Raman Shift vs Time')
plt.tight_layout()
plt.savefig(nfn + '_3dplot.png', dpi=300)
plt.show()
