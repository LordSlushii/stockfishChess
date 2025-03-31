import requests
import chess

# Persistent board instance
board = chess.Board()

# Lichess Cloud Analysis API (No token required)
LICHESS_API_URL = "https://lichess.org/api/cloud-eval"

def stockfishPrediction(opponentMove):
    global board

    try:
        move = chess.Move.from_uci(opponentMove.strip())
        if move in board.legal_moves:
            board.push(move)
        else:
            return "Invalid move!"
    except:
        return "Invalid input!"

    if board.is_game_over():
        return "Game Over!"

    # Request best move from Lichess
    params = {"fen": board.fen(), "multiPv": 1}
    response = requests.get(LICHESS_API_URL, params=params)

    if response.status_code == 200:
        best_move = response.json().get("pvs", [{}])[0].get("moves", "").split()[0]
        if best_move:
            board.push(chess.Move.from_uci(best_move))
            return best_move
        else:
            return "No move found!"
    else:
        return f"Error from Lichess: {response.status_code}, {response.text}"

# Function to reset the board when logging out
def reset_board():
    global board
    board = chess.Board()  # Reset to a fresh chess board
