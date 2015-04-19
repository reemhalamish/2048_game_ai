'''
Created on 18 april 2015

@author: Reem
'''
from miniboard import Miniboard
DEPTH = 2
manhattanDistance = lambda x1,y1,x2,y2 : abs(y2-y1) + abs(x2-x1)
class ExpectimaxAgent:
    '''
    The agent that solves the 2048 game
    '''
    
    def h1(self, board):
        ''' heuristic that returns the score '''
        return Miniboard.score_for_board(board)
    def h2(self, board):
        ''' try to store the higher numbers in corners '''
        tile0 = board[0][0] if board[0][0] else 0
        tile1 = board[0][3] if board[0][3] else 0
        tile2 = board[3][3] if board[3][3] else 0
        tile3 = board[3][0] if board[3][0] else 0
        return tile0 + tile1 + tile2 + tile3
    def h3(self, board):
        ''' try to store the big tiles close to each other, the further they are the bigger the punishment '''
        biggestTile, x, y = Miniboard.Max(board)
        board[x][y] = None
        secondBiggest, x2, y2 = Miniboard.Max(board)
        board[x][y] = biggestTile
        return - (biggestTile + secondBiggest) * (abs(y2 -y) + abs(x2 - x))
        
    def h4(self, board):
        ''' the further the maximum tile is from a corner - the harder the punishment is '''
        biggestTile, x, y = Miniboard.Max(board)
        x = min (x, 3-x) # x = 1 or x = 2 is the same distance from a corner
        y = min (y, 3-y)
        return - (biggestTile * (x+y))
    
    def h5(self, board):
        ''' sort the board, for every two tiles that match and can be merged give a bonus worth of one tile '''
        sorted_list = Miniboard.sort_board_by_highest_number(board)
        bonus = 0
        while sorted_list:
            cur, x, y = sorted_list.pop(0)
            if cur == None: continue
            for item, i, j in sorted_list:
                if item > cur: break
                # else - we are assured that they are the same
                if (x == i and abs(y-j) == 1) or (y == j and abs(x-i) == 1): # if can be mergeds
                    bonus += cur
        return bonus
    
    def h6(self, board):
        ''' try to find "snakes" (i.e. [32,16,8,4,2] ) from the largest tile.
        returning: 2*biggest if a complete snake, //2 for every missing part '''
        return 0
    # TODO continue...
        biggest, x, y = Miniboard.Max(board)
        bonus = 2
        while True:# biggest has neighbours close to x,y
            pass
        
    def h7(self, board):
        ''' gain some bonus for every None point '''
        bonus = Miniboard.Max(board)[0] / 16
        bonusTimes = 0
        for tile in Miniboard.generator(board):
            if tile[0] == None:
                bonusTimes += 1
        return bonus * bonusTimes
        
    def h8(self,board):
        ''' the bigger the tile is, and the closer it is to the biggest dot, the smaller the punishment is '''
        biggest, bx,by = Miniboard.Max(board)
        retval = 0
        for tile, x, y in Miniboard.generator(board):
            if tile == None: tile = 0
            retval -= tile * manhattanDistance(bx,by,x,y)
        return retval
            




    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def getAction(self, boardWithTiles):
        boardWithInt = Miniboard.convertBoardWithTiles(boardWithTiles)
        action, score = self.expectimax(boardWithInt, DEPTH, myTurn = True)
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
        ''' board is None when there is a game over '''
        if board == None:
            return float("-inf")
        return \
        self.h4(board) + \
        self.h8(board)
#         self.h1(board) + \
#         self.h2(board) + \
#         self.h3(board) + \
        

#         self.h5(board) + \
#         self.h6(board) + \
#         self.h7(board) + \
#     + ... + ... TODO: ...