class Game:

    def __init__(self, board, player1, player2):
        self.ticks = 0
        self.board = board
        self.board.set(player1, 1, 1)
        self.board.set(player2, 8, 8)
        self.player1 = player1
        self.player2 = player2
        self.winner = None

    # Advance the game state until an input is needed
    def step(self):
        while not (self.player1.get_moves(self) or self.player2.get_moves(self)):
            self.tick()

    # Advance the game state one tick
    def tick(self):
        self.player1.tick(self)
        self.player2.tick(self)

    # Make directional moves
    def make_moves(self, player1_move, player2_move):
        self.board.resolve_moves(self.player1, player1_move, self.player2, player2_move)


class Bot:

    def __init__(self):
        self.ticks_between_moves = 0
        self.sleep = 0
        self.weight = 1
        self.pos_x = -100
        self.pos_y = -100

    def tick(self, state):
        if self.sleep > 0:
            self.sleep -= 1

        self.tick_bot(state)

    def get_moves(self, state):
        moves = [None]

        if self.sleep == 0:
            moves += self.get_moves_bot(state) + self.get_actions_bot(state)

        return moves

    def get_moves_bot(self, state):
        return state.board.get_valid_moves(self)

    def after_move(self, direction, state):
        self.sleep = self.ticks_between_moves

    def act(self):
        pass

    def tick_bot(self, state):
        pass

    def get_actions_bot(self, state):
        return []
