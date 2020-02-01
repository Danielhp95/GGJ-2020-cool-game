from gym_cool_game.envs.cool_game_env import CoolGameEnv

from gym.envs.registration import register

register(id="RandomWalk-v0", entry_point='gym_cool_game.envs.RandomWalk:RandomWalkEnv',
         max_episode_steps=20, reward_threshold=1.0)

# gym.make("RandomWalk-v0", target=2) is then relevant make command
