from Piece import Piece


class King(Piece):
	def __init__(self, row, column, color, board):
		super().__init__(row, column, color, board)
		self.representation = color.upper()

	def possible_moves(self):  # available moves on empty board
		moves_ru = []  # RightUp (A1 to H8)
		moves_rd = []  # RightDown (A8 to H1)
		moves_ld = []  # LeftDown (H8 to A1)
		moves_lu = []  # LeftUp (H1 to A8)
		r = self.row
		c = self.column

		for i in range(1, self.board.BOARD_SIZE):  # RightUp (A1 to H8)
			if r + i > self.board.BOARD_SIZE - 1 or c + i > self.board.BOARD_SIZE - 1:
				break
			else:
				moves_ru.append([i, i])
		for i in range(1, self.board.BOARD_SIZE):  # RightDown (A8 to H1)
			if r - i < 0 or c + i > self.board.BOARD_SIZE - 1:
				break
			else:
				moves_rd.append([-i, i])
		for i in range(1, self.board.BOARD_SIZE):  # LeftDown (H8 to A1)
			if r - i < 0 or c - i < 0:
				break
			else:
				moves_ld.append([-i, -i])
		for i in range(1, self.board.BOARD_SIZE):  # LeftUp (H1 to A8)
			if r + i > self.board.BOARD_SIZE - 1 or c - i < 0:
				break
			else:
				moves_lu.append([i, -i])
		return [moves_ru, moves_rd, moves_ld, moves_lu]

	def valid_moves(self):
		valid_moves = []
		moves = self.possible_moves()
		for direction in moves:
			for move in direction:
				if self.board.is_tile_empty(self.row+move[0], self.column+move[1]):
					valid_moves.append(move)
				else:
					break
		return valid_moves

	def valid_jumps(self):
		valid_jumps = []
		moves = self.possible_moves()
		opponent = self.board.get_opponent_color()
		for direction in moves:
			hit_opponent = False  # opponent at tile
			for move in direction:
				move_tile = [self.row+move[0], self.column+move[1]]
				if self.board.is_tile_empty(move_tile[0], move_tile[1]) and hit_opponent:  # empty tile behind opponent
					valid_jumps.append(move)
				elif self.board.get_tile_color(move_tile[0], move_tile[1]) == opponent:  # tile with opponent
					hit_opponent = True
				elif hit_opponent:  # first not empty tile behind opponent
					break
		return valid_jumps
