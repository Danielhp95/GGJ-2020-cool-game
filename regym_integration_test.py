import gym_cool_game
import regym
from regym.environments import generate_task, EnvType
from regym.rl_algorithms import build_Random_Agent, build_MCTS_Agent, build_Human_Agent


def main():
    task = generate_task('CoolGame-v0', EnvType.MULTIAGENT_SIMULTANEOUS_ACTION,
                         botA_type=0, botB_type=1)
    random_r1 = build_Random_Agent(task, {}, agent_name='random')
    random_r2 = random_r1.clone()

    mcts_r1 = build_MCTS_Agent(task, {'budget': 300}, agent_name='MCTS')
    mcts_r2 = mcts_r1.clone()

    human_r1 = build_Human_Agent(task, {}, agent_name='Oz')
    human_r2 = build_Human_Agent(task, {}, agent_name='Daniiii')
    t = task.run_episode([mcts_r1, mcts_r2], training=False, render_mode='rgb')
    print(t)


if __name__ == '__main__':
    main()
