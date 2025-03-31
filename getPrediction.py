import requests
import chess

# Initialize the chess board
board = chess.Board()


def stockfishPrediction(opponentMove):
    global board  # Ensure we're using the same board instance

    # Validate and apply the UCI move
    try:
        move = chess.Move.from_uci(opponentMove.strip())
        if move in board.legal_moves:
            board.push(move)
        else:
            return "Invalid move!"
    except:
        return "Invalid input!"

    # Check if the game is over
    if board.is_game_over():
        return "Game Over!"

    # Convert the updated board to FEN format
    fen_position = board.fen()

    # Call Lichess Cloud API with the new FEN
    url = f"https://lichess.org/api/cloud-eval?fen={fen_position}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        best_move = data.get("pvs", [{}])[0].get("moves", "").split()[0]
        return best_move if best_move else "No move found"

    return "Error fetching move!"
