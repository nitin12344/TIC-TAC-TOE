"""
main.py — Entry point for the Tic-Tac-Toe AI game.

Run:
    python main.py
"""

import sys
from board import PLAYER_X, PLAYER_O
from game import play_game, ScoreBoard


# ── helpers ──────────────────────────────────────────────────────────────────

def _bold(t):   return f"\033[1m{t}\033[0m"
def _cyan(t):   return f"\033[96m{t}\033[0m"
def _yellow(t): return f"\033[93m{t}\033[0m"
def _green(t):  return f"\033[92m{t}\033[0m"


def _prompt(question: str, choices: dict, default: str) -> str:
    """
    Display a menu and return the user's validated choice key.
    choices = {"1": ("label", "value"), ...}
    """
    print()
    for key, (label, _) in choices.items():
        marker = _green("►") if _ == default else " "
        print(f"  {marker} {_bold(key)}) {label}")
    while True:
        raw = input(f"\n  Your choice [{default}]: ").strip()
        if raw == "":
            raw = default
        # Accept either the key or the shorthand value directly
        for key, (label, value) in choices.items():
            if raw.lower() in (key, value.lower(), label.lower()):
                return value
        print("  Invalid choice, please try again.")


# ── main menu ─────────────────────────────────────────────────────────────────

def main_menu() -> dict:
    """Display the main menu and return a settings dict."""
    print()
    print(_bold(_cyan("  ╔══════════════════════════════════╗")))
    print(_bold(_cyan("  ║     TIC-TAC-TOE  AI  PLAYER      ║")))
    print(_bold(_cyan("  ║      Minimax Algorithm AI         ║")))
    print(_bold(_cyan("  ╚══════════════════════════════════╝")))

    # ── Game mode ──
    print(_bold("\n  Select game mode:"))
    mode = _prompt(
        "mode",
        {
            "1": ("Human vs AI  (you play against the unbeatable AI)", "hva"),
            "2": ("AI vs AI    (watch two AIs play each other)",        "ava"),
        },
        default="1",
    )

    human_symbol = PLAYER_X
    if mode == "hva":
        # ── Symbol choice ──
        print(_bold("\n  Choose your symbol:"))
        sym = _prompt(
            "symbol",
            {
                "1": ("X  (you go first)", PLAYER_X),
                "2": ("O  (AI goes first)", PLAYER_O),
            },
            default="1",
        )
        human_symbol = sym

        # ── Difficulty ──
        print(_bold("\n  Choose difficulty:"))
        difficulty = _prompt(
            "difficulty",
            {
                "1": ("Easy    — random AI moves",            "easy"),
                "2": ("Medium  — AI looks 3 moves ahead",     "medium"),
                "3": ("Hard    — unbeatable (full Minimax)",  "hard"),
            },
            default="3",
        )
    else:
        difficulty = "hard"

    return {
        "mode": mode,
        "human_symbol": human_symbol,
        "difficulty": difficulty,
    }


# ── play-again loop ────────────────────────────────────────────────────────────

def run() -> None:
    print("\033[?25h", end="")   # ensure cursor visible on exit
    try:
        settings = main_menu()
        scoreboard = ScoreBoard(settings["human_symbol"])

        while True:
            result = play_game(
                human_symbol=settings["human_symbol"],
                difficulty=settings["difficulty"],
                ai_vs_ai=(settings["mode"] == "ava"),
            )
            scoreboard.record(result)
            scoreboard.display()

            print()
            again = input("  Play again? (y/n) [y]: ").strip().lower()
            if again in ("n", "no", "q", "quit"):
                print(_bold(_cyan("\n  Thanks for playing! Goodbye.\n")))
                break

    except KeyboardInterrupt:
        print(_bold(_cyan("\n\n  Game interrupted. Goodbye!\n")))
        sys.exit(0)


if __name__ == "__main__":
    run()
