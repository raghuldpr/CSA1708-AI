"""
A* Search for 2D Grid Pathfinding
Problem: Find the shortest path from a start cell to a goal cell on a 2D grid with obstacles
using the A* Search algorithm with Manhattan Distance heuristic.
f(n) = g(n) + h(n)
"""

import heapq

def manhattan_distance(cell1, cell2):
    """Computes Manhattan distance h(n) between two cells (r1, c1) and (r2, c2)."""
    return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])


def astar_grid_search(grid, start, goal):
    """
    Executes A* search on a 2D grid.
    0 represents a passable cell, 1 represents an obstacle.
    """
    rows = len(grid)
    cols = len(grid[0])

    # Priority queue stores tuples: (f_score, g_score, (r, c))
    open_heap = []
    initial_h = manhattan_distance(start, goal)
    heapq.heappush(open_heap, (initial_h, 0, start))

    # Maps to track g_score and parents
    g_score = {start: 0}
    parent = {start: None}
    closed_set = set()

    print(f"Executing A* Grid Search from Start {start} to Goal {goal}...")
    print(f"Grid Dimensions: {rows} x {cols}\n")

    # 4 directional movements: Up, Down, Left, Right (cost = 1 each)
    directions = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]

    nodes_expanded = 0

    while open_heap:
        f, g, current = heapq.heappop(open_heap)

        if current in closed_set:
            continue
        closed_set.add(current)
        nodes_expanded += 1

        if current == goal:
            print(f"[GOAL REACHED] Total path cost: {g_score[goal]} | Nodes expanded: {nodes_expanded}")
            # Reconstruct path
            path = []
            curr = goal
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            return path

        r, c = current
        for dr, dc, _ in directions:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            # Check boundary conditions and obstacle check
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                if neighbor in closed_set:
                    continue

                tentative_g = g + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = tentative_g
                    parent[neighbor] = current
                    f_val = tentative_g + manhattan_distance(neighbor, goal)
                    heapq.heappush(open_heap, (f_val, tentative_g, neighbor))

    print("[FAILURE] No path exists to the goal.")
    return None


def print_visual_grid(grid, path, start, goal):
    """Visualizes the grid with obstacles (#), path (*), Start (S), and Goal (G)."""
    rows = len(grid)
    cols = len(grid[0])
    path_set = set(path) if path else set()

    print("+" + "---+" * cols)
    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            cell = (r, c)
            if cell == start:
                row_str += " S |"
            elif cell == goal:
                row_str += " G |"
            elif cell in path_set:
                row_str += " * |"
            elif grid[r][c] == 1:
                row_str += " # |"  # Obstacle
            else:
                row_str += "   |"
        print(row_str)
        print("+" + "---+" * cols)


if __name__ == "__main__":
    # 0 = Free cell, 1 = Obstacle
    grid_map = [
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0]
    ]

    start_pos = (0, 0)
    goal_pos = (5, 5)

    path = astar_grid_search(grid_map, start_pos, goal_pos)

    if path:
        print(f"\nOptimal Path ({len(path)} cells):")
        print(" -> ".join(map(str, path)))
        print("\nVisual Grid Representation (S: Start, G: Goal, #: Obstacle, *: Path):")
        print_visual_grid(grid_map, path, start_pos, goal_pos)
