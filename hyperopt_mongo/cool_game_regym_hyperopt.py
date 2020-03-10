import time
from copy import deepcopy

import numpy as np
from hyperopt import Trials, fmin, hp, tpe
from hyperopt.mongoexp import MongoTrials

from docopt import docopt


import gym
import gym_cool_game
import regym
from regym.environments import generate_task, EnvType
from regym.evaluation import benchmark_agents_on_tasks
from regym.rl_algorithms import build_MCTS_Agent

import logging

def MSE_edge_distance(target, graph):
    return ((target - graph)**2).mean()


def absolute_edge_distance(target, graph):
    return np.abs((target - graph)).mean()


def compute_matchup_winrates(agent, task, matchup: str,
                             benchmarking_episodes: int, mcts_budget: int,
                             logger: logging.Logger) -> float:
    logger.info(f'START: {matchup} for {benchmarking_episodes} episodes. Budget: {mcts_budget}')
    winrates = []
    for i in range(benchmarking_episodes):
        logger.info(f'Budget: {mcts_budget}. {matchup} episode: {i + 1}/{benchmarking_episodes}')
        start = time.time()
        winrates += benchmark_agents_on_tasks(tasks=[task],
                                              agents=[agent],
                                              populate_all_agents=True,
                                              num_episodes=1)
        total = time.time() - start
        logger.info(f'{matchup} with Budget: {mcts_budget} took {total:.1f}s. Winner: {winrates[-1]}')
    winrate = sum(winrates) / len(winrates)
    logger.info(f'END: {matchup} for {benchmarking_episodes} episodes. winrate: {winrate}')
    return winrate


def generate_evaluation_matrix(cool_game_params,
                               benchmarking_episodes, mcts_budget, logger: logging.Logger):
    # 0: SawBot 1: TorchBot 2: NailBot
    import gym_cool_game
    saw_vs_torch_task = generate_task('CoolGame-v0', EnvType.MULTIAGENT_SIMULTANEOUS_ACTION,
                                       botA_type=0, botB_type=1, **cool_game_params)
    saw_vs_nail_task = generate_task('CoolGame-v0', EnvType.MULTIAGENT_SIMULTANEOUS_ACTION,
                                       botA_type=0, botB_type=2, **cool_game_params)
    torch_vs_nail_task = generate_task('CoolGame-v0', EnvType.MULTIAGENT_SIMULTANEOUS_ACTION,
                                       botA_type=1, botB_type=2, **cool_game_params)

    mcts_config = {'budget': mcts_budget}
    mcts_agent = build_MCTS_Agent(saw_vs_torch_task, mcts_config, agent_name='MCTS agent')

    saw_vs_torch = compute_matchup_winrates(mcts_agent, saw_vs_torch_task,
                                            'Saw vs Torch', benchmarking_episodes,
                                            mcts_budget, logger)

    saw_vs_nail = compute_matchup_winrates(mcts_agent, saw_vs_nail_task,
                                           'Saw vs Nail', benchmarking_episodes,
                                           mcts_budget, logger)

    torch_vs_nail = compute_matchup_winrates(mcts_agent, saw_vs_nail_task,
                                             'Torch vs Nail', benchmarking_episodes,
                                             mcts_budget, logger)


    bench_msg = f'episodes={benchmarking_episodes} MCTS_budget={mcts_budget}'
    winrates_msg = f'winrates=saw:[{saw_vs_torch}, {saw_vs_nail}] nail:[{torch_vs_nail}]'
    logger.info(bench_msg)
    logger.info(winrates_msg)
    logger.info(f'params={cool_game_params}')
    return np.array([[0., saw_vs_torch, saw_vs_nail],
                     [1. - saw_vs_torch, 0., torch_vs_nail],
                     [1. - saw_vs_nail, 1. - torch_vs_nail, 0.]])


