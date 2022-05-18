#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Use Neural Networks to simulate a League of Legends draft."""

__file__ = 'lol_draft_simulator.py'
__author__ = 'Jesse Estes'
__copyright__ = 'Copyright 2022, LolDraftSimulator'
__credits__ = ['Jesse Estes']
__license__ = 'MIT'
__version__ = '1.0.2'
__maintainer__ = 'Jesse Estes'
__email__ = 'jestes5111@gmail.com'
__status__ = 'Prototype'

# --------------------------------------------------------------------------- #
#                                  Imports                                    #
# --------------------------------------------------------------------------- #
# Standard libraries

# Third-party libraries
import constraint

# Owned libraries

# --------------------------------------------------------------------------- #
#                                    Code                                     #
# --------------------------------------------------------------------------- #
def main():
  problem = constraint.Problem()

  problem.addVariables('ab', range(10))

  def temp(a, b):
    if a + b == 10:
      return True

  problem.addConstraint(temp, ['a', 'b'])

  solutions = problem.getSolutions()
  for solution in solutions:
    print(solution)

if __name__ == '__main__':
  main()
