from __future__ import annotations
from algorithms.utils import bfs_distance, dijkstra
import math

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from world.game_state import GameState


def evaluation_function(state: GameState) -> float:
    """
    Evaluation function for non-terminal states of the drone vs. hunters game.

    A good evaluation function can consider multiple factors, such as:
      (a) BFS distance from drone to nearest delivery point (closer is better).
          Uses actual path distance so walls and terrain are respected.
      (b) BFS distance from each hunter to the drone, traversing only normal
          terrain ('.' / ' ').  Hunters blocked by mountains, fog, or storms
          are treated as unreachable (distance = inf) and pose no threat.
      (c) BFS distance to a "safe" position (i.e., a position that is not in the path of any hunter).
      (d) Number of pending deliveries (fewer is better).
      (e) Current score (higher is better).
      (f) Delivery urgency: reward the drone for being close to a delivery it can
          reach strictly before any hunter, so it commits to nearby pickups
          rather than oscillating in place out of excessive hunter fear.
      (g) Adding a revisit penalty can help prevent the drone from getting stuck in cycles.

    Returns a value in [-1000, +1000].

    Tips:
    - Use state.get_drone_position() to get the drone's current (x, y) position.
    - Use state.get_hunter_positions() to get the list of hunter (x, y) positions.
    - Use state.get_pending_deliveries() to get the set of pending delivery (x, y) positions.
    - Use state.get_score() to get the current game score.
    - Use state.get_layout() to get the current layout.
    - Use state.is_win() and state.is_lose() to check terminal states.
    - Use bfs_distance(layout, start, goal, hunter_restricted) from algorithms.utils
      for cached BFS distances. hunter_restricted=True for hunter-only terrain.
    - Use dijkstra(layout, start, goal) from algorithms.utils for cached
      terrain-weighted shortest paths, returning (cost, path).
    - Consider edge cases: no pending deliveries, no hunters nearby.
    - A good evaluation function balances delivery progress with hunter avoidance.
    """
    # TODO: Implement your code here

    '''drone_pos = state.get_drone_position()
    hunter_positions = state.get_hunter_positions()
    deliveries = state.get_pending_deliveries()
    layout = state.get_layout()

    
    if state.is_win():
        return 1000.0
    if state.is_lose():
        return -1000.0
    score= state.get_score()

    value=score

    if deliveries:
        delivery_distances = [bfs_distance(layout, drone_pos, delivery) for delivery in deliveries]
        min_delivery_distance = min(delivery_distances)
        value += 100 / (min_delivery_distance + 1)
    for hunter_pos in hunter_positions:
        hunter_distance = bfs_distance(layout, drone_pos, hunter_pos, hunter_restricted=True)
        if hunter_distance == math.inf:
            continue
        value -= 100 / (hunter_distance + 1)

    return value'''

    '''promtpt: use the code in evaluation function to fix my errors in the evaluation function. (Adjunto estaba el codigo del intento hecho a mano)'''


    drone_pos = state.get_drone_position()
    hunters = state.get_hunter_positions()
    deliveries = state.get_pending_deliveries()
    score = state.get_score()
    layout = state.get_layout()

    # ---- DELIVERY DISTANCE (MUCHO MAS IMPORTANTE) ----
    if deliveries:
        min_delivery_dist = float("inf")

        for delivery in deliveries:
            dist = dijkstra(layout, drone_pos, delivery)[0]
            if dist < min_delivery_dist:
                min_delivery_dist = dist

        # más incentivo por acercarse
        score += 20 / (min_delivery_dist + 1)


    # ---- HUNTER DISTANCE (menos conservador) ----
    for hunter in hunters:

        dist = bfs_distance(layout, hunter, drone_pos, hunter_restricted=True)

        if dist == float("inf"):
            continue

        if dist <= 1:
            score -= 300   # morir sigue siendo muy malo
        elif dist <= 2:
            score -= 80
        elif dist <= 3:
            score -= 20
        else:
            score += dist * 0.1


    # ---- NUMBER OF DELIVERIES (penalización fuerte) ----
    score -= 50 * len(deliveries)

    return score