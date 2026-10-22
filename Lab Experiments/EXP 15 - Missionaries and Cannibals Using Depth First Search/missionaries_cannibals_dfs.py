"""
Missionaries and Cannibals Problem Using Depth-First Search (DFS)
Problem: Safely transport 3 missionaries and 3 cannibals across a river using a boat
with capacity 2. At no point may cannibals outnumber missionaries on either bank.
State: (M_left, C_left, Boat_left)
  M_left: Number of missionaries on left bank (0 to 3)
  C_left: Number of cannibals on left bank (0 to 3)
  Boat_left: 1 if boat is on left bank, 0 if boat is on right bank
"""

def is_valid_state(state):
    """
    Checks whether a state satisfies problem constraints:
    On neither bank may cannibals outnumber missionaries (unless missionaries count is 0).
    """
    m_left, c_left, _ = state
    m_right = 3 - m_left
    c_right = 3 - c_left

    # Check boundaries
    if not (0 <= m_left <= 3 and 0 <= c_left <= 3):
        return False

    # Check left bank safety
    if m_left > 0 and c_left > m_left:
        return False

    # Check right bank safety
    if m_right > 0 and c_right > m_right:
        return False

    return True


def get_successors(state):
    """
    Generates all valid transitions.
    Possible boat loads: (1, 0), (2, 0), (0, 1), (0, 2), (1, 1) [M, C]
    """
    m_left, c_left, boat_left = state
    successors = []
    possible_boat_moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]

    for m_move, c_move in possible_boat_moves:
        if boat_left == 1:
            # Move from left to right bank
            next_state = (m_left - m_move, c_left - c_move, 0)
            action_desc = f"Boat moves {m_move}M and {c_move}C: Left -> Right"
        else:
            # Move from right to left bank
            next_state = (m_left + m_move, c_left + c_move, 1)
            action_desc = f"Boat moves {m_move}M and {c_move}C: Right -> Left"

        if is_valid_state(next_state):
            successors.append((next_state, action_desc))

    return successors


def dfs_solve(current_state, goal_state, visited, path):
    """
    Recursive DFS search to find a sequence of safe transitions to goal_state.
    """
    if current_state == goal_state:
        return path

    for next_state, action_desc in get_successors(current_state):
        if next_state not in visited:
            visited.add(next_state)
            result = dfs_solve(next_state, goal_state, visited, path + [(next_state, action_desc)])
            if result is not None:
                return result
            # Note: in standard DFS graph search with loop avoidance,
            # visited set prevents redundant cycles

    return None


def solve_missionaries_cannibals():
    """
    Top-level solver function.
    """
    start_state = (3, 3, 1)  # All on left bank
    goal_state = (0, 0, 0)   # All on right bank

    print("=== Missionaries and Cannibals Problem via Depth-First Search (DFS) ===")
    print(f"Start State : {start_state} (3 Missionaries, 3 Cannibals on Left)")
    print(f"Goal State  : {goal_state} (All on Right Bank)\n")

    visited = {start_state}
    initial_path = [(start_state, "Initial Configuration")]

    solution_path = dfs_solve(start_state, goal_state, visited, initial_path)

    if solution_path:
        print(f"[SUCCESS] Solution found in {len(solution_path) - 1} boat crossings!\n")
        print("Detailed Step-by-Step Traversal:")
        print("=" * 75)
        for step_idx, ((ml, cl, b), action) in enumerate(solution_path):
            mr = 3 - ml
            cr = 3 - cl
            b_loc = "Left" if b == 1 else "Right"
            print(f"Step {step_idx:2d} | Left: {ml}M, {cl}C | Right: {mr}M, {cr}C | Boat: {b_loc:<5} | {action}")
        print("=" * 75)
    else:
        print("[FAILURE] No solution could be found.")


if __name__ == "__main__":
    solve_missionaries_cannibals()
