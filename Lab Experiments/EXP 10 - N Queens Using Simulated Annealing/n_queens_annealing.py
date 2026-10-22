"""
N-Queens Problem Using Simulated Annealing
Problem: Solve the N-Queens puzzle using the Simulated Annealing optimization heuristic.
Energy Function E: Number of pairs of attacking queens (E = 0 corresponds to a valid solution).
Acceptance Criterion:
  If delta_E < 0: accept move
  Else: accept move with probability P = exp(-delta_E / T)
"""

import math
import random

def calculate_conflicts(board):
    """
    Computes total pairs of attacking queens.
    board[i] represents the row position of queen in column i.
    """
    n = len(board)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            # Same row
            if board[i] == board[j]:
                conflicts += 1
            # Same diagonal
            elif abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts


def get_neighbor(board):
    """
    Generates a neighbor state by moving a randomly selected queen to a new row.
    """
    neighbor = list(board)
    n = len(board)
    col = random.randint(0, n - 1)
    current_row = neighbor[col]
    new_row = random.randint(0, n - 1)
    while new_row == current_row:
        new_row = random.randint(0, n - 1)
    neighbor[col] = new_row
    return neighbor


def print_board(board):
    """Nicely displays the N-Queens chessboard."""
    n = len(board)
    print("+" + "---+" * n)
    for r in range(n):
        row_str = "|"
        for c in range(n):
            row_str += " Q |" if board[c] == r else " . |"
        print(row_str)
        print("+" + "---+" * n)


def simulated_annealing_nqueens(n=8, initial_temp=100.0, cooling_rate=0.99, min_temp=0.001, max_steps=5000):
    """
    Simulated Annealing algorithm to find a 0-conflict configuration.
    """
    # Initialize random board configuration
    current_board = [random.randint(0, n - 1) for _ in range(n)]
    current_cost = calculate_conflicts(current_board)
    temperature = initial_temp

    print(f"=== Solving {n}-Queens using Simulated Annealing ===")
    print(f"Initial Board Conflicts: {current_cost}")
    print(f"Parameters: Initial Temp = {initial_temp}, Cooling Rate = {cooling_rate}\n")

    step = 0
    while temperature > min_temp and current_cost > 0 and step < max_steps:
        step += 1
        neighbor = get_neighbor(current_board)
        neighbor_cost = calculate_conflicts(neighbor)
        delta_cost = neighbor_cost - current_cost

        # Acceptance check
        if delta_cost < 0:
            current_board = neighbor
            current_cost = neighbor_cost
        else:
            acceptance_prob = math.exp(-delta_cost / temperature)
            if random.random() < acceptance_prob:
                current_board = neighbor
                current_cost = neighbor_cost

        temperature *= cooling_rate

        if step % 200 == 0 or current_cost == 0:
            print(f"Step {step:4d} | Temp: {temperature:8.4f} | Current Conflicts: {current_cost}")

    return current_board, current_cost, step


if __name__ == "__main__":
    # Fix seed for guaranteed reproducible successful execution
    random.seed(1)
    N = 8

    final_board, final_conflicts, total_steps = simulated_annealing_nqueens(n=N)

    print("\n" + "=" * 50)
    if final_conflicts == 0:
        print(f"[SUCCESS] Found valid solution in {total_steps} steps with 0 conflicts!")
        print(f"Queen column positions (index = col, value = row): {final_board}\n")
        print("Final Chessboard:")
        print_board(final_board)
    else:
        print(f"[FAILED] Reached minimum temperature with {final_conflicts} conflicts.")
