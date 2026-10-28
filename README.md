# Tic-Tac-Toe AI

An unbeatable Tic-Tac-Toe AI built in Python using the **Minimax algorithm**.

---

## Features

| Feature | Detail |
|---|---|
| **Unbeatable AI** | Full Minimax search — the AI never loses on Hard |
| **3 Difficulty Levels** | Easy (random), Medium (depth-3), Hard (full search) |
| **Symbol Choice** | Play as X (go first) or O (go second) |
| **AI vs AI Mode** | Watch two Minimax agents play each other |
| **Score Tracker** | Persistent win/draw/loss counter across rounds |
| **Clean Terminal UI** | ANSI colours, position hints on empty cells |

---

## Project Structure

```
TIC-TAC-TOE/
├── main.py           # Entry point — menus and play-again loop
├── game.py           # Game loop, human input, score board
├── ai.py             # Minimax engine
├── board.py          # Board state, move generation, win detection
├── test_tictactoe.py # Unit tests (board logic + AI correctness)
└── README.md
```

---

## How to Run

```bash
cd TIC-TAC-TOE
python main.py
```

### Run the Tests

```bash
python test_tictactoe.py
# or, if pytest is installed:
python -m pytest test_tictactoe.py -v
```

---

## How to Play

1. **Choose a game mode** — Human vs AI or AI vs AI (watch mode).
2. **Pick your symbol** — X goes first, O goes second.
3. **Choose difficulty** — Easy, Medium, or Hard.
4. **Enter a position (1–9)** corresponding to the board grid:

```
 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9
```

---

## Algorithm

### Minimax

Minimax is a recursive decision algorithm used in two-player zero-sum games.
It simulates all possible future moves to the end of the game and assigns scores:

| Outcome | Score |
|---|---|
| AI wins  | +10 |
| Human wins | −10 |
| Draw | 0 |

The **maximiser** (AI / O) picks the move with the highest score;
the **minimiser** (Human / X) picks the move with the lowest score.
The full game tree for a 3 × 3 board has at most **9! = 362,880** nodes,
which is small enough to explore completely without any pruning.

### Depth-adjusted scoring

Winning in fewer moves scores higher (`+10 − depth`) and losing in more moves
scores less negative (`−10 + depth`). This makes the AI both choose the fastest
win **and** delay a loss as long as possible.

---

## Requirements

- Python 3.10+ (uses the `str | None` union type hint)
- No third-party packages required
