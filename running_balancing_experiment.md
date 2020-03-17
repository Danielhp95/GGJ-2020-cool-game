# How to run balancing experiment

## Installation

You will need three things installed

### Python packages:

+ [docopt](https://github.com/docopt/docopt): `pip install docopt`
+ [Hyperopt](https://github.com/hyperopt/hyperopt): `pip install hyperopt`
+ [pymongo](https://pypi.org/project/pymongo/): `pip install pymongo`
+ [Regym](https://github.com/Danielhp95) in the branch `develop-improving-play-match-utils`: 
    1. Clone repo: `git clone https://github.com/Danielhp95`
    2. Checkout branch: `git checkout develop-improving-play-match-utils`
    3. Install locally: `pip install -e Regym/.`

### Non python packages:

[MongoDB](https://docs.mongodb.com/manual/installation/) is required. Click link for installation guide

## Usage: `parallel_autobalancing.py`

**WARNING**: This script generates a lot of files in the directory you run it!

Inside of this repo (`Danielhp95/GGJ-2020-cool-game`), run the script `hyperopt_mongo/parallel_autobalancing.py`. This script takes 3 parameters:

- **Benchmarking episodes**: Number of episodes used to compute winrates between each bot matchup (higher values yield higher winrate accuracy, it increases computational time). **RECOMENDED**: `20`
- **MCTS Budget**: Computational budget given to MCTS (higher values indicate higher skill, it increases computational time). **RECOMENDED**: `1296`
- **Max evals**: Number of trials to be run before terminating balancing run. **NOTE**: Because we are using MongoDB, the results of trials are permanent, so you can stop the balancing script and restart it at any time. **RECOMENDED**: `100`

The script spawns as many processes as there are CPUs, meaning that it will consume a lot of your computational power! You should still be able to (more slowly) navigate around your computer.

The script that actually does the balancing work is `cool_game_regym_hyperopt.py`. This shares the same parameters as above, with the exception of a flag `--use_mongo` which dictates whether you want to run a single thread or use `mongo` for parallelism.


#### Sample usage:

`python parallel_autobalancing.py 20 1296 100`

This will run many parallel workers, each carrying out a balancing test on a single set of game parameters.
