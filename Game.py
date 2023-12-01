def get_pieces_with_given_jumps(board, longest_chain_len):
	pieces_with_best_jumps = []
	for row in range(board.BOARD_SIZE):
		for column in range(board.BOARD_SIZE):
			pose = (row, column)
			if board.get_tile_color(pose) == board.turn:
				_, _, chain_len = board.get_tile(pose).occupying_piece.find_longest_chain_jumps()
				if chain_len == longest_chain_len:
					pieces_with_best_jumps.append(pose)
	return pieces_with_best_jumps


def get_pieces_with_moves(board):
	pieces_with_moves = []
	for row in range(board.BOARD_SIZE):
		for column in range(board.BOARD_SIZE):
			pose = (row, column)
			if board.get_tile_color(pose) == board.turn:
				pieces_moves = board.get_tile(pose).occupying_piece.valid_moves()
				if pieces_moves:
					pieces_with_moves.append(pose)
	return pieces_with_moves


class Game:
	def __init__(self):
		self.winner = None
		self.is_jump = False
		self.valid_moves = []
		self.valid_jumps = []
		self.beaten_in_jumps = []

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

	def is_jump(self):
		return self.is_jump

	def valid_piece_jumps(self):
		return self.valid_jumps

	def final_message(self):
		if self.winner is not None:
			print(f"{self.winner} Wins!")
		else:
			print("Draw!")

	def get_pieces_with_best_jumps(self, board):
		longest_jump = 0
		self.is_jump = False
		for row in board.tile_list:
			for tile in row:
				if tile.occupying_piece is not None:
					if tile.occupying_piece.color == board.turn:
						_, _, chain_len = tile.occupying_piece.find_longest_chain_jumps()
						longest_jump = max(longest_jump, chain_len)
		if longest_jump != 0:
			self.is_jump = True
			return get_pieces_with_given_jumps(board, longest_jump)
		else:
			return []

	def handle_pose_input(self, board, pose=(-1, -1), no_jump=-1):  # TODO
		selected_tile = board.get_tile(pose)
		if not board.is_piece_selected():  # user select piece pose
			pieces_with_jumps = self.get_pieces_with_best_jumps(board)
			pieces_with_moves = get_pieces_with_moves(board)
			if not pieces_with_jumps and not pieces_with_moves:  # No possible moves
				print("Over - no moves")  # TODO opponent wins
				return False
			elif selected_tile.occupying_piece is None:  # Empty tile
				print("Selected empty tile. Choose again.")
				return False
			elif selected_tile.occupying_piece.color != board.turn:  # Wrong color selected
				print("Selected opponent piece. Choose again.")
				return False
			elif self.is_jump and pose not in pieces_with_jumps:  # Exist move with more jumps
				print(f"Select one of pieces with jumps: {pieces_with_jumps}")
				return False
			elif (not self.is_jump) and pose not in pieces_with_moves:  # No possible move on selected piece
				print(f"Select piece with move: {pieces_with_moves}")
				return False
			else:  # Selected valid piece
				board.selected_piece = selected_tile.occupying_piece
				self.valid_moves = board.selected_piece.valid_moves()
				self.beaten_in_jumps, self.valid_jumps, _ = board.selected_piece.find_longest_chain_jumps()
				board.update_marks(self.valid_moves, self.valid_jumps)
		else:  # user select target tile pose or jump / jumps chain
			valid_select = False
			if self.is_jump:
				if len(self.valid_jumps) > no_jump >= 0:
					valid_select = True
				if not valid_select:
					print(f"Select valid jump.")
					return False
			elif not valid_select:
				for moves in self.valid_moves:
					if pose in moves or pose == moves:    # TODO king check
						valid_select = True
						break
				if not valid_select:
					print(f"Select tile with valid move.")
					return False
			if valid_select:
				board.selected_piece.move(pose, self.valid_jumps[no_jump], self.beaten_in_jumps[no_jump])
				board.next_turn()
