"""
Thermal diffusitivity data analysis.

By Ryan for PHYS 307
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.odr as odr
from uncertainties.unumpy import uarray


def process_dataset(material: str, frequency: float, plot=False,
                    pr=False) -> float:
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
    plot : bool
        True if the ODR output should be printed.

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
        dx = np.full(6, 0.015)
    elif material == 'Al':
        x = np.array([27.5, 70, 150, 310, 630]) / 1000
        dx = np.array([0.25, 0.25, 0.25, 0.25, 0.5]) / 100

    # Start processing data into a useful format
    data = raw.to_numpy()

    # delete first row of zeroes
    data = np.delete(data, 0, 0)

    # For every temperature measurement, associates it with time and position
    # Also dumps data from the dodgy sensor
    # Calculates error in Temperature based a C class Pt100
    def add_independents(row):
        if material == 'Cu':
            t = np.full(6, row[0])
            relative_temperature = row[3:] - row[1]
            temp_err = (row[3:] + row[1]) * 0.01 + 1.2
        elif material == 'Al':
            t = np.full(5, row[0])
            relative_temperature = row[4:] - row[1]
            temp_err = (row[4:] + row[1]) * 0.01 + 1.2
        return np.column_stack((t, x, dx, relative_temperature, temp_err))

    # This produces an array for each time measurment,
    # where each row is [t, x, T(x,t) ]
    data = np.apply_along_axis(add_independents, 1, data)
    # Extract the rows from each time measurement array into one big array
    data = np.reshape(data, (-1, 5))

    # Split columns into named vars for clarity
    # Note how the array has been transposed
    time, x, dx, Temperature, dT = data.T

    # Estimate time error
    dtime = np.full(len(time), 0.01)
    dindep = [dx, dtime]

    # Set angular frquency, given we know frequency
    w = 2 * np.pi * (frequency / 1000)

    # Equation to fit to
    def model(params, independent):
        A, B, C = params
        t, x = independent
        return A * np.exp(- B * x) * np.sin(w * t - (C * x))

    # Fit curve
    mod = odr.Model(model)
    realData = odr.RealData([time, x], y=Temperature, sx=dindep, sy=dT)
    myodr = odr.ODR(realData, mod, beta0=[11., 2., 9.])
    output = myodr.run()
    parameters = output.beta

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
        sample_time = np.linspace(0, sampling_time, 750)
        sample_x = np.linspace(0, 0.65, 750)

        Time, X = np.meshgrid(sample_time, sample_x, sparse=True)

        sample_Temperature = model(parameters, [Time, X])

        ax.plot_surface(Time, X, sample_Temperature, cmap='plasma',
                        alpha=0.4)
        # ax.plot_wireframe(Time, X, sample_Temperature, color='black',
        #                   alpha=0.5)

    # Include sd uncertainties with parameters
    pu = uarray(parameters, output.sd_beta)

    if pr:
        output.pprint()
        # print(pu)

    # Calculate diffusitivity
    return w / (2 * pu[1] * pu[2])


def diff_all():
    """Find diffustivities."""
    diff = {}
    for material in ['Cu', 'Al']:
        for frequency in [1, 2]:
            D = process_dataset(material, frequency)
            diff['{} {}mHz'.format(material, frequency)] = D

    print(diff)
    diff_avg = {}
    diff_avg['Cu'] = (diff['Cu 1mHz'] + diff['Cu 2mHz']) / 2
    diff_avg['Al'] = (diff['Al 1mHz'] + diff['Al 2mHz']) / 2
    print(diff_avg)


diff_all()
# process_dataset('Cu', 1, pr=True)
