'''
Created on 23 april 2015

@author: Reem
'''
from miniboard import Miniboard
from ai import DEPTH, ExpectimaxAgent
from game import weighted_choice, Directions, PriorityQueue, GAME_OVER_VALUE_FOR_HEURISTICS
from random import choice as choose_uni_from_seq

heuristicsAll = ExpectimaxAgent.heuristicsInUse
WEIGHT_VALUE_FOR_HEURISTIC_MINIMUM = 1
WEIGHT_VALUE_FOR_HEURISTIC_START = 128
TIMES_TO_RUN_EVERY_GAME = 3
SCORE_FOR_4096 = 45056
class QuietRunner():
    '''
    A member of this class can run 2048 games quietly (without GUI)
    '''


    def __init__(self, heuristics = [], weights = {}):
        '''
        Constructor. gets the heuristics and runs the game
        '''
        for h in heuristics:
            if not h in weights:
                weights[h] = WEIGHT_VALUE_FOR_HEURISTIC_START
        self.board = [[0 for i in range(4)] for j in range(4)]
        self.heuristics = heuristics
        self.weights = weights
        while True:
            success = self.nextTurn()
            if not success:
                break
        # game over
        
    def nextTurn(self):
        if not self.putRandomTile(): # returns None on failure or the board on success
            return 0
        direction = self.calculateBestNextMove()
        self.board = self.move(direction)
        return 1
    
    def putRandomTile(self, board = None):
        if not board: board = self.board
        emptySlots = [(x,y) for x in range(4) for y in range(4) if board[x][y] == 0]
        if len(emptySlots) == 0:
            return None
        numberToPutInSlot = weighted_choice()
        x,y = choose_uni_from_seq(emptySlots)
        board[x][y] = numberToPutInSlot
        return board
    
    ''' update the board '''
    def move(self, direction, board = None):
        if board == None:
            board = self.board
        return Miniboard.calculateNextBoardUsing(direction, board)
        
    
    ''' find the best move '''
    def calculateBestNextMove(self):
        action = self.expectimax(self.board, myTurn = True)[0]
        return action
    
    ''' copied from the ai module '''
    def expectimax(self, board, depth = DEPTH, myTurn = False):
        if board == None or depth == 0:
            return (None, self.combine_heuristics(board)) # returns tuple, all the time
        if myTurn:
#             Return value of maximum-valued child node
            alpha = float("-inf")
            returnedAction = None
            for action, nextState in Miniboard.getNextStatesOfMyTurn(board):
                value = self.expectimax(nextState, depth - 1, myTurn=False)[1]
                if value >= alpha:
                    returnedAction = action
                    alpha = value
            return returnedAction, alpha
        else: # now random supposed to be
#         so Return weighted average of all child nodes' values
            alpha = 0
            for prob, newBoard in Miniboard.getNextStatesForRandomPlacements(board):
                action, tempValue = self.expectimax(newBoard, depth-1, myTurn=True) # need only the value
                alpha  += prob * tempValue
            return (None, alpha)

    def combine_heuristics(self, board):
        ''' board is None when there is a game over '''
        if board == None:
            return GAME_OVER_VALUE_FOR_HEURISTICS
        
        retval = 0
        for h in self.heuristics:
            score = h(self, board) * self.weights[h]
            retval += score
            
        return retval    

    ''' getters '''
    def getLastBoard(self): return self.board
    def getScore(self): return Miniboard.score_for_board(self.board)
    def getHighestTile(self): return Miniboard.Max(self.board)[0]
    
class Node():
    def __eq__(self, other): return self.score == other.score
    def __lt__(self, other): return self.score < other.score
    def __le__(self, other): return self < other or self == other
    def __gt__(self, other): return other < self
    def __ge__(self, other): return self > other or self == other
    def __int__(self): return self.score
    
    def __init__(self, heuristics = set(), weights = dict()):
        for h in heuristics:
            if not h in weights:
                weights[h] = WEIGHT_VALUE_FOR_HEURISTIC_START
        self.heuristics = heuristics
        self.weights = weights
        self.runGame()
    def runGame(self):
        print("best tiles:", end = ' ')
        score = 0
        highestTile = 0
        for i in range(TIMES_TO_RUN_EVERY_GAME):
            runner = QuietRunner(self.heuristics, self.weights)
            score += runner.getScore()
            highestTile = max(highestTile, runner.getHighestTile())
            print(runner.getHighestTile(), end = ",")
        print()
        self.score = score // TIMES_TO_RUN_EVERY_GAME
        self.hughestTile = highestTile
        
    
    def getNextNodes(self):
