from robodk import *      # RoboDK API
from robolink import *    # Robot toolbox


class Robot:
    D_BETWEEN_TITLES = 45
    D_BETWEEN_KINGS = 40
    D_APPROACH = 80
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

        init_signal_ = 1 if self.color == 'White' else 0
        self.robot.setDO(self.SIGNAL_NAME, init_signal_)

        self.robot.setPoseTool(self.tool)
        self.robot.MoveJ(self.t_home)
        self.robot.setPoseFrame(self.f_board)

        if self.color == 'White':
            p_dk_init = self.Rdk.Item(f'Init', ITEM_TYPE_PROGRAM)
            p_dk_init.RunProgram()
            p_dk_init.WaitFinished()

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

    def pick_king(self):
        r = self.used_kings // 2
        c = self.used_kings % 2
        self.move_j(self.t_king, [r * self.D_BETWEEN_KINGS, c * self.D_BETWEEN_KINGS, -self.D_APPROACH])
        self.move_l(self.t_king, [r * self.D_BETWEEN_KINGS, c * self.D_BETWEEN_KINGS, 0.0])
        self.p_attach.RunProgram()
        self.p_attach.WaitFinished()
        self.move_l(self.t_king, [r * self.D_BETWEEN_KINGS, c * self.D_BETWEEN_KINGS, -self.D_APPROACH])
        self.used_kings += 1

    def place_dead(self):
        stack = self.beaten_pawns % 2
        height_multiply = self.beaten_pawns // 2

        self.move_j(self.t_beaten_stack, [stack*self.D_BETWEEN_TITLES, 0.0,
                                          -self.D_APPROACH - (self.beaten_pawns * self.D_PAWN_HEIGHT)])
        self.move_l(self.t_beaten_stack, [stack*self.D_BETWEEN_TITLES, 0.0, -(height_multiply * self.D_PAWN_HEIGHT)])
        self.p_detach.RunProgram()
        self.p_detach.WaitFinished()
        self.move_l(self.t_beaten_stack, [stack*self.D_BETWEEN_TITLES, 0.0,
                                          -self.D_APPROACH - (height_multiply * self.D_PAWN_HEIGHT)])
        self.beaten_pawns += 1

    def pawn_to_king(self, column):
        row_ = 7 if self.color == 'White' else 0
        pose_ = (row_, column)
        self.remove_pawn(pose_)
        self.pick_king()
        self.place_pawn(pose_)

    def move_pawn(self, pose_from, pose_to):
        self.pick_pawn(pose_from)
        self.place_pawn(pose_to)

    def remove_pawn(self, pose):
        self.pick_pawn(pose)
        self.place_dead()

    def wait_to_opponent(self):
        self.p_wait.RunProgram()
        self.p_wait.WaitFinished()

    def turn(self, moves_from: list, moves_to: list, remove_pawn: list, king_column: int):
        self.wait_to_opponent()
        self.robot.setDO(self.SIGNAL_NAME, 1)

        self.robot.setPoseTool(self.tool)
        self.robot.MoveJ(self.t_home)
        self.robot.setPoseFrame(self.f_board)

        king_column_ = king_column

        for i in range(len(moves_from)):
            move_from_ = moves_from[i]
            move_to_ = moves_to[i]
            self.move_pawn(move_from_, move_to_)
            if move_to_[1] == king_column_:
                self.pawn_to_king(king_column_)
                king_column_ = -1  # promotion handled

        remove_pawn_ = [elem for elem in remove_pawn]  # set to list
        for i in range(len(remove_pawn_)):
            self.remove_pawn(remove_pawn_[i])

        self.robot.setDO(self.SIGNAL_NAME, 0)
        self.robot.MoveJ(self.t_home)
