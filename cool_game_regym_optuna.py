from copy import deepcopy
import numpy as np
import optuna
from optuna.visualization import plot_optimization_history, plot_slice, plot_intermediate_values, plot_contour
from plotly.offline import plot

import regym

# TODO: cool game
import gym_cool_game
from regym.environments import generate_task, EnvType
from regym.evaluation import benchmark_agents_on_tasks
from regym.rl_algorithms import build_MCTS_Agent

import logging

def MSE_edge_distance(target, graph):
    return ((target - graph)**2).mean()


def absolute_edge_distance(target, graph):
    return np.abs((target - graph)).mean()


def generate_evaluation_matrix(cool_game_params, logger):
    player1_type = 1  # TorchBot
    player2_type = 2  # NailBot
    benchmarking_episodes = 20

    saw_vs_torch_task = generate_task('CoolGame-v0', EnvType.MULTIAGENT_SIMULTANEOUS_ACTION,
                                      botA_type=player1_type,
                                      botB_type=player2_type,
                                      **cool_game_params)

    mcts_config = {'budget': 1}
    mcts_agent = build_MCTS_Agent(saw_vs_torch_task, mcts_config, agent_name='MCTS agent')

    saw_vs_torch_winrates = benchmark_agents_on_tasks(tasks=[saw_vs_torch_task],
                                                      agents=[mcts_agent],
                                                      populate_all_agents=True,
                                                      num_episodes=benchmarking_episodes)
    logger.info(f'winrates={saw_vs_torch_winrates[0]}')
    logger.info(f'winrates={saw_vs_torch_winrates[0]}params=\n{cool_game_params}')
    return np.array([[0., saw_vs_torch_winrates[0]],
                     [-saw_vs_torch_winrates[0], 0.]])


def evaluate_graph(target, game_params, logger):
    # Train agents (not-necessary for rps)
    # Generate evaluation matrix
    a = generate_evaluation_matrix(game_params, logger)
    # Compute response graph
    g = np.where(a < 0,  0, a) # Set to 0 all negative values
    # Compute graph distance
    distance = absolute_edge_distance(target, g)
    return distance

def objective(trial, target, logger):
    params = {'torch_dmg': trial.suggest_int('torch_dmg', 1, 5),
              'torch_weight': trial.suggest_int('torch_weight', 1, 5),
              'torch_torch_range': trial.suggest_int('torch_torch_range', 1, 5),
              'torch_duration': trial.suggest_int('torch_duration', 1, 5),
              'torch_cooldown': trial.suggest_int('torch_cooldown', 1, 5),
              'torch_ticks_between_moves': trial.suggest_int('torch_ticks_between_moves', 1, 5),
              # SawBot parameters 
              'saw_dmg_min': trial.suggest_int('saw_dmg_min', 1, 5),
              'saw_dmg_max': trial.suggest_int('saw_dmg_max', 1, 5),
              'saw_weight': trial.suggest_int('saw_weight', 1, 5),
              'saw_duration': trial.suggest_int('saw_duration', 1, 5),
              'saw_cooldown': trial.suggest_int('saw_cooldown', 1, 5),
              'saw_ticks_between_moves': trial.suggest_int('saw_ticks_between_moves', 1, 5),
              # NaileBot parameters
              # 'nail_dmg': trial.suggest_int('nail_dmg', 1, 5),
              # 'nail_weight': trial.suggest_int('nail_weight', 1, 5),
              # 'nail_cooldown': trial.suggest_int('nail_cooldown', 1, 5),
              # 'nail_ticks_between_moves': trial.suggest_int('nail_ticks_between_moves', 1, 5)
              }
    return evaluate_graph(target, params, logger)


def generate_targets():
    return {'rps_target': rps_target, 'biased_rps_target': biased_rps_target,
            'extended_rps_target': extended_rps_target}

def log_trial(logger, trial):
    pass


if __name__ == '__main__':
    logging.basicConfig()
    logger = logging.getLogger('CoolGame_autobalancing')
    logger.setLevel(logging.INFO)

    # Graph targets
    rps_target = np.array([[0, 0.5],
                           [0.5, 0]])
    study = optuna.create_study()

    logger.info('START game parameter search')
    study.optimize(lambda trial: objective(trial, rps_target, logger),
                   n_trials=2000, n_jobs=1)
    print(study.best_params)
