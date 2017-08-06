#coding: utf-8

import numpy as np
from superdoku import Grid

arr = np.loadtxt("l2.csv",delimiter=",",dtype=int)
g = Grid(arr,list(range(1,10)))

g.iter_fill()

print(arr)
