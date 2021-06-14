#coding: utf-8

import numpy as np
from superdoku import solve_all_arr, solve_arr, UnsolvableError

arr = np.loadtxt("l2.csv", delimiter=",", dtype=int)
print(arr)

print("Searching for all solutions may take a very long time if there are "
      "too may possibilities. This program WILL hang forever if the number of "
      "solutions is too high (i.e. there are too many empty boxes)")
if input("Search for all solutions? [y]/n: ").strip().lower()[0] != "n":
  s = solve_all_arr(arr)
  print(f"This grid has exactly {len(s)} solution{'s' if len(s) > 1 else ''}")
  for i in s:
    print("\n======\n")
    print(i)
else:
  try:
    s = solve_arr(arr)
  except UnsolvableError:
    print("This grid has no solution")
  else:
    print("First solution:")
    print(s)
