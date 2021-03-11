# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 17:56:32 2021

@author: Ryan's PC
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Process data into a usable format

raw = pd.read_csv('Cu_1mHz.csv', names=['Time', 'Ref', 'Source', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6'])
x = np.array([12, 35, 70, 150, 310, 610]) / 1000

data = raw.to_numpy()

# delete first row
data = np.delete(data, 0, 0)


# Put ambient in a variable before we remove it from data
ambient = data[:, 1]

# For every temperature measurement, associates it with time and position
def add_independents(row):
    t = np.full(6, row[0])
    relative_temperature = row[3:] - row[1]
    return np.column_stack((t, x, relative_temperature))

# This produces an array for each time measurment, where each row is [t, x, T(x,t) ]
data = np.apply_along_axis(add_independents, 1, data)
# Extract the rows from each time measurement array into one big array
data = np.reshape(data, (-1, 3))

#split columns into named vars for clarity
time, x, Temperature = data.T

# Plot it
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# ax.scatter(time, x, Temperature, s=1, color='black')
ax.scatter(time, x, Temperature, s=1, c=Temperature, cmap='plasma')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Distance (m)')
ax.set_zlabel('Temperature (C)')
# plt.draw()

# Set angular frquency, given we know frequency
f = 0.001
w = 2 * np.pi * f

# Equation to fit to
def model(independent, A, B, C):
    t, x = independent
    return A * np.exp( - B * x ) * np.sin(w * t - (B * x) ) +  C

# Fit curve
parameters, covariance = curve_fit(model, [time, x], Temperature)

# Plot the fitted function
sample_time = np.linspace(0, 5000, 650)
sample_x = np.linspace(0, 0.65, 650)

Time, X = np.meshgrid(sample_time, sample_x)

sample_Temperature = model([Time, X], *parameters)

# ax.plot_surface(Time, X, sample_Temperature, cmap='plasma', alpha=0.35)
ax.plot_wireframe(Time, X, sample_Temperature)

d = 1/parameters[1]
D = (d ** 2) * w / 2
print(D)