import gym_cool_game
import regym
from regym.environments import generate_task, EnvType
from regym.rl_algorithms import build_Random_Agent, build_MCTS_Agent
import numpy as np
import random

class HumanAgent:

    def __init__(self, number_of_actions: int, name: str):
        self.name = name
        self.number_of_actions = number_of_actions

    def take_action(self, state):
        action = input(f'Take action [0, {self.number_of_actions}]: ')
        if action.isnumeric() and int(action) in range(0, 6):
            return int(action)
        else:
            print("Invalid entry. Defaulting to null action.")
            return 5

def main():
    task = generate_task('CoolGame-v0', EnvType.MULTIAGENT_SIMULTANEOUS_ACTION,
                         botA_type=0, botB_type=2)

    random_r1 = build_Random_Agent(task, {}, agent_name='random')
    random_r2 = random_r1.clone()

    mcts_r1 = build_MCTS_Agent(task, {'budget': 1296}, agent_name='P1: MCTS')
    mcts_r2 = build_MCTS_Agent(task, {'budget': 1296}, agent_name='P2: MCTS')

    human_r1 = HumanAgent(task.action_dim, name='P1')
    human_r2 = HumanAgent(task.action_dim, name='P2')

    import cProfile, pstats, io
    pr = cProfile.Profile()
    pr.enable()
    # Stuff

    t = task.run_episode([mcts_r1, mcts_r2], training=False, render_mode='rgb')
    
    pr.disable()
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

    print(t)


if __name__ == '__main__':
    main()
