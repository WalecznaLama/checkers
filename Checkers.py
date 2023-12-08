import time

import Board
from Game import Game
import ChessBot
from Robot import Robot


def player_input(board, game):
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
	p_input = input(input_message)
	return p_input


def bot_input(board, game):
	pieces_with_jumps = game.get_pieces_with_best_jumps(board)  # TODO
	pieces_with_moves = game.get_pieces_with_moves(board)
	if not board.is_piece_selected():
		return ChessBot.select_piece(pieces_with_jumps, pieces_with_moves)

	if game.is_jump:  # Select no. jump (e.g. J0 J1)
		valid_jumps = game.valid_jumps
		return ChessBot.jump_select(valid_jumps)
	else:
		valid_moves = game.get_valid_moves()
		return ChessBot.move_select(valid_moves)


class Checkers:
	def __init__(self):
		self.running = True
		self.turn = None
		self.WhiteRobot = Robot("White")
		self.BlackRobot = Robot("Black")

	def main(self):
		game = Game()
		board = Board.Board()
		while self.running:
			self.turn = board.get_turn()
			# board.draw()
			if not game.is_game_over(board):
				# if self.turn == board.WHITE:
				# 	coordinates = player_input(board, game)
				# 	pose = Board.coordinate_to_pose(coordinates)
				# else:
				# time.sleep(0.5)
				pose = bot_input(board, game)
				moves_from, moves_to, beaten_in_chain, king_column = game.handle_pose_input(board, pose)
				if self.turn == board.WHITE:
					self.WhiteRobot.turn(moves_from, moves_to, beaten_in_chain, king_column)
				else:
					self.BlackRobot.turn(moves_from, moves_to, beaten_in_chain, king_column)
				board.promotion_handled()
			else:
				game.final_message()
				self.running = False


if __name__ == "__main__":
	checkers = Checkers()
	checkers.main()
