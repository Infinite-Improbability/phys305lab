"""
Thermal diffusitivity data analysis.

By Ryan for PHYS 307
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def process_dataset(material: str, frequency: float, plot=False) -> float:
    """
    Take a set of data, fit curve and find thermal diffustivity.

    Parameters
    ----------
    material : str
        Gives material of this dataset. 'Cu' or 'Al'.
    frequency : float
        Frequency used, in mHz.
    plot : bool
        True if a plot of the curves should be shown.

    Returns
    -------
    diffustivity : float
        The estimated thermal diffusivity of this material.

    """
    # Check parameter validity
    if material not in ['Cu', 'Al']:
        raise ValueError('Invalid material name')

    # Get file
    filename = '{}_{}mHz.csv'.format(material, frequency)

    raw = pd.read_csv(filename,
                      names=['Time',
                             'Ref',
                             'Source',
                             'S1',
                             'S2',
                             'S3',
                             'S4',
                             'S5',
                             'S6'])

    # Set sensor position (in m) based on bar material
    if material == 'Cu':
        x = np.array([12, 35, 70, 150, 310, 610]) / 1000
    elif material == 'Al':
        x = np.array([27.5, 70, 150, 310, 630]) / 1000

    # Start processing data into a useful format
    data = raw.to_numpy()

    # delete first row of zeroes
    data = np.delete(data, 0, 0)

    # Put ambient in a variable before we remove it from data
    # ambient = data[:, 1]

    # For every temperature measurement, associates it with time and position
    # Also dumps data from the dodgy sensor
    def add_independents(row):
        if material == 'Cu':
            t = np.full(6, row[0])
            relative_temperature = row[3:] - row[1]
        elif material == 'Al':
            t = np.full(5, row[0])
            relative_temperature = row[4:] - row[1]
        return np.column_stack((t, x, relative_temperature))

    # This produces an array for each time measurment,
    # where each row is [t, x, T(x,t) ]
    data = np.apply_along_axis(add_independents, 1, data)
    # Extract the rows from each time measurement array into one big array
    data = np.reshape(data, (-1, 3))

    # Split columns into named vars for clarity
    time, x, Temperature = data.T

    # Set angular frquency, given we know frequency
    w = 2 * np.pi * (frequency / 1000)

    # Equation to fit to
    def model(independent, A, B, C, D):
        t, x = independent
        return A * np.exp(- B * x) * np.sin(w * t - (C * x)) + D

    # Fit curve
    parameters, covariance = curve_fit(model, [time, x], Temperature)

    if plot:
        # Plot experimental data
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(time, x, Temperature, s=1, color='black')
        # ax.scatter(time, x, Temperature, s=1, c=Temperature, cmap='plasma')
        ax.set_title('{} at {}mHz'.format(material, frequency))
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Distance (m)')
        ax.set_zlabel('Temperature (C)')

        # Plot the fitted function
        sampling_time = 5 * 1000 / frequency
        sample_time = np.linspace(0, sampling_time, 1000)
        sample_x = np.linspace(0, 0.65, 1000)

        Time, X = np.meshgrid(sample_time, sample_x, sparse=True)

        sample_Temperature = model([Time, X], *parameters)

        ax.plot_surface(Time, X, sample_Temperature, cmap='plasma',
                        alpha=0.5)
        # ax.plot_wireframe(Time, X, sample_Temperature, color='black',
        #                   alpha=0.5)

    # Calculate diffusitivity
    return w / (2 * parameters[1] * parameters[2])


def diff_all():
    """Find diffustivities."""
    diff = {}
    for material in ['Cu', 'Al']:
        for frequency in [1, 2]:
            D = process_dataset(material, frequency)
            diff['{} {}mHz'.format(material, frequency)] = D

    print(diff)
    diff_avg = {}
    diff_avg['Cu'] = [(diff['Cu 1mHz'] + diff['Cu 2mHz']) / 2,
                      np.abs(diff['Cu 1mHz'] - diff['Cu 2mHz']) / 2]
    diff_avg['Al'] = [(diff['Al 1mHz'] + diff['Al 2mHz']) / 2,
                      np.abs(diff['Al 1mHz'] - diff['Al 2mHz']) / 2]
    print(diff_avg)


diff_all()
