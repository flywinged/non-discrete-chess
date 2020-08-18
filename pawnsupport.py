from methods import create_arc

# Pawn Support pieces come in a variety of types
# Pawn Support pieces are placed on the third column in on the first row
# Pawn Support pieces can only move forward
# Pawn Support pieces generally are much wider than other pawns

utilitypawns = {
   '3-Way Straight SP' : {
      'Movement' : [
   [[1, (0, 0), (.24, 0.1)]],
   [[1, (0, 0), (0, .14)]],
   [[1, (0, 0), (-.24, 0.1)]]
         ],
      'Blockable' : [[0], [0], [0]],
      'Radius' : .018,
      'Shorthand' : 'SP'
      },
}