from movement_methods import create_arc
from math import pi
epsilon = pi * 10e-12

# Jumpers start in the second in on the back row
# Jumpers share the common trait that they can jump, obviously

jumpers = {
   'Ring Jumper' : {
      'Movement' : [
   [[0, (0, 0), .21, 0, 2*pi - epsilon, False]]
         ],
      'Blockable' : [[1]],
      'Radius' : .024,
      'Shorthand' : 'RJ'
      },

   'Pad Jumper' : {
      'Movement' : [
   [[0, (.2, .2), .042, 0, 2*pi - epsilon, False]],
   [[0, (.2, -.2), .042, 0, 2*pi - epsilon, False]],
   [[0, (-.2, .2), .042, 0, 2*pi - epsilon, False]],
   [[0, (-.2, -.2), .042, 0, 2*pi - epsilon, False]],
   ],
      'Blockable' : [[1], [1], [1], [1]],
      'Radius' : .025,
      'Shorthand' : 'PJ'
      },
}