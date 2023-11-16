class Tile:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.occupying_piece = None
		self.mark = None  # * - possible move; @ - possible jump

	def is_empty(self):
		return self.occupying_piece is None
