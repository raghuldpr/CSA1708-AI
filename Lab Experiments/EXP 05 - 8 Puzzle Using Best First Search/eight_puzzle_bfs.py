"""
8-Puzzle Problem Using Best-First Search (Greedy Best-First)
Problem: Solve the 8-puzzle sliding tile game using Best-First Search guided by
the Misplaced Tiles heuristic (h(n)).
"""

import heapq

GOAL_STATE = (
    1, 2, 3,
    4, 5, 6,
    7, 8, 0
)

def misplaced_tiles_heuristic(state, goal=GOAL_STATE):
    """
    Counts the number of tiles that are not in their goal position
    (ignoring the empty blank tile represented by 0).
    """
    misplaced = 0
    for i in range(9):
        if state[i] != 0 and state[i] != goal[i]:
            misplaced += 1
    return misplaced


def get_neighbors(state):
    """
    Generates successor states by sliding the blank tile (0) Up, Down, Left, or Right.
    """
    neighbors = []
    blank_idx = state.index(0)
    row, col = divmod(blank_idx, 3)

    moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
    for dr, dc, move_name in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_blank_idx = new_row * 3 + new_col
            state_list = list(state)
            # Swap blank with target neighbor tile
            state_list[blank_idx], state_list[new_blank_idx] = state_list[new_blank_idx], state_list[blank_idx]
            neighbors.append((tuple(state_list), move_name))
    return neighbors


def print_board(state):
    """Prints a 3x3 puzzle board nicely."""
    for r in range(3):
        row_vals = [str(state[r * 3 + c]) if state[r * 3 + c] != 0 else ' ' for c in range(3)]
        print(f"| {' | '.join(row_vals)} |")


def solve_8_puzzle_best_first(initial_state):
    """
    Solves 8-puzzle using Best-First Search based on h(n).
    """
    # Priority Queue stores: (h_score, counter, current_state, path_of_states_and_moves)
    counter = 0
    open_heap = []
    initial_h = misplaced_tiles_heuristic(initial_state)
    heapq.heappush(open_heap, (initial_h, counter, initial_state, [(initial_state, "INITIAL")]))

    visited = set()
    visited.add(initial_state)

    print("=== Solving 8-Puzzle using Best-First Search (Misplaced Tiles Heuristic) ===")
    print("\nInitial State:")
    print_board(initial_state)
    print(f"Initial Misplaced Tiles Heuristic h(s0) = {initial_h}\n")

    nodes_expanded = 0

    while open_heap:
        h, _, current_state, path = heapq.heappop(open_heap)
        nodes_expanded += 1

        if current_state == GOAL_STATE:
            print(f"[GOAL REACHED] Solution found in {len(path) - 1} moves! (Nodes expanded: {nodes_expanded})\n")
            print("Step-by-step Solution Path:")
            print("=" * 40)
            for step_num, (st, action) in enumerate(path):
                print(f"Step {step_num}: Action = {action} | Heuristic h = {misplaced_tiles_heuristic(st)}")
                print_board(st)
                print("-" * 20)
            return path

        for next_state, action in get_neighbors(current_state):
            if next_state not in visited:
                visited.add(next_state)
                next_h = misplaced_tiles_heuristic(next_state)
                counter += 1
                heapq.heappush(open_heap, (next_h, counter, next_state, path + [(next_state, action)]))

    print("No solution found.")
    return None


if __name__ == "__main__":
    # Solvable initial state (easy to moderate complexity)
    start_state = (
        1, 2, 3,
        4, 0, 6,
        7, 5, 8
    )

    solve_8_puzzle_best_first(start_state)
