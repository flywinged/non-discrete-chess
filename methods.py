import math
import copy
from movement_methods import *

from kings import kings
from middlepawns import middlepawns
from utilitypawns import utilitypawns
from sliders import sliders
from jumpers import jumpers
from powerpieces import powerpieces
from sidepawns import sidepawns

def initialize_pieces(data):
 
# Piece locations on board (team, piece_number) : (x, y)
   data.pieces = {
      (1, 0)  : (5/100,   12/100),
      (1, 1)  : (15/100,  12/100),
      (1, 2)  : (25/100,  12/100),
      (1, 3)  : (35/100,  12/100),
      (1, 4)  : (45/100,  12/100),
      (1, 5)  : (55/100,  12/100),
      (1, 6)  : (65/100,  12/100),
      (1, 7)  : (75/100,  12/100),
      (1, 8)  : (85/100,  12/100),
      (1, 9)  : (95/100,  12/100),
      (1, 10) : (5/100,   4/100),
      (1, 11) : (15/100,  4/100),
      (1, 12) : (25/100,  4/100),
      (1, 13) : (37.5/100,  4/100),
      (1, 14) : (50/100,  4/100),
      (1, 15) : (62.5/100,  4/100),
      (1, 16) : (75/100,  4/100),
      (1, 17) : (85/100,  4/100),
      (1, 18) : (95/100,  4/100),
   }

# Flip locations for the other player
   add = {}
   for p in data.pieces:
      pos = data.pieces[p]
      new_pos = (1 - pos[0], 1 - pos[1])
      new_piece = (2, p[1])
      add[new_piece] = new_pos
   for p in add:
      data.pieces[p] = add[p]

# Relates each piece number to a type of piece
   data.piece_type_hash = {
      1 : {
         0 : 1,
         1 : 1,
         2 : 2,
         3 : 0,
         4 : 0,
         5 : 0,
         6 : 0,
         7 : 2,
         8 : 1,
         9 : 1,
         10: 3,
         11: 5,
         12: 4,
         13: 6,
         14: 7,
         15: 8,
         16: 4,
         17: 5,
         18: 3
      },
      2 : {
         0 : 1,
         1 : 1,
         2 : 2,
         3 : 0,
         4 : 0,
         5 : 0,
         6 : 0,
         7 : 2,
         8 : 1,
         9 : 1,
         10: 3,
         11: 5,
         12: 4,
         13: 6,
         14: 7,
         15: 8,
         16: 4,
         17: 5,
         18: 3
      }
   }

# Determine which piece the pawn will promote to
def promote_click(x_mouse, y_mouse, data):
   y = 100
   y_add = 40

# Confirm the promotion
   if data.complete_promote:
      if x_mouse > 850 and x_mouse < 1230 and y_mouse > 470 and y_mouse < 490:
         data.promote = False

   if x_mouse > 1130 or x_mouse < 850:
      return False

   pieces = [0, 1, 2, 5, 3, 4, 8, 6, 7]
   for p in pieces:
      if p in data.promote_options and y_mouse > y and y_mouse < y + y_add:
         data.complete_promote = True
         return p
      y += y_add

   return False

# Bug-Fixing for promotions
def check_promote_options(data, piece):
   data.promote_options = []
   data.promote_locations = []
   position = data.pieces[piece]
   normal_type = get_piece_type(data, piece)
   normal_width = data.piece_widths[normal_type]
   team = piece[0]

   for piece_number in [3, 4, 5, 6, 8]:
      piece_type = data.player_piece_types[piece[0]][piece_number]
      piece_width = data.piece_widths[piece_type]
      if team == 1:
         new_position = add_vectors(position, (0, normal_width-piece_width))
      else:
         new_position = add_vectors(position, (0, piece_width-normal_width))
      can_promote = True
      for p in data.pieces:
         if is_point_close_to_piece(data, new_position, piece_width, [piece]):
            can_promote = False
            break
      if can_promote:
         data.promote_options.append(piece_number)
         data.promote_locations.append(new_position)

# Determine if a pawn has reached the other side of the board
def check_pawn_across(data):
   epsilon = 10e-5
   for p in data.pieces:
      piece_number = data.piece_type_hash[p[0]][p[1]]
      piece_type = get_piece_type(data, p)
      piece_width = data.piece_widths[piece_type]
      y = data.pieces[p][1]
      team = p[0]
      if piece_number == 0 or piece_number == 1 or piece_number == 2:
         if team == 1 and y + piece_width + epsilon > 1:
            check_promote_options(data, p)
            return p
         elif team == 2 and y - piece_width - epsilon < 0:
            check_promote_options(data, p)
            return p

   return False

# Determine and assign if the mouse is hovering over a piece
def check_hover_piece(x, y, data):
   for piece in data.pieces:
      piece_type = get_piece_type(data, piece)
      piece_width = data.piece_widths[piece_type] * 750
      position = (750 * data.pieces[piece][0] + 25, 750 * data.pieces[piece][1] + 25)
      x_change = position[0] - x
      y_change = position[1] - y
      d = (x_change**2 + y_change**2)**(1/2)
      if d < piece_width:
         data.hovering_over_piece = piece
         return True
   data.hovering_over_piece = False
   return False

# Determine if the mouse is "inside" the board
def check_hover_board(x, y, data):
   if x > 25 and x < 775 and y > 25 and y < 775:
      board_x = (x - 25) / 750
      board_y = (y - 25) / 750
      data.hovering = 'Board'
      data.hovering_over_board = (board_x, board_y)
      return True
   data.hovering_over_board = False
   return False

