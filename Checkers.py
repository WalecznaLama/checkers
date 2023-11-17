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
