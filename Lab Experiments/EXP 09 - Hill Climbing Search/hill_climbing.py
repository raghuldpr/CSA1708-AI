"""
Hill Climbing Search
Problem: Find the maximum value of a mathematical function using Hill Climbing Search.
Objective: Maximize f(x) = -(x - 4)^2 + 25 (Peak at x = 4, f(x) = 25)
"""

def objective_function(x):
    """
    Mathematical function to be maximized.
    f(x) = -(x - 4)^2 + 25
    Maximum occurs at x = 4.0 where f(4.0) = 25.0
    """
    return -(x - 4) ** 2 + 25


def get_neighbors(current_x, step_size):
    """
    Generates left and right neighbors along the continuous domain.
    """
    return [current_x - step_size, current_x + step_size]


def hill_climbing(start_x, step_size=0.1, max_iterations=200):
    """
    Executes Steepest Ascent Hill Climbing to find the local/global maximum.
    """
    current_x = start_x
    current_value = objective_function(current_x)

    print(f"=== Hill Climbing Search for Function Maximization ===")
    print(f"Objective Function : f(x) = -(x - 4)^2 + 25")
    print(f"Initial Starting x : {current_x:.4f} | Initial f(x) = {current_value:.4f}")
    print(f"Step Size          : {step_size}")
    print("-" * 55)

    trajectory = [(current_x, current_value)]

    for iteration in range(1, max_iterations + 1):
        neighbors = get_neighbors(current_x, step_size)
        best_neighbor = None
        best_neighbor_val = current_value

        # Evaluate neighbors
        for neighbor in neighbors:
            val = objective_function(neighbor)
            if val > best_neighbor_val:
                best_neighbor_val = val
                best_neighbor = neighbor

        # If no neighbor yields a strictly better objective value, we reached a peak (local/global maximum)
        if best_neighbor is None or best_neighbor_val <= current_value:
            print(f"\n[TERMINATION] Local/Global Maximum reached at iteration {iteration}!")
            break

        current_x = best_neighbor
        current_value = best_neighbor_val
        trajectory.append((current_x, current_value))

        if iteration <= 10 or iteration % 5 == 0:
            print(f"Iteration {iteration:3d}: x = {current_x:8.4f} | f(x) = {current_value:8.4f}")

    return current_x, current_value, trajectory


if __name__ == "__main__":
    initial_point = -2.0  # Starting point far from peak x = 4.0
    step = 0.2

    best_x, maximum_val, path = hill_climbing(initial_point, step_size=step)

    print("\n" + "=" * 55)
    print(f"FINAL RESULT:")
    print(f"Optimal x Coordinate : {best_x:.4f}")
    print(f"Maximum f(x) Value   : {maximum_val:.4f}")
    print(f"Total Steps Climbed  : {len(path) - 1}")
