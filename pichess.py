import chess
import chess.engine

# Path to your Stockfish executable
stockfish_path = "stockfish"  # Replace with your Stockfish path

# Initialize board and engine
board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

def player_move(move):
    # Check if the move is legal
    if move in board.legal_moves:
        board.push(move)
        return True
    else:
        print("Illegal move! Try again.")
        return False

def stockfish_best_move():
    # Use Stockfish to get the best move
    result = engine.play(board, chess.engine.Limit(time=1.0))  # 1 second thinking time
    best_move = result.move
    print(f"Stockfish suggests: {best_move}")
    board.push(best_move)

# Game loop
while not board.is_game_over():
    # Display the board
    print(board)
    
    # Get player's input
    player_input = input("Enter your move (e.g., e2e4), or type 'board' to see the current board: ")
    
    # Check if the input is the 'board' command
    if player_input.lower() == "board":
        print("Current board state:")
        print(board)
        continue  # Skip the rest of the loop and prompt for the next input

    try:
        # Parse the player's move
        move = chess.Move.from_uci(player_input)
    except ValueError:
        print("Invalid move format! Please try again.")
        continue

    # Attempt to make the player's move
    if player_move(move):
        # Get Stockfish's best move
        stockfish_best_move()

# End the game and close the engine
print("Game over!")
engine.quit()

