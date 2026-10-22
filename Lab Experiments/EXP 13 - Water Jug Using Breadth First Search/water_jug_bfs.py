"""
Water Jug Problem Using Breadth-First Search (BFS)
Problem: Given two jugs of capacities X and Y liters, measure exactly Z liters
in one of the jugs using the minimum number of steps via BFS.
Possible Actions:
  1. Fill Jug 1
  2. Fill Jug 2
  3. Empty Jug 1
  4. Empty Jug 2
  5. Pour Jug 1 -> Jug 2
  6. Pour Jug 2 -> Jug 1
"""

from collections import deque

def get_successors(state, cap1, cap2):
    """
    Generates all valid next states from the current (j1, j2) state.
    """
    j1, j2 = state
    successors = []

    # 1. Fill Jug 1 completely
    if j1 < cap1:
        successors.append(((cap1, j2), f"Fill Jug 1 (Cap: {cap1}L)"))

    # 2. Fill Jug 2 completely
    if j2 < cap2:
        successors.append(((j1, cap2), f"Fill Jug 2 (Cap: {cap2}L)"))

    # 3. Empty Jug 1
    if j1 > 0:
        successors.append(((0, j2), "Empty Jug 1"))

    # 4. Empty Jug 2
    if j2 > 0:
        successors.append(((j1, 0), "Empty Jug 2"))

    # 5. Pour Jug 1 -> Jug 2
    if j1 > 0 and j2 < cap2:
        pour = min(j1, cap2 - j2)
        successors.append(((j1 - pour, j2 + pour), f"Pour {pour}L from Jug 1 into Jug 2"))

    # 6. Pour Jug 2 -> Jug 1
    if j2 > 0 and j1 < cap1:
        pour = min(j2, cap1 - j1)
        successors.append(((j1 + pour, j2 - pour), f"Pour {pour}L from Jug 2 into Jug 1"))

    return successors


def solve_water_jug_bfs(cap1, cap2, target):
    """
    Solves the Water Jug problem using Breadth-First Search.
    """
    print(f"=== Water Jug Problem using BFS ===")
    print(f"Jug 1 Capacity : {cap1} Liters")
    print(f"Jug 2 Capacity : {cap2} Liters")
    print(f"Target Volume  : {target} Liters\n")

    initial_state = (0, 0)
    # Queue stores: (current_state, path_of_actions_and_states)
    queue = deque([(initial_state, [(initial_state, "Initial State (Both Empty)")])])
    visited = {initial_state}

    nodes_explored = 0

    while queue:
        (j1, j2), path = queue.popleft()
        nodes_explored += 1

        # Check goal condition: either jug contains the target amount
        if j1 == target or j2 == target:
            print(f"[TARGET REACHED] Solution found in {len(path) - 1} steps! (Explored {nodes_explored} states)\n")
            print("Step-by-step Solution Sequence:")
            print("=" * 60)
            for step_idx, ((s1, s2), action_desc) in enumerate(path):
                print(f"Step {step_idx:2d}: Jug 1 = {s1}L, Jug 2 = {s2}L  -->  {action_desc}")
            print("=" * 60)
            return path

        for next_state, action_desc in get_successors((j1, j2), cap1, cap2):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [(next_state, action_desc)]))

    print("[FAILURE] No solution exists to measure the target volume.")
    return None


if __name__ == "__main__":
    # Standard classic test case: 4L jug, 3L jug, target = 2L
    jug1_capacity = 4
    jug2_capacity = 3
    target_amount = 2

    solve_water_jug_bfs(jug1_capacity, jug2_capacity, target_amount)
