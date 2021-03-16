import numpy as np
from uncertainties import ufloat

Cu = {
      'l': ufloat(45.95 / 1000, 0.02 / 1000),
      'd': ufloat(9.49 / 1000, 0.02 / 1000),
      'm_density': ufloat(31.46 / 1000, 0.02 / 1000),
      'm_heat': ufloat(31.46 / 1000, 0.02 / 1000),
      'm_w': ufloat(90.43 / 1000, 0.02 / 1000) - ufloat(
          63.09 / 1000, 0.02 / 1000),
      'Tr': ufloat(80.4, 1),
      'Tw': ufloat(22.9, 0.2),
      'Te': ufloat(29.4, 0.1),
      'Dt': ufloat(0.0001021, 8e-07)
    }

Al = {
      'l': ufloat(35.59 / 1000, 0.02 / 1000),
      'd': ufloat(9.56 / 1000, 0.02 / 1000),
      'm_density': ufloat(7.27 / 1000, 0.02 / 1000),
      'm_heat': ufloat(7.27 / 1000, 0.02 / 1000),
      'm_w': ufloat(89.34 / 1000, 0.02 / 1000) - ufloat(
          63.79 / 1000, 0.02 / 1000),
      'Tr': ufloat(91.0, 1),
      'Tw': ufloat(23.4, 0.5),
      'Te': ufloat(26.8, 0.1),
      'Dt': ufloat(5e-5, 7e-7)
      }


def density(mat):
    """Calculate density"""
    volume = (mat['d'] / 2) ** 2 * np.pi * mat['l']
    return mat['m_density'] / volume


def specific_heat(mat):
    """Calculate specifc heat"""
    cw = 4183
    mr = mat['m_heat']
    mw = mat['m_w']
    Tr = mat['Tr']
    Tw = mat['Tw']
    Te = mat['Te']
    return (mw * cw * (Te - Tw)) / (mr * (Tr - Te))


def thermal_conductivity(mat):
    """Calculate thermal conductivity"""
    p = density(mat)
    c = specific_heat(mat)
    return mat['Dt'] * p * c


print('Copper')
print(thermal_conductivity(Cu))
print('Aluminium')
print(thermal_conductivity(Al))
