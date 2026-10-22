"""
Sudoku Puzzle Using CSP Backtracking
Problem: Solve a 9x9 Sudoku grid as a Constraint Satisfaction Problem (CSP)
using Backtracking with Minimum Remaining Values (MRV) variable selection heuristic.
Constraints:
  1. Each row must contain digits 1-9 without repetition.
  2. Each column must contain digits 1-9 without repetition.
  3. Each 3x3 subgrid must contain digits 1-9 without repetition.
"""

def is_valid(grid, row, col, num):
    """
    Checks whether placing 'num' at grid[row][col] satisfies all CSP constraints.
    """
    # Constraint 1: Check row
    for c in range(9):
        if grid[row][c] == num:
            return False

    # Constraint 2: Check column
    for r in range(9):
        if grid[r][col] == num:
            return False

    # Constraint 3: Check 3x3 box
    box_r, box_c = 3 * (row // 3), 3 * (col // 3)
    for r in range(box_r, box_r + 3):
        for c in range(box_c, box_c + 3):
            if grid[r][c] == num:
                return False

    return True


def find_mrv_empty_cell(grid):
    """
    MRV (Minimum Remaining Values) Heuristic:
    Finds the unassigned cell with the fewest legal values remaining in its domain.
    Returns (row, col) or None if all cells are assigned.
    """
    best_cell = None
    min_legal_values = 10

    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                # Count available valid domain values
                legal_count = sum(1 for val in range(1, 10) if is_valid(grid, r, c, val))
                if legal_count < min_legal_values:
                    min_legal_values = legal_count
                    best_cell = (r, c)
                    if min_legal_values == 1:
                        return best_cell  # Cannot get fewer than 1 remaining choice

    return best_cell


def solve_sudoku_csp(grid):
    """
    Recursive CSP Backtracking solver.
    """
    empty_cell = find_mrv_empty_cell(grid)
    if not empty_cell:
        return True  # Puzzle completely solved

    row, col = empty_cell

    for val in range(1, 10):
        if is_valid(grid, row, col, val):
            grid[row][col] = val  # Assign value

            if solve_sudoku_csp(grid):
                return True

            grid[row][col] = 0  # Backtrack

    return False


def print_sudoku(grid):
    """Prints a formatted 9x9 Sudoku board."""
    for r in range(9):
        if r % 3 == 0 and r != 0:
            print("- - - - - - - - - - -")
        row_str = ""
        for c in range(9):
            if c % 3 == 0 and c != 0:
                row_str += "| "
            val = str(grid[r][c]) if grid[r][c] != 0 else "."
            row_str += val + " "
        print(row_str.strip())


if __name__ == "__main__":
    # Predefined Sudoku puzzle (0 indicates empty cell)
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    print("=== Sudoku Solver using CSP Backtracking (MRV Heuristic) ===")
    print("\nInitial Unsolved Board:")
    print_sudoku(puzzle)
    print("\nSolving...")

    if solve_sudoku_csp(puzzle):
        print("\n[SUCCESS] Sudoku Solved Successfully!")
        print("\nFinal Solved Board:")
        print_sudoku(puzzle)
    else:
        print("\n[FAILURE] No solution exists for this Sudoku configuration.")
