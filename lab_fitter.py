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

dataframe = pd.read_csv('Cu_1mHz.csv')
print(dataframe)