#coding: utf-8

import numpy as np
from superdoku import solve_arr

arr = np.loadtxt("l6.csv",delimiter=",",dtype=int)
print(arr)
print(solve_arr(arr))
