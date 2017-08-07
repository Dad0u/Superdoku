#coding: utf-8

import numpy as np
from superdoku import solve_arr

arr = np.loadtxt("l4.csv",delimiter=",",dtype=int)
print(solve_arr(arr))

