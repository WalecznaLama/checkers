class Tile:
	POSSIBLE_MOVE = '*'
	POSSIBLE_JUMP = '@'

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.occupying_piece = None
		self.mark = None

	def is_empty(self):
		return self.occupying_piece is None

	def set_possible_move(self):
		self.mark = self.POSSIBLE_MOVE

	def set_possible_jump(self):
		self.mark = self.POSSIBLE_JUMP

	def clear_mark(self):
		self.mark = None
