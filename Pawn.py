from Piece import Piece


class Pawn(Piece):
    def __init__(self, row, column, color, board):
        super().__init__(row, column, color, board)

    def _possible_moves(self):  # available moves on empty board
        possible_moves = []
        row_direction = 1 if self.color == self.board.WHITE else -1
        rules_moves = ((1 * row_direction, 1), (1 * row_direction, -1))
        for i in range(len(rules_moves)):
            if (0 <= self.row + rules_moves[i][0] <= self.board.BOARD_SIZE - 1
                    and 0 <= self.column + rules_moves[i][1] <= self.board.BOARD_SIZE - 1):
                possible_moves.append(rules_moves[i])
        return possible_moves

    def valid_moves(self):
        valid_moves = []
        moves = self._possible_moves()
        for move in moves:
            move_pose = (self.pose[0] + move[0], self.pose[1] + move[1])
            if self.board.is_tile_empty(move_pose):
                valid_moves.append(move_pose)
        return valid_moves

    def _possible_jump_moves(self, pose):  # available jumps on empty board
        possible_moves = []
        all_jumps = ((2, 2), (-2, 2), (-2, -2), (2, -2))  # RightUp, RightDown, LeftDown, LeftUp
        for i in range(len(all_jumps)):
            if (0 <= pose[0] + all_jumps[i][0] <= self.board.BOARD_SIZE - 1
                    and 0 <= pose[1] + all_jumps[i][1] <= self.board.BOARD_SIZE - 1):
                possible_moves.append(all_jumps[i])
        return possible_moves

    # valid jumps with pose of beaten opponent, except_pose for skip start pose in chain
    def _valid_jumps(self, pose, except_pose=None):
        valid_jumps = []
        # all possible piece jump positions, assuming that board is empty
        possible_jumps = self._possible_jump_moves(pose)
        opponent = self.board.get_opponent_color()
        for jump in possible_jumps:
            adjacent_move = (pose[0] + int(jump[0] / 2), pose[1] + int(jump[1] / 2))  # closest black tiles poses
            jump_move = (pose[0] + jump[0], pose[1] + jump[1])
            # tile with opponent
            if self.board.get_tile_color(adjacent_move) == opponent:
                if self.board.is_tile_empty(jump_move) or jump_move == except_pose:  # empty tile behind opponent
                    valid_jumps.append([adjacent_move, jump])
        return valid_jumps

    def _find_chain_jumps(self, current_position, beaten_pieces=None, except_pose=None):
        if beaten_pieces is None:
            beaten_pieces = set()

        valid_jumps = self._valid_jumps(current_position, except_pose=except_pose)
        all_chains = []

        for beaten_pose, jump in valid_jumps:
            if beaten_pose not in beaten_pieces:
                new_beaten_pieces = beaten_pieces.copy()
                new_beaten_pieces.add(beaten_pose)

                new_position = (current_position[0] + jump[0], current_position[1] + jump[1])

                further_jumps = self._find_chain_jumps(new_position, new_beaten_pieces, except_pose=except_pose)

                if further_jumps:
                    for chain, beaten_in_chain in further_jumps:
                        all_chains.append(([new_position] + chain, beaten_in_chain))
                else:
                    all_chains.append(([new_position], new_beaten_pieces))

        return all_chains

    def find_longest_chain_jumps(self):
        chains = self._find_chain_jumps(self.pose, except_pose=self.pose)
        longest_chains_jumps = []
        longest_chains_beaten = []
        max_len = 0
        if not chains:  # empty
            return longest_chains_beaten, longest_chains_jumps, max_len
        else:  # find the longest chain
            for i in chains:
                max_len = max(max_len, len(i[0]))  # [1] - beaten poses

        for i in chains:  # add the longest chains to return variable
            if len(i[1]) == max_len:  # [1] - beaten poses
                longest_chains_beaten.append(i[1])
                longest_chains_jumps.append(i[0])

        return longest_chains_beaten, longest_chains_jumps, max_len
