import random

BOT_MODE = 0  # 0 random, 1 first available move


def move_select(moves):
    if BOT_MODE == 0:
        pose_ = random.choice(moves)
    elif BOT_MODE == 1:
        pose_ = moves[0]
    else:
        pose_ = -1, -1
    return pose_


def jump_select(jumps):
    if BOT_MODE == 0:
        jump_ = random.randint(0, len(jumps)-1)
    elif BOT_MODE == 1:
        jump_ = len(jumps) - 1
    else:
        jump_ = -1
    return jump_, -1


def select_piece(pieces_with_jumps, pieces_with_moves):
    if pieces_with_jumps:
        if BOT_MODE == 0:
            selected_ = random.choice(pieces_with_jumps)
        elif BOT_MODE == 1:
            selected_ = pieces_with_jumps[0]
        else:
            selected_ = (-1, -1)
    elif pieces_with_moves:
        if BOT_MODE == 0:
            selected_ = random.choice(pieces_with_moves)
        elif BOT_MODE == 1:
            selected_ = pieces_with_moves[0]
        else:
            selected_ = (-1, -1)
    else:
        selected_ = (-1, -1)
    return selected_


class ChessBot:
    def __init__(self):
        pass
