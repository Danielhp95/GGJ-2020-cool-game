from typing import List
from copy import deepcopy
import numpy as np
import gym
import pygame


class CoolGameEnv(gym.Env):

    def __init__(self):
        # TODO: figure out params
        self.reset()

    def reset(self):
        return np.array([[],[]]) # TODO: must return observation for each agent

    def clone(self):
        """ 
        Creates a deep copy of the game state.
        NOTE: it is _really_ important that a copy is used during simulations
              Because otherwise MCTS would be operating on the real game board.
        :returns: deep copy of this GameState
        """
        return None # TODO

    def step(self, actions: List):
        """ 
        :param actions: List of two elements, containing one action for each player
        """
        # TODO: find correct reward vector
        reward_vector = [0, 0]

        # TODO: find if a player has won
        self.winner = 0 

        # info should be kept empty
        info = {}
        return [[], []], reward_vector, \
               self.winner != 0, info
            
    def get_moves(self):
        """
        :returns: array with all possible moves, index of columns which aren't full
        TODO: figure out what are the valid moves an agent can take.
        (i.e figure ability cooldowns / collision against map borders)
        """
        if self.winner != 0:
            return []
        return [] # TODO

    def get_result(self, player):
        """ 
        :param player: (int) player which we want to see if he / she is a winner
        :returns: winner from the perspective of the param player
        """
        return player == self.winner

    def render(self, mode='human'):
        # TODO: Here's where we would show the screen based on the game state
        if mode == 'rgb':
            # This might be useful
            return pygame.surfarray.array3d(
                    pygame.display.get_surface()).astype(np.uint8)
