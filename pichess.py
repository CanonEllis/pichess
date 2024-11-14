import chess
import chess.engine
import serial
import time

# Stockfish and CNC configuration
stockfish_path = "/path/to/stockfish"  # Replace with your Stockfish path
gcode_file_path = "gcode_file.nc"
port = "/dev/ttyACM0"  # Change this to your CNC serial port
baud_rate = 115200  # Common baud rate for CNC machines

# Initialize chess board and engine
board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

# Open serial connection to CNC machine
try:
    ser = serial.Serial(port, baud_rate, timeout=1)
    print(f"Successfully connected to {port} at {baud_rate} baud.")
except Exception as e:
    print(f"Error opening serial port: {e}")
    exit(1)

# Allow some time for the connection to stabilize
time.sleep(2)

# Function to write Stockfish's move to G-code file
def write_move_to_gcode_file(move):
    with open(gcode_file_path, "a") as gcode_file:
        gcode_command = f"G1 {move.uci()}\n"  # Example G-code command format
        gcode_file.write(gcode_command)
        print(f"Appended move to G-code file: {gcode_command.strip()}")

# Function to send the G-code file to the CNC machine
def send_gcode_to_cnc():
    try:
        with open(gcode_file_path, "r") as file:
            print(f"Sending G-code commands from {file.name}...")
            for line in file:
                line = line.strip()
                if line:
                    print(f"Sending: {line}")
                    ser.write((line + "\n").encode())  # Send each G-code line to the CNC machine
                    time.sleep(0.1)  # Small delay for processing
                else:
                    print("Skipping empty line.")
    except FileNotFoundError:
        print("Error: G-code file not found!")
        exit(1)
    except Exception as e:
        print(f"Error reading the G-code file: {e}")
        exit(1)

# Function for player's move input and legality check
def player_move(move):
    if move in board.legal_moves:
        board.push(move)
        return True
    else:
        print("Illegal move! Try again.")
        return False

# Function for Stockfish's best move and updating G-code file
def stockfish_best_move():
    result = engine.play(board, chess.engine.Limit(time=1.0))  # 1-second think time
    best_move = result.move
    print(f"Stockfish suggests: {best_move}")
    board.push(best_move)
    write_move_to_gcode_file(best_move)  # Add move to G-code file
    send_gcode_to_cnc()  # Send updated G-code to CNC

# Game loop
while not board.is_game_over():
    print(board)
    
    # Get player's input
    player_input = input("Enter your move (e.g., e2e4), or type 'board' to see the current board: ")
    
    if player_input.lower() == "board":
        print("Current board state:")
        print(board)
        continue

    try:
        move = chess.Move.from_uci(player_input)
    except ValueError:
        print("Invalid move format! Please try again.")
        continue

    if player_move(move):
        stockfish_best_move()

# End game and close serial connection
print("Game over!")
engine.quit()
ser.close()
print("G-code sent successfully.")
