from gym.envs.registration import register

register(
    id='CoolGame-v0',
    entry_point='gym_cool_game.envs:CoolGameEnv',
)