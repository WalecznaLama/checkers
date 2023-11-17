from Piece import Piece


class King(Piece):
	def __init__(self, row, column, color, board):
		super().__init__(row, column, color, board)
		self.representation = color.upper()

	def possible_moves(self, pose):  # available moves on empty board
		moves_ru = []  # RightUp (A1 to H8)
		moves_rd = []  # RightDown (A8 to H1)
		moves_ld = []  # LeftDown (H8 to A1)
		moves_lu = []  # LeftUp (H1 to A8)
		r = pose[0]
		c = pose[1]

		for i in range(1, self.board.BOARD_SIZE):  # RightUp (A1 to H8)
			if r + i > self.board.BOARD_SIZE - 1 or c + i > self.board.BOARD_SIZE - 1:
				break
			else:
				moves_ru.append((i, i))
		for i in range(1, self.board.BOARD_SIZE):  # RightDown (A8 to H1)
			if r - i < 0 or c + i > self.board.BOARD_SIZE - 1:
				break
			else:
				moves_rd.append((-i, i))
		for i in range(1, self.board.BOARD_SIZE):  # LeftDown (H8 to A1)
			if r - i < 0 or c - i < 0:
				break
			else:
				moves_ld.append((-i, -i))
		for i in range(1, self.board.BOARD_SIZE):  # LeftUp (H1 to A8)
			if r + i > self.board.BOARD_SIZE - 1 or c - i < 0:
				break
			else:
				moves_lu.append((i, -i))
		return [moves_ru, moves_rd, moves_ld, moves_lu]

	def valid_moves(self):
		valid_moves = []
		moves = self.possible_moves(self.pose)
		for direction in moves:
			for move in direction:
				if self.board.is_tile_empty((self.pose[0]+move[0], self.pose[1]+move[1])):
					valid_moves.append(move)
				else:
					break
		if valid_moves:
			return valid_moves
		else:
			return False

	# valid jumps with pose of beaten opponent, except_pose for skip start pose in chain
	def _valid_jumps(self, pose, except_pose=None):
		valid_jumps = []
		moves = self.possible_moves(pose)  # all possible piece moves, assuming that board is empty
		opponent = self.board.get_opponent_color()
		for direction in moves:
			hit_opponent = False  # opponent at tile
			beaten_pose = None
			beaten_pose_buff = None  # buffer for beaten pose - necessary because used in next loop
			valid_behind_moves = []  # valid moves behind beaten opponent
			for move in direction:
				move_tile = (pose[0]+move[0], pose[1]+move[1])
				# empty tile behind opponent
				if (self.board.is_tile_empty(move_tile) or move_tile == except_pose) and hit_opponent:
					valid_behind_moves.append(move)
					beaten_pose = beaten_pose_buff
				elif self.board.get_tile_color(move_tile) == opponent:  # tile with opponent
					hit_opponent = True
					beaten_pose_buff = move_tile
				elif hit_opponent:  # first not empty tile behind opponent
					break
			if hit_opponent:
				valid_jumps.append([beaten_pose, valid_behind_moves])
				beaten_pose = []
				valid_behind_moves = []
		return valid_jumps

	def _find_chain_jumps(self, current_position, beaten_pieces=None, except_pose=None):
		if beaten_pieces is None:
			beaten_pieces = set()

		valid_jumps = self._valid_jumps(current_position, except_pose=except_pose)
		all_chains = []

		for beaten_pose, moves_after_beating in valid_jumps:
			if beaten_pose not in beaten_pieces:
				new_beaten_pieces = beaten_pieces.copy()
				new_beaten_pieces.add(beaten_pose)
				for move in moves_after_beating:
					new_position = (current_position[0] + move[0], current_position[1] + move[1])
					further_jumps = self._find_chain_jumps(new_position, new_beaten_pieces, except_pose)

					if further_jumps:
						for chain, beaten_in_chain in further_jumps:
							all_chains.append(([new_position] + chain, beaten_in_chain))
					else:
						all_chains.append(([new_position], new_beaten_pieces))

		return all_chains

	def find_longest_chain_jumps(self):
		chains = self._find_chain_jumps(self.pose, except_pose=self.pose)
		longest_chains = []
		if not chains:  # empty
			return False
		else:  # find the longest chain
			max_len = 0
			for i in chains:
				max_len = max(max_len, len(i[1]))

		for i in chains:  # add the longest chains to return variable
			if len(i[1]) == max_len:
				longest_chains.append(i)

		return longest_chains
