from typing import List
from .valid_inputs import *
import pygame


class Game:

    def __init__(self, board, player1, player2,
                 p1_initial_pos: List, p2_initial_pos: List):
        self.ticks = 0
        self.board = board
        self.board.set(player1, *p1_initial_pos)
        self.board.set(player2, *p2_initial_pos)
        self.player1 = player1
        self.player2 = player2
        self.winner = -1


    def get_score(self, bot):
        if self.is_gameover:
            return 10000 if self.winner == bot else 0
        return bot.health - self.opponent(bot).health

    def opponent(self, bot):
        return self.player1 if bot == self.player2 else self.player1

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
        self.player1.tick(self)
        self.player2.tick(self)

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
