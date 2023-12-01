class Piece:
	def __init__(self, row, column, color, board):
		self.row = row
		self.column = column
		self.pose = (self.row, self.column)
		self.color = color
		self.board = board
		self.representation = self.color

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
		else:
			target_tile.occupying_piece = self

		return True

	def get_pose(self):
		pose = (self.row, self.column)
		return pose

