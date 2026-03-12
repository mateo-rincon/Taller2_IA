from __future__ import annotations

import random
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from algorithms.utils import bfs_distance, dijkstra

import algorithms.evaluation as evaluation
from world.game import Agent, Directions

if TYPE_CHECKING:
    from world.game_state import GameState


class MultiAgentSearchAgent(Agent, ABC):
    """
    Base class for multi-agent search agents (Minimax, AlphaBeta, Expectimax).
    """

    def __init__(self, depth: str = "2", _index: int = 0, prob: str = "0.0") -> None:
        self.index = 0  # Drone is always agent 0
        self.depth = int(depth)
        self.prob = float(
            prob
        )  # Probability that each hunter acts randomly (0=greedy, 1=random)
        self.evaluation_function = evaluation.evaluation_function

    @abstractmethod
    def get_action(self, state: GameState) -> Directions | None:
        """
        Returns the best action for the drone from the current GameState.
        """
        pass


class RandomAgent(MultiAgentSearchAgent):
    """
    Agent that chooses a legal action uniformly at random.
    """

    def get_action(self, state: GameState) -> Directions | None:
        """
        Get a random legal action for the drone.
        """
        legal_actions = state.get_legal_actions(self.index)
        return random.choice(legal_actions) if legal_actions else None


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Minimax agent for the drone (MAX) vs hunters (MIN) game.
    """

    def get_action(self, state: GameState) -> Directions | None:
        """
        Returns the best action for the drone using minimax.

        Tips:
        - The game tree alternates: drone (MAX) -> hunter1 (MIN) -> hunter2 (MIN) -> ... -> drone (MAX) -> ...
        - Use self.depth to control the search depth. depth=1 means the drone moves once and each hunter moves once.
        - Use state.get_legal_actions(agent_index) to get legal actions for a specific agent.
        - Use state.generate_successor(agent_index, action) to get the successor state after an action.
        - Use state.is_win() and state.is_lose() to check terminal states.
        - Use state.get_num_agents() to get the total number of agents.
        - Use self.evaluation_function(state) to evaluate leaf/terminal states.
        - The next agent is (agent_index + 1) % num_agents. Depth decreases after all agents have moved (full ply).
        - Return the ACTION (not the value) that maximizes the minimax value for the drone.
        """
        # TODO: Implement your code here
        '''num_agents = state.get_num_agents()
    
        if state.is_win() or state.is_lose() or self.depth == 0:
            return self.evaluation_function(state)
        
        def minimax(state, depth, agent_index):
            if state.is_win() or state.is_lose() or self.depth == 0:
                return self.evaluation_function(state)
            if agent_index == 0:
                return maximize(state, depth) 
            else: 
                return minimize(state, depth, agent_index)        
        
        
        def maximize(state, depth):
            max=float("-inf")
            for action in state.get_legal_actions(0):
                succ = state.generate_successor(0, action)
                max = max(max, minimax(succ, depth, 1))
            return max
        
        def minimize(state, depth, agent_index):
            min = float("inf")
            for action in state.get_legal_actions(agent_index):
                succ = state.generate_successor(agent_index, action)
                if agent_index == num_agents - 1:
                    min = min(min, minimax(succ, depth-1, 0))
                else:
                    min = min(min, minimax(succ, depth, agent_index+1))
            return min'''
        
        '''Prompt: Implement the minimax algorithm for the drone (MAX) vs hunters (MIN) game. The game tree alternates between the drone and multiple hunters. Use self.depth to control the search depth, and self.evaluation_function to evaluate leaf/terminal states. Return the ACTION that maximizes the minimax value for the drone.
        (Adjunto estaba el codigo del intento hecho a mano)'''
        num_agents = state.get_num_agents()

        def minimax(state, depth, agent_index):
            if state.is_win() or state.is_lose() or depth == 0:
                return self.evaluation_function(state)

            actions = state.get_legal_actions(agent_index)
            if not actions:
                return self.evaluation_function(state)

            next_agent = (agent_index + 1) % num_agents
            next_depth = depth - 1 if next_agent == 0 else depth

            if agent_index == 0:  # Drone (MAX)
                value = float("-inf")
                for action in actions:
                    succ = state.generate_successor(agent_index, action)
                    value = max(value, minimax(succ, next_depth, next_agent))
                return value

            else:  # Hunters (MIN)
                value = float("inf")
                for action in actions:
                    succ = state.generate_successor(agent_index, action)
                    value = min(value, minimax(succ, next_depth, next_agent))
                return value

        # Root
        actions = state.get_legal_actions(0)
        if not actions:
            return None

        # Never choose STOP unless only option
        non_stop = [a for a in actions if a != Directions.STOP]
        if non_stop:
            actions = non_stop

        best_action = None
        best_value = float("-inf")
        for action in actions:
            succ = state.generate_successor(0, action)
            value = minimax(succ, self.depth, 1)
            if value > best_value:
                best_value = value
                best_action = action

        return best_action
                


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Alpha-Beta pruning agent. Same as Minimax but with alpha-beta pruning.
    MAX node: prune when value > beta (strict).
    MIN node: prune when value < alpha (strict).
    """

    def get_action(self, state: GameState) -> Directions | None:
        """
        Returns the best action for the drone using alpha-beta pruning.

        Tips:
        - Same structure as MinimaxAgent, but with alpha-beta pruning.
        - Alpha: best value MAX can guarantee (initially -inf).
        - Beta: best value MIN can guarantee (initially +inf).
        - MAX node: prune when value > beta (strict inequality, do NOT prune on equality).
        - MIN node: prune when value < alpha (strict inequality, do NOT prune on equality).
        - Update alpha at MAX nodes: alpha = max(alpha, value).
        - Update beta at MIN nodes: beta = min(beta, value).
        - Pass alpha and beta through the recursive calls.
        """


        # TODO: Implement your code here (BONUS)

        '''num_agents = state.get_num_agents()
        def alphabeta(state, depth, agent_index, alpha, beta):

            if state.is_win() or state.is_lose() or depth == 0:
                return self.evaluation_function(state)

            if agent_index == 0:
                return maximize(state, depth, alpha, beta)
            else:
                return minimize(state, depth, agent_index, alpha, beta)
            
        def maximize(state, depth, alpha, beta):

            max_val = float("-inf")

            for action in state.get_legal_actions(0):
                succ = state.generate_successor(0, action)
                value = alphabeta(succ, depth, 1, alpha, beta)
                max_val = max(max_val, value)

                if max_val > beta:
                    return max_val

                alpha = max(alpha, max_val)

            return max_val
        def minimize(state, depth, agent_index, alpha, beta):

            min_val = float("inf")

            for action in state.get_legal_actions(agent_index):
                succ = state.generate_successor(agent_index, action)

                if agent_index == num_agents - 1:
                    value = alphabeta(succ, depth - 1, 0, alpha, beta)
                else:
                    value = alphabeta(succ, depth, agent_index + 1, alpha, beta)

                min_val = min(min_val, value)

                if min_val < alpha:
                    return min_val

                beta = min(beta, min_val)

            return min_val'''
        
        '''Prompt: use the code in minimax to fix my errors in alhpa beta prunning. (Adjunto estaba el codigo del intento hecho a mano)'''
        num_agents = state.get_num_agents()

        def alphabeta(state, depth, agent_index, alpha, beta):
            if state.is_win() or state.is_lose() or depth == 0:
                return self.evaluation_function(state)

            actions = state.get_legal_actions(agent_index)
            if not actions:
                return self.evaluation_function(state)

            next_agent = (agent_index + 1) % num_agents
            next_depth = depth - 1 if next_agent == 0 else depth

            if agent_index == 0:  # Drone (MAX)
                value = float("-inf")
                for action in actions:
                    succ = state.generate_successor(agent_index, action)
                    value = max(value, alphabeta(succ, next_depth, next_agent, alpha, beta))
                    if value > beta:    # prune
                        return value
                    alpha = max(alpha, value)
                return value

            else:  # Hunters (MIN)
                value = float("inf")
                for action in actions:
                    succ = state.generate_successor(agent_index, action)
                    value = min(value, alphabeta(succ, next_depth, next_agent, alpha, beta))
                    if value < alpha:   # prune
                        return value
                    beta = min(beta, value)
                return value

        # Root
        actions = state.get_legal_actions(0)
        if not actions:
            return None

        non_stop = [a for a in actions if a != Directions.STOP]
        if non_stop:
            actions = non_stop

        best_action = None
        best_value = float("-inf")
        alpha = float("-inf")
        beta = float("inf")

        for action in actions:
            succ = state.generate_successor(0, action)
            value = alphabeta(succ, self.depth, 1, alpha, beta)
            if value > best_value:
                best_value = value
                best_action = action
            alpha = max(alpha, best_value)

        return best_action


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Expectimax agent with a mixed hunter model.

    Each hunter acts randomly with probability self.prob and greedily
    (worst-case / MIN) with probability 1 - self.prob.

    * When prob = 0:  behaves like Minimax (hunters always play optimally).
    * When prob = 1:  pure expectimax (hunters always play uniformly at random).
    * When 0 < prob < 1: weighted combination that correctly models the
      actual MixedHunterAgent used at game-play time.

    Chance node formula:
        value = (1 - p) * min(child_values) + p * mean(child_values)
    """

    def get_action(self, state: GameState) -> Directions | None:
        #print('AAAA')
        """
        Returns the best action for the drone using expectimax with mixed hunter model.

        Tips:
        - Drone nodes are MAX (same as Minimax).
        - Hunter nodes are CHANCE with mixed model: the hunter acts greedily with
          probability (1 - self.prob) and uniformly at random with probability self.prob.
        - Mixed expected value = (1-p) * min(child_values) + p * mean(child_values).
        - When p=0 this reduces to Minimax; when p=1 it is pure uniform expectimax.
        - Do NOT prune in expectimax (unlike alpha-beta).
        - self.prob is set via the constructor argument prob.
        """
        # TODO: Implement your code here
        '''prob = self.prob
        num_agents = state.get_num_agents()

        def expectimax(state, depth, agent_index):

            if state.is_win() or state.is_lose() or depth == 0:
                return self.evaluation_function(state)

            if agent_index == 0:
                return maximize(state, depth)
            else:
                return chance(state, depth, agent_index)
            
            
        def maximize(state, depth):

            max_val = float("-inf")

            for action in state.get_legal_actions(0):
                succ = state.generate_successor(0, action)
                value = expectimax(succ, depth, 1)
                max_val = max(max_val, value)

            return max_val
        
        def minimize(state, depth, agent_index):

            min_val = float("inf")

            for action in state.get_legal_actions(agent_index):
                succ = state.generate_successor(agent_index, action)

                if agent_index == num_agents - 1:
                    value = expectimax(succ, depth - 1, 0)
                else:
                    value = expectimax(succ, depth, agent_index + 1)

                min_val = min(min_val, value)

            return min_val
        
        def chance(state, depth, agent_index):
            if prob == 0:
                return minimize(state, depth, agent_index)
            elif prob == 1:
                return maximize(state, depth)
            else:
                child_values = []
                for action in state.get_legal_actions(agent_index):
                    succ = state.generate_successor(agent_index, action)

                    if agent_index == num_agents - 1:
                        value = expectimax(succ, depth - 1, 0)
                    else:
                        value = expectimax(succ, depth, agent_index + 1)

                    child_values.append(value)

                expected_value = (1 - prob) * min(child_values) + prob * (sum(child_values) / len(child_values))
                return expected_value

        best_action = None
        best_value = float("-inf")
        return best_action'''

        '''Prompt: Implement the expectimax algorithm for the drone (MAX) vs hunters (CHANCE) game. Each hunter acts randomly with probability self.prob and greedily (worst-case / MIN) with probability 1 - self.prob. Use the formula value = (1-p) * min(child_values) + p * mean(child_values) for chance nodes. Return the ACTION that maximizes the expectimax value for the drone.
        (Adjunto estaba el codigo del intento hecho a mano)'''

        num_agents = state.get_num_agents()
        #print("prob:", self.prob)
        def expectimax(state, depth, agent_index):

            if state.is_win() or state.is_lose() or depth == 0:
                return self.evaluation_function(state)

            actions = state.get_legal_actions(agent_index)

            next_agent = (agent_index + 1) % num_agents
            next_depth = depth - 1 if next_agent == 0 else depth

            # DRONE (MAX)
            if agent_index == 0:

                value = float("-inf")

                for action in actions:
                    successor = state.generate_successor(agent_index, action)
                    value = max(value, expectimax(successor, next_depth, next_agent))

                return value

            # HUNTERS (CHANCE)
            else:

                values = []

                for action in actions:
                    successor = state.generate_successor(agent_index, action)
                    v = expectimax(successor, next_depth, next_agent)
                    values.append(v)

                greedy_val = min(values)
                random_val = sum(values) / len(values)

                return (1 - self.prob) * greedy_val + self.prob * random_val


        best_action = None
        best_value = float("-inf")

        for action in state.get_legal_actions(0):

            successor = state.generate_successor(0, action)
            value = expectimax(successor, self.depth, 1)

            if value > best_value:
                best_value = value
                best_action = action

        return best_action
