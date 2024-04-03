import random
import chess
import chess.svg
from mcts import mcts, Node
import os
import sys
import platform

def play_game():
    board = chess.Board()

    print("Please enter moves using UCI format (e.g., 'e2e4').\n")

    # Display the board in the console
    print("Current board state:\n", board.unicode(invert_color=True, borders=True))

    while not board.is_game_over(claim_draw=True):     
        #"""
        root_player_color = chess.WHITE if board.turn else chess.BLACK
        root = Node(state=board.copy(), player_color=root_player_color)
        ai_move = mcts(root, iterations=100)   #.state
        board.push(ai_move)

        clear_terminal()

        print(f"AI move: {ai_move}")
        print("Current board state:\n", board.unicode(invert_color=True, borders=True))

        """
        if board.turn == chess.WHITE:   
            # Get the current player's move
            move = input("Enter your move (or 'q' to quit): ")
            if move == 'q':
                print("Game has been quit.")
                sys.exit()

            # Try to make the move
            try:
                chess_move = chess.Move.from_uci(move)
                if chess_move in board.legal_moves:
                    board.push(chess_move)
                    
                    clear_terminal()

                    print("Current board state:\n", board.unicode(invert_color=True, borders=True))
                else:
                    print("That is not a legal move. Please try again.")
            except ValueError:
                print("Invalid move format. Please use UCI format (e.g., 'e2e4').")
        
        else:
            root_player_color = chess.WHITE if board.turn else chess.BLACK
            root = Node(state=board.copy(), player_color=root_player_color)
            #root = Node(state=board.copy())
            ai_move = mcts(root, iterations=100) 
            board.push(ai_move)

            clear_terminal()

            print(f"AI move: {ai_move}")
            print("Current board state:\n", board.unicode(invert_color=True, borders=True))
        """
            

    # The game is over; print the result
    print("Game over")
    result = None
    if board.is_checkmate():
        winning_color = "Black" if board.turn else "White"
        result = "Checkmate. " + winning_color + " wins."
    elif board.is_stalemate():
        result = "Stalemate"
    elif board.is_insufficient_material():
        result = "Draw due to insufficient material"
    elif board.can_claim_draw():
        result = "Draw claimed"
    print(f"Result: {result}")

    ply_count = board.ply()
    move_number = (ply_count + 1) // 2
    print(f"Move Count: {move_number}")

def clear_terminal():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        # Assuming the OS is Unix/Linux/MacOS
        os.system('clear')

def main():
    while True:
        play_game()  # Play a single game.

        # Ask if the players want to play again.
        again = input("Do you want to play another game? (y/n): ").lower()
        if again != 'y':
            print("Thank you for playing!")
            break  # Exit the loop if the answer is not 'yes'.

        clear_terminal()

if __name__ == "__main__":
    main()