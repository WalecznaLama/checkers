from Pawn import Pawn
from Tile import Tile


def coordinate_to_pose(coordinate):  # Map coordinates (A1, B2, ...) to row, column
    i_row = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
    pose = (int(coordinate[1]) - 1, i_row[coordinate[0].upper()])  # ! First column, then row (A1, B3,...) !
    return pose


class Board:
    BOARD_SIZE = 8
    WHITE = 'w'
    BLACK = 'b'
    EMPTY = ''
    
    def __init__(self):
        self.turn = self.WHITE  # white first turn
        self.is_jump = False
        self.selected_piece = None

        # self.setup_config = [
        #     [self.WHITE, self.EMPTY, self.WHITE, self.EMPTY, self.WHITE, self.EMPTY, self.WHITE, self.EMPTY],  # A
        #     [self.EMPTY, self.WHITE, self.EMPTY, self.WHITE, self.EMPTY, self.WHITE, self.EMPTY, self.WHITE],  # B
        #     [self.WHITE, self.EMPTY, self.WHITE, self.EMPTY, self.WHITE, self.EMPTY, self.WHITE, self.EMPTY],  # C
        #     [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY],  # D
        #     [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY],  # E
        #     [self.EMPTY, self.BLACK, self.EMPTY, self.BLACK, self.EMPTY, self.BLACK, self.EMPTY, self.BLACK],  # F
        #     [self.BLACK, self.EMPTY, self.BLACK, self.EMPTY, self.BLACK, self.EMPTY, self.BLACK, self.EMPTY],  # G
        #     [self.EMPTY, self.BLACK, self.EMPTY, self.BLACK, self.EMPTY, self.BLACK, self.EMPTY, self.BLACK]]  # H

        self.setup_config = [
            [self.WHITE, self.EMPTY, self.WHITE, self.EMPTY, self.WHITE, self.EMPTY, self.WHITE, self.EMPTY],  # A
            [self.EMPTY, self.WHITE, self.EMPTY, self.WHITE, self.EMPTY, self.WHITE, self.EMPTY, self.WHITE],  # B
            [self.WHITE, self.EMPTY, self.WHITE, self.EMPTY, self.WHITE, self.EMPTY, self.WHITE, self.EMPTY],  # C
            [self.EMPTY, self.BLACK, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY],  # D
            [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY],  # E
            [self.EMPTY, self.BLACK, self.EMPTY, self.BLACK, self.EMPTY, self.EMPTY, self.EMPTY, self.BLACK],  # F
            [self.BLACK, self.EMPTY, self.BLACK, self.EMPTY, self.BLACK, self.EMPTY, self.BLACK, self.EMPTY],  # G
            [self.EMPTY, self.BLACK, self.EMPTY, self.BLACK, self.EMPTY, self.BLACK, self.EMPTY, self.EMPTY]]  # H

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

    def is_piece_selected(self):
        return self.selected_piece is not None

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

