from Pawn import Pawn
from Tile import Tile


def coordinate_to_pose(coordinate):  # Map coordinates (A1, B2, ...) to row, column / or number of jump when J*
    except_return = (-1, -1)
    if len(coordinate) != 2:
        print(f"Wrong input! Invalid length: {coordinate}")
        return except_return
    row = int(coordinate[1])
    if coordinate[0].lower() == 'j':
        return int(coordinate[1]), -1
    if not 9 > row > 0:
        print(f"Wrong input! Invalid row: {row}")
        return except_return
    try:
        i_row = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        pose = (int(coordinate[1]) - 1, i_row[coordinate[0].upper()])
        return pose
    except ValueError:
        print(f"Wrong input! Problem with number conversion: {coordinate}")
        return except_return
    except KeyError:
        print(f"Wrong input! Invalid row letter: {coordinate}")
        return except_return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return except_return


def pose_to_coordinate(pose):
    coordinate = ''
    i_row = 'ABCDEFGH'
    coordinate += i_row[pose[1]] + str(pose[0] + 1)
    return coordinate


class Board:
    BOARD_SIZE = 8
    WHITE = 'w'
    BLACK = 'b'
    EMPTY = ''

    def __init__(self):
        self.turn = self.WHITE  # white first turn
        self.is_jump = False
        self.selected_piece = None

        self.setup_config = [
            [self.WHITE, self.EMPTY, self.WHITE, self.EMPTY, self.WHITE, self.EMPTY, self.WHITE, self.EMPTY],  # A
            [self.EMPTY, self.WHITE, self.EMPTY, self.WHITE, self.EMPTY, self.WHITE, self.EMPTY, self.WHITE],  # B
            [self.WHITE, self.EMPTY, self.WHITE, self.EMPTY, self.WHITE, self.EMPTY, self.WHITE, self.EMPTY],  # C
            [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY],  # D
            [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY],  # E
            [self.EMPTY, self.BLACK, self.EMPTY, self.BLACK, self.EMPTY, self.BLACK, self.EMPTY, self.BLACK],  # F
            [self.BLACK, self.EMPTY, self.BLACK, self.EMPTY, self.BLACK, self.EMPTY, self.BLACK, self.EMPTY],  # G
            [self.EMPTY, self.BLACK, self.EMPTY, self.BLACK, self.EMPTY, self.BLACK, self.EMPTY, self.BLACK]]  # H

        # self.setup_config = [
        #     [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY],  # A
        #     [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY],  # B
        #     [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.BLACK, self.EMPTY, self.EMPTY, self.EMPTY],  # C
        #     [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY],  # D
        #     [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.BLACK, self.EMPTY],  # E
        #     [self.EMPTY, self.WHITE, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY],  # F
        #     [self.EMPTY, self.EMPTY, self.BLACK, self.EMPTY, self.BLACK, self.EMPTY, self.EMPTY, self.EMPTY],  # G
        #     [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY]]  # H

        self.tile_list = self._generate_tiles()
        self._setup()

    def _setup(self):
        for r_index, row in enumerate(self.setup_config):
            for c_index, x in enumerate(row):
                if x != self.EMPTY:
                    self.tile_list[r_index][c_index].occupying_piece = Pawn(r_index, c_index, x, self)

    def _generate_tiles(self):
        tile_list = []
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                tile_list.append(Tile(row, column))
        tiles_8x8 = [tile_list[i:i + self.BOARD_SIZE] for i in range(0,
                                                                     self.BOARD_SIZE*self.BOARD_SIZE,
                                                                     self.BOARD_SIZE)]
        return tiles_8x8

    def draw(self):
        selected_piece_pose = None if self.selected_piece is None else self.selected_piece.get_pose()
        for i, row in enumerate(reversed(self.tile_list)):  # reversed - more intuitive (0,0)==A1 bottom left
            tile_row = []
            for t in row:
                on_tile = ' '
                if t.occupying_piece is not None:
                    if t.occupying_piece.get_pose() == selected_piece_pose:
                        on_tile = "\033[4m" + t.occupying_piece.representation + "\033[0m"
                    else:
                        on_tile = t.occupying_piece.representation
                elif t.mark is not None:
                    on_tile = t.mark
                tile_row.append(on_tile)

            print(f"{self.BOARD_SIZE - i} | {' | '.join(tile_row)} |")
            if i < self.BOARD_SIZE - 1:
                print("  +---+---+---+---+---+---+---+---+")
        print("    A   B   C   D   E   F   G   H")

    def get_pieces_number(self):  # num of: white_piece, black_piece, white_king, black_king
        white_piece, black_piece, white_king, black_king = 0, 0, 0, 0
        for row in self.tile_list:
            for x in row:
                if x.occupying_piece is not None:
                    if x.occupying_piece.color == self.WHITE:
                        white_piece += 1
                        if x.occupying_piece.representation.isupper():
                            white_king += 1
                    else:
                        black_piece += 1
                        if x.occupying_piece.representation.isupper():
                            black_king += 1
        return white_piece, black_piece, white_king, black_king

    def get_tile(self, pose):
        return self.tile_list[pose[0]][pose[1]]

    def is_tile_empty(self, pose):
        return self.get_tile(pose).is_empty()

    def get_tile_color(self, pose):
        if not self.is_tile_empty(pose):
            return self.get_tile(pose).occupying_piece.color
        else:
            return self.EMPTY

    def reset_tile_marks(self):
        for row in self.tile_list:
            for t in row:
                t.clear_mark()

    def next_turn(self):
        self.turn = self.BLACK if self.turn == self.WHITE else self.WHITE
        self.selected_piece = None

    def is_piece_selected(self):
        return self.selected_piece is not None

    def get_selected_piece_pose(self):
        if self.is_piece_selected():
            return self.selected_piece.get_pose()

    def get_opponent_color(self):
        return self.BLACK if self.turn == self.WHITE else self.WHITE

    def get_white_poses(self):
        poses = []
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                if self.get_tile_color([row, column]) == self.WHITE:
                    poses.append((row, column))
        return poses

    def get_black_poses(self):
        poses = []
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                if self.get_tile_color((row, column)) == self.BLACK:
                    poses.append((row, column))
        return poses

    def get_current_board_state(self):  # returns BOARD_SIZExBOARD_SIZE list of colors positions on board
        r = []
        board = []
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                r.append(self.get_tile_color((row, column)))
            board.append(r)
            r = []
        return board

    def update_marks(self, valid_moves, valid_jumps):
        is_jump = len(valid_jumps) > 0
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                pose = (row, column)
                for jump in valid_jumps:
                    if pose in jump:
                        self.get_tile(pose).set_possible_jump()
                if not is_jump:
                    for move in valid_moves:
                        if pose in move or pose == move:
                            self.get_tile(pose).set_possible_move()

    def leave_tile(self, pose):
        self.get_tile(pose).occupying_piece = None

    def get_turn(self):
        return self.turn

    def get_promotion_column(self):
        index_ = 0 if self.turn == self.WHITE else self.BOARD_SIZE - 1
        row = self.tile_list[index_]
        column_ = -1
        for tile in row:
            if tile.occupying_piece.is_promotion_to_handle():
                column_ = tile.occupying_piece.get_pose()[1]

        return column_

    def promotion_handled(self):
        index_ = 0 if self.turn == self.WHITE else self.BOARD_SIZE - 1
        row = self.tile_list[index_]
        for tile in row:
            if not tile.is_empty():
                tile.occupying_piece.promotion_handled()
