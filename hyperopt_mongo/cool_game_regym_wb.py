import time
from copy import deepcopy

import numpy as np
import argparse


import gym
import gym_cool_game
import regym
from regym.environments import generate_task, EnvType
from regym.rl_algorithms import build_MCTS_Agent
from regym.rl_loops.trajectory import compute_winrates

import numpy as np

from loguru import logger

def MSE_edge_distance(target, graph):
    return ((target - graph)**2).mean()


def absolute_edge_distance(target, graph):
    return np.abs((target - graph)).mean()


def compute_matchup_winrates(agent, task: regym.environments.Task, matchup: str,
                             benchmarking_episodes: int, mcts_budget: int) -> float:

    logger.info(f'START: {matchup} for {benchmarking_episodes} episodes. Budget: {mcts_budget}')
    winrates = []
    trajectories = []
    for i in range(benchmarking_episodes):
        logger.info(f'Budget: {mcts_budget}. {matchup} episode: {i + 1}/{benchmarking_episodes}')
        start = time.time()
        trajectory = task.run_episode(agent_vector=[agent, agent], training=False)
        trajectories.append(trajectory)
        total = time.time() - start
        logger.info(f'{matchup}  took {total:.1f}s')
    mean_trajectory_length = np.mean([len(t) for t in trajectories])
    wandb.log({'Mean trajectory length': mean_trajectory_length})
    winrates = compute_winrates(trajectories)
    logger.info(f'END: {matchup} for {benchmarking_episodes} episodes. winrate: {winrates[0]}, mean trajectory len: {mean_trajectory_length}')
    return winrates[0]


def generate_evaluation_matrix(cool_game_params,
                               benchmarking_episodes, mcts_budget):
    # 0: SawBot 1: TorchBot 2: NailBot
    import gym_cool_game
    saw_vs_torch_task = generate_task('CoolGame-v0', EnvType.MULTIAGENT_SIMULTANEOUS_ACTION,
                                       botA_type=0, botB_type=1, **cool_game_params)
    saw_vs_nail_task = generate_task('CoolGame-v0', EnvType.MULTIAGENT_SIMULTANEOUS_ACTION,
                                       botA_type=0, botB_type=2, **cool_game_params)
    torch_vs_nail_task = generate_task('CoolGame-v0', EnvType.MULTIAGENT_SIMULTANEOUS_ACTION,
                                       botA_type=1, botB_type=2, **cool_game_params)

    mcts_config = {
        'budget': mcts_budget,
        'rollout_budget': 1000,
        'selection_phase': 'ucb1',
        'exploration_factor_ucb1': 4  # Might need to tweak this?
    }
    mcts_agent = build_MCTS_Agent(saw_vs_torch_task, mcts_config, agent_name='MCTS agent')

    saw_vs_torch = compute_matchup_winrates(mcts_agent, saw_vs_torch_task,
                                            'Saw vs Torch', benchmarking_episodes,
                                            mcts_budget)

    saw_vs_nail = compute_matchup_winrates(mcts_agent, saw_vs_nail_task,
                                           'Saw vs Nail', benchmarking_episodes,
                                           mcts_budget)

    torch_vs_nail = compute_matchup_winrates(mcts_agent, torch_vs_nail_task,
                                             'Torch vs Nail', benchmarking_episodes,
                                             mcts_budget)


    bench_msg = f'episodes={benchmarking_episodes} MCTS_budget={mcts_budget}'
    winrates_msg = f'winrates=saw:[{saw_vs_torch}, {saw_vs_nail}] nail:[{torch_vs_nail}]'
    logger.info(bench_msg)
    logger.info(winrates_msg)
    logger.info(f'params={cool_game_params}')
    wandb.log({'Winrate_Saw_vs_Torch': saw_vs_torch, 'Winrate_Saw_vs_Nail': saw_vs_nail, 'Winrate_Torch_vs_Nail': torch_vs_nail})
    return np.array([[0., saw_vs_torch, saw_vs_nail],
                     [1. - saw_vs_torch, 0., torch_vs_nail],
                     [1. - saw_vs_nail, 1. - torch_vs_nail, 0.]])


def evaluate_graph(game_params, target,
                   benchmarking_episodes, mcts_budget):
    start = time.time()
    logger.info('START: New iteration')
    # Generate evaluation matrix
    a = generate_evaluation_matrix(game_params,
                                   benchmarking_episodes, mcts_budget)
    logger.info(f'Response balance graph: {a}')
    # Compute response graph
    g = np.where(a < 0,  0, a) # Set to 0 all negative values
    # Compute graph distance
    distance = absolute_edge_distance(target, g)
    total = time.time() - start
    logger.info(f'END: iteration. Loss: {distance}. Total time: {total:.1f}s')
    return distance

if __name__ == '__main__':
    import wandb

    parser = argparse.ArgumentParser(description='Autobalancing for Workshop warfare')
    parser.add_argument('--benchmarking_episodes', required=True)
    parser.add_argument('--mcts_budget', required=True)
    parser.add_argument('--balancing_type', required=True)
    args = parser.parse_args()

    wandb.init()
    config = wandb.config
    if args.balancing_type == 'fair':
        target   = np.array([[0.0, 0.5, 0.5], [0.5, 0.0, 0.5], [0.5, 0.5, 0.0]])
    elif args.balancing_type == 'cyclic':
        target = np.array([[0.0, 0.7, 0.3], [0.3, 0.0, 0.7], [0.7, 0.3, 0.0]])
    else: raise ValueError(f"Unknown balancing type specified: {args.balancing_type}")

    logger.info(f'START parameter evaluation')
    start = time.time()
    evaluate_graph(config, target,
                   int(args.benchmarking_episodes),
                   int(args.mcts_budget))
    total = time.time() - start
    logger.info(f'END evaluation. Total time: {total:.1f}')
    wandb.log({'Param evaluation time': total})
