import gym
from gym_cool_game.envs.RandomWalk import RandomWalkEnv
from gym_cool_game.MCTS.simul_mcts import MCTS_UCT

if __name__ == '__main__':
    game = RandomWalkEnv(target=3)

    print("Game state: %s, winner = %d" % (game, game.winner))
    while game.winner == -1:
        print("Deciding next move")
        moves = MCTS_UCT(game, 100)
        print("Moves %s" % moves)
        game.step(moves)
        print("New game state %s" % game.__repr__())
