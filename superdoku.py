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
    self.check_validity()

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
        r.remove(i)
      except ValueError:
        pass
    for i in self.table[:,x]:
      try:
        r.remove(i)
      except ValueError:
        pass
    for i in self.subzone(y,x).flatten():
      try:
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

  def check_validity(self):
    for i in range(self.size):
      l = self.table[i,:][self.table[i,:]!=self.empty]
      assert len(set(l)) == len(l),"Invalid grid"
      l = self.table[:,i][self.table[:,i]!=self.empty]
      assert len(set(l)) == len(l),"Invalid grid"
      for j in range(self.size):
        sub = self.subzone(j*self.size,i*self.size)
        l = sub[sub != self.empty]
        assert len(set(l)) == len(l),"Invalid grid"

  def iter_fill(self):
    while self.fill():
      pass

  def solved(self):
    return not self.empty in self.table

  def get_hypothesis(self):
    lowest = len(self.choices)+1
    for i in range(self.size):
      for j in range(self.size):
        if not self.table[j,i] == self.empty:
          continue
        v = self.get_values(j,i)
        if v == 0:
          continue
        if len(v) < lowest:
          lowest = len(v)
          y,x = j,i
        if len(v) == 2:
          return j,i
    if lowest == len(self.choices)+1:
      raise UnsolvableError
    return y,x

# ==============

def solve(g):
  g.iter_fill()
  if g.solved():
    return g
  y,x = g.get_hypothesis()
  for v in g.get_values(y,x):
    new_a = g.table.copy()
    new_a[y,x] = v
    try:
      r = solve(Grid(new_a,g.choices,g.empty))
    except UnsolvableError:
      pass
    else:
      if r.solved():
        return r
  raise UnsolvableError

def solve_arr(arr,choices=list(range(1,10)),empty=0):
  g = Grid(arr,choices,empty)
  return solve(g).table
