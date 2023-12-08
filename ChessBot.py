import random


def move_select(moves):
    # pose_ = moves[0]
    pose_ = random.choice(moves)
    return pose_


def jump_select(jumps):
    # jump_ = len(jumps) - 1
    jump_ = random.randint(0, len(jumps)-1)
    return jump_, -1


def select_piece(pieces_with_jumps, pieces_with_moves):
    if pieces_with_jumps:
        # selected_ = pieces_with_jumps[0]
        selected_ = random.choice(pieces_with_jumps)

    elif pieces_with_moves:
        # selected_ = pieces_with_moves[0]
        selected_ = random.choice(pieces_with_moves)
    else:
        selected_ = (-1, -1)
    return selected_


class ChessBot:
    def __init__(self):
        pass
