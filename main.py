#This code framework for this file was taken from the CMU 112 Website

from tkinter import *
from methods import *
from drawing import *
from movement_methods import *
from piece_initializer import initialize_piece_movement
import copy

def reset_promote(data):
    data.promote = False
    data.promote_options = None
    data.promote_locations = None
    data.complete_promote = False
    data.turn_start_piece_hash = copy.deepcopy(data.piece_type_hash)

def reset_selected_piece(data):
    data.selected_piece = False
    data.selected_piece_location = False
    data.selected_piece_movement = False
    data.move_selected_piece_to = False
    data.show_all_piece_moves = False
    data.show_these_piece_moves = []

def reset_movement(data):
    data.movement_availability = None
    data.capture_availability = None
    data.protection_availability = None
    data.start_turn_locations = copy.deepcopy(data.pieces)

def reset_turn(data):
    data.hovering_over_piece = False
    data.hovering_over_board = False
    data.moves = 0

def start_game(data):
    data.playing = True
    data.selecting_pieces = False

    data.player_turn = 2

    reset_promote(data)
    reset_selected_piece(data)
    reset_movement(data)
    reset_turn(data)

    initialize_pieces(data)
    check_all_piece_movement(data)


def init(data):
    data.mouse_x = 0
    data.mouse_y = 0

    initialize_pieces(data)
    initialize_piece_movement(data)

    data.player_piece_types = {
      1 : {
         0 : None,
         1 : None,
         2 : None,
         3 : None,
         4 : None,
         5 : None,
         6 : None,
         7 : None,
         8 : None,
      },
      2 : {
         0 : None,
         1 : None,
         2 : None,
         3 : None,
         4 : None,
         5 : None,
         6 : None,
         7 : None,
         8 : None,
      }
    }

    start_game(data)
    data.playing = False
    data.selecting_pieces = True
    
    data.player_turn = 2
    data.preview_piece = False
    data.selecting_piece_type = False
    data.selecting_list = []


def mousePressed(event, data):
    x, y = event.x, event.y

# Handles selecting pieces prior to the game starting
    if data.selecting_pieces:
        select_team_piece_click(x, y, data)
        if data.selecting_piece_type:
            select_piece_from_list_click(x, y, data)
        return

# Handles promoting a piece if it reaches the other side of the board
    if data.promote:
        promote = promote_click(x, y, data)
        if promote:
            data.piece_type_hash[data.promote[0]][data.promote[1]] = promote
            i = data.promote_options.index(promote)
            new_location = data.promote_locations[i]
            data.pieces[data.promote] = new_location
            check_all_piece_movement(data)
        return

# Handles moving the piece
    if data.selected_piece:
        if data.selected_piece[0] == data.player_turn:
            data.moves += 1
        else:
            data.moves += 2
        check_capture(data, data.selected_piece)
        data.promote = check_pawn_across(data)
        data.selected_piece = False
        data.move_selected_piece_to = False
        return

# Moves the temporary "hovering_over" to "selected"
    if data.hovering_over_piece and not data.selected_piece:
        data.placing_piece = data.hovering_over_piece
        data.selected_piece = data.hovering_over_piece
        data.selected_piece_location = data.pieces[data.selected_piece]
        data.selected_piece_captures = data.capture_availability[data.selected_piece]
        data.selected_piece_protections = data.protection_availability[data.selected_piece]
        data.selected_piece_movement = copy.deepcopy(data.movement_availability[data.selected_piece])
        return

    
def keyPressed(event, data):
    key = event.keysym

# Piece Selection Menu
    if data.selecting_pieces:
        page = data.selecting_page
        max_pages = (len(data.selecting_list) - 1) // 19 + 1
    # Change page on list if applicable
        if key == 'Right':
            if page < max_pages:
                data.selecting_page += 1
        elif key == 'Left':
            if page > 1:
                data.selecting_page -= 1
    # Move on to playing the actual game
        elif key == 'Return':
            if check_setup(data):
                data.playing = True
                data.selecting_pieces = False
                start_game(data)
        return

# Set down the piece you're "holding"
    if key == 'space':
        if data.selected_piece:
            data.pieces[data.selected_piece] = data.selected_piece_location
            check_all_piece_movement(data)
            data.selected_piece = False
            data.move_selected_piece_to = False

# Reset turn
    if key == 'Escape':
        data.moves = 0
        data.selected_piece = False
        data.move_selected_piece_to = False
        data.pieces = copy.deepcopy(data.start_turn_locations)
        data.piece_type_hash = copy.deepcopy(data.turn_start_piece_hash)
        reset_promote(data)
        check_all_piece_movement(data)

# End turn
    if key == 'Return':
        if data.selected_piece == False and not data.promote:
            if data.moves == 1:
                reset_movement(data)
                reset_promote(data)
                reset_turn(data)
                check_all_piece_movement(data)
                if data.player_turn == 1:
                    data.player_turn = 2
                else:
                    data.player_turn = 1
            else:
                pass
            win = check_win(data)
            if win:
                if win == 1:
                    print('Blue Wins')
                else:
                    print('Red Wins')

# Show how every piece on the board can move
    if key == 'a':
        if data.show_all_piece_moves:
            data.show_all_piece_moves = False
        else:
            data.show_all_piece_moves = True

# Toggles showing how the piece you're currently hovering over moves
    if key == 's':
        if data.hovering_over_piece:
            if data.hovering_over_piece in data.show_these_piece_moves:
                data.show_these_piece_moves.remove(data.hovering_over_piece)
            else:
                data.show_these_piece_moves.append(data.hovering_over_piece)
        else:
            pass

# Un-Show how every piece on the board can move
    if key == 'd':
        data.show_these_piece_moves = []


def timerFired(data, root):
    x = root.winfo_pointerx() - root.winfo_rootx()
    y = root.winfo_pointery() - root.winfo_rooty()
    data.mouse_x = x
    data.mouse_y = y

    if data.selecting_pieces:
        return

    if not data.selected_piece:
        check_hover_piece(x, y, data)
    else:
        moving_piece(x, y, data)
    check_hover_board(x, y, data)
    
# Handles what to draw based on screen the game is on
def redrawAll(canvas, data):
    if data.selecting_pieces:
        draw_select_piece_menu(canvas, data)
        if data.preview_piece:
            draw_board(canvas, data)
        if data.selecting_piece_type:
            draw_piece_selector(canvas, data)
            draw_select_piece_moves(canvas, data)
        return

    draw_board(canvas, data)
    if data.promote:
        draw_promote_controls(canvas, data)
    draw_controls(canvas, data)
    
    if data.hovering_over_board:
        draw_hovering_over_board_info(canvas, data)
    
    if data.hovering_over_piece:
        draw_hovering_over_piece_info(canvas, data)
    draw_pieces(canvas, data)


def run(width=1280, height=800):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data, root):
        timerFired(data, root)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data, root)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 40 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height, highlightthickness = 0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data, root)
    # and launch the app
    root.mainloop()  # blocks until window is closed

run(1280, 800)