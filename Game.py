def get_pieces_with_given_jumps(board, longest_chain_len):
	pieces_with_best_jumps = []
	for row in range(board.BOARD_SIZE):
		for column in range(board.BOARD_SIZE):
			pose = (row, column)
			if board.get_tile_color(pose) == board.turn:
				chains = board.get_tile(pose).occupying_piece.find_longest_chain_jumps()
				if chains:
					for chain in chains:
						if len(chain[1]) == longest_chain_len:  # [1] are opponent poses
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


def get_pieces_with_best_jumps(board):
	longest_jump = 0
	for tile in board.tile_list:
		if tile.occupying_piece is not None:
			if tile.occupying_piece.color == board.turn:
				chain_len = tile.occupying_piece.find_longest_chain_jumps()
				if chain_len:
					longest_jump = max(longest_jump, chain_len)
	if longest_jump != 0:
		return get_pieces_with_given_jumps(board, longest_jump)
	else:
		return False


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

	def handle_pose_input(self, board, pose):  # TODO
		selected_tile = board.get_tile(pose)
		if not board.is_piece_selected():  # user select piece
			if selected_tile.occupying_piece is None:  # Empty tile
				print("Selected empty tile. Choose again.")
				return False
			elif selected_tile.occupying_piece.color != board.turn:  # Wrong color selected
				print("Selected opponent piece. Choose again.")
				return False
			else:
				pieces_with_best_jumps = get_pieces_with_best_jumps(board)
				if pose not in pieces_with_best_jumps:  # Exist move with more jumps
					print(f"Select one of pieces with jumps: {pieces_with_best_jumps}")
					return False
				pieces_with_moves = get_pieces_with_moves(board)
				if pose not in pieces_with_moves:  # No possible move on selected piece
					print(f"Select piece with move: {pieces_with_moves}")
				board.selected_piece = selected_tile.occupying_piece
				# TODO update tile marks
		else:  # user select target
			print()  # TODO