def evaluate_graph(game_params, target,
                   benchmarking_episodes, mcts_budget, logger):
    start = time.time()
    logger.info('START: New iteration')
    # Generate evaluation matrix
    a = generate_evaluation_matrix(game_params,
                                   benchmarking_episodes, mcts_budget, logger)
    logger.info(f'Response balance graph: {a}')
    # Compute response graph
    g = np.where(a < 0,  0, a) # Set to 0 all negative values
    # Compute graph distance
    distance = absolute_edge_distance(target, g)
    total = time.time() - start
    logger.info(f'END: iteration. Loss: {distance}. Total time: {total:.1f}s')
    return distance


def optimization_space():
    return {'torch_health': hp.uniformint('torch_health', 1, 10),
            'torch_dmg': hp.uniformint('torch_dmg', 1, 10),
            # 'torch_weight': hp.uniformint('torch_weight', 1, 10),
            'torch_torch_range': hp.uniformint('torch_torch_range', 1, 10),
            'torch_duration': hp.uniformint('torch_duration', 1, 10),
            'torch_cooldown': hp.uniformint('torch_cooldown', 1, 10),
            'torch_ticks_between_moves': hp.uniformint('torch_ticks_between_moves', 1, 10),
            # SawBot parameters 
            'saw_health': hp.uniformint('saw_health', 1, 10),
            'saw_dmg_min': hp.uniformint('saw_dmg_min', 1, 10),
            'saw_dmg_max': hp.uniformint('saw_dmg_max', 1, 10),
            # 'saw_weight': hp.uniformint('saw_weight', 1, 10),
            'saw_duration': hp.uniformint('saw_duration', 1, 10),
            'saw_cooldown': hp.uniformint('saw_cooldown', 1, 10),
            'saw_ticks_between_moves': hp.uniformint('saw_ticks_between_moves', 1, 10),
            # NailBot parameters
            'nail_health': hp.uniformint('nail_health', 1, 10),
            'nail_dmg': hp.uniformint('nail_dmg', 1, 10),
            # 'nail_weight': hp.uniformint('nail_weight', 1, 10),
            'nail_cooldown': hp.uniformint('nail_cooldown', 1, 10),
            'nail_ticks_between_moves': hp.uniformint('nail_ticks_between_moves', 1, 10)
           }


if __name__ == '__main__':
    usage = '''
    Usage:
        cool_game_regym_hyperopt.py BENCHMARK_EPISODES MCTS_BUDGET MAX_EVALS [--use_mongo]

    Arguments:
        BENCHMARK_EPISODES Number of episodes that will be run per matchup
                           to compute winrates between bots
        MCTS_BUDGET        Number of MCTS iterations for each agent
        MAX_EVALS          Target number of parameters updates

    Options:
        --use_mongo        Whether to use MongoTrials or normal trials in Hyperopt
    '''
    arguments = docopt(usage)
    # Defining parameter space
    space = optimization_space()

    # Graph target
    target = np.array([[0.0, 0.5, 0.5], [0.5, 0.0, 0.5], [0.5, 0.5, 0.0]])

    benchmarking_episodes = int(arguments['BENCHMARK_EPISODES'])
    mcts_budget = int(arguments['MCTS_BUDGET'])
    balancing_run_name = f'budget_{mcts_budget}_benchmarkingepisodes_{benchmarking_episodes}'

    # logging
    logging.basicConfig()
    logger = logging.getLogger(balancing_run_name)
    logger.setLevel(logging.INFO)

    use_mongo = arguments['--use_mongo']
    logger.info(f'Creating trials object use mongo: {use_mongo}')

    if use_mongo: trials = MongoTrials('mongo://localhost:1234/foo_db/jobs', exp_key=balancing_run_name)
    else: trials = Trials()

    logger.info(f'START game parameter search')
    start = time.time()
    best = fmin(
            lambda params: evaluate_graph(params, target,
                                          benchmarking_episodes,
                                          mcts_budget,
                                          logger),
            space=space,
            algo=tpe.suggest,
            max_evals=int(arguments['MAX_EVALS']),
            trials=trials)
    total = time.time() - start
    logger.info(f'END game parameter search. Total time: {total:.1f}')
    logger.info(f'Best params: {best}')
