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
                    
                    if platform.system() == "Windows":
                        os.system('cls')
                    else:
                        # Assuming the OS is Unix/Linux/MacOS
                        os.system('clear')

                    print("Current board state:\n", board.unicode(invert_color=True, borders=True))
                else:
                    print("That is not a legal move. Please try again.")
            except ValueError:
                print("Invalid move format. Please use UCI format (e.g., 'e2e4').")
        
        else:
            #ai_move = random.choice(list(board.legal_moves))
            #board.push(ai_move)


            root = Node(state=board.copy())
            ai_move = mcts(root, iterations=100)   #.state
            board.push(ai_move)


            if platform.system() == "Windows":
                os.system('cls')
            else:
                # Assuming the OS is Unix/Linux/MacOS
                os.system('clear')
            print(f"AI move: {ai_move}")
            print("Current board state:\n", board.unicode(invert_color=True, borders=True))

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

def main():
    while True:
        play_game()  # Play a single game.

        # Ask if the players want to play again.
        again = input("Do you want to play another game? (y/n): ").lower()
        if again != 'y':
            print("Thank you for playing!")
            break  # Exit the loop if the answer is not 'yes'.

        if platform.system() == "Windows":
            os.system('cls')
        else:
            # Assuming the OS is Unix/Linux/MacOS
            os.system('clear')

if __name__ == "__main__":
    main()