from valid_inputs import *

class Game:

    def __init__(self, board, player1, player2):
        self.ticks = 0
        self.board = board
        self.board.set(player1, 2, 2)
        self.board.set(player2, 7, 7)
        self.player1 = player1
        self.player2 = player2
        self.winner = None

    # Advance the game state until an input is needed
    def step(self):
        while not self.is_waiting():
            self.tick()

    # Is the game waiting to recieve ANY input?
    def is_waiting(self):
        return self.is_waiting_for(self.player1) or self.is_waiting_for(self.player2)

    # Advance the game state one tick
    def tick(self):
        self.player1.tick(self)
        self.player2.tick(self)

    # resolve actions, then resolve moves.
    def handle_input(self, player1_input, player2_input):
        self.take_actions(player1_input, player2_input)
        self.make_moves(player1_input, player2_input)
        self.tick()

    # do we need input from this bot? i.e. is the bot asleep?
    def is_waiting_for(self, bot):
        return not bot.is_sleeping()

    # is this input valid for this bot?
    def is_valid_for(self, bot, inp):
        return inp in bot.get_moves(self)

    # activate specials
    def take_actions(self, player1_input, player2_input):
        if player1_input == ACTION:
            self.player1.act()

        if player2_input == ACTION:
            self.player2.act()

    # Make directional moves
    def make_moves(self, player1_input, player2_input):
        self.board.resolve_moves(self.player1, player1_input, self.player2, player2_input)
    
        # if this bot moved, put it to sleep based on speed.
        if player1_input in DIRECTIONS:
            self.player1.after_move()
        
        if player2_input in DIRECTIONS:
            self.player2.after_move()


class Bot:

    def __init__(self, name=""):
        self.ticks_between_moves = 1
        self.sleep = 0
        self.weight = 1
        self.pos_x = -100
        self.pos_y = -100
        self.name = str(name)

    def tick(self, state):
        if self.sleep > 0:
            self.sleep -= 1

        self.tick_bot(state)

    def is_sleeping(self):
        return self.sleep > 0

    def get_moves(self, state):
        moves = []

        if not self.is_sleeping():
            moves += self.get_moves_bot(state) + self.get_actions_bot(state)

        return moves

    def get_moves_bot(self, state):
        return DIRECTIONS

    def get_actions_bot(self, state):
        return [ACTION]

    def after_move(self):
        self.sleep = self.ticks_between_moves

    def act(self):
        pass

    def tick_bot(self, state):
        pass

    def __repr__(self):
        return self.name if self.name else "."