from typing import List
from .valid_inputs import *
from .bots import Bot
import pygame


class Game:

    def __init__(self, board, player1, player2,
                 p1_initial_pos: List, p2_initial_pos: List,
                 max_game_ticks: int):
        self.ticks = 0
        self.max_game_ticks = max_game_ticks
        self.board = board
        self.board.set(player1, *p1_initial_pos)
        self.board.set(player2, *p2_initial_pos)
        self.player1 = player1
        self.player2 = player2
        self.winner = -1

        # Reward hacking variables
        self.distance_reward_coefficient = -1.
        self.health_reward_coefficient = 10.
        self.winning_reward_coefficient = 1000.


    def get_score(self, bot):
        if self.is_gameover():
            # ASSUMPTION self.winner must either be self.player1 or self.player2
            x = 1 if self.winner == bot else -1
            return x * self.winning_reward_coefficient
        else:
            opponent = self.opponent(bot)
            distance = self._compute_distance(bot, opponent)
            health_diff = self._compute_health_diference(bot, opponent)
            return (distance * self.distance_reward_coefficient
                    + health_diff * self.health_reward_coefficient)

    def _compute_distance(self, bot1: Bot, bot2: Bot) -> float:
        x_distance = abs((bot1.pos_x - bot1.pos_x) / len(self.board.grid[0]))
        y_distance = abs((bot1.pos_y - bot2.pos_y) / len(self.board.grid[1]))
        return x_distance + y_distance


    def _compute_health_diference(self, bot1: Bot, bot2: Bot) -> float:
        normalize = lambda b: b.health / b.max_health
        return normalize(bot1) - normalize(bot2)


    def opponent(self, bot):
        if bot == self.player2: return self.player1
        if bot == self.player1: return self.player2

    # Advance the game state until an input is needed
    def step(self):
        while not self.is_waiting() and not self.is_gameover():
            self.tick()

    def is_gameover(self):
        return self.winner != -1

    # Is the game waiting to recieve ANY input?
    def is_waiting(self):
        return self.is_waiting_for(self.player1) or self.is_waiting_for(self.player2)

    # Advance the game state one tick
    def tick(self):
        self.ticks += 1
        self.player1.tick(self)
        self.player2.tick(self)

        if self.ticks >= self.max_game_ticks:
            self.player1.health -= 1
            self.player2.health -= 1

        if self.player1.health <= 0:
            self.winner = self.player2
        elif self.player2.health <= 0:
            self.winner = self.player1

    # resolve actions, then resolve moves.
    def handle_input(self, state, player1_input, player2_input):
        if not self.is_gameover():
            self.take_actions(state, player1_input, player2_input)
            self.make_moves(player1_input, player2_input)
            self.tick()

    # do we need input from this bot? i.e. is the bot asleep?
    def is_waiting_for(self, bot):
        return not bot.is_sleeping()

    # is this input valid for this bot?
    def is_valid_for(self, bot, inp):
        return inp in bot.get_valid_moves(self)

    # activate specials
    def take_actions(self, state, player1_input, player2_input):
        if player1_input == ACTION: self.player1.act(state)
        if player2_input == ACTION: self.player2.act(state)

    # Make directional moves
    def make_moves(self, player1_input, player2_input):
        self.board.resolve_moves(self.player1, player1_input, self.player2, player2_input)
        # if this bot moved, put it to sleep based on speed.
        if player1_input in DIRECTIONS: self.player1.after_move()
        if player2_input in DIRECTIONS: self.player2.after_move()
