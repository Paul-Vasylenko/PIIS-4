import chess
from Node import Node
from math import log,sqrt,e,inf
import random

class GameEngine:
    def __init__(self, board: chess.Board):
        self.board = board

    def playHumanMove(self):
        print("Possible moves: ", self.board.legal_moves)
        play = input("Enter your move: ")
        
        self.board.push_san(play)

    def selection(self, node: Node, color):
        if(color == chess.WHITE):
            maxUCB = -inf
            selectedChild = None
            for child in node.children:
                currentUCB = self.ucb(child)
                if(currentUCB>maxUCB):
                    maxUCB = currentUCB
                    selectedChild = child
            return (selectedChild)
        if(color == chess.BLACK):
            minUCB = inf
            selectedChild = None
            for child in node.children:
                currentUCB = self.ucb(child)
                if(currentUCB<minUCB):
                    minUCB = currentUCB
                    selectedChild = child
            return (selectedChild)


    def expansion(self, node: Node):
        if (len(node.children) == 0):
            return node
        maxUCB = -inf
        selectedChild = None
        for child in node.children:
            currentUCB = self.ucb(child)
            if(currentUCB>maxUCB):
                maxUCB = currentUCB
                selectedChild = child
        return self.expansion(selectedChild)

    def rollout(self, node: Node):
        board = node.state
        if(board.is_game_over()):
            if(board.result()=='1-0'):
                return (1, node)
            if(board.result()=='0-1'):
                return (-1, node)
            return (0.5, node)
        
        possibleMoves = [ node.state.san(i) for i in list(node.state.legal_moves)]

        for i in possibleMoves:
            state = chess.Board(node.state.fen())
            state.push_san(i)
            child = Node()
            child.state = state
            child.parent = node
            node.children.add(child)
        
        randomState = random.choice(list(node.children))
        return self.rollout(randomState)

    def backpropogation(self, node: Node, reward):
        node.n+=1
        node.v += reward
        while(node.parent != None):
            node.N+=1
            node = node.parent
        return node
    

    def monteCarlo(self, currentNode: Node, isOver: bool, color: chess.Color, iteractions=50):
        if isOver:
            return -1
        possibleMoves = [ currentNode.state.san(i) for i in list(currentNode.state.legal_moves)]
        stateToMoves = dict()

        for move in possibleMoves:
            state = chess.Board(currentNode.state.fen())
            # make a move
            state.push_san(move)

            child = Node()
            child.state = state
            child.parent = currentNode
            currentNode.children.add(child)
            stateToMoves[child] = move

        while iteractions > 0:
            selectedNode = self.selection(currentNode, color)
            expansionResult = self.expansion(selectedNode)
            reward, state = self.rollout(expansionResult)
            currentNode = self.backpropogation(state, reward)

            iteractions-=1
        
        bestMove = ''
        if color == chess.WHITE:
            maxUCB = -inf
            for child in currentNode.children:
                ucb = self.ucb(child)
                if ucb > maxUCB:
                    maxUCB = ucb
                    bestMove = stateToMoves[child]
        else:
            minUCB = inf
            for child in currentNode.children:
                ucb = self.ucb(child)
                if(ucb < minUCB):
                    minUCB = ucb
                    bestMove = stateToMoves[child]
        return bestMove

    def playAIMove(self, color, isOver):
        node = Node(self.board)
        bestMove = self.monteCarlo(node, isOver, color)
            
        print('BEST MOVE', bestMove)
        self.board.push_san(bestMove)
        return

    def ucb(self, node: Node):
        return node.v+2*(sqrt(log(node.N+e+(10**-6))/(node.n+(10**-10))))

    def startGame(self):
        aiColor = chess.BLACK
        print("The game started!")
        print("You play WHITE!")

        turn = chess.WHITE

        while (not self.board.is_checkmate()):
            print(self.board)
            if turn == chess.WHITE:
                print('\n\nWhite move\n\n')
                self.playHumanMove()
                turn = chess.BLACK
                continue
            if turn == chess.BLACK:
                print('\n\nBlack move\n\n')
                self.playAIMove(-aiColor, self.board.is_checkmate())
                turn = chess.WHITE
                continue
        return

    

game = GameEngine(chess.Board())
game.startGame()
