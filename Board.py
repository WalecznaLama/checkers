from Pawn import Pawn
from Tile import Tile


def coordinate_to_pose(coordinate):  # Map coordinates (A1, B2, ...) to row, column
    i_row = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    return int(coordinate[1]) - 1, i_row[coordinate[0].lower()]  # ! First column, then row (A1, B3,...) !


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
            [self.EMPTY, self.BLACK, self.EMPTY, self.BLACK, self.EMPTY, self.BLACK, self.EMPTY, self.BLACK]   # H
        ]

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
        for i, row in enumerate(reversed(self.tile_list)):  # reversed - more intuitive (0,0) bottom left
            tile = [" " if item.occupying_piece is None else item.occupying_piece.representation for item in row]
            print(f"{self.BOARD_SIZE - i} | {' | '.join(tile)} |")
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

    def get_tile(self, row, column):
        return self.tile_list[row][column]

    def is_tile_empty(self, row, column):
        return self.get_tile(row, column).is_empty()

    def get_tile_color(self, row, column):
        if not self.is_tile_empty(row, column):
            return self.get_tile(row, column).occupying_piece.color

    def reset_tile_marks(self):
        for i in self.tile_list:
            i.mark = None

    def next_turn(self):
        self.turn = self.BLACK if self.turn == self.WHITE else self.WHITE

    def is_piece_selected(self):
        return self.selected_piece is not None

    def handle_pose_input(self, row, column):  # TODO
        selected_tile = self.get_tile(row, column)

        if not self.is_piece_selected():  # user select piece
            if selected_tile.occupying_piece is None:
                print("Selected empty tile. Choose again.")
                return False
            elif selected_tile.occupying_piece.color != self.turn:
                print("Selected opponent piece. Choose again.")
                return False
            else:
                self.selected_piece = selected_tile.occupying_piece

    def get_opponent_color(self):
        return self.BLACK if self.turn == self.WHITE else self.WHITE

    def get_white_poses(self):
        poses = []
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                if self.get_tile(row, column).occupying_piece.color == self.WHITE:
                    poses.append([row, column])
        return poses

    def get_black_poses(self):
        poses = []
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                if self.get_tile(row, column).occupying_piece.color == self.BLACK:
                    poses.append([row, column])
        return poses
