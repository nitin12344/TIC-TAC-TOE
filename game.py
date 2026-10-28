"""
game.py — Game loop: Human vs AI, AI vs AI, or Human vs Human.
"""

import time
from board import (
    make_board,
    display_board,
    available_moves,
    make_move,
    check_winner,
    PLAYER_X,
    PLAYER_O,
    EMPTY,
)
from ai import best_move


# ── ANSI colour helpers (graceful fallback on systems without ANSI support) ──
def _coloured(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

def green(t):  return _coloured(t, "92")
def red(t):    return _coloured(t, "91")
def yellow(t): return _coloured(t, "93")
def cyan(t):   return _coloured(t, "96")
def bold(t):   return _coloured(t, "1")


# ─────────────────────────────────────────────
#  Human input helper
# ─────────────────────────────────────────────

def _get_human_move(board: list, player: str) -> int:
    """Prompt until the human enters a valid, unoccupied position (1-9)."""
    while True:
        try:
            raw = input(f"  {bold(player)} — enter position (1-9): ").strip()
            index = int(raw) - 1
            if index not in range(9):
                raise ValueError
            if board[index] != EMPTY:
                print(red("  That cell is already taken. Try again."))
                continue
            return index
        except (ValueError, IndexError):
            print(red("  Invalid input. Enter a number from 1 to 9."))


# ─────────────────────────────────────────────
#  Single-game runner
# ─────────────────────────────────────────────

def play_game(
    human_symbol: str = PLAYER_X,
    difficulty: str = "hard",
    ai_vs_ai: bool = False,
) -> str:
    """
    Run one complete game.

    Returns
    -------
    The winner symbol ('X' or 'O') or 'draw'.
    """
    board = make_board()
    current = PLAYER_X          # X always goes first
    ai_symbol = PLAYER_O if human_symbol == PLAYER_X else PLAYER_X

    print()
    print(bold(cyan("  ╔══════════════════════╗")))
    print(bold(cyan("  ║   TIC-TAC-TOE  AI    ║")))
    print(bold(cyan("  ╚══════════════════════╝")))

    if not ai_vs_ai:
        print(f"  You are {bold(yellow(human_symbol))}  |  AI is {bold(red(ai_symbol))}  |  Difficulty: {bold(difficulty.upper())}")
    else:
        print(f"  {bold('AI vs AI')} watch-mode  |  X uses Minimax, O uses Minimax")

    display_board(board)

    while True:
        is_ai_turn = ai_vs_ai or (current == ai_symbol)

        if is_ai_turn:
            print(f"  {bold(red('AI'))} ({current}) is thinking…")
            time.sleep(0.4)          # tiny pause so it feels natural
            move = best_move(board, difficulty)
            print(f"  AI played position {bold(str(move + 1))}")
        else:
            move = _get_human_move(board, current)

        board = make_move(board, move, current)
        display_board(board)

        result = check_winner(board)
        if result is not None:
            if result == "draw":
                print(bold(yellow("  It's a draw! Well played.")))
            elif result == human_symbol and not ai_vs_ai:
                print(bold(green(f"  🎉  {result} wins! Congratulations!")))
            else:
                label = "AI" if result == ai_symbol and not ai_vs_ai else result
                print(bold(red(f"  {label} wins!")))
            return result

        # Switch turn
        current = PLAYER_O if current == PLAYER_X else PLAYER_X


# ─────────────────────────────────────────────
#  Score tracker across multiple rounds
# ─────────────────────────────────────────────

class ScoreBoard:
    def __init__(self, human_symbol: str):
        self.human = human_symbol
        self.ai    = PLAYER_O if human_symbol == PLAYER_X else PLAYER_X
        self.scores = {human_symbol: 0, self.ai: 0, "draw": 0}

    def record(self, result: str) -> None:
        self.scores[result] = self.scores.get(result, 0) + 1

    def display(self) -> None:
        h, a, d = self.scores[self.human], self.scores[self.ai], self.scores["draw"]
        print()
        print(bold("  ── Score ──────────────────"))
        print(f"  You ({self.human}):  {green(str(h))}   AI ({self.ai}):  {red(str(a))}   Draw:  {yellow(str(d))}")
        print(bold("  ────────────────────────────"))
