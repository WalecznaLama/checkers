from Piece import Piece


class Pawn(Piece):
    def __init__(self, row, column, color, board):
        super().__init__(row, column, color, board)
        self.representation = color

    def _possible_moves(self):  # available moves on empty board
        possible_moves = []
        row_direction = 1 if self.color == self.board.WHITE else -1
        rules_moves = [[1 * row_direction, 1], [1 * row_direction, -1]]
        for i in range(len(rules_moves)):
            if (0 < self.row + rules_moves[i][0] < self.board.BOARD_SIZE - 1
                    and 0 < self.column + rules_moves[i][1] < self.board.BOARD_SIZE - 1):
                possible_moves.append(rules_moves[i])
        return possible_moves

    def _possible_jump_moves(self):  # available jumps on empty board
        possible_moves = []
        all_jumps = [[2, 2], [-2, 2], [-2, -2], [2, -2]]  # RightUp, RightDown, LeftDown, LeftUp
        for i in range(len(all_jumps)):
            if (0 <= self.row + all_jumps[i][0] <= self.board.BOARD_SIZE - 1
                    and 0 <= self.column + all_jumps[i][1] <= self.board.BOARD_SIZE - 1):
                possible_moves.append(all_jumps[i])
        return possible_moves

    def valid_moves(self):
        valid_moves = []
        moves = self._possible_moves()
        for move in moves:
            if self.board.is_tile_empty(self.row + move[0], self.column + move[1]):
                valid_moves.append(move)
        return valid_moves

    def valid_jumps(self):
        valid_jumps = []
        possible_jumps = self._possible_jump_moves()
        opponent = self.board.get_opponent_color()
        for jump in possible_jumps:
            adjacent_move = [int(jump[0] / 2), int(jump[1] / 2)]
            # tile with opponent
            if self.board.get_tile_color(adjacent_move[0], adjacent_move[1]) == opponent:
                if self.board.is_tile_empty(self.row + jump[0], self.column + jump[1]):  # empty tile behind opponent
                    valid_jumps.append(jump)
        return valid_jumps
