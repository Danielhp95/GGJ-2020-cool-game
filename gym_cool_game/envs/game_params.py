from dataclasses import dataclass


@dataclass
class TorchParams:
    dmg: int = 2
    weight: int = 2
    torch_range: int = 2
    duration: int = 2
    cooldown: int = 3
    ticks_between_moves: int = 2


@dataclass
class SawBotParams:
    dmg_min: int = 1
    dmg_max: int = 5
    weight: int = 3
    duration: int = 3
    cooldown: int = 5
    ticks_between_moves: int = 1


@dataclass
class NailBotParams:
    dmg: int = 1
    weight: int = 1
    bullet_speed: int = 3
    cooldown: int = 2
    ticks_between_moves: int = 3


@dataclass
class GameParams:
    torch_params: TorchParams
    saw_params: SawBotParams
    nail_params: NailBotParams


def construct_game_params(torch_dmg, torch_weight, torch_torch_range,
                          torch_duration, torch_cooldown,
                          torch_ticks_between_moves,
                          saw_dmg_min, saw_dmg_max, saw_weight,
                          saw_duration, saw_cooldown, saw_ticks_between_moves,
                          nail_dmg, nail_weight, nail_bullet_speed,
                          nail_cooldown, nail_ticks_between_moves):


    torch_params = TorchParams(dmg=torch_dmg, weight=torch_weight,
                               torch_range=torch_torch_range, duration=torch_duration,
                               cooldown=torch_cooldown,
                               ticks_between_moves=torch_ticks_between_moves)
    saw_params = SawBotParams(dmg_min=saw_dmg_min, dmg_max=saw_dmg_max,
                              weight=saw_weight, duration=saw_duration, cooldown=saw_cooldown,
                              ticks_between_moves=saw_ticks_between_moves)
    nail_params = NailBotParams(dmg=nail_dmg, weight=nail_weight,
                                bullet_speed=nail_bullet_speed, cooldown=nail_cooldown,
                                ticks_between_moves=nail_ticks_between_moves)
    return GameParams(torch_params, saw_params, nail_params)
