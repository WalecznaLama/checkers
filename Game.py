class Game:
	def __init__(self):
		self.winner = None

	def is_game_over(self, board):
		white_piece, black_piece, white_king, black_king = board.get_pieces_number()
		# draw - 2 kings vs 2 kings, 1 king vs 2 kings
		if (white_piece < 3 and black_piece < 3) and (white_king == white_piece and black_king == black_piece):
			return True
		elif white_piece == 0 or black_piece == 0:
			self.winner = "White" if white_piece > black_piece else "Black"
			return True
		else:
			return False

	def final_message(self):
		if self.winner is not None:
			print(f"{self.winner} Wins!")
		else:
			print("Draw!")

	def check_jump(self, board):
		pieces_with_jump = []
		best_jump = []
		for tile in board.tile_list:
			if tile.occupying_piece is not None:
				if tile.occupying_piece.color == board.turn:
					piece = tile.occupying_piece
					if len(piece.valid_jumps()) != 0:
						board.is_jump = True
						pieces_with_jump.append(piece)
					else:
						board.is_jump = False

		# TODO how to not jump over 2 times same piece