# Determine how the currently selected piece can move
def moving_piece(x, y, data):
   position = (data.selected_piece_location[0], data.selected_piece_location[1])
   x = (x - 25) / 750 - position[0]
   y = (y - 25) / 750 - position[1]

   piece_movement = data.selected_piece_movement

   points = []
   for movement_type in piece_movement:
   # If the line is a line
      for line in movement_type:
         if line[0] == 1:
            closest = closest_point_on_segment(line, (x, y))
   # If the line is an arc
         elif line[0] == 0:
            closest = closest_point_on_arc(line, (x, y))
         points.append(closest)
   
   try:
      close = min(points)[1]
      close = add_vectors(close, position)
      close = nudge_piece(close, data)
   except:
      close = position
   data.move_selected_piece_to = close
   data.pieces[data.selected_piece] = close
   check_all_piece_movement(data)

# If piece is too close to another piece, slightly nudge it
# Necessary in order to avoid bugs where pieces appear to be inside each other
def nudge_piece(point, data):

   nudged = False
   piece = data.selected_piece
   piece_type = get_piece_type(data, piece)
   piece_position = data.pieces[piece]
   size = data.piece_widths[piece_type]
   epsilon = 10e-6

   if point[0] - size - epsilon <= 0:
      point = (point[0] + epsilon, point[1])
      nudged = True
   elif point[0] + size + epsilon >= 1:
      point = (point[0] - epsilon, point[1])
      nudged = True
   if point[1] - size - epsilon <= 0:
      point = (point[0], point[1] + epsilon)
      nudged = True
   elif point[1] + size + epsilon >= 1:
      point = (point[0], point[1] - epsilon)
      nudged = True

   if nudged:
      return nudge_piece(point, data)

   nudged = False
   for p in data.pieces:
      if p == piece:
         continue
      p_type = get_piece_type(data, p)
      p_size = data.piece_widths[p_type]
      position = (data.pieces[p][0], data.pieces[p][1])
      effective_size = size + p_size + epsilon

      d = calculate_distance(position, point)
      if d < effective_size:
         nudged = True
         nudge_vector = add_vectors(point, scale_vector(position, -1))
         nudge_vector = normalize_vector(nudge_vector)
         nudge_vector = scale_vector(nudge_vector, epsilon)
         point = add_vectors(point, nudge_vector)

   if nudged:
      return nudge_piece(point, data)
   else:
      return point


def check_capture(data, piece):
   position = data.pieces[piece]
   team = piece[0]
   piece_type = get_piece_type(data, piece)
   piece_width = data.piece_widths[piece_type]

   epsilon = 10e-5
   remove = False
   for p in data.pieces:
      p_position = data.pieces[p]
      p_team = p[0]
      p_type = get_piece_type(data, p)
      p_width = data.piece_widths[p_type]

      effective_size = p_width + piece_width + epsilon

      if p_team == team:
         continue

      d = calculate_distance(p_position, position)
      if d < effective_size:
         remove = p

   if remove:
      del data.pieces[remove]
      check_all_piece_movement(data)
      return True      

   return False

# Prior to game beginning, determine what pieces are of each type
def select_team_piece_click(x, y, data):
   if x < 850 or x > 1230 or y < 410 or y > 790:
      return False

   y_loc = 415
   y_add = 40

   for i in [['Middle Pawns', 0], ['Side Pawns', 1], ['Utility Pawns', 2], ['Jumpers', 5],
             ['Outer Sliders', 3], ['Inner Sliders', 4], ['Left Power Piece', 6], ['Right Power Piece', 8], ['King', 7], ['Presets', 9]]:
      if y > y_loc - 8 and y < y_loc + 32:
         if x < 1040:
            team = 2
         else:
            team = 1
         data.selecting_piece_type = (team, i[0], i[1])
         set_selecting_list(data)
      y_loc += y_add

# Used in select_team_piece_click(). Just assigns the correct list
def set_selecting_list(data):
   data.selecting_list = []
   data.selecting_page = 1

   table = {
      0 : middlepawns,
      1 : sidepawns,
      2 : utilitypawns,
      3 : sliders,
      4 : sliders,
      5 : jumpers,
      6 : powerpieces,
      7 : kings,
      8 : powerpieces,
      9 : data.piecepresets
   }

   piece_dict = table[data.selecting_piece_type[2]]

   for p in piece_dict:
      data.selecting_list.append(p)
   data.selecting_list.sort()

# Determine which piece was clicked on while selecting pieces before the game starts
def select_piece_from_list_click(x, y, data):
   if x < 850 or x > 1230 or y < 16 or y > 396:
      return False
   index = (y - 16) // 20

   index = ((data.selecting_page - 1) * 19) + index
   if index >= len(data.selecting_list):
      return False
   else:
      if data.selecting_piece_type[2] == 9:
         set_preset(data, data.selecting_list[index])
      else:
         data.player_piece_types[data.selecting_piece_type[0]][data.selecting_piece_type[2]] = data.selecting_list[index]

# Sets the team of a player to a preset
def set_preset(data, preset):
   team = data.selecting_piece_type[0]
   data.player_piece_types[team] = data.piecepresets[preset]

# Make sure all the pieces have been set bfor each team before starting the game
def check_setup(data):
   for player in data.player_piece_types:
      for piece in data.player_piece_types[player]:
         if data.player_piece_types[player][piece] == None:
            return False
   return True

# Determine if either player has won
def check_win(data):
   player_1 = False
   player_2 = False
   for p in data.pieces:
      if p[1] == 14:
         if p[0] == 1:
            player_1 = True
         else:
            player_2 = True
      pass
   if not player_1:
      return 2
   elif not player_2:
      return 1
   else:
      return False
