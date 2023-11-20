class Piece:
	def __init__(self, row, column, color, board):
		self.row = row
		self.column = column
		self.pose = (row, column)

		self.color = color
		self.board = board
		self.is_alive = True

	def move(self, pose, valid_jumps, valid_moves):
		self.board.reset_tile_marks()

		selected_tile = self.board.get_tile(pose)

		return True
		# TODO

	def get_pose(self):
		pose = (self.row, self.column)
		return pose

	def is_alive(self):
		return self.is_alive

	def kill(self):
		self.is_alive = False
