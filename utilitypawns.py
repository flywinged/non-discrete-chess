from movement_methods import create_arc
from math import pi
epsilon = pi * 10e-12

# Utility Pawns pieces come in a variety of types
# Utility Pawns pieces are placed on the third column in on the first row
# Utility Pawns pieces can only move forward
# Utility Pawns pieces generally are much wider than other pawns

utilitypawns = {
   '3-Way Straight UP' : {
      'Movement' : [
   [[1, (0, 0), (.24, 0.1)]],
   [[1, (0, 0), (0, .14)]],
   [[1, (0, 0), (-.24, 0.1)]]
         ],
      'Blockable' : [[0], [0], [0]],
      'Radius' : .020,
      'Shorthand' : 'UP'
      },

   'Wide Wine Glass UP' : {
      'Movement' : [
   [[1, (0, 0), (0, 0.08)], create_arc((0, .08), (.21, .12), start_direction = (1, 0))],
   [[1, (0, 0), (0, 0.08)], create_arc((0, .08), (-.21, .12), start_direction = (-1, 0))]
         ],
      'Blockable' : [[0, 0], [0, 0]],
      'Radius' : .021,
      'Shorthand' : 'UP'
      },
}