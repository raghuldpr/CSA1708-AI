"""
Tic-Tac-Toe Using Minimax Algorithm with Alpha-Beta Pruning
Problem: Implement optimal game playing for Tic-Tac-Toe using Minimax search
enhanced by Alpha-Beta Pruning to prune redundant branches.
"""

# Symbols
AI_PLAYER = 'X'     # Maximizer
HUMAN_PLAYER = 'O'  # Minimizer
EMPTY = ' '

def print_board(board):
    """Displays the 3x3 Tic-Tac-Toe board."""
    print("-------------")
    for r in range(3):
        print(f"| {board[r][0]} | {board[r][1]} | {board[r][2]} |")
        print("-------------")


def evaluate_board(board):
    """
    Evaluates terminal states:
      +10 if AI ('X') wins
      -10 if Opponent ('O') wins
        0 if draw or non-terminal
    """
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return 10 if board[i][0] == AI_PLAYER else -10
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return 10 if board[0][i] == AI_PLAYER else -10

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return 10 if board[0][0] == AI_PLAYER else -10
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return 10 if board[0][2] == AI_PLAYER else -10

    return 0


def is_moves_left(board):
    """Returns True if any empty cell remains on the board."""
    for r in range(3):
        for c in range(3):
            if board[r][c] == EMPTY:
                return True
    return False


def minimax_alpha_beta(board, depth, is_maximizing, alpha, beta):
    """
    Minimax search with Alpha-Beta Pruning.
    """
    score = evaluate_board(board)

    # If maximizer has won the game
    if score == 10:
        return score - depth  # Prefer faster wins

    # If minimizer has won the game
    if score == -10:
        return score + depth  # Prefer slower losses

    # If no more moves and no winner, it's a draw
    if not is_moves_left(board):
        return 0

    if is_maximizing:
        max_eval = -float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = AI_PLAYER
                    eval_val = minimax_alpha_beta(board, depth + 1, False, alpha, beta)
                    board[r][c] = EMPTY
                    max_eval = max(max_eval, eval_val)
                    alpha = max(alpha, eval_val)
                    if beta <= alpha:
                        break  # Beta cutoff / pruning
        return max_eval
    else:
        min_eval = float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = HUMAN_PLAYER
                    eval_val = minimax_alpha_beta(board, depth + 1, True, alpha, beta)
                    board[r][c] = EMPTY
                    min_eval = min(min_eval, eval_val)
                    beta = min(beta, eval_val)
                    if beta <= alpha:
                        break  # Alpha cutoff / pruning
        return min_eval


def find_best_move(board):
    """
    Finds the optimal move (row, col) for the AI player ('X') using Alpha-Beta Minimax.
    """
    best_val = -float('inf')
    best_move = (-1, -1)

    for r in range(3):
        for c in range(3):
            if board[r][c] == EMPTY:
                board[r][c] = AI_PLAYER
                move_val = minimax_alpha_beta(board, 0, False, -float('inf'), float('inf'))
                board[r][c] = EMPTY

                if move_val > best_val:
                    best_val = move_val
                    best_move = (r, c)

    return best_move, best_val


def demonstrate_scenario():
    """
    Demonstrates the AI analyzing a critical mid-game board state and selecting the winning move.
    """
    print("=== Tic-Tac-Toe Minimax with Alpha-Beta Pruning Demonstration ===\n")

    # Scenario 1: Strategic scenario where 'X' can win or block
    scenario_board = [
        ['X', 'O', 'X'],
        ['O', 'X', ' '],
        [' ', ' ', 'O']
    ]

    print("Current Board State (AI = 'X', Opponent = 'O'):")
    print_board(scenario_board)

    best_move, score = find_best_move(scenario_board)
    print(f"Alpha-Beta Evaluation Score : {score}")
    print(f"Optimal Selected Move (r, c): {best_move} (Row {best_move[0] + 1}, Col {best_move[1] + 1})")

    scenario_board[best_move[0]][best_move[1]] = AI_PLAYER
    print("\nBoard After AI Move:")
    print_board(scenario_board)

    # Scenario 2: Simulation of full end-game resolution
    print("\nProceeding to full game completion from this state...")
    turn = HUMAN_PLAYER
    while is_moves_left(scenario_board) and evaluate_board(scenario_board) == 0:
        if turn == AI_PLAYER:
            mv, _ = find_best_move(scenario_board)
            scenario_board[mv[0]][mv[1]] = AI_PLAYER
            print(f"AI ('X') moves at {mv}")
            print_board(scenario_board)
            turn = HUMAN_PLAYER
        else:
            # Simple defensive/opportunistic response from empty cells
            empty_cells = [(r, c) for r in range(3) for c in range(3) if scenario_board[r][c] == EMPTY]
            mv = empty_cells[0]
            scenario_board[mv[0]][mv[1]] = HUMAN_PLAYER
            print(f"Opponent ('O') moves at {mv}")
            print_board(scenario_board)
            turn = AI_PLAYER

    final_eval = evaluate_board(scenario_board)
    print("\n" + "=" * 40)
    if final_eval == 10:
        print("RESULT: AI ('X') Won the Game!")
    elif final_eval == -10:
        print("RESULT: Opponent ('O') Won the Game!")
    else:
        print("RESULT: The game ended in a DRAW (Optimal defense)!")
    print("=" * 40)


if __name__ == "__main__":
    demonstrate_scenario()
