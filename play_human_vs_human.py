import gym
import gym_cool_game


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


def play_as_human(p1, p2): 
    env = gym.make('CoolGame-v0',
                   botA_type=p1, botB_type=p2)

    render_mode = 'rgb'
    human_agent_1 = HumanAgent(number_of_actions=5, name='P1')
    human_agent_2 = HumanAgent(number_of_actions=5, name='P2')
    run_episode(env, render_mode, agent_vector=[human_agent_1, human_agent_2])


def run_episode(env, render_mode, agent_vector):
    '''
    :param render_mode: can either be 'string' or 'rgb'
    '''
    observations = env.reset()
    done = False
    while not done:
        if render_mode != '': rendered_state = env.render(render_mode)
        if render_mode == 'string': print(rendered_state)
        action_vector = [agent.take_action(observations[i]) for i, agent in enumerate(agent_vector)]
        succ_observations, reward_vector, done, info = env.step(action_vector)


if __name__ == '__main__':
    SAW, TORCH, NAIL = 0, 1, 2
    play_as_human(p1=TORCH, p2=TORCH)
