from movement_methods import create_arc
from math import pi
epsilon = pi * 10e-12

# If your King is taken, you lose the game
# Kings should be relatively stationary


kings = {
   'Ring King' : {
      'Movement' : [
   [[0, (0, 0), .12, 0, 2*pi - epsilon, False]]
         ],
      'Blockable' : [[1]],
      'Radius' : .038,
      'Shorthand' : 'Ring\nKing'
      },

   'Plus King' : {
      'Movement' : [
         [[1, (0, 0), (0, .16)]],
         [[1, (0, 0), (0, -.16)]],
         [[1, (0, 0), (.16, 0)]],
         [[1, (0, 0), (-.16, 0)]]
         ],
      'Blockable' : [[0], [0], [0], [0]],
      'Radius'    : .038,
      'Shorthand' : 'Plus\nKing'
   },
   'Cross King' : {
      'Movement' : [
         [[1, (0, 0), (.11, .11)]],
         [[1, (0, 0), (.11, -.11)]],
         [[1, (0, 0), (-.11, .11)]],
         [[1, (0, 0), (-.11, -.11)]]
         ],
      'Blockable' : [[0], [0], [0], [0]],
      'Radius'    : .038,
      'Shorthand' : 'Cross\nKing'
   },
}
