"""
Beam Search Algorithm
Problem: Find a path from start to goal in a state-space graph using Beam Search
with a predefined beam width (beta).
At each level/step, only the top beta best nodes (lowest heuristic h(n)) are retained.
"""

def beam_search(graph, heuristics, start, goal, beam_width=2):
    """
    Executes Beam Search on a state-space graph.
    """
    print(f"=== Beam Search (Beam Width = {beam_width}) ===")
    print(f"Searching path from '{start}' to '{goal}'\n")

    # The beam stores candidates: (node, path)
    beam = [(start, [start])]
    level = 0

    while beam:
        print(f"--- Level {level} (Beam Size: {len(beam)}) ---")
        for node, path in beam:
            print(f"  Candidate: {' -> '.join(path)} (h = {heuristics.get(node, float('inf'))})")

        # Check if goal is present in current beam
        for node, path in beam:
            if node == goal:
                print(f"\n[GOAL FOUND] Goal '{goal}' reached at level {level}!")
                return path

        # Generate all successor candidates from the current beam
        all_candidates = []
        for node, path in beam:
            for neighbor in graph.get(node, []):
                if neighbor not in path:  # Prevent cyclic looping
                    new_path = path + [neighbor]
                    all_candidates.append((neighbor, new_path))

        if not all_candidates:
            print("\n[FAILURE] No further successors to expand.")
            return None

        # Sort all successors by heuristic value (ascending)
        all_candidates.sort(key=lambda item: heuristics.get(item[0], float('inf')))

        # Select top 'beam_width' candidates to form the new beam (pruning the rest)
        beam = all_candidates[:beam_width]
        level += 1

    print("\n[FAILURE] Beam became empty without finding goal.")
    return None


if __name__ == "__main__":
    # State-space graph representing a tree/graph
    # Level 0: S
    # Level 1: A, B, C
    # Level 2: D, E, F, G, H
    # Level 3: I, J, K, Goal
    state_space_graph = {
        'S': ['A', 'B', 'C'],
        'A': ['D', 'E'],
        'B': ['F', 'G'],
        'C': ['H'],
        'D': ['I'],
        'E': ['J'],
        'F': ['GOAL'],
        'G': ['K'],
        'H': ['GOAL'],
        'I': [],
        'J': [],
        'K': [],
        'GOAL': []
    }

    # Heuristic estimates h(n) representing estimated distance to GOAL
    heuristic_values = {
        'S': 10,
        'A': 8,
        'B': 5,
        'C': 7,
        'D': 6,
        'E': 7,
        'F': 2,
        'G': 4,
        'H': 3,
        'I': 5,
        'J': 6,
        'K': 4,
        'GOAL': 0
    }

    start_node = 'S'
    target_goal = 'GOAL'
    w = 2  # Beam width

    solution_path = beam_search(state_space_graph, heuristic_values, start_node, target_goal, beam_width=w)

    if solution_path:
        print("\n" + "=" * 45)
        print(f"Optimal Beam Path : {' -> '.join(solution_path)}")
        print(f"Path Length (Edges): {len(solution_path) - 1}")
