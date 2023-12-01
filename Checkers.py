import Board
from Game import Game


class Checkers:
	def __init__(self):
		self.running = True

	def main(self):
		game = Game()
		board = Board.Board()
		while self.running:
			board.draw()
			if not game.is_game_over(board):
				if not board.is_piece_selected():
					input_message = 'Select piece (e.g. A1 B2): '
				else:
					if game.is_jump:
						input_message = f'Select no. jump (e.g. J0 J1): '
						valid_jumps = game.valid_jumps
						for i in range(len(valid_jumps)):
							jumps = [Board.pose_to_coordinate(p) for p in valid_jumps[i]]
							input_message += f"\nNo. {i} - {jumps}"
						input_message += ": "
					else:
						input_message = 'Select target (e.g. A1 B2): '
				user_input = input(input_message)
				pose = Board.coordinate_to_pose(user_input)
				game.handle_pose_input(board, pose)
			else:
				game.final_message()
				self.running = False


if __name__ == "__main__":
	checkers = Checkers()
	checkers.main()
