"""
ai.py — Minimax AI for an unbeatable Tic-Tac-Toe player.

Algorithm overview
------------------
Minimax explores the entire game tree, scoring leaf nodes:
  +10  — AI wins
  -10  — Human wins
   0   — Draw

The maximiser (AI / O) picks the move with the highest score.
The minimiser (Human / X) picks the move with the lowest score.
Scores are adjusted by depth so the AI prefers faster wins
and delays losses as long as possible.

Difficulty levels control search depth / move quality:
  easy   — random move (no search)
  medium — minimax limited to depth 3
  hard   — full minimax (unbeatable)
"""

import random
from board import (
    available_moves,
    make_move,
    check_winner,
    PLAYER_X,
    PLAYER_O,
)

# Scores from the AI's perspective (AI is always PLAYER_O internally)
_SCORES = {
    PLAYER_O: +10,  # AI wins    → maximise
    PLAYER_X: -10,  # Human wins → minimise
    "draw":     0,
}


def _minimax(board: list, depth: int, is_maximising: bool, max_depth: int) -> int:
    """
    Recursive Minimax (no pruning).

    Parameters
    ----------
    board         : current board state
    depth         : current recursion depth (increments downward)
    is_maximising : True when it is the AI's turn
    max_depth     : cut-off depth (use a large number for full search)

    Returns
    -------
    The heuristic score of the board from the AI's perspective.
    The score is adjusted by depth so the AI prefers faster wins
    and delays losses as long as possible.
    """
    result = check_winner(board)
    if result is not None:
        # Adjust terminal score by depth: prefer faster wins, slower losses
        # Positive score (AI wins) → subtract depth so earlier wins score higher
        # Negative score (human wins) → add depth so later losses score higher
        base = _SCORES[result]
        if base > 0:
            return base - depth
        elif base < 0:
            return base + depth
        return 0  # draw

    if depth >= max_depth:
        return 0  # neutral evaluation at cut-off (no heuristic needed for 3×3)

    if is_maximising:
        best = -1000
        for move in available_moves(board):
            new_board = make_move(board, move, PLAYER_O)
            score = _minimax(new_board, depth + 1, False, max_depth)
            best = max(best, score)
        return best
    else:
        best = +1000
        for move in available_moves(board):
            new_board = make_move(board, move, PLAYER_X)
            score = _minimax(new_board, depth + 1, True, max_depth)
            best = min(best, score)
        return best


def best_move(board: list, difficulty: str = "hard") -> int:
    """
    Return the index of the AI's chosen move.

    difficulty
    ----------
    'easy'   : random legal move
    'medium' : minimax with depth limit 3
    'hard'   : full minimax (unbeatable)
    """
    moves = available_moves(board)

    if difficulty == "easy":
        return random.choice(moves)

    max_depth = 3 if difficulty == "medium" else 9  # 9 is effectively unlimited for 3×3

    best_score = -1000
    chosen = moves[0]

    for move in moves:
        new_board = make_move(board, move, PLAYER_O)
        score = _minimax(new_board, 0, False, max_depth)
        if score > best_score:
            best_score = score
            chosen = move

    return chosen
