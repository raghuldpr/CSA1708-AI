"""
Iterative Deepening Depth-First Search (IDDFS)
Problem: Finding a path from a start node to a goal node in a state-space graph
using iterative deepening of depth limits.
"""

def depth_limited_dfs(graph, current_node, goal_node, depth_limit, visited_path):
    """
    Recursive depth-limited search helper.
    Returns (found_boolean, path_list).
    """
    visited_path.append(current_node)

    if current_node == goal_node:
        return True, visited_path

    if depth_limit <= 0:
        visited_path.pop()
        return False, None

    for neighbor in graph.get(current_node, []):
        if neighbor not in visited_path:  # Avoid cycles within current path branch
            found, path = depth_limited_dfs(graph, neighbor, goal_node, depth_limit - 1, visited_path)
            if found:
                return True, path

    visited_path.pop()  # Backtrack
    return False, None


def iddfs(graph, start, goal, max_depth):
    """
    Performs IDDFS up to max_depth.
    """
    print(f"Starting IDDFS from '{start}' to '{goal}' (Max Depth Limit: {max_depth})")
    print("-" * 50)

    for depth in range(max_depth + 1):
        print(f"Exploring at Depth Limit = {depth} ...")
        found, path = depth_limited_dfs(graph, start, goal, depth, [])
        if found:
            print(f"\n[SUCCESS] Goal '{goal}' found at depth limit {depth}!")
            return path
        else:
            print(f"  Goal not found within depth limit {depth}.")

    print(f"\n[FAILURE] Goal '{goal}' could not be reached within depth {max_depth}.")
    return None


if __name__ == "__main__":
    # Predefined state-space graph (directed graph representing nodes and connections)
    # Graph structure:
    #         A
    #       /   \
    #      B     C
    #     / \   / \
    #    D   E F   G
    #   /
    #  H
    state_space_graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F', 'G'],
        'D': ['H'],
        'E': [],
        'F': [],
        'G': [],
        'H': []
    }

    start_node = 'A'
    target_goal = 'G'
    maximum_depth = 4

    solution_path = iddfs(state_space_graph, start_node, target_goal, maximum_depth)

    if solution_path:
        print(f"Optimal Path Found : {' -> '.join(solution_path)}")
        print(f"Number of Edges    : {len(solution_path) - 1}")
