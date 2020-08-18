from movement_methods import create_arc
from math import pi
epsilon = pi * 10e-12

# There is one power piece on either side of the king
# Power pieces have great power that range dramatically in appearance

powerpieces = {
   'Royal Gaurd' : {
      'Movement' : [
   [[0, (0, 0), .24, 11*pi/6, 7*pi/6, True]],
   [[1, (0, 0), (.8, 1)]],
   [[1, (0, 0), (-.8, 1)]],
   [[1, (0, 0), (0, 1)]],
         ],
      'Blockable' : [[1], [0], [0], [0]],
      'Radius' : .032,
      'Shorthand' : 'RY\nGD'
      },

   'Super Ring Jumper' : {
      'Movement' : [
   [[0, (0, 0), .34, 0, 2*pi - epsilon, False]],
         ],
      'Blockable' : [[1]],
      'Radius' : .032,
      'Shorthand' : 'S\nRJ'
      },

   'Dual Slider' : {
      'Movement' : [
   [[1, (0, 0), (1, 1)]],
   [[1, (0, 0), (1, -1)]],
   [[1, (0, 0), (-1, -1)]],
   [[1, (0, 0), (-1, 1)]],
   [[1, (0, 0), (0, 1)]],
   [[1, (0, 0), (0, -1)]],
   [[1, (0, 0), (1, 0)]],
   [[1, (0, 0), (-1, 0)]],
         ],
      'Blockable' : [[0], [0], [0], [0], [0], [0], [0], [0]],
      'Radius' : .034,
      'Shorthand' : 'Dual\nSL'
      },
}