from tkinter import *
from math import pi

from movement_methods import *


# Draws on the screen all the information necessary for promoting pieces
def draw_promote_controls(canvas, data):
   y_start = 500
   canvas.create_text(830, y_start + 16, anchor = W, text = 'Pawn has reached the other side', font = 'Courier 12')
   canvas.create_text(830, y_start + 32, anchor = W, text = 'Click one of the piece categories to promote pawn', font = 'Courier 12')
   canvas.create_text(830, y_start + 48, anchor = W, text = 'Green check Mark = Available. Red Cross = Unavailable', font = 'Courier 12')

   canvas.create_rectangle(850, 470, 1230, 490)
   if data.complete_promote:
      canvas.create_text(1040, 480, text = 'Click To Complete Promotion', font = 'Courier 12', fill = 'green')
   else:
      canvas.create_text(1040, 480, text = 'Click A Category to Continue', font = 'Courier 12', fill = 'red')

   y = 220
   y_add = 40

   count = 0
   for i in [5, 4, 3, 8, 6]:
      if i in data.promote_options:
         canvas.create_line(850, y + 15, 856, y + 25, fill = 'green', width = 2)
         canvas.create_line(856, y + 25, 870, y + 5, fill = 'green', width = 2)

      else:
         canvas.create_line(850, y + 5, 870, y + 25, fill = 'red', width = 2)
         canvas.create_line(850, y + 25, 870, y + 5, fill = 'red', width = 2)

      y += y_add

# Draws all the instructional information in the bottom right of the screen
def draw_controls(canvas, data):
   y_start = 580
   canvas.create_text(830, y_start, anchor = W, text = 'Click to select a piece to move', font = 'Courier 12')
   canvas.create_text(830, y_start + 16, anchor = W, text = 'Click again to place the piece', font = 'Courier 12')
   canvas.create_text(830, y_start + 32, anchor = W, text = 'You can move one of your pieces per turn', font = 'Courier 12')
   canvas.create_text(830, y_start + 48, anchor = W, text = 'Press Space to return a picked up piece', font = 'Courier 12')
   canvas.create_text(830, y_start + 64, anchor = W, text = 'Press Enter to end turn', font = 'Courier 12')
   canvas.create_text(830, y_start + 80, anchor = W, text = 'Press Escape to reset board to the beginning of your turn', font = 'Courier 12')
   canvas.create_text(830, y_start + 96, anchor = W, text = 'Press a to toggle showing all lines', font = 'Courier 12')
   canvas.create_text(830, y_start +112, anchor = W, text = 'Press s to toggle showing lines', font = 'Courier 12')
   canvas.create_text(830, y_start +128, anchor = W, text = 'Press d to remove all showing lines', font = 'Courier 12')

# Draw the actual board as well as all the pieces on the board
def draw_board(canvas, data):

   background_color = '#%02x%02x%02x' % (240, 170, 45)
   red = '#%02x%02x%02x' % (180, 0, 0)
   blue= '#%02x%02x%02x' % (0, 0, 180)

# Sections of the Display
   canvas.create_line(800, 10, 800, 790)
   canvas.create_rectangle(820, 50, 1260, 720)
   canvas.create_rectangle(25,  25, 775, 775, fill = background_color)

# Piece Counts
   y = 100
   y_add = 40
   piece_counts = count_pieces(data)
   
   canvas.create_text(830,  y - 30, anchor = W, text = 'Red Team Counts',  font = 'Courier 18', fill = red)
   canvas.create_text(1250, y - 30, anchor = E, text = 'Blue Team Counts', font = 'Courier 18', fill = blue)
   
   count = 0
   for i in [['Middle Pawns', 0], ['Side Pawns', 1], ['Utility Pawns', 2], ['Jumpers', 5],
             ['Outer Sliders', 3], ['Inner Sliders', 4], ['Left Power Piece', 8], ['Right Power Piece', 6], ['King', 7]]:
      canvas.create_text(1040, y, anchor = N, text = str(piece_counts[1][i[1]]) + ' : ' + i[0] + ' : ' + str(piece_counts[0][i[1]]), font = 'Courier 12 bold')
      canvas.create_text(1035, y + 17, anchor = NE, text = data.player_piece_types[2][i[1]], font = 'Courier 12', fill = red)
      canvas.create_text(1045, y + 17, anchor = NW, text = data.player_piece_types[1][i[1]], font = 'Courier 12', fill = blue)

      canvas.create_line(850, y + 32, 1230, y + 32)
      canvas.create_line(950, y + 13, 1130, y + 13)
      canvas.create_line(1040, y + 32, 1040, y + 13)

      y += y_add

# Instructional bits about game flow in the bottom right
   if data.player_turn == 1:
      color = '#%02x%02x%02x' % (0, 0, 180)
      team = 'Blue'
   else:
      color = '#%02x%02x%02x' % (180, 0, 0)
      team = 'Red'

   canvas.create_text(1040, 740, text = team + ' Turn', font = 'Courier 24', fill = color)
   if data.moves == 0:
      canvas.create_text(1040, 770, text = 'Move a piece!', font = 'Courier 18')
   elif data.moves == 1:
      canvas.create_text(1040, 770, text = 'Press enter to end turn', font = 'Courier 18')
   else:
      canvas.create_text(1040, 770, text = 'Illegal Move. Press Escape to restart turn.', font = 'Courier 18')


# returns the number of each type of piece on the board
def count_pieces(data):
   piece_counts = [
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0]
   ]
   piece_type = data.piece_type_hash

   for p in data.pieces:
      t = piece_type[p[0]][p[1]]
      piece_counts[p[0] - 1][t] += 1

   return piece_counts


def draw_pieces(canvas, data):

   if data.player_turn == 1:
      color = '#%02x%02x%02x' % (0, 0, 180)
      team = 'Blue'
   else:
      color = '#%02x%02x%02x' % (180, 0, 0)
      team = 'Red'

   for piece in data.pieces:
      position = (750 * data.pieces[piece][0] + 25, 750 * data.pieces[piece][1] + 25)
      piece_type = get_piece_type(data, piece)
      piece_team = piece[0]
      piece_width = data.piece_widths[piece_type] * 750

      if data.show_all_piece_moves:
         draw_piece_moves(canvas, data, piece)
      elif piece in data.show_these_piece_moves:
         draw_piece_moves(canvas, data, piece)

      piece_name = data.piece_shorthand[piece_type]
      draw_piece(canvas, position, piece_type, piece_width, piece_team, piece_name)

   if data.move_selected_piece_to:
      piece = data.selected_piece
      position = (750 * data.selected_piece_location[0] + 25, 750 * data.selected_piece_location[1] + 25)
      piece_type = get_piece_type(data, piece)
      piece_team = piece[0]
      piece_width = data.piece_widths[piece_type] * 750
      piece_name = data.piece_shorthand[piece_type]
      draw_piece(canvas, position, piece_type, piece_width, piece_team, piece_name)

# Draws the position of the pointer in the top right
def draw_hovering_over_board_info(canvas, data):
   position = data.hovering_over_board
   x = round(position[0] * 100, 2)
   y = round(position[1] * 100, 2)
   position = (x, y)
   
   canvas.create_text(400, 12, text = str(position), font = 'Courier 18')


def draw_hovering_over_piece_info(canvas, data):
   piece = data.hovering_over_piece
   piece_type = get_piece_type(data, piece)
   piece_width = round(data.piece_widths[piece_type] * 100, 1)
   piece_team = piece[0]
   piece_position = (round(100 * data.pieces[piece][0], 1), round(100 * data.pieces[piece][1], 1))

   if piece_team == 1:
      team = 'Blue'
      color = '#%02x%02x%02x' % (0, 0, 180)
   else:
      team = 'Red'
      color = '#%02x%02x%02x' % (180, 0, 0)

   canvas.create_text(1040, 20, text = str(piece_type), font = 'Courier 24', fill = color)
   canvas.create_text(940, 40, text = 'Position : ' + str(piece_position), font = 'Courier 14')
   canvas.create_text(1140, 40, text = 'Piece Width : ' + str(piece_width), font = 'Courier 14')

   draw_piece_moves(canvas, data, data.hovering_over_piece)