#         for h in heuristicsAll:
#             if not h in self.heuristics:
#                 yield self.newNodeAppendheuristc(h)
#             else:
#                 yield self.newNodeMaximizeHeuristic(h)
#                 yield self.newNodeMinimizeHeuristic(h)
                # TODO: should i put all of them? or maybe just start with everyone and dont use newNodeAppendHeuristc()
        for h in self.heuristics:
            yield self.newNodeMinimizeHeuristic(h)
    def newNodeAppendheuristc(self, h):
        return Node(self.heuristics + [h], self.weights)
    def newNodeMaximizeHeuristic(self, h):
        newWeights = {v : k for v,k in self.weights.items()}
        newWeights[h] += self.weights[h]
        return Node(self.heuristics, newWeights)
    def newNodeMinimizeHeuristic(self, h):
        newWeights = {v : k for v,k in self.weights.items()}
        heuristics = {h for h in self.heuristics}
        temp = newWeights[h]
        temp //= 2
        if (temp < WEIGHT_VALUE_FOR_HEURISTIC_MINIMUM):
            newWeights.pop(h)
            heuristics.discard(h)
        else:
            newWeights[h] = temp
        return Node(heuristics, newWeights)
    ''' return this state - what specializes this node '''
    def getImportantInfoForVisited(self):
        heuristics, w = self.heuristics, self.weights
        return (frozenset([
                       (h,w[h]) for h in heuristics
                       ]))
    def printInfo(self):
        print("score:", self.score,". best tile:", self.hughestTile,"heuristics:", end = '')
        for h in self.heuristics:
            print(ExpectimaxAgent.heuristicsNames[h]+"("+str(self.weights[h])+")",end = ', ')
        print()
            
        
def test_runner():
    runner = QuietRunner(heuristicsAll, {})
    Miniboard.debug_board(runner.getLastBoard())
    print("best tile:", runner.getHighestTile())
    print("score: ",runner.getScore())
    
    runner = QuietRunner([], {})
    Miniboard.debug_board(runner.getLastBoard())
    print("best tile:", runner.getHighestTile())
    print("score: ",runner.getScore())
def test_node():
    goodHeuristics = [#h1, h7, h11, h12
                  ExpectimaxAgent.h1,
                  ExpectimaxAgent.h7,
                  ExpectimaxAgent.h11,
                  ExpectimaxAgent.h12,
                  ]
    a = Node(goodHeuristics)
    b = Node([])
    print(a > b)

def first_node(): return Node(set(heuristicsAll[0:4])) #TODO: remove the [0:4], update the rellevan heuristics based on the results from data_handler 
"Search the node that has the lowest combined cost and heuristic first."
def aStarSearch():
    fringe = PriorityQueue()
    start = first_node()
    fringe.push(start, 0)
    visited = set()
    
    while not fringe.isEmpty():
        cur_node = fringe.pop()
        cur_visited = cur_node.getImportantInfoForVisited()
        cur_node.printInfo()
        if cur_visited in visited:
            print("already visited - ", cur_visited)
            continue
        visited.add(cur_visited)
        
        if int(cur_node) >= SCORE_FOR_4096: # means it scored more then 4096 on the AVERAGE score - this is good!
            return cur_node
        for nextNode in cur_node.getNextNodes():
            if not nextNode.getImportantInfoForVisited() in visited:
                fringe.push(nextNode, -int(nextNode))
    
    # haven't reach anything?
    return None
if __name__ == '__main__':
#     test_runner()
#     test_node()
    solution = aStarSearch()
    if solution:
        f = open("A*.log", 'a')
        f.write("score: " + solution.score + ". best tile: " + solution.highestTile + "heuristics:")
        for h in solution.heuristics:
            f.write(ExpectimaxAgent.heuristicsNames[h]+"("+str(solution.weights[h])+"), ")
        f.write("\n")
        

# TODO: run A* on the nodes