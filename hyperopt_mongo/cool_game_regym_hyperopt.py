import time
from copy import deepcopy

import numpy as np
from hyperopt import Trials, fmin, hp, tpe
from hyperopt.mongoexp import MongoTrials


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


def generate_evaluation_matrix(cool_game_params, logger):
    # 0: SawBot 1: TorchBot 2: NailBot
    benchmarking_episodes = 1
    mcts_budget = 1

    import gym_cool_game
    saw_vs_torch_task = generate_task('CoolGame-v0', EnvType.MULTIAGENT_SIMULTANEOUS_ACTION,
                                       botA_type=0, botB_type=1, **cool_game_params)
    saw_vs_nail_task = generate_task('CoolGame-v0', EnvType.MULTIAGENT_SIMULTANEOUS_ACTION,
                                       botA_type=0, botB_type=2, **cool_game_params)
    torch_vs_nail_task = generate_task('CoolGame-v0', EnvType.MULTIAGENT_SIMULTANEOUS_ACTION,
                                       botA_type=1, botB_type=2, **cool_game_params)

    mcts_config = {'budget': mcts_budget}
    mcts_agent = build_MCTS_Agent(saw_vs_torch_task, mcts_config, agent_name='MCTS agent')

    saw_winrates = benchmark_agents_on_tasks(tasks=[saw_vs_torch_task, saw_vs_nail_task],
                                             agents=[mcts_agent],
                                             populate_all_agents=True,
                                             num_episodes=benchmarking_episodes)
    nail_winrate = benchmark_agents_on_tasks(tasks=[torch_vs_nail_task],
                                             agents=[mcts_agent],
                                             populate_all_agents=True,
                                             num_episodes=benchmarking_episodes)

    bench_msg = f'episodes={benchmarking_episodes} MCTS_budget={mcts_budget}'
    winrates_msg = f'winrates=saw:{saw_winrates} nail:{nail_winrate}'
    logger.info(bench_msg)
    logger.info(winrates_msg)
    logger.info(f'params={cool_game_params}')
    return np.array([[0., saw_winrates[0], saw_winrates[1]],
                     [-saw_winrates[0], 0., nail_winrate[0]],
                     [-saw_winrates[0], -nail_winrate[0], 0.]])


def evaluate_graph(game_params, target, logger):
    start = time.time()
    logger.info('New iteration')
    # Train agents (not-necessary for rps)
    # Generate evaluation matrix
    a = generate_evaluation_matrix(game_params, logger)
    # Compute response graph
    g = np.where(a < 0,  0, a) # Set to 0 all negative values
    # Compute graph distance
    total = time.time() - start
    logger.info(f'Total: {total}s')
    distance = absolute_edge_distance(target, g)
    return distance


if __name__ == '__main__':
    # Defining parameter space
    space = {'torch_health': hp.uniformint('torch_health', 1, 10),
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
             'nail_health': hp.uniformint('nail_dmg', 1, 10),
             'nail_dmg': hp.uniformint('nail_dmg', 1, 10),
             # 'nail_weight': hp.uniformint('nail_weight', 1, 10),
             'nail_cooldown': hp.uniformint('nail_cooldown', 1, 10),
             'nail_ticks_between_moves': hp.uniformint('nail_ticks_between_moves', 1, 10)
             }

    # Graph target
    target = np.array([[0.0, 0.5, 0.5], [0.5, 0.0, 0.5], [0.5, 0.5, 0.0]])

    # logging
    logging.basicConfig()
    logger = logging.getLogger('CoolGame_autobalancing')
    logger.setLevel(logging.INFO)

    use_mongo = True
    logger.info(f'Creating trials object use mongo: {use_mongo}')
    if use_mongo: trials = MongoTrials('mongo://localhost:1234/foo_db/jobs', exp_key='exp4')
    else: trials = Trials()

    logger.info(f'START game parameter search')
    start = time.time()
    best = fmin(
            lambda params: evaluate_graph(params, target, logger),
            space=space,
            algo=tpe.suggest,
            max_evals=50,
            trials=trials)
    import ipdb; ipdb.set_trace()
    total = time.time() - start
    logger.info(f'END game parameter search. Total time: {total}')
    logger.info(f'Best params: {best}')

    print(best)
