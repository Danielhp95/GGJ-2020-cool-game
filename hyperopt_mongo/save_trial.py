from typing import Dict
import os
import json

import hyperopt
import pandas as pd


def save_trial(trials: hyperopt.Trials, name: str):
    '''
    I already have code that plots this expecting dataframes
    as configured by Optuna (python package). So here i'm
    just creating a dataframe with the same format from our
    Hyperopt trials. A hack.
    '''
    param_value_evolution = create_formated_dicts(trials)

    file_name = name + '.json'

    if os.path.isfile(file_name):
        override = bool(input(f'Override file {file_name}? (y/n)'))
        if not override:
            print(f'Aborting overriding {file_name}')
            return

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(param_value_evolution, f,
                  ensure_ascii=False, indent=4)


def create_formated_dicts(trials):
    param_names = trials.trials[0]['misc']['vals'].keys()
    param_value_evolution = {'params_' + str(name): [] for name in param_names}
    param_value_evolution['value'] = []
    for t in trials.trials:
        # Add values for this iteration
        if t['result']['status'] != 'ok':
            print(f"Skipping trial with status: {t['result']['status']}")
            continue
        for p_name, p_value in t['misc']['vals'].items():
            param_value_evolution['params_'+p_name].append(p_value[0]) # p_value is a singleton list
        # Add loss
        param_value_evolution['value'].append(t['result']['loss'])
    return param_value_evolution
