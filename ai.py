'''
Created on 18 april 2015

@author: Reem
'''
from miniboard import Miniboard
DEPTH = 2
class ExpectimaxAgent:
    '''
    The agent that solves the 2048 game
    '''
    
    def h1(self, board):
        ''' heuristic that returns the score '''
        return Miniboard.score_for_board(board)

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def getAction(self, boardWithTiles):
        boardWithInt = Miniboard.convertBoardWithTiles(boardWithTiles)
        action, score = self.expectimax(boardWithInt, DEPTH, myTurn = True)
        print("score supposed:", score)
        return action
    
    def expectimax(self, board, depth, myTurn = False):
        if board == None or depth == 0:
            return (None, self.combine_heuristics(board)) # returns tuple, all the time
        if myTurn:
#             Return value of maximum-valued child node
            alpha = float("-inf")
            returnedAction = None
            for action, nextState in Miniboard.getNextStatesOfMyTurn(board):
                value = self.expectimax(nextState, depth, myTurn=False)
                if value >= alpha:
                    returnedAction = action
                    alpha = value
            return returnedAction, alpha
        else: # now random supposed to be
#         so Return weighted average of all child nodes' values
            alpha = 0
            for prob, newBoard in Miniboard.getNextStatesForRandomPlacements(board):
                alpha += prob * self.expectimax(newBoard, depth-1, myTurn=True)[1] # need only the value
            return alpha

    def combine_heuristics(self, board):
        if board == None:
            return float("-inf")
        return self.h1(board) # + ... + ... TODO