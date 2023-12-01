class Piece:
	def __init__(self, row, column, color, board):
		self.row = row
		self.column = column
		self.pose = (self.row, self.column)

		self.color = color
		self.board = board
		self.is_alive = True

	def move(self, target_pose):
		self.board.reset_tile_marks()
		self.board.get_tile(self.pose).occupying_piece = None
		self.row = target_pose[0]
		self.column = target_pose[1]
		self.pose = (self.row, self.column)  # TODO check if necessary
		self.board.get_tile(self.pose).occupying_piece = self

		#  check if row 0 or 7 enough because pawn move possible forward only
		if self.row == 0 or self.row == 7:  # TODO promotion to king ()
			pass

		return True

	def get_pose(self):
		pose = (self.row, self.column)
		return pose

	def is_alive(self):
		return self.is_alive

	def kill(self):
		self.is_alive = False
