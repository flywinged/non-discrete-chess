from movement_methods import create_arc
from math import pi
epsilon = pi * 10e-12

# Pawns should only be able to move forward (or sideways)
# Side Pawns are the outer 2 pawns on either side
# Side Pawns should have more utility than middle pawns

sidepawns = {
   '3-Way Straight SP' : {
      'Movement' : [
   [[1, (0, 0), (.12, 0.14)]],
   [[1, (0, 0), (0, .19)]],
   [[1, (0, 0), (-.12, 0.14)]]
         ],
      'Blockable' : [[0], [0], [0]],
      'Radius' : .018,
      'Shorthand' : 'SP'
      },

   '2-Way Straight SP' : {
      'Movement' : [
   [[1, (0, 0), (.06, 0.27)]],
   [[1, (0, 0), (-.06, 0.27)]]
         ],
      'Blockable' : [[0], [0]],
      'Radius' : .017,
      'Shorthand' : 'SP'
      },

   '1 Pad SP' : {
      'Movement' : [
   [[0, (0, .19), .07, 0, 2*pi - epsilon, False]]
         ],
      'Blockable' : [[1]],
      'Radius' : .022,
      'Shorthand' : 'SP'
      },
}