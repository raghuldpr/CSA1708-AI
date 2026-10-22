"""
Greedy Best-First Search
Problem: Find a path from a start node to a goal node in a weighted graph
using Greedy Best-First Search guided strictly by heuristic estimates h(n).
"""

import heapq

def greedy_best_first_search(graph, heuristics, start, goal):
    """
    Executes Greedy Best-First Search.
    Priority Queue key: h(n)
    """
    # Priority Queue stores: (h_score, counter, current_node, path, accumulated_cost)
    counter = 0
    open_heap = []
    heapq.heappush(open_heap, (heuristics[start], counter, start, [start], 0))

    visited = set()

    print(f"Executing Greedy Best-First Search from '{start}' to '{goal}'...")
    print(f"Initial node: {start} with heuristic h({start}) = {heuristics[start]}\n")

    step = 1
    while open_heap:
        h_val, _, current, path, path_cost = heapq.heappop(open_heap)

        print(f"Step {step}: Visiting '{current}' (Heuristic h = {h_val}, Accumulated Cost = {path_cost})")
        step += 1

        if current == goal:
            print(f"\n[GOAL REACHED] Goal node '{goal}' reached successfully!")
            return path, path_cost

        visited.add(current)

        for neighbor, edge_weight in graph.get(current, []):
            if neighbor not in visited and neighbor not in [item[2] for item in open_heap]:
                counter += 1
                heapq.heappush(
                    open_heap,
                    (heuristics[neighbor], counter, neighbor, path + [neighbor], path_cost + edge_weight)
                )

    print("\n[FAILURE] Goal node could not be reached.")
    return None, 0


if __name__ == "__main__":
    # Predefined weighted graph (Romania map snippet or standard AI benchmark)
    # Directed / undirected edge list with weights
    weighted_graph = {
        'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
        'Zerind': [('Arad', 75), ('Oradea', 71)],
        'Oradea': [('Zerind', 71), ('Sibiu', 151)],
        'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
        'Timisoara': [('Arad', 118), ('Lugoj', 111)],
        'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
        'Mehadia': [('Lugoj', 70), ('Drobeta', 75)],
        'Drobeta': [('Mehadia', 75), ('Craiova', 120)],
        'Craiova': [('Drobeta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
        'Rimnicu Vilcea': [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)],
        'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
        'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
        'Bucharest': [('Fagaras', 211), ('Pitesti', 101)]
    }

    # Straight-line distance heuristics to Bucharest
    heuristic_values = {
        'Arad': 366,
        'Zerind': 374,
        'Oradea': 380,
        'Sibiu': 253,
        'Timisoara': 329,
        'Lugoj': 244,
        'Mehadia': 241,
        'Drobeta': 242,
        'Craiova': 160,
        'Rimnicu Vilcea': 193,
        'Fagaras': 176,
        'Pitesti': 100,
        'Bucharest': 0
    }

    start_city = 'Arad'
    destination_city = 'Bucharest'

    solution_path, total_cost = greedy_best_first_search(
        weighted_graph, heuristic_values, start_city, destination_city
    )

    if solution_path:
        print(f"Greedy Best-First Path : {' -> '.join(solution_path)}")
        print(f"Total Traversal Cost   : {total_cost} km")
