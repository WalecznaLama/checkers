from Piece import Piece


class Pawn(Piece):
    def __init__(self, row, column, color, board):
        super().__init__(row, column, color, board)
        self.representation = color

    def _possible_moves(self):  # available moves on empty board
        possible_moves = []
        row_direction = 1 if self.color == self.board.WHITE else -1
        rules_moves = ((1 * row_direction, 1), (1 * row_direction, -1))
        for i in range(len(rules_moves)):
            if (0 < self.row + rules_moves[i][0] < self.board.BOARD_SIZE - 1
                    and 0 < self.column + rules_moves[i][1] < self.board.BOARD_SIZE - 1):
                possible_moves.append(rules_moves[i])
        return possible_moves

    def valid_moves(self):
        valid_moves = []
        moves = self._possible_moves()
        for move in moves:
            if self.board.is_tile_empty((self.row + move[0], self.column + move[1])):
                valid_moves.append(move)
        return valid_moves

    def _possible_jump_moves(self, pose):  # available jumps on empty board
        possible_moves = []
        all_jumps = ((2, 2), (-2, 2), (-2, -2), (2, -2))  # RightUp, RightDown, LeftDown, LeftUp
        for i in range(len(all_jumps)):
            if (0 <= pose[0] + all_jumps[i][0] <= self.board.BOARD_SIZE - 1
                    and 0 <= pose[1] + all_jumps[i][1] <= self.board.BOARD_SIZE - 1):
                possible_moves.append(all_jumps[i])
        return possible_moves

    def valid_jumps(self, pose):  # TODO skip start pose in chain
        valid_jumps = []
        # all possible piece jump positions, assuming that board is empty
        possible_jumps = self._possible_jump_moves(pose)
        opponent = self.board.get_opponent_color()
        for jump in possible_jumps:
            adjacent_move = (pose[0] + int(jump[0] / 2), pose[1] + int(jump[1] / 2))  # closest black tiles poses
            # tile with opponent
            if self.board.get_tile_color(adjacent_move) == opponent:
                if self.board.is_tile_empty((pose[0] + jump[0], pose[1] + jump[1])):  # empty tile behind opponent
                    valid_jumps.append(jump)
        return valid_jumps

    def find_chain_jumps(self, current_position, beaten_pieces=None):
        if beaten_pieces is None:
            beaten_pieces = set()

        valid_jumps = self.valid_jumps(current_position)
        all_chains = []

        for jump in valid_jumps:
            new_position = (current_position[0] + jump[0], current_position[1] + jump[1])
            adjacent_move = (int(jump[0] / 2), int(jump[1] / 2))
            beaten_piece = (current_position[0] + adjacent_move[0], current_position[1] + adjacent_move[1])

            if beaten_piece not in beaten_pieces:
                beaten_pieces.add(beaten_piece)
                further_jumps = self.find_chain_jumps(new_position, beaten_pieces.copy())

                if further_jumps:
                    for chain, beaten_in_chain in further_jumps:
                        all_chains.append(([new_position] + chain, beaten_pieces.union(beaten_in_chain)))
                else:
                    all_chains.append(([new_position], beaten_pieces))

        return all_chains

    def find_longest_chain_jumps(self):
        chains = self.find_chain_jumps(self.pose)
        longest_chains = []
        if not chains:  # empty
            return None
        else:  # find the longest chain
            max_len = 0
            for i in chains:
                max_len = max(max_len, len(i[1]))

        for i in chains:  # add the longest chains to return variable
            if len(i[1]) == max_len:
                longest_chains.append(i)

        return longest_chains
