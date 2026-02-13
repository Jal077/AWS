"""A simple terminal Tic-Tac-Toe game for two players."""


def print_board(board: list[str]) -> None:
    """Display the current game board."""
    rows = [board[i : i + 3] for i in range(0, 9, 3)]
    for row_index, row in enumerate(rows):
        print(f" {row[0]} | {row[1]} | {row[2]} ")
        if row_index < 2:
            print("---+---+---")


def check_winner(board: list[str], player: str) -> bool:
    """Return True if player has any winning combination."""
    win_patterns = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]
    return any(all(board[pos] == player for pos in pattern) for pattern in win_patterns)


def is_draw(board: list[str]) -> bool:
    """Return True if there are no open cells left."""
    return all(cell in {"X", "O"} for cell in board)


def ask_move(board: list[str], player: str) -> int:
    """Prompt the player for a valid move and return its board index."""
    while True:
        move = input(f"Player {player}, pick a spot (1-9): ").strip()
        if not move.isdigit():
            print("Please enter a number from 1 to 9.")
            continue

        position = int(move) - 1
        if position < 0 or position > 8:
            print("That spot is out of range. Choose 1 to 9.")
            continue

        if board[position] in {"X", "O"}:
            print("That spot is already taken. Try another one.")
            continue

        return position


def play_game() -> None:
    """Run a full two-player game loop."""
    board = [str(i) for i in range(1, 10)]
    current_player = "X"

    print("Welcome to Tic-Tac-Toe!")
    print("Use numbers 1-9 to place your mark:")
    print_board(board)

    while True:
        move = ask_move(board, current_player)
        board[move] = current_player
        print()
        print_board(board)

        if check_winner(board, current_player):
            print(f"\nPlayer {current_player} wins!")
            break

        if is_draw(board):
            print("\nIt's a draw!")
            break

        current_player = "O" if current_player == "X" else "X"


if __name__ == "__main__":
    play_game()
