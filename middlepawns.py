from movement_methods import create_arc
from math import pi
epsilon = pi * 10e-12

# Pawns should only be able to move forward (or sideways)
# Middle Pawns are the middle 4 pawns
# Middle Pawns should focus slightly off-center

middlepawns = {
   '2-Split Straight MP' : {
      'Movement' : [
   [[1, (0, 0), (0, 0.1)], [1, (0, .1), (.12, 0.27)]],
   [[1, (0, 0), (0, 0.1)], [1, (0, .1), (-.12, 0.27)]]
         ],
      'Blockable' : [[0, 0], [0, 0]],
      'Radius' : .018,
      'Shorthand' : 'MP'
      },

   '3-Split Straight MP' : {
      'Movement' : [
   [[1, (0, 0), (0, 0.09)], [1, (0, .09), (.1, 0.16)]],
   [[1, (0, 0), (0, 0.25)]],
   [[1, (0, 0), (0, 0.09)], [1, (0, .09), (-.1, 0.16)]]
         ],
      'Blockable' : [[0, 0], [0], [0, 0]],
      'Radius' : .018,
      'Shorthand' : 'MP'
      },

   '2-Pad MP' : {
      'Movement' : [
   [[0, (.09, .21), .054, 0, 2*pi - epsilon, False]],
   [[0, (-.09, .21), .054, 0, 2*pi - epsilon, False]],
         ],
      'Blockable' : [[1], [1]],
      'Radius' : .016,
      'Shorthand' : 'MP'
      },
}