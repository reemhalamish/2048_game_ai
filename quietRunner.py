'''
Created on 23 april 2015

@author: Reem
'''
from miniboard import Miniboard
from ai import DEPTH, ExpectimaxAgent
from game import weighted_choice, Directions, PriorityQueue, GAME_OVER_VALUE_FOR_HEURISTICS
from random import choice as choose_uni_from_seq

heuristicsAll = ExpectimaxAgent.heuristicsInUse
WEIGHT_VALUE_FOR_HEURISTIC_MINIMUM = 0
WEIGHT_VALUE_FOR_HEURISTIC_START = 45
TIMES_TO_RUN_EVERY_GAME = 7
BoardWith2048 = [[2048,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
BoardWith4096 = [[4096,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
SCORE_FOR_WINNING = (Miniboard.score_for_board(BoardWith4096))
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
    
    def __init__(self, heuristics = set(), weights = dict(), computedScore = None):
        for h in heuristics:
            if not h in weights:
                weights[h] = WEIGHT_VALUE_FOR_HEURISTIC_START
        self.heuristics = heuristics
        self.weights = weights
        if computedScore:
            self.score = computedScore
        else:
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
        self.highestTile = highestTile
        
    
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
    
    def getNextNodesVer2(self):
        for h in self.heuristics:
            yield self.newNodeMinimizeHeuristicBy10(h)
            yield self.newNodeMaximizeHeuristicBy10(h)

    def newNodeMaximizeHeuristicBy10(self, h):
        newWeights = {v : k for v,k in self.weights.items()}
        newWeights[h] += 10
        return Node(self.heuristics, newWeights)
    def newNodeMinimizeHeuristicBy10(self, h):
        newWeights = {v : k for v,k in self.weights.items()}
        heuristics = {h for h in self.heuristics}
        temp = newWeights[h]
        temp -= 10
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
        print("score:", self.score,". best tile:", self.highestTile,"heuristics:", end = '')
        for h in self.heuristics:
            print(ExpectimaxAgent.heuristicsNames[h]+"("+str(self.weights[h])+")",end = ', ')
        print()
        f = open("A_star_heuristics.log", "a")
        f.write("score:"+ str(self.score)+". best tile:"+ str(self.highestTile)+"heuristics:")
        for h in self.heuristics:
            f.write(ExpectimaxAgent.heuristicsNames[h]+"("+str(self.weights[h])+"), ")
        f.write('\n')
        f.close()
            
        
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

''' can yield the nodes one at a time '''
def first_nodes(): 
    WEIGHTS_FOR_ALL_THE_GOOD_HEURISTICS = 32
    
    WEIGHTS_FOR_4096        = 64
    WEIGHTS_FOR_2048_GOOD   = 128
    WEIGHTS_FOR_2048_ALL    = 32
    WEIGHTS_FOR_1024        = 32
    WEIGHTS_FOR_ALL         = 8
    
    
    h4096 = ExpectimaxAgent.heuristicsWon4096
    weights4096 = {h : WEIGHTS_FOR_4096 for h in h4096}
    #yield Node(h4096, weights4096)
    
    h2048 = ExpectimaxAgent.heuristicsWon2048
    weights2048 = {h : WEIGHTS_FOR_2048_GOOD for h in h2048}
    #yield Node(h2048, weights2048)
    
    h2048all = ExpectimaxAgent.heuristicOK2048
    weights2048all = {h : WEIGHTS_FOR_2048_ALL for h in h2048all}
    #yield Node(h2048all, weights2048all)
    
    h1024 = ExpectimaxAgent.heuristicsWon1024
    weights1024 = {h : WEIGHTS_FOR_1024 for h in h1024}
    #yield Node(h1024, weights1024)
    
    hAll = ExpectimaxAgent.heuristicsInUse
    weightsAll = {h : WEIGHTS_FOR_ALL for h in hAll}
    #yield Node(hAll, weightsAll)
    
    hAllRelevant = set()
    for h in h4096:
        hAllRelevant.add(h)
    for h in h2048:
        hAllRelevant.add(h)
    for h in h2048all:
        hAllRelevant.add(h)
    weightsAllRelevant = {h : WEIGHTS_FOR_ALL_THE_GOOD_HEURISTICS for h in hAllRelevant}
    #yield Node(hAllRelevant, weightsAllRelevant)
    
    yield Node(ExpectimaxAgent.curHeuToCheck, ExpectimaxAgent.curHeuWeights)
    
    
     
"Search the node that has the lowest combined cost and heuristic first."
def aStarSearch():
    fringe = PriorityQueue()
    start = first_nodes()
    for node in start:
        fringe.push(node, -int(node))
    visited = set()
    
    while not fringe.isEmpty():
        cur_node = fringe.pop()
        cur_visited = cur_node.getImportantInfoForVisited()
        cur_node.printInfo()
        if cur_visited in visited:
            print("already visited - ",end = "")
            print("score:", cur_node.score,". best tile:", cur_node.highestTile,"heuristics:", end = '')
            for h in cur_node.heuristics:
                print(ExpectimaxAgent.heuristicsNames[h]+"("+str(cur_node.weights[h])+")",end = ', ')
            print()
            continue
        visited.add(cur_visited)
        
        if int(cur_node) >= SCORE_FOR_WINNING: # means it scored more then 4096 on the AVERAGE score - this is good!
            return cur_node
        for nextNode in cur_node.getNextNodesVer2():
            if not nextNode.getImportantInfoForVisited() in visited:
                fringe.push(nextNode, -int(nextNode))
    
    # haven't reach anything?
    return None
if __name__ == '__main__':
#     test_runner()
#     test_node()
    solution = aStarSearch()
    if solution:
        f = open("A_star_heuristics.log", 'a')
        f.write("\n\n found a solution!")
        f.write("score: " + str(solution.score) + ". best tile: " + str(solution.highestTile) + "heuristics:")
        for h in solution.heuristics:
            f.write(ExpectimaxAgent.heuristicsNames[h]+"("+str(solution.weights[h])+"), ")
        f.write("\n")
        f.close()
        

# TODO: run A* on the nodes