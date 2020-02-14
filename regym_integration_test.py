import gym_cool_game
import regym
from regym.environments import generate_task, EnvType
from regym.rl_algorithms import build_Random_Agent, build_MCTS_Agent, build_Human_Agent


def main():
    task = generate_task('CoolGame-v0', EnvType.MULTIAGENT_SIMULTANEOUS_ACTION,
                         botA_type=2, botB_type=1)
    random_r1 = build_Random_Agent(task, {}, agent_name='random')
    random_r2 = random_r1.clone()

    mcts_r1 = build_MCTS_Agent(task, {'budget': 5000}, agent_name='P1: MCTS')
    mcts_r2 = build_MCTS_Agent(task, {'budget': 5000}, agent_name='P2: MCTS')

    human_r1 = build_Human_Agent(task, {}, agent_name='P1')
    human_r2 = build_Human_Agent(task, {}, agent_name='P2')
    #t = task.run_episode([human_r1, human_r2], training=False, render_mode='rgb')
    t = task.run_episode([mcts_r1, mcts_r2], training=False, render_mode='rgb')
    print(t)


if __name__ == '__main__':
    main()
