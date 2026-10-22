"""
4-Queens Problem Using Backtracking
Problem: Place 4 non-attacking queens on a 4x4 chessboard such that no two queens
share the same row, column, or diagonal.
"""

def is_safe(board, row, col, n):
    """
    Check if placing a queen at board[row][col] is safe from attack.
    Since queens are placed column by column from left to right,
    we only need to check the left side for conflicts.
    """
    # Check left side of current row
    for j in range(col):
        if board[row][j] == 1:
            return False

    # Check upper diagonal on left side
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1

    # Check lower diagonal on left side
    i, j = row + 1, col - 1
    while i < n and j >= 0:
        if board[i][j] == 1:
            return False
        i += 1
        j -= 1

    return True


def print_board(board, n):
    """Nicely format and display the chessboard configuration."""
    print("+" + "---+" * n)
    for i in range(n):
        row_str = "|"
        for j in range(n):
            row_str += " Q |" if board[i][j] == 1 else " . |"
        print(row_str)
        print("+" + "---+" * n)


def solve_nqueens(board, col, n, solutions):
    """
    Recursive backtracking function to find all valid placements.
    """
    if col >= n:
        # All queens are successfully placed
        solution_snapshot = [row[:] for row in board]
        solutions.append(solution_snapshot)
        return

    for row in range(n):
        if is_safe(board, row, col, n):
            board[row][col] = 1  # Place queen

            solve_nqueens(board, col + 1, n, solutions)  # Recurse for next column

            board[row][col] = 0  # Backtrack


if __name__ == "__main__":
    N = 4
    print(f"Solving the {N}-Queens Problem using Backtracking...")
    initial_board = [[0 for _ in range(N)] for _ in range(N)]
    all_solutions = []

    solve_nqueens(initial_board, 0, N, all_solutions)

    print(f"\nTotal Distinct Solutions Found: {len(all_solutions)}\n")
    for idx, sol in enumerate(all_solutions, 1):
        print(f"--- Solution #{idx} ---")
        print_board(sol, N)
        # Display queen positions as (row, col) coordinates
        queen_coords = [(r, c) for r in range(N) for c in range(N) if sol[r][c] == 1]
        print(f"Queen Coordinates (row, col): {queen_coords}\n")
