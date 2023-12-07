from robodk import *      # RoboDK API
from robolink import *    # Robot toolbox


class Robot:
    D_BETWEEN_TITLES = 45
    D_BETWEEN_KINGS = 40
    D_APPROACH = 70
    D_PAWN_HEIGHT = 10

    def __init__(self, robot_color):
        self.Rdk = robolink.Robolink()
        self.color = robot_color

        self.F_BOARD = f'Board'  # Board Center
        self.T_HOME = f'Home_{self.color}'
        self.T_KING = f'Corner_King_{self.color}'
        self.T_A1 = f'A1_{self.color}'
        self.T_BEATEN_STACK = f'Ded_Stack_{self.color}'
        self.SIGNAL_NAME = f"Working_{self.color}"

        self.robot = self.Rdk.Item(f'KUKA {self.color}', ITEM_TYPE_ROBOT)
        self.tool = self.Rdk.Item(f'TCP_{self.color[0]}', ITEM_TYPE_TOOL)

        # Frames
        self.f_board = self.Rdk.Item(self.F_BOARD, ITEM_TYPE_FRAME)

        # Targets
        self.t_home = self.Rdk.Item(self.T_HOME, ITEM_TYPE_TARGET)
        self.t_king = self.Rdk.Item(self.T_KING, ITEM_TYPE_TARGET)
        self.t_a1 = self.Rdk.Item(self.T_A1, ITEM_TYPE_TARGET)
        self.t_beaten_stack = self.Rdk.Item(self.T_BEATEN_STACK, ITEM_TYPE_TARGET)

        # Programs
        self.p_attach = self.Rdk.Item(f'Pick{self.color[0]}', ITEM_TYPE_PROGRAM)
        self.p_detach = self.Rdk.Item(f'Place{self.color[0]}', ITEM_TYPE_PROGRAM)
        self.p_wait = self.Rdk.Item(f'Wait{self.color[0]}', ITEM_TYPE_PROGRAM)

        self.used_kings = 0
        self.beaten_pawns = 0

        if self.color == 'White':
            self.robot.setDO(self.SIGNAL_NAME, 1)
        else:
            self.robot.setDO(self.SIGNAL_NAME, 0)

        self.robot.setPoseTool(self.tool)
        self.robot.MoveJ(self.t_home)
        self.robot.setPoseFrame(self.f_board)

    def move_j(self, target, transposition=None):
        pose = target.Pose()
        if transposition and len(transposition) == 3:
            pose *= transl(*transposition)
        self.robot.MoveJ(pose)

    def move_l(self, target, transposition=None):
        pose = target.Pose()
        if transposition and len(transposition) == 3:
            pose *= transl(transposition[0], transposition[1], transposition[2])
        self.robot.MoveL(pose)

    def pick_pawn(self, pose):
        self.move_j(self.t_a1, [pose[0] * self.D_BETWEEN_TITLES,
                                pose[1] * self.D_BETWEEN_TITLES, -self.D_APPROACH])
        self.move_l(self.t_a1, [pose[0] * self.D_BETWEEN_TITLES, pose[1] * self.D_BETWEEN_TITLES, 0.0])
        self.p_attach.RunProgram()
        self.p_attach.WaitFinished()
        self.move_l(self.t_a1, [pose[0] * self.D_BETWEEN_TITLES,
                                pose[1] * self.D_BETWEEN_TITLES, -self.D_APPROACH])

    def place_pawn(self, pose):
        self.move_j(self.t_a1, [pose[0] * self.D_BETWEEN_TITLES,
                                pose[1] * self.D_BETWEEN_TITLES, -self.D_APPROACH])
        self.move_l(self.t_a1, [pose[0] * self.D_BETWEEN_TITLES, pose[1] * self.D_BETWEEN_TITLES, 0.0])
        self.p_detach.RunProgram()
        self.p_detach.WaitFinished()
        self.move_l(self.t_a1, [pose[0] * self.D_BETWEEN_TITLES,
                                pose[1] * self.D_BETWEEN_TITLES, -self.D_APPROACH])

    def pick_king(self, n):
        r = n // 2
        c = n % 2
        self.move_j(self.t_king, [r * self.D_BETWEEN_KINGS, c * self.D_BETWEEN_KINGS, -self.D_APPROACH])
        self.move_l(self.t_king, [r * self.D_BETWEEN_KINGS, c * self.D_BETWEEN_KINGS, 0.0])
        self.p_attach.RunProgram()
        self.p_attach.WaitFinished()
        self.move_l(self.t_king, [r * self.D_BETWEEN_KINGS, c * self.D_BETWEEN_KINGS, -self.D_APPROACH])
        n += 1

    def place_dead(self, n):
        self.move_j(self.t_beaten_stack, [0.0, 0.0, -self.D_APPROACH - (n * self.D_PAWN_HEIGHT)])
        self.move_l(self.t_beaten_stack, [0.0, 0.0, -(n * self.D_PAWN_HEIGHT)])
        self.p_detach.RunProgram()
        self.p_detach.WaitFinished()
        self.move_l(self.t_beaten_stack, [0.0, 0.0, -self.D_APPROACH - (n * self.D_PAWN_HEIGHT)])
        n += 1

    def pawn_to_king(self, column):
        row = 7 if self.color == 'White' else 0
        pose = (row, column)
        self.pick_pawn(pose)
        self.place_dead(self.beaten_pawns + self.used_kings)
        self.pick_king(self.used_kings)
        self.place_pawn(pose)
        self.used_kings += 1

    def move_pawn(self, pose_from, pose_to):
        self.pick_pawn(pose_from)
        self.place_pawn(pose_to)

    def remove_pawn(self, pose):
        self.pick_pawn(pose)
        self.place_dead(self.beaten_pawns + self.used_kings)
        self.beaten_pawns += 1

    def wait_to_opponent(self):
        self.p_wait.RunProgram()
        self.p_wait.WaitFinished()

    def turn(self, moves_from: list, moves_to: list, remove_pawn: list, king_column: int):
        self.wait_to_opponent()
        self.robot.setDO(self.SIGNAL_NAME, 1)
        king_column_ = king_column

        for i in range(len(moves_from)):
            move_from = moves_from[i]
            move_to = moves_to[i]
            self.move_pawn(move_from, move_to)
            if move_to[1] == king_column_:
                self.pawn_to_king(move_to[1])
                king_column_ = -1  # promotion handled

        for i in range(len(remove_pawn)):
            self.remove_pawn(remove_pawn[i])

        self.robot.setDO(self.SIGNAL_NAME, 0)
        self.robot.MoveJ(self.t_home)