# Draws the circles and the text for each piece
def draw_piece(canvas, position, piece_type, piece_width, piece_team, shorthand):
   if piece_team == 1:
      color = '#%02x%02x%02x' % (0, 0, 180)
      piece_color = '#%02x%02x%02x' % (255, 255, 255)
   else:
      color = '#%02x%02x%02x' % (180, 0, 0)
      piece_color = '#%02x%02x%02x' % (0, 0, 0)

   left = round(position[0] - piece_width)
   right= round(position[0] + piece_width)
   top  = round(position[1] - piece_width)
   bottom=round(position[1] + piece_width)
   canvas.create_oval(left, top, right, bottom, outline = color, fill = piece_color, width = 1)
   canvas.create_text(position, text = shorthand, font = 'Courier 12 bold', fill = color, justify = CENTER, anchor = CENTER)

# Big function which draws all the lines and small red and green circles describing a piece's movement
def draw_piece_moves(canvas, data, piece):
   piece_type = get_piece_type(data, piece)
   if piece_type == None:
      return

   piece_width = data.piece_widths[piece_type]
   piece_team = piece[0]
   piece_position = (750 * data.pieces[piece][0] + 25, 750 * data.pieces[piece][1] + 25)

   if piece_team == 1:
      team = 'Blue'
      color = '#%02x%02x%02x' % (0, 0, 180)
   else:
      team = 'Red'
      color = '#%02x%02x%02x' % (180, 0, 0)


# Draw each line describing the movement
   piece_movement = data.movement_availability[piece]
   for movement_type in piece_movement:
      for line in movement_type:
   # If the line is a line
         if line[0] == 1:
            draw_movement_line(canvas, line, piece_position)
   # If the line is an arc
         elif line[0] == 0:
            draw_movement_arc(canvas, line, piece_position)

# If you are moving the piece, this draws its previous position for reference on where you can move it
   if data.selected_piece:
      piece_position = (750 * data.selected_piece_location[0] + 25, 750 * data.selected_piece_location[1] + 25)
      piece_movement = data.selected_piece_movement
      for movement_type in piece_movement:
         for line in movement_type:
      # If the line is a line
            if line[0] == 1:
               draw_movement_line(canvas, line, piece_position)
      # If the line is an arc
            elif line[0] == 0:
               draw_movement_arc(canvas, line, piece_position)

      captures = data.selected_piece_captures
      protections = data.selected_piece_protections
      for c in captures:
         pos = (c[0] * 750 + 25, c[1] * 750 + 25)
         canvas.create_oval(pos[0] - 3, pos[1] - 3, pos[0] + 3, pos[1] + 3, outline = 'red')
      for p in protections:
         pos = (p[0] * 750 + 25, p[1] * 750 + 25)
         canvas.create_oval(pos[0] - 3, pos[1] - 3, pos[0] + 3, pos[1] + 3, outline = 'green')

# Draws the little red and green "capture circles"
   captures = data.capture_availability[piece]
   protections = data.protection_availability[piece]
   for c in captures:
      pos = (c[0] * 750 + 25, c[1] * 750 + 25)
      canvas.create_oval(pos[0] - 3, pos[1] - 3, pos[0] + 3, pos[1] + 3, outline = 'red')
   for p in protections:
      pos = (p[0] * 750 + 25, p[1] * 750 + 25)
      canvas.create_oval(pos[0] - 3, pos[1] - 3, pos[0] + 3, pos[1] + 3, outline = 'green')

# Draws a line
def draw_movement_line(canvas, line, piece_position):
   start = (line[1][0] * 750, line[1][1] * 750)
   end = (line[2][0] * 750, line[2][1] * 750)
   start = (start[0] + piece_position[0], start[1] + piece_position[1])
   end = (end[0] + piece_position[0], end[1] + piece_position[1])

   canvas.create_line(start, end, fill = 'black')

# Draws an arc
def draw_movement_arc(canvas, line, piece_position):
   center = (line[1][0] * 750, line[1][1] * 750)
   center = (center[0] + piece_position[0], center[1] + piece_position[1])
   radius = line[2] * 750
   clockwise = line[5]
   theta_start = line[3] / pi * 180
   theta_end = line[4] / pi * 180

# Makes sure the arc is drawn from the correct angles
   if theta_start < 90 or theta_start > 270:
      theta_start = -theta_start
   else:
      theta_start = 360 - theta_start

   if theta_end < 90 or theta_end > 270:
      theta_end = -theta_end
   else:
      theta_end = 360 - theta_end

   if clockwise:  
      extent = (theta_end - theta_start) % (360)
      begin = theta_start
   else:
      extent = (theta_start - theta_end) % (360)
      begin = theta_end

   top = center[1] - radius
   left = center[0] - radius
   bottom = center[1] + radius
   right = center[0] + radius

   canvas.create_arc(left, top, right, bottom, start = begin, extent = extent, style = ARC, outline = 'black')

