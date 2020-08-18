from math import cos, acos, sin, asin, tan, atan2, pi

from kings import kings
from middlepawns import middlepawns
from utilitypawns import utilitypawns
from sliders import sliders
from jumpers import jumpers
from powerpieces import powerpieces
from sidepawns import sidepawns
from piecepresets import piecepresets

def flip_movement(movement_1):
   movement_2 = []
   for t in movement_1:
      new_type = []
      for l in t:
         if l[0] == 0:
            new_center = (-l[1][0], -l[1][1])
            new_theta_start = (l[3] + pi) % (2 * pi)
            new_theta_end = (l[4] + pi) % (2 * pi)
            new_l = [l[0], new_center, l[2], new_theta_start, new_theta_end, l[5]]
         else:
            new_start = (-l[1][0], -l[1][1])
            new_end = (-l[2][0], -l[2][1])
            new_l = [l[0], new_start, new_end]
         new_type.append(new_l)
      movement_2.append(new_type)
   return movement_2

def initialize_piece_movement(data):
   data.piece_movement = {}
   data.piece_shorthand = {}

   for piece_type in [kings, middlepawns, utilitypawns, sidepawns, sliders, jumpers, powerpieces]:
      for piece in piece_type:
         data.piece_movement[piece] = {}
         movement_1 = piece_type[piece]['Movement']
         movement_2 = flip_movement(movement_1)
         blockable = piece_type[piece]['Blockable']
         radius = piece_type[piece]['Radius']
         data.piece_movement[piece][1] = movement_1
         data.piece_movement[piece][2] = movement_2
         data.piece_movement[piece][3] = blockable
         data.piece_movement[piece][4] = radius
         data.piece_shorthand[piece] = piece_type[piece]['Shorthand']

   data.piece_widths = {}
   for p in data.piece_movement:
      data.piece_widths[p] = data.piece_movement[p][4]

   data.piecepresets = piecepresets



