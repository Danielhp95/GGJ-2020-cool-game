## Game description

TODO: copy from paper or paste from here to paper


### Action space

TODO

### Observation space

TODO

### Game parameterization
TODO


## Usage

This environment follows the [OpenAI Gym interface](https://gym.openai.com/). 

To play Human vs Human, run script `play_human_vs_human.py`. On each step you will be asked to input an action via the terminal (0-5), corresponding to all possible five actions. You can find the value of each action in `gym_cool_game/envs/valid_inputs.py`.

## Installation

**Please use a virtual environment** to install this game. Otherwise the dependencies will be installed system-wide. We recommend [poetry](https://github.com/python-poetry/poetry)

### Dependencies:

All dependencies are listed inside the top level file `requirements.txt`. These are:

```bash
pygame
gym
numpy
```

They can be installed by running `pip install -r requirements`.

**Important!**: `pygame` has some non-python dependencies. Please make sure to have all these dependencies ready before installing `pygame`.

#### Installing `pygame`:

On Windows / Mac and Ubuntu: [https://www.pygame.org/wiki/Compilation](https://www.pygame.org/wiki/Compilation)

On Arch based systems: Install `python-pygame-git` from [AUR](https://aur.archlinux.org/packages/python-pygame-git/).
