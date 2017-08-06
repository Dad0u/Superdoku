#coding: utf-8

import numpy as np

class UnsolvableError(Exception):
  pass

class Grid(object):
  def __init__(self,table,choices,empty=0):
    self.table = table
    self.choices = choices
    self.empty = empty
    assert len(self.table.shape) == 2,"Only 2D is supported"
    assert self.table.shape[0]  == self.table.shape[1],"Not square"
    self.size = self.table.shape[0]
    self.primary = int(np.sqrt(self.size))
    assert self.primary == np.sqrt(self.size),"Invalid size"
    self.invalid = [[[] for i in range(self.size)] for i in range(self.size)]

  def subzone(self,y,x):
    b = (y//self.primary)*self.primary
    a = (x//self.primary)*self.primary
    return self.table[b:b+self.primary,a:a+self.primary]

  def get_values(self,y,x):
    if self.table[y,x] != self.empty:
      return self.table[y,x]
    r = list(self.choices)
    for i in self.table[y,:]:
      try:
        #print("R",i)
        r.remove(i)
      except ValueError:
        pass
    for i in self.table[:,x]:
      try:
        #print("C",i)
        r.remove(i)
      except ValueError:
        pass
    for i in self.subzone(y,x).flatten():
      try:
        #print("S",i)
        r.remove(i)
      except ValueError:
        pass
    return r

  def fill(self):
    left = self.table == self.empty
    old = left.copy()
    for i in range(self.size):
      for j in range(self.size):
        if not left[j,i]:
          continue
        v = self.get_values(j,i)
        #print(j,i,v)
        if len(v) == 0:
          raise UnsolvableError
        elif len(v) != 1:
          continue
        self.table[j,i] = v[0]
        left[j,i] = False
    return (old != left).any()

  def iter_fill(self):
    while self.fill():
      pass

  def solved(self):
    return not self.empty in self.table
