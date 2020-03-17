import gym_cool_game
import regym
from regym.environments import generate_task, EnvType
from regym.rl_algorithms import build_Random_Agent, build_MCTS_Agent

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
                         botA_type=2, botB_type=1)
    random_r1 = build_Random_Agent(task, {}, agent_name='random')
    random_r2 = random_r1.clone()

    mcts_r1 = build_MCTS_Agent(task, {'budget': 2000}, agent_name='P1: MCTS')
    mcts_r2 = build_MCTS_Agent(task, {'budget': 200}, agent_name='P2: MCTS')

    human_r1 = HumanAgent(5, 'P1')
    human_r2 = HumanAgent(5, 'P2')
    #t = task.run_episode([human_r1, human_r2], training=False, render_mode='rgb')
    t = task.run_episode([mcts_r1, mcts_r2], training=False, render_mode='rgb')
    print(t)


if __name__ == '__main__':
    main()
