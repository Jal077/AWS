"""Accessible Flask Tic-Tac-Toe web app."""

from __future__ import annotations

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"

WIN_PATTERNS = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


def fresh_state() -> dict[str, object]:
    """Create a new game state."""
    return {
        "board": ["" for _ in range(9)],
        "current_player": "X",
        "winner": "",
        "status": "Player X's turn.",
        "game_over": False,
    }


def get_state() -> dict[str, object]:
    """Read the game state from session or initialize it."""
    if "game" not in session:
        session["game"] = fresh_state()
    return session["game"]


def calculate_winner(board: list[str], player: str) -> bool:
    """Return True if player has a winning pattern."""
    return any(all(board[idx] == player for idx in pattern) for pattern in WIN_PATTERNS)


def board_is_full(board: list[str]) -> bool:
    """Return True if all cells are taken."""
    return all(cell in {"X", "O"} for cell in board)


@app.get("/")
def index() -> str:
    """Render the game board."""
    state = get_state()
    return render_template("index.html", state=state)


@app.post("/move")
def move() -> str:
    """Apply a player move and update game state."""
    state = get_state()
    if state["game_over"]:
        return redirect(url_for("index"))

    move_raw = request.form.get("cell", "")
    if not move_raw.isdigit():
        state["status"] = "Invalid move. Choose an open square."
        session["game"] = state
        return redirect(url_for("index"))

    position = int(move_raw)
    if position < 0 or position > 8:
        state["status"] = "Invalid move. Choose an open square."
        session["game"] = state
        return redirect(url_for("index"))

    board = state["board"]
    if board[position]:
        state["status"] = "That square is already taken. Pick another one."
        session["game"] = state
        return redirect(url_for("index"))

    current_player = state["current_player"]
    board[position] = current_player

    if calculate_winner(board, current_player):
        state["winner"] = current_player
        state["game_over"] = True
        state["status"] = f"Player {current_player} wins!"
    elif board_is_full(board):
        state["game_over"] = True
        state["status"] = "It's a draw!"
    else:
        state["current_player"] = "O" if current_player == "X" else "X"
        state["status"] = f"Player {state['current_player']}'s turn."

    session["game"] = state
    return redirect(url_for("index"))


@app.post("/reset")
def reset() -> str:
    """Reset game to initial state."""
    session["game"] = fresh_state()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
