from math import sqrt, log
import random
from .multiplayer_olnode import MultiplayerOpenLoopNode


def UCB1(node, child, exploration_constant=sqrt(2)):
    return child.wins / child.visits + exploration_constant * sqrt(log(node.visits) / child.visits)


def selection_phase(nodes, state, selection_policy=UCB1, selection_policy_args=None):
    if selection_policy_args is None:
        selection_policy_args = []
    expanded = [False for _ in nodes]
    while not (all(expanded) or state.is_over()):
        moves, expanded = choose_moves(nodes, selection_policy, selection_policy_args)
        state.step(moves)
        nodes = [n.doStuff(moves, state) for n in nodes]
    return nodes


def choose_moves(nodes, selection_policy, selection_policy_args):
    expanded = []
    moves = []
    for n in nodes:
        if n.is_fully_expanded():
            expanded.append(False)
       #     grand_children_nodes = [gc for ch in n.child_nodes for gc in ch.child_nodes]
            selected_node = sorted(n.child_nodes,
                                   key=lambda child: selection_policy(n, child, *selection_policy_args))[-1]
            moves.append(selected_node.move)
        else:
            expanded.append(True)
            moves.append(random.choice(n.untried_moves))
    return moves, expanded


def rollout_phase(state):
    # TODO: Currently we just stop once we reach the end of the tree
    # TODO: Currently get_result() returns True/False...this needs to be a numeric score for Back Prop
    return state


def backpropagation_phase(nodes, state):
    for n in nodes:
        if n is not None:
            #TODO: get_result() returns True/False...we need a numeric score (evaluation) for
            # each player in the state
            while n is not None:
                n.update(state.get_result(n.perspective_player))
                n = n.parent_node


def action_selection_phase(nodes):
    return [sorted(n.child_nodes, key=lambda c: c.wins / c.visits)[-1].move
            for n in nodes]


def MCTS_UCT(rootstate, itermax, exploration_factor_ucb1=sqrt(2), player_count = 2):
    """ 
    Conducts a game tree search using the MCTS-UCT algorithm
    for a total of param itermax iterations. The search begins
    in the param rootstate. Defaults to 2 players with results in [0.0, 1.0].

    :param rootstate: The game state for which an action must be selected.
    :param itermax: number of MCTS iterations to be carried out. Also knwon as the computational budget.
    :returns: List[int] Action that will be taken by EACH player.
    """
    root_nodes = [MultiplayerOpenLoopNode(state=rootstate, perspective_player=i)
                  for i in range(player_count)]
    for _ in range(itermax):
        nodes = root_nodes
        state = rootstate.clone()
        nodes = selection_phase(nodes, state, selection_policy=UCB1, selection_policy_args=[exploration_factor_ucb1])
        rollout_phase(state)
        backpropagation_phase(nodes, state)

    for i, n in enumerate(root_nodes):
        print(f'Player {i}')
        print(n)
    return action_selection_phase(root_nodes)
