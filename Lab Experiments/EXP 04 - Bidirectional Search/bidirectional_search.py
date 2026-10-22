"""
Bidirectional Search
Problem: Find a path between a source node and a goal node by running two simultaneous
breadth-first searches (one forward from start, one backward from goal) until they meet.
"""

from collections import deque

def bidirectional_search(graph, start, goal):
    """
    Executes Bidirectional BFS between start and goal nodes.
    Returns the complete path if connected, else None.
    """
    if start == goal:
        return [start]

    # Queues for forward and backward frontiers
    forward_queue = deque([start])
    backward_queue = deque([goal])

    # Parent tracking maps: node -> parent
    forward_parent = {start: None}
    backward_parent = {goal: None}

    intersection_node = None

    print(f"Initiating Bidirectional Search from '{start}' to '{goal}'...")
    step = 1

    while forward_queue and backward_queue:
        # Step Forward Search
        f_current = forward_queue.popleft()
        print(f"Step {step}a [Forward]  : Expanding node '{f_current}'")
        for neighbor in graph.get(f_current, []):
            if neighbor not in forward_parent:
                forward_parent[neighbor] = f_current
                forward_queue.append(neighbor)

                # Check if this node has been visited by backward search
                if neighbor in backward_parent:
                    intersection_node = neighbor
                    print(f"\n[INTERSECTION FOUND] Frontiers met at node '{intersection_node}'!")
                    break

        if intersection_node:
            break

        # Step Backward Search
        b_current = backward_queue.popleft()
        print(f"Step {step}b [Backward] : Expanding node '{b_current}'")
        for neighbor in graph.get(b_current, []):
            if neighbor not in backward_parent:
                backward_parent[neighbor] = b_current
                backward_queue.append(neighbor)

                # Check if this node has been visited by forward search
                if neighbor in forward_parent:
                    intersection_node = neighbor
                    print(f"\n[INTERSECTION FOUND] Frontiers met at node '{intersection_node}'!")
                    break

        if intersection_node:
            break

        step += 1

    if not intersection_node:
        print("\n[NO PATH] The start and goal nodes are disconnected.")
        return None

    # Reconstruct path from start to intersection
    path_forward = []
    curr = intersection_node
    while curr is not None:
        path_forward.append(curr)
        curr = forward_parent[curr]
    path_forward.reverse()

    # Reconstruct path from intersection to goal
    path_backward = []
    curr = backward_parent[intersection_node]
    while curr is not None:
        path_backward.append(curr)
        curr = backward_parent[curr]

    full_path = path_forward + path_backward
    return full_path


if __name__ == "__main__":
    # Predefined undirected state-space graph
    # Graph Topology:
    # 0 - 1 - 4 - 7 - 10 - 13 - 14
    # |   |   |   |   |
    # 2 - 3   5 - 6   8 - 9 - 11 - 12 - 14
    undirected_graph = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 3],
        3: [1, 2],
        4: [1, 5, 7],
        5: [4, 6],
        6: [5],
        7: [4, 8, 10],
        8: [7, 9],
        9: [8, 11],
        10: [7, 13],
        11: [9, 12],
        12: [11, 14],
        13: [10, 14],
        14: [12, 13]
    }

    source = 0
    destination = 14

    solution_path = bidirectional_search(undirected_graph, source, destination)

    if solution_path:
        print(f"\nConstructed Solution Path: {' -> '.join(map(str, solution_path))}")
        print(f"Total Path Length (Edges): {len(solution_path) - 1}")
