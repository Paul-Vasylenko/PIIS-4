import chess

class Node():
    def __init__(self, board=chess.Board()):
        self.state = board #current posiiton on the board
        self.children = set() # Set of all possible states from legal action from current node
        self.parent = None # Parent node of current node
        self.v = 0 # Exploitation factor of current node(used in UCB)
        self.n = 0 # Number of times current node has been visited(used in UCB)
        self.N = 0 # Number of times parent node has been visited(used in UCB)