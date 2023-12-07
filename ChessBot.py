def move_select(moves):
    pose = moves[0]
    return pose


def jump_select(jumps):
    return 0, -1


def select_piece(pieces_with_jumps, pieces_with_moves):
    if pieces_with_jumps:
        return pieces_with_jumps[0]
    elif pieces_with_moves:
        return pieces_with_moves[0]


class ChessBot:
    def __init__(self):
        pass
