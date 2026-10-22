"""
15-Puzzle Problem Using A* Search and Manhattan Distance Heuristic
Problem: Solve the 15-puzzle (4x4 sliding tile game) using the A* Search algorithm.
Evaluation Function:
  f(n) = g(n) + h(n)
  where g(n) is the path cost (number of moves made so far),
  and h(n) is the total Manhattan distance of all numbered tiles from their goal positions.
"""

import heapq

# Target Goal State for 15-Puzzle
GOAL_STATE = (
    1,  2,  3,  4,
    5,  6,  7,  8,
    9, 10, 11, 12,
   13, 14, 15,  0
)

# Precompute goal positions (row, col) for each tile (1-15)
GOAL_POSITIONS = {}
for idx, tile_num in enumerate(GOAL_STATE):
    if tile_num != 0:
        GOAL_POSITIONS[tile_num] = divmod(idx, 4)


def manhattan_distance_heuristic(state):
    """
    Computes total Manhattan distance: sum of |r - r_goal| + |c - c_goal|
    for all tiles 1 through 15 (ignoring the empty blank 0).
    """
    total_distance = 0
    for idx, val in enumerate(state):
        if val != 0:
            target_r, target_c = GOAL_POSITIONS[val]
            curr_r, curr_c = divmod(idx, 4)
            total_distance += abs(curr_r - target_r) + abs(curr_c - target_c)
    return total_distance


def get_neighbors(state):
    """
    Generates successor configurations by moving blank tile (0) Up, Down, Left, or Right.
    """
    neighbors = []
    blank_idx = state.index(0)
    row, col = divmod(blank_idx, 4)

    moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
    for dr, dc, move_name in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 4 and 0 <= new_col < 4:
            new_blank_idx = new_row * 4 + new_col
            state_list = list(state)
            # Swap blank tile with adjacent tile
            state_list[blank_idx], state_list[new_blank_idx] = state_list[new_blank_idx], state_list[blank_idx]
            neighbors.append((tuple(state_list), move_name))
    return neighbors


def print_15_board(state):
    """Nicely formats and prints a 4x4 board."""
    print("+----+----+----+----+")
    for r in range(4):
        row_str = "|"
        for c in range(4):
            val = state[r * 4 + c]
            row_str += f" {val:2d} |" if val != 0 else "    |"
        print(row_str)
        print("+----+----+----+----+")


def solve_15_puzzle_astar(initial_state):
    """
    Executes A* search with Manhattan Distance heuristic.
    """
    initial_h = manhattan_distance_heuristic(initial_state)

    # Priority queue stores: (f_score, g_score, counter, current_state, path)
    counter = 0
    open_heap = []
    heapq.heappush(open_heap, (initial_h, 0, counter, initial_state, [(initial_state, "INITIAL")]))

    visited_costs = {initial_state: 0}

    print("=== Solving 15-Puzzle using A* Search (Manhattan Distance) ===")
    print("\nInitial State Board:")
    print_15_board(initial_state)
    print(f"Initial Manhattan Distance h(s0) = {initial_h}\n")

    nodes_expanded = 0

    while open_heap:
        f_val, g_val, _, current_state, path = heapq.heappop(open_heap)
        nodes_expanded += 1

        if current_state == GOAL_STATE:
            print(f"[GOAL REACHED] Solution found in {g_val} moves! (Nodes expanded: {nodes_expanded})\n")
            print("Step-by-Step Solution Path:")
            print("=" * 45)
            for step_num, (st, action) in enumerate(path):
                h = manhattan_distance_heuristic(st)
                print(f"Step {step_num}: Action = {action} | g = {step_num}, h = {h}, f = {step_num + h}")
                print_15_board(st)
                print()
            return path

        for neighbor_state, action in get_neighbors(current_state):
            tentative_g = g_val + 1
            if tentative_g < visited_costs.get(neighbor_state, float('inf')):
                visited_costs[neighbor_state] = tentative_g
                h_val = manhattan_distance_heuristic(neighbor_state)
                counter += 1
                heapq.heappush(
                    open_heap,
                    (tentative_g + h_val, tentative_g, counter, neighbor_state, path + [(neighbor_state, action)])
                )

    print("[FAILURE] No solution path found.")
    return None


if __name__ == "__main__":
    # Solvable 15-Puzzle configuration (optimal 4-move distance to goal)
    start_state = (
        1,  2,  3,  4,
        5,  6,  7,  8,
        9, 10,  0, 11,
       13, 14, 15, 12
    )

    solve_15_puzzle_astar(start_state)
