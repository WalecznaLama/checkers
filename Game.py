# import time

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

# TODO jump chain modify when pawn turn into king


class Game:
	def __init__(self):
		self.winner = None
		self.is_jump = False
		self.valid_moves = []
		self.valid_jumps = []
		self.beaten_in_jumps = []
		self.pieces_with_jumps = []
		self.pieces_with_moves = []

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

	def get_pieces_with_moves(self, board):
		pieces_with_moves = []
		for row in range(board.BOARD_SIZE):
			for column in range(board.BOARD_SIZE):
				pose = (row, column)
				if board.get_tile_color(pose) == board.turn:
					pieces_moves = board.get_tile(pose).occupying_piece.valid_moves()
					if pieces_moves:
						pieces_with_moves.append(pose)
		self.pieces_with_moves = pieces_with_moves
		return self.pieces_with_moves

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
			self.pieces_with_jumps = get_pieces_with_given_jumps(board, longest_jump)
		else:
			self.pieces_with_jumps = []

		return self.pieces_with_jumps

	def handle_pose_input(self, board, pose):
		selected_tile = board.get_tile(pose)  # TODO problem when jump? [pose=(J,-1)]
		empty_output = [], [], [], -1
		if not board.is_piece_selected():  # user select piece pose
			self.get_pieces_with_best_jumps(board)
			self.get_pieces_with_moves(board)
			if not self.pieces_with_jumps and not self.pieces_with_moves:  # No possible moves
				print("Over - no moves")  # TODO opponent wins
			elif selected_tile.occupying_piece is None:  # Empty tile
				print("Selected empty tile. Choose again.")
			elif selected_tile.occupying_piece.color != board.turn:  # Wrong color selected
				print("Selected opponent piece. Choose again.")
			elif self.is_jump and pose not in self.pieces_with_jumps:  # Exist move with more jumps
				print(f"Select one of pieces with jumps: {self.pieces_with_jumps}")
			elif (not self.is_jump) and pose not in self.pieces_with_moves:  # No possible move on selected piece
				print(f"Select piece with move: {self.pieces_with_moves}")
			else:  # Select valid piece
				board.selected_piece = selected_tile.occupying_piece
				self.valid_moves = board.selected_piece.valid_moves()
				self.beaten_in_jumps, self.valid_jumps, _ = board.selected_piece.find_longest_chain_jumps()
				board.update_marks(self.valid_moves, self.valid_jumps)
			return empty_output
		else:  # user select target tile pose or jump / jumps chain
			valid_select = False
			no_jump = -1
			if self.is_jump:
				if len(self.valid_jumps) > pose[0] >= 0 and pose[1] == -1:
					no_jump = pose[0]
					valid_select = True
				else:
					print(f"Select valid jump.")
					return False
			elif not valid_select:
				for moves in self.valid_moves:
					if pose in moves or pose == moves:
						valid_select = True
						break
				if not valid_select:
					print(f"Select tile with valid move.")
					return False
			if valid_select:
				king_column = -1
				beaten_in_chain = []
				moves_from = []
				if self.is_jump:
					selected_jump = self.valid_jumps[no_jump]
					moves_to = selected_jump
					beaten_in_chain = self.beaten_in_jumps[no_jump]
					for p in selected_jump:
						moves_from.append(board.selected_piece.get_pose())
						move_status = board.selected_piece.move(p)
						if move_status == 2:
							king_column = p[1]
						# board.draw()
						# time.sleep(1.5)
					for op in beaten_in_chain:  # remove beaten pieces
						board.get_tile(op).occupying_piece = None
				else:  # normal move
					moves_from.append(board.selected_piece.get_pose())
					move_status = board.selected_piece.move(pose)
					moves_to = [pose]
					if move_status == 2:
						king_column = pose[1]
				board.next_turn()
				return moves_from, moves_to, beaten_in_chain, king_column

	def get_valid_moves(self):
		return self.valid_moves

	def get_valid_jumps(self):
		return self.valid_jumps
