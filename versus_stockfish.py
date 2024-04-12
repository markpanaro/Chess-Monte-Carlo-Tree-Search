import chess
from mcts import mcts, Node
import chess.engine

def self_play(engine_path):
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci(engine_path)

    engine.configure({"Skill Level": 0})

    while not board.is_game_over(claim_draw=True):
        if board.turn == chess.WHITE:
            # MCTS AI's turn (White)
            root_player_color = chess.WHITE
            root = Node(state=board.copy(), player_color=root_player_color)
            ai_move = mcts(root, iterations=1200) 
            board.push(ai_move)

            print(f"MCTS AI move: {ai_move}")
            print("Current board state:\n", board.unicode(invert_color=True, borders=True))
        else:
            # Stockfish's turn (Black)
            # Limit Stockfish's thinking time
            result = engine.play(board, chess.engine.Limit(time=0.0001))
            board.push(result.move)

            print(f"Stockfish move: {result.move}")
            print("Current board state:\n", board.unicode(invert_color=True, borders=True))

    engine.quit()

    outcome = board.outcome()

    if outcome.winner is None:
        print(f"Game result: Draw")
    else:
        winner = "MCTS AI" if outcome.winner == chess.WHITE else "Stockfish"
        print(f"Game result: {winner} wins")
        ply_count = board.ply()
        move_number = (ply_count + 1) // 2
        print(f"Move Count: {move_number}")

if __name__ == "__main__":
    # Replace the below path with Stockfish's path on your system to try this:
    engine_path = r"C:\Users\mpanaro\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"
    self_play(engine_path)