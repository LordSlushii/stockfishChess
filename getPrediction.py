import chess
import chess.engine

# Persistent board instance
board = chess.Board()

def stockfishPrediction(opponentMove):
    stockfish_path = "/Users/navaneethkrishna/Downloads/stockfish/stockfish-macos-m1-apple-silicon"
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    global board  # Use the same board instance

    try:
        move = chess.Move.from_uci(opponentMove.strip())
        if move in board.legal_moves:
            board.push(move)
        else:
            engine.quit()
            return "Invalid move!"
    except:
        engine.quit()
        return "Invalid input!"

    if board.is_game_over():
        engine.quit()
        return "Game Over!"

    # Get best move from Stockfish
    result = engine.play(board, chess.engine.Limit(time=1.0))
    best_move = result.move
    board.push(best_move)

    engine.quit()
    return best_move.uci()  # Return move in UCI format

# Function to reset the board when logging out
def reset_board():
    global board
    board = chess.Board()  # Reset to a fresh chess board
