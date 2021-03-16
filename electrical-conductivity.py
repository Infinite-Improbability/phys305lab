import numpy as np
from uncertainties import ufloat

Cu = {
      'd': ufloat(9.53 / 1000, 0.02 / 1000),
      'I': ufloat(5.00, 0.01),
      # data in the format (length, voltage)
      'data': [
          (ufloat(25.5 / 100, 0.15 / 100), ufloat(0.309e-3, 0.001e-3)),
          (ufloat(18.6 / 100, 0.15 / 100), ufloat(0.220e-3, 0.001e-3)),
          (ufloat(3.75 / 100, 0.15 / 100), ufloat(0.044e-3, 0.001e-3))
          ]
      }

Al = {
      'd': ufloat(9.54 / 1000, 0.02 / 1000),
      'I': ufloat(5.00, 0.01),
      # data in the format (length, voltage)
      'data': [
          (ufloat(33.0 / 100, 0.15 / 100), ufloat(0.815e-3, 0.001e-3)),
          (ufloat(18.3 / 100, 0.15 / 100), ufloat(0.453e-3, 0.001e-3)),
          (ufloat(4.90 / 100, 0.15 / 100), ufloat(0.116e-3, 0.001e-3))
          ]
      }


def electrical_conductivity(mat):
    """Calculate electrical conductivity"""
    el_con = []
    for i in mat['data']:
        L, V = i
        sigma = (4 * mat['I'] * L) / (mat['d'] ** 2 * np.pi * V)
        el_con.append(sigma)
    return sum(el_con) / 3


# ambient
T = ufloat(22 + 273.15, 0.5)

print('Copper')
# thermal conductivity
cec = electrical_conductivity(Cu)
ctc = ufloat(485, 20)
print(cec)
# Should equal Lorenz number if W-F relationship holds
print(ctc / cec / T)

print('Aluminium')
aec = electrical_conductivity(Al)
atc = ufloat(110, 20)
print(cec)
print(atc / aec / T)
