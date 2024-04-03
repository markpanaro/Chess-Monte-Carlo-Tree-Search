import random
import math
import chess

class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 1  # Initialize visits to 1 to avoid division by zero
        self.untried_moves = list(state.legal_moves)

    def uct_select_child(self):
        """Select a child node using UCT (Upper Confidence bounds applied to Trees)."""
        log_parent_visits = math.log(self.visits)
        # Avoid division by zero by ensuring child.visits is never zero
        return max(self.children, key=lambda child: child.wins / child.visits + math.sqrt(2 * log_parent_visits / child.visits))
        
    def add_child(self, move, state):
        """Add a new child node for the move."""
        child_node = Node(state=state, parent=self, move=move)
        self.untried_moves.remove(move)
        self.children.append(child_node)
        return child_node
    
    def update(self, result):
        """Update this node - one additional visit and an update to the win count."""
        self.visits += 1
        self.wins += result

def selection(node):
    """Select a node in the tree to expand."""
    while not node.state.is_game_over(claim_draw=True):
        if node.untried_moves:
            return expansion(node)
        else:
            node = node.uct_select_child()
    return node

def expansion(node):
    """Expand the chosen node by adding a new child."""
    move = random.choice(node.untried_moves)
    new_state = node.state.copy()
    new_state.push(move)
    return node.add_child(move, new_state)

def simulation(node):
    """Simulate a random game from the given node."""
    temp_state = node.state.copy()
    while not temp_state.is_game_over(claim_draw=True):
        temp_state.push(random.choice(list(temp_state.legal_moves)))
    result = game_result(temp_state)
    return result

def backpropagation(node, result):
    """Backpropagate the result of the simulation up the tree."""
    while node is not None:
        node.update(result)
        node = node.parent

def game_result(state):
    """Determine the game result from the perspective of the current player."""

    # Will need to replace with a better method of evaluation
    # Playing the game to completion is not practical or effective
    if state.is_checkmate():
        return 1  # Win
    elif state.is_game_over():
        return 0.5  
    else:
        return 0 

def mcts(root, iterations=10):
    for _ in range(iterations):
        leaf = selection(root)
        simulation_result = simulation(leaf)
        backpropagation(leaf, simulation_result)
    # Return the move of the best child based on the highest number of visits
    return max(root.children, key=lambda child: child.visits).move