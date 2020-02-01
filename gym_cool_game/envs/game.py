class Game:

    def __init__(self, board, player1, player2):
        self.ticks = 0
        self.board = board
        self.board.set(0, 0, player1)
        self.board.set(9, 9, player2)
        self.winner = None

    # Advance the game state until an input is needed
    def step(self):
        while not (self.player1.get_moves(self) or self.player2.get_moves(self)):
            self.tick()

    # Advance the game state one tick
    def tick(self):
        self.player1.tick(self)
        self.player2.tick(self)


class Bot:

    def __init__(self):
        self.ticks_between_moves = 0
        self.sleep = 0
        self.pos = [-100, -100]

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

    def move(self, direction, state):
        state.board.move(self, direction)
        self.sleep = self.ticks_between_moves

    def tick_bot(self, state):
        pass

    def get_actions_bot(self, state):
        pass
