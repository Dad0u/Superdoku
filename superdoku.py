#coding: utf-8

import numpy as np


class UnsolvableError(Exception):
  """The exception to raise if the grid cannot be solved"""
  pass


class Grid:
  """
  This class represents a Sudoku grid

  It takes the base array (a numpy array), a list of the authorized values and
  the value that represents an empty box.

  It implements the methods necessary for adeterministic resolution.
  """

  def __init__(self, table, choices=[i for i in range(1, 10)], empty=0):
    """
    Basic checks to make sure the input array is correct and
    extracts the size
    """
    self.table = table
    self.choices = choices
    self.empty = empty
    assert len(self.table.shape) == 2, "Only 2D is supported"
    assert self.table.shape[0] == self.table.shape[1], "Not square"
    self.size = self.table.shape[0]
    self.primary = int(np.sqrt(self.size))
    assert self.primary == np.sqrt(self.size), "Invalid size"
    self.check_validity()

  def subzone(self, y, x):
    """
    Returns the subzone of a box (in which only one of each vaue is allowed)
    """
    b = (y // self.primary) * self.primary
    a = (x // self.primary) * self.primary
    return self.table[b:b + self.primary, a:a + self.primary]

  def get_values(self, y, x):
    """
    Returns the allowed values for an empty box

    If the box is filled, returns the value of the box
    """
    if self.table[y, x] != self.empty:
      return self.table[y, x]
    r = list(self.choices)
    for i in self.table[y, :]:
      try:
        r.remove(i)
      except ValueError:
        pass
    for i in self.table[:, x]:
      try:
        r.remove(i)
      except ValueError:
        pass
    for i in self.subzone(y, x).flatten():
      try:
        r.remove(i)
      except ValueError:
        pass
    return r

  def fill(self):
    """
    Fills all the boxes that have only one option left

    Returns True if anything changed, False otherwise
    """
    left = self.table == self.empty
    old = left.copy()
    for i in range(self.size):
      for j in range(self.size):
        if not left[j, i]:
          continue
        v = self.get_values(j, i)
        # print(j,i,v)
        if len(v) == 0:
          raise UnsolvableError
        elif len(v) != 1:
          continue
        self.table[j, i] = v[0]
        left[j, i] = False
    return (old != left).any()

  def check_validity(self):
    """
    To check if the grid is valid

    It raises an assertion error if this grid is invalid
    """
    for i in range(self.size):
      l = self.table[i, :][self.table[i, :] != self.empty]
      assert len(set(l)) == len(l), "Invalid grid"
      l = self.table[:, i][self.table[:, i] != self.empty]
      assert len(set(l)) == len(l), "Invalid grid"
      for j in range(self.size):
        sub = self.subzone(j * self.size, i * self.size)
        l = sub[sub != self.empty]
        assert len(set(l)) == len(l), "Invalid grid"

  def iter_fill(self):
    """
    Fills the grid until it no longer changes anything
    """
    while self.fill():
      pass

  def solved(self):
    """
    Returns True if the grid is solved
    """
    return not self.empty in self.table

  def get_hypothesis(self):
    """
    Returns coordinates of the box where the hypothesis are the cheapest

    It looks for the box with least possible values (2 at best)
    It asserts that the box was iter_filled and therefore there are
    no box with only one possibility
    """
    lowest = len(self.choices) + 1
    for i in range(self.size):
      for j in range(self.size):
        if not self.table[j, i] == self.empty:
          continue
        v = self.get_values(j, i)
        if v == 0:
          continue
        if len(v) < lowest:
          lowest = len(v)
          y, x = j, i
        if len(v) == 2:
          return j, i
    if lowest == len(self.choices) + 1:
      raise UnsolvableError
    return y, x

# ==============


def solve(g, stop=True):
  """
  Takes a grid object and tries to solve it

  It is a recursive function that looks for a solution by filling the
  grid and making hypothesis if necessary.

  It raises UnsolvableError if there are no solutions

  If stop is True, it will return the first solution
  Else, it will try to find all the solutions
  """
  if not stop:
    rl = []
  try:
    g.iter_fill()
  except UnsolvableError:
    if not stop:
      return []
    raise
  if g.solved():
    return g if stop else [g]
  y, x = g.get_hypothesis()
  for v in g.get_values(y, x):
    new_a = g.table.copy()
    new_a[y, x] = v
    try:
      r = solve(Grid(new_a, g.choices, g.empty), stop=stop)
    except UnsolvableError:
      continue  # Run the loop with another value
    else:
      if stop:
        if r.solved():
          return r  # Returns the solved one
      else:
        rl.extend([i for i in r if i.solved()])
  # If none of the hypothesis worked, it is unsolvable
  # Maybe the previous hypothesis is the cause
  # So it wil enter the except and loop on antoher value
  if not stop:
    return rl
  raise UnsolvableError


def solve_arr(arr, choices=list(range(1, 10)), empty=0):
  """
  To instanciate the Grid object, to hide it to the user
  """
  g = Grid(arr, choices, empty)
  return solve(g).table


def solve_all_arr(arr, choices=list(range(1, 10)), empty=0):
  g = Grid(arr, choices, empty)
  return [i.table for i in solve(g, stop=False)]
