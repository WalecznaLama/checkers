class Piece:
	OUT_PROMOTE = 2

	def __init__(self, row, column, color, board):
		self.row = row
		self.column = column
		self.pose = (self.row, self.column)
		self.color = color
		self.board = board
		self.representation = self.color
		self.promotion_to_handle = False

	def move(self, target_pose):
		self.board.reset_tile_marks()
		self.board.get_tile(self.pose).occupying_piece = None
		self.row = target_pose[0]
		self.column = target_pose[1]
		self.pose = (self.row, self.column)  # TODO check if necessary
		target_tile = self.board.get_tile(self.pose)

		#  check if row 0 or 7 is enough - pawn possible move forward only
		if (self.row == 0 or self.row == 7) and self.representation.islower():
			from King import King
			target_tile.occupying_piece = King(self.row, self.column, self.color, self.board)
			self.promotion_to_handle = True
			return self.OUT_PROMOTE  # promotion -> 2
		else:
			target_tile.occupying_piece = self
			return 0  # ok normal -> 0

	def get_pose(self):
		return self.pose

	def is_promotion_to_handle(self):
		return self.promotion_to_handle

	def promotion_handled(self):
		self.promotion_to_handle = False
