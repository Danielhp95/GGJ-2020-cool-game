from typing import List
from copy import deepcopy
import numpy as np
import gym
from gym.spaces import Discrete, Box, Tuple
import pygame

from .game import Game
from .board import Board

from .bots import SawBot, TorchBot

BOT_TYPE_SPIKE = 0
BOT_TYPE_TORCH = 1
BOT_TYPE_NAIL = 1

class CoolGameEnv(gym.Env):

    def __init__(self,
                 botA_type: int = 0, botB_type: int = 1,
                 board_size: int = 10,
                 p1_starting_position: List = [2,2],
                 p2_starting_position: List = [7,7]
                 ):
        # Each player has 5 actions. Directional moves: UP / DOWN/ LEFT / RIGHT
        # And a 5th "Action", which is bot dependant

        # Game params
        self.p1_starting_position = p1_starting_position
        self.p2_starting_position = p2_starting_position

        self.action_space = Tuple([Discrete(5), Discrete(5)])
        single_agent_observation = Box(shape=(board_size, board_size),
                                       low=0, high=5, dtype=int) # TODO: find maximum number of values
        self.observation_space = Tuple([single_agent_observation,
                                        single_agent_observation])

        self.botA_type = botA_type
        self.botB_type = botB_type
        self.board_size = board_size
        self.reset()

    def reset(self):
        self.winner = -1 # Values: [-1, 0, 1]
        self.player1 = self.get_bot(self.botA_type)
        self.player2 = self.get_bot(self.botB_type)
        self.board = Board(self.board_size)
        self.current_state = Game(self.board, self.player1, self.player2,
                                  self.p1_starting_position, self.p2_starting_position)
        return np.array([[],[]]) # TODO: must return observation for each agent

    def get_bot(self, bot_type):
        if bot_type == BOT_TYPE_SPIKE:
            return SawBot()
        elif bot_type == BOT_TYPE_TORCH:
            return TorchBot()
        elif bot_type == BOT_TYPE_NAIL:
            return NailBot()
        else:
            raise ValueError("ERROR: Invalid Bot Type")

    def clone(self):
        """
        Creates a deep copy of the game state.
        NOTE: it is _really_ important that a copy is used during simulations
              Because otherwise MCTS would be operating on the real game board.
        :returns: deep copy of this GameState
        """

        return deepcopy(self)


    def step(self, actions: List):
        """
        returns: (obsvervations: List, rewards: List, done: bool)
        :param actions: List of two elements, containing one action for each player
        """

        self.current_state.handle_input(actions[0], actions[1])
        self.current_state.step()

        reward_vector = [self.current_state.get_score(self.player1),
                         self.current_state.get_score(self.player2)]

        # TODO: find if a player has won
        if self.current_state.is_gameover():
            self.winner = 0 if self.player1 == self.current_state.winner else 1

        # info should be kept empty
        info = {}
        return [[], []], reward_vector, \
               self.winner != -1, info

    def get_moves(self, player: int):
        """
        :param player: (int) player for whom we wish to generate moves
        :returns: array with all possible moves, index of columns which aren't full
        TODO: figure out what are the valid moves an agent can take.
        (i.e figure ability cooldowns / collision against map borders)
        """
        available_moves = (self.player1 if player == 0 else self.player2).get_valid_moves(self.current_state)

        if self.winner != -1:
            return []

        return available_moves

    def is_over(self):
        return self.winner == -1

    def get_result(self, player):
        """
        :param player: (int) player which we want to see if he / she is a winner
        :returns: winner from the perspective of the param player
        """
        return self.current_state.get_score(self.player1 if player == 0 else self.player2)

    def render(self, mode='human'):
        # TODO: Here's where we would show the screen based on the game state
        if mode == 'rgb':
            # This might be useful
            return pygame.surfarray.array3d(
                    pygame.display.get_surface()).astype(np.uint8)
        elif mode == 'string':
            return self.current_state.board.test_print()
