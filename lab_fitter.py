# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 17:56:32 2021

@author: Ryan's PC
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
from scipy.optimize import curve_fit

# Process data into a usable format

raw = pd.read_csv('Cu_1mHz.csv', names=['Time', 'Ref', 'Source', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6'])
x = np.array([12, 35, 70, 150, 310, 610]) / 1000

data = raw.to_numpy()

# delete first row
data = np.delete(data, 0, 0)

# For every temperature measurement, associates it with time and position
def add_independents(row):
    t = np.full(6, row[0])
    return np.column_stack((t, x, row[3:]))

# This produces an array for each time measurment, where each row is [t, x, T(x,t) ]
data = np.apply_along_axis(add_independents, 1, data)
# Extract the rows from each time measurement array into one big array
data = np.reshape(data, (-1, 3))

#split columns into named vars for clarity
time, x, Temperature = data.T

# plt.style.use('fast')
plt.get_cmap('viridis')
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(time, x, Temperature, s=1)
plt.draw()

def model(independent, A, d, w, C):
    x = independent[0]
    t = independent[1]
    return A * np.exp(- (x / d) ) * np.sin(w*t - (x / d) )



