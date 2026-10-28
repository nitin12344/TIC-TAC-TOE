"""
board.py — Tic-Tac-Toe board state, rendering, and rule checks.
"""

# Win combinations (indices into the 9-cell flat board list)
WIN_COMBOS = [
    (0, 1, 2),  # top row
    (3, 4, 5),  # middle row
    (6, 7, 8),  # bottom row
    (0, 3, 6),  # left column
    (1, 4, 7),  # middle column
    (2, 5, 8),  # right column
    (0, 4, 8),  # diagonal \
    (2, 4, 6),  # diagonal /
]

EMPTY = " "
PLAYER_X = "X"
PLAYER_O = "O"


def make_board() -> list:
    """Return a fresh 9-cell board (indices 0-8, left-to-right, top-to-bottom)."""
    return [EMPTY] * 9


def display_board(board: list) -> None:
    """Pretty-print the board with position hints on empty cells."""
    def cell(i):
        return board[i] if board[i] != EMPTY else str(i + 1)

    print()
    print(f" {cell(0)} | {cell(1)} | {cell(2)} ")
    print("---+---+---")
    print(f" {cell(3)} | {cell(4)} | {cell(5)} ")
    print("---+---+---")
    print(f" {cell(6)} | {cell(7)} | {cell(8)} ")
    print()


def available_moves(board: list) -> list:
    """Return list of indices that are still empty."""
    return [i for i, v in enumerate(board) if v == EMPTY]


def make_move(board: list, index: int, player: str) -> list:
    """Return a NEW board with the player's mark placed at index."""
    new_board = board[:]
    new_board[index] = player
    return new_board


def check_winner(board: list) -> str | None:
    """
    Return the winning player symbol ('X' or 'O'),
    'draw' if the board is full with no winner, or None if game is ongoing.
    """
    for a, b, c in WIN_COMBOS:
        if board[a] == board[b] == board[c] != EMPTY:
            return board[a]
    if not available_moves(board):
        return "draw"
    return None


def is_terminal(board: list) -> bool:
    """True when the game is over (win or draw)."""
    return check_winner(board) is not None


def opponent(player: str) -> str:
    """Return the other player."""
    return PLAYER_O if player == PLAYER_X else PLAYER_X