# Draws the list of piece types to choose from
def draw_select_piece_menu(canvas, data):
   red = '#%02x%02x%02x' % (180, 0, 0)
   blue= '#%02x%02x%02x' % (0, 0, 180)
   background_color = '#%02x%02x%02x' % (240, 170, 45)

   canvas.create_rectangle(820, 10, 1260, 400)
   canvas.create_rectangle(820, 400, 1260, 790)
   canvas.create_rectangle(25, 25, 775, 775, fill = background_color)

   canvas.create_text(1025, 772, anchor = NE, text = 'Use A Preset', font = 'Courier 14', fill = red)
   canvas.create_text(1055, 772, anchor = NW, text = 'Use A Preset', font = 'Courier 14', fill = blue)

   y = 415
   y_add = 40
   for i in [['Middle Pawns', 0], ['Side Pawns', 1], ['Utility Pawns', 2], ['Jumpers', 5],
             ['Outer Sliders', 3], ['Inner Sliders', 4], ['Left Power Piece', 6], ['Right Power Piece', 8], ['King', 7]]:
      category = i[0]
      piece_number = i[1]
      blue_piece = str(data.player_piece_types[1][piece_number])
      red_piece  = str(data.player_piece_types[2][piece_number])
      
      canvas.create_text(1040, y, anchor = N, text = category, font = 'Courier 12 bold')
      canvas.create_text(1035, y + 17, anchor = NE, text = red_piece, font = 'Courier 12', fill = red)
      canvas.create_text(1045, y + 17, anchor = NW, text = blue_piece, font = 'Courier 12', fill = blue)

      canvas.create_line(850, y + 32, 1230, y + 32)
      canvas.create_line(950, y + 13, 1130, y + 13)
      canvas.create_line(1040, y + 32, 1040, y + 13)

      y += y_add

# Draws this lists of pieces of a given type to choose from
def draw_piece_selector(canvas, data):
   page = data.selecting_page
   max_pages = (len(data.selecting_list) - 1) // 19 + 1
   start_index = (page - 1) * 19

   canvas.create_text(1257, 13, text = str(page) + '/' + str(max_pages), font = 'Courier 12', anchor = NE)

   if data.selecting_piece_type[0] == 2:
      color = '#%02x%02x%02x' % (180, 0, 0)
   else:
      color= '#%02x%02x%02x' % (0, 0, 180)

   y = 20
   y_add = 20

   for i in range(0, 19):
      try:
         canvas.create_text(1040, y, anchor = N, text = data.selecting_list[start_index + i], font = 'Courier 12', fill = color)
         if i!= 18:
            canvas.create_line(950, y + 16, 1130, y + 16)
      except:
         break
      y += y_add


# While selecting pieces for the player, draw the sample piece with moves on the board
def draw_select_piece_moves(canvas, data):

   h = {
      'Middle Pawns' : 0,
      'Side Pawns' : 1,
      'Utility Pawns' : 2,
      'Outer Sliders' : 3,
      'Inner Sliders' : 4,
      'Jumpers' : 5,
      'Left Power Piece' : 6,
      'Right Power Piece' : 8,
      'King' : 7
   }
   g = {
      0 : 5,
      1 : 0,
      2 : 2,
      3 : 10,
      4 : 12,
      5 : 11,
      6 : 13,
      7 : 14,
      8 : 15, 

   }

   if data.selecting_piece_type[2] == 9:
      return
   piece_type = data.selecting_piece_type[1]
   piece_team = data.selecting_piece_type[0]
   piece_name = data.player_piece_types[piece_team][h[piece_type]]
   piece_team = data.selecting_piece_type[0]
   if piece_name == None:
      return
   piece_width= data.piece_widths[piece_name] * 750

   x = data.mouse_x
   y = data.mouse_y

   x = (x - 25) / 750
   y = (y - 25) / 750
   if x < .04 or x > .96 or y > .96 or y < .04:
      x, y = .5, .5

   data.show_these_piece_moves = [(piece_team, g[h[piece_type]])]
   data.pieces = {
      (piece_team, g[h[piece_type]]) : (x, y)
      }
   check_all_piece_movement(data)
   draw_pieces(canvas, data)









