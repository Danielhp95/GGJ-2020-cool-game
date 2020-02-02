from typing import List
from copy import deepcopy
import numpy as np
import gym
import pygame


class RandomWalkEnv(gym.Env):
    def __init__(self, target=3, current_positions=None):
        if current_positions is None:
            current_positions = [0, 0]
        self.target = target
        self.winner = -1
        self.current_positions = current_positions
        self.done = False

    def __repr__(self):
        return "%s, t:%d" % (self.current_positions, self.target)

    def reset(self):
        self.done = False
        self.winner = -1
        self.current_positions = [0, 0]
        return np.array([[], []])  # TODO: must return observation for each agent

    def clone(self):
        """
        Creates a deep copy of the game state.
        NOTE: it is _really_ important that a copy is used during simulations
              Because otherwise MCTS would be operating on the real game board.
        :returns: deep copy of this GameState
        """
        return RandomWalkEnv(target=self.target, current_positions=self.current_positions.copy())

    def step(self, actions: List):
        """
        :param actions: List of two elements, containing one action for each player
        """
        if self.done:
            return [self.current_positions[0]], [self.current_positions[1]], [0, 0], self.done, {}
        for i in range(2):
            if actions[i] == 0:
                self.current_positions[i] += 1
            elif actions[i] == 1:
                self.current_positions[i] -= 1
            else:
                pass

        reward_vector = [1 if self.target == p else 0 for p in self.current_positions]

        # TODO: find if a player has won
        if reward_vector[1] == 1:
            self.winner = 1
        elif reward_vector[0] == 1:
            self.winner = 0
        else:
            self.winner = -1

        # info should be kept empty
        info = {}
        self.done = self.winner != -1
        return [[self.current_positions[0]], [self.current_positions[1]]], reward_vector, self.done, info

    def get_moves(self, perspective_player: int):
        """
        :returns: array with all possible moves, index of columns which aren't full
        TODO: figure out what are the valid moves an agent can take.
        (i.e figure ability cooldowns / collision against map borders)
        """
        if self.winner != -1:
            return []
        return [0, 1]

    def is_over(self):
        return self.winner != -1

    def get_result(self, player):
        """
        :param player: (int) player which we want to see if he / she is a winner
        :returns: winner from the perspective of the param player
        """
        return int(self.current_positions[player] == self.target)

    def render(self, mode='human'):
        # TODO: Here's where we would show the screen based on the game state
        if mode == 'rgb':
            # This might be useful
            return pygame.surfarray.array3d(
                pygame.display.get_surface()).astype(np.uint8)
