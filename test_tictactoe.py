"""
test_tictactoe.py — Unit tests for board logic and Minimax AI correctness.

Run:
    python -m pytest test_tictactoe.py -v
  or simply:
    python test_tictactoe.py
"""

import sys
import unittest

# Allow running from the TIC-TAC-TOE folder or from its parent
sys.path.insert(0, ".")

from board import (
    make_board,
    available_moves,
    make_move,
    check_winner,
    is_terminal,
    opponent,
    PLAYER_X,
    PLAYER_O,
    EMPTY,
)
from ai import best_move


# ─────────────────────────────────────────────
#  Board logic tests
# ─────────────────────────────────────────────

class TestBoard(unittest.TestCase):

    def test_fresh_board_is_all_empty(self):
        b = make_board()
        self.assertEqual(len(b), 9)
        self.assertTrue(all(c == EMPTY for c in b))

    def test_available_moves_full_range_on_new_board(self):
        self.assertEqual(available_moves(make_board()), list(range(9)))

    def test_make_move_does_not_mutate_original(self):
        b = make_board()
        b2 = make_move(b, 0, PLAYER_X)
        self.assertEqual(b[0], EMPTY)      # original untouched
        self.assertEqual(b2[0], PLAYER_X)

    def test_available_moves_shrinks_after_move(self):
        b = make_move(make_board(), 4, PLAYER_X)
        moves = available_moves(b)
        self.assertNotIn(4, moves)
        self.assertEqual(len(moves), 8)

    def test_no_winner_on_empty_board(self):
        self.assertIsNone(check_winner(make_board()))

    def test_row_win(self):
        b = make_board()
        for i in (0, 1, 2):
            b = make_move(b, i, PLAYER_X)
        self.assertEqual(check_winner(b), PLAYER_X)

    def test_column_win(self):
        b = make_board()
        for i in (0, 3, 6):
            b = make_move(b, i, PLAYER_O)
        self.assertEqual(check_winner(b), PLAYER_O)

    def test_diagonal_win(self):
        b = make_board()
        for i in (0, 4, 8):
            b = make_move(b, i, PLAYER_X)
        self.assertEqual(check_winner(b), PLAYER_X)

    def test_anti_diagonal_win(self):
        b = make_board()
        for i in (2, 4, 6):
            b = make_move(b, i, PLAYER_O)
        self.assertEqual(check_winner(b), PLAYER_O)

    def test_draw_detection(self):
        # X O X
        # X X O
        # O X O  — no winner, all filled
        moves = [
            (0, PLAYER_X), (1, PLAYER_O), (2, PLAYER_X),
            (3, PLAYER_X), (4, PLAYER_X), (5, PLAYER_O),
            (6, PLAYER_O), (7, PLAYER_X), (8, PLAYER_O),
        ]
        b = make_board()
        for idx, player in moves:
            b = make_move(b, idx, player)
        self.assertEqual(check_winner(b), "draw")

    def test_is_terminal_true_on_win(self):
        b = make_board()
        for i in (0, 1, 2):
            b = make_move(b, i, PLAYER_X)
        self.assertTrue(is_terminal(b))

    def test_is_terminal_false_mid_game(self):
        b = make_move(make_board(), 0, PLAYER_X)
        self.assertFalse(is_terminal(b))

    def test_opponent(self):
        self.assertEqual(opponent(PLAYER_X), PLAYER_O)
        self.assertEqual(opponent(PLAYER_O), PLAYER_X)


# ─────────────────────────────────────────────
#  AI correctness tests
# ─────────────────────────────────────────────

class TestAI(unittest.TestCase):

    def _board_from(self, x_positions, o_positions):
        """Convenience: place X's and O's by index."""
        b = make_board()
        for i in x_positions:
            b = make_move(b, i, PLAYER_X)
        for i in o_positions:
            b = make_move(b, i, PLAYER_O)
        return b

    def test_ai_takes_winning_move(self):
        # O has 3,4 — should play 5 to win the middle row
        #  X | X | .
        #  O | O | .
        #  . | . | .
        b = self._board_from(x_positions=[0, 1], o_positions=[3, 4])
        move = best_move(b, difficulty="hard")
        self.assertEqual(move, 5, "AI must take the winning move at index 5")

    def test_ai_blocks_human_win(self):
        # X has 0,1 — O must block at 2
        #  X | X | .
        #  . | O | .
        #  . | . | .
        b = self._board_from(x_positions=[0, 1], o_positions=[4])
        move = best_move(b, difficulty="hard")
        self.assertEqual(move, 2, "AI must block X from winning at index 2")

    def test_ai_prefers_winning_over_blocking(self):
        # O has 6,7 (can win at 8) AND X has 0,1 (can win at 2)
        # AI should win rather than block
        b = self._board_from(x_positions=[0, 1], o_positions=[6, 7])
        move = best_move(b, difficulty="hard")
        self.assertEqual(move, 8, "AI must win at index 8 rather than just block")

    def test_ai_plays_on_fresh_board(self):
        b = make_board()
        move = best_move(b, difficulty="hard")
        self.assertIn(move, range(9))

    def test_easy_ai_plays_random_valid_move(self):
        b = make_board()
        for _ in range(50):
            move = best_move(b, difficulty="easy")
            self.assertIn(move, available_moves(b))

    def test_medium_ai_blocks(self):
        # same blocking scenario — medium depth-3 search still catches this
        b = self._board_from(x_positions=[0, 1], o_positions=[4])
        move = best_move(b, difficulty="medium")
        self.assertEqual(move, 2)

    def test_hard_ai_never_loses(self):
        """Simulate 100 games where X plays random; hard Minimax AI (O) must never lose."""
        import random
        from board import check_winner, available_moves, make_move

        losses = 0
        for _ in range(100):
            board = make_board()
            current = PLAYER_X
            while True:
                if current == PLAYER_X:
                    move = random.choice(available_moves(board))
                else:
                    move = best_move(board, difficulty="hard")
                board = make_move(board, move, current)
                result = check_winner(board)
                if result:
                    if result == PLAYER_X:
                        losses += 1
                    break
                current = PLAYER_O if current == PLAYER_X else PLAYER_X

        self.assertEqual(losses, 0, f"Hard AI lost {losses}/100 games — should be 0")


# ─────────────────────────────────────────────
#  Runner
# ─────────────────────────────────────────────

if __name__ == "__main__":
    unittest.main(verbosity=2)
