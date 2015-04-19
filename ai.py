'''
Created on 18 april 2015

@author: Reem
'''
from miniboard import Miniboard, tileIsInBoundaries
from time import time
from game import BOUNDARYS
from random import random
from turtledemo.forest import randomize
DEPTH = 2
manhattanDistance = lambda x1,y1,x2,y2 : abs(y2-y1) + abs(x2-x1)
spreadXY = lambda x,y : [(x-1,y), (x+1, y), (x,y-1), (x,y+1)]
STOP_BEFORE_COMPUTER_BURNS_FAT = 7
'''
TODO: priorities:
   h1 - ORANGE
   h2 - ORANGE
   h3 - ORANGE
   h4 - RED
   h6 - RED
   h8 - GREEN
   h9 - ORANGE
   h10 - RED
   h12 - ORANGE
   h13 - RED
   h14 - ORANGE
'''
NORMALIZE_1 = lambda x : x//2
NORMALIZE_2 = 8
NORMALIZE_3 = 1
NORMALIZE_4 = 8
NORMALIZE_6 = 8
NORMALIZE_8 = lambda x : x//4
NORMALIZE_9 = 1
NORMALIZE_10 = 32
NORMALIZE_12 = lambda x : x//4
NORMALIZE_13 = lambda x : x//2
NORMALIZE_14 = lambda x : x//2

class ExpectimaxAgent:
    '''
    The agent that solves the 2048 game
    '''
    
    def h1(self, board):
        ''' heuristic that returns the score '''
        return NORMALIZE_1(Miniboard.score_for_board(board))
    def h2(self, board):
        ''' try to store the higher numbers in corners '''
        tile0 = board[0][0]
        tile1 = board[0][3]
        tile2 = board[3][3]
        tile3 = board[3][0]
        return max(tile0, tile1, tile2, tile3) * NORMALIZE_2
    def h3(self, board):
        ''' try to store the big tiles close to each other, the further they are the bigger the punishment '''
        biggestTile, x, y = Miniboard.Max(board)
        board[x][y] = 0
        secondBiggest, x2, y2 = Miniboard.Max(board)
        board[x][y] = biggestTile
        return - (biggestTile + secondBiggest) * manhattanDistance(x,y,x2,y2) * NORMALIZE_3
    def h4(self, board):
        ''' the further the maximum tile is from a corner - the harder the punishment is '''
        biggestTile, x, y = Miniboard.Max(board)
        x = min (x, 3-x) # x = 1 or x = 2 is the same distance from a corner
        y = min (y, 3-y)
        return - (biggestTile * (x+y)) * NORMALIZE_4
    def h5(self, board):
        ''' sort the board, for every two tiles that match and can be merged give a bonus worth of one tile '''
        ''' try it different way: instead of sorting, just go tile by tile to search for friends '''
        bonus = 0
        for x in range(3):
            for y in range(3):
                cur = board[x][y]
                nextX = board[x+1][y]
                nextY = board[x][y+1]
                if cur == nextX: bonus += cur
                if cur == nextY: bonus += cur
        # run on 3x3 board, need to check board[3] and board[*][3]
        for i in range(3):
            cur = board[3][i]
            neighbour = board[4][i]
            if cur == neighbour: bonus += cur
            
            cur = board[i][3]
            neighbour = board[i][4]
            if cur == neighbour: bonus += cur
            
        return bonus
    def h6(self, board):
        ''' try to find "snakes" (i.e. [32,16,8,4,2] ) from the largest tile.
        returning: 2*biggest if a complete snake, //2 for every missing part '''
        biggest, x, y = Miniboard.Max(board)
        bonus = 0
        somethingNewHappend = True
        while somethingNewHappend:# biggest has good neighbours close to x,y
            somethingNewHappend = False
            for newX, newY in spreadXY(x,y):
                if not tileIsInBoundaries(newX, newY): continue
                if board[newX][newY] == (biggest // 2):
                    bonus += biggest
                    biggest = biggest // 2
                    x,y = newX, newY
                    somethingNewHappend = True
                    break
        return bonus * NORMALIZE_6
    def h7(self, board):
        ''' gain some bonus for every Zero point '''
        bonus = Miniboard.Max(board)[0] / 16
        bonusTimes = 0
        for tile in Miniboard.generator(board):
            if tile[0] == 0:
                bonusTimes += 1
        return bonus * bonusTimes
    def h8(self,board):
        ''' go throuhgh the dots and punish them
        based on how big they are and how far are they from the biggest dot '''
        bx,by = Miniboard.Max(board)[1:]
        retval = 0
        for tile, x, y in Miniboard.generator(board):
            retval -= tile * manhattanDistance(bx,by,x,y)
        return NORMALIZE_8(retval)
    def h9(self, board):
        ''' go throuhgh the dots and punish them
        based on how big they are and how far are they from the corners '''
        punish = 0
        for tile, x, y in Miniboard.generator(board):
            x = min(x, 3-x)
            y = min(y, 3-y)
            punish += tile * manhattanDistance(0,0,x,y)
        return punish * NORMALIZE_9
    def h10(self, board):
        ''' heavier blocks should be in the sides - return the heaviness of the blocks in the boundaries '''
        bonus = 0
        for line in BOUNDARYS:
            xy0,xy1,xy2,xy3 = line
            t0,t1,t2,t3 = board[xy0[0]][xy0[1]],board[xy1[0]][xy1[1]],board[xy2[0]][xy2[1]],board[xy3[0]][xy3[1]],
            sumLine = t0+t1+t2+t3
            
            # if the line is ordinared - double the bonus!
            if (t0 >= t1 and t1 >= t2 and t2 >= t3) or (t0 <= t1 and t1 <= t2 and t2 <= t3):
                sumLine *= 2
            bonus = max(bonus, sumLine)
        return bonus * NORMALIZE_10

        
    def h11(self, board):
        ''' arrange the tiles on the heavy line '''
        bonus = 0
        for line in BOUNDARYS:
            xy0,xy1,xy2,xy3 = line
            t0,t1,t2,t3 = board[xy0[0]][xy0[1]],board[xy1[0]][xy1[1]],board[xy2[0]][xy2[1]],board[xy3[0]][xy3[1]],
            if (t0 >= t1 and t1 >= t2 and t2 >= t3) or (t0 <= t1 and t1 <= t2 and t2 <= t3):
                sumLine = t0+t1+t2+t3
                bonus = max(sumLine, bonus)
        return bonus 
            
    def h12(self, board):
        ''' arrange the tiles on all the board - [64,32,4,0] will get more then [64,32,0,4] '''
        sumLines = 0
        sumTurs = 0
        for line in board:
            sumLine = 0 # sum of the line - straghit and opposite
            t0,t1,t2,t3 = line
            if t0>= t1:
                sumLine = t0 + t1
                if t1 >= t2:
                    sumLine += t2
                    if t2 >= t3:
                        sumLine += + t3
#                         print("line is arranged!", line)
            elif t3 >= t2:
            # the first is smaller then the second - try the other side! (i.e. --> [4,8,15,256] )
                sumLine = t3 + t2
                if t2 >= t1:
                    sumLine += t1
                    if t1 >= t0:
                        sumLine += t0
#                         print("line is arranged!", line)
            sumLines += sumLine
        for tur in zip(board[0], board[1], board[2], board[3]):
            t0,t1,t2,t3 = tur
            sumTur = 0
            if t0>= t1:
                sumTur = t0 + t1
                if t1 >= t2:
                    sumTur += t2
                    if t2 >= t3:
                        sumTur += t3
#                         print("Tur is arranged! ", line)
            elif t3 >= t2:
            # the first is smaller then the second - try the other side! (i.e. --> [4,8,15,256] )
                sumTur = t3 + t2
                if t2 >= t1:
                    sumTur += t1
                    if t1 >= t0:
                        sumTur += t0
#                         print("Tur is arranged! ", line)
            sumTurs += sumTur
            return NORMALIZE_12(sumLines + sumTurs)
        
    def h13(self, board):
        ''' very close like h12, this function checks for monotonicity.
        only this heuristic checks monotonicity on the WHOLE SCREEN '''
        turs = zip(board[0], board[1], board[2], board[3])
        reversedTurs = zip(reversed(board[0]), reversed(board[1]), reversed(board[2]), reversed(board[3]))
        lines = board
        reversedLines = reversed(board)
        bonus = [0,0,0,0] # bonus for each of the 4. at the end will choose the best from turs\reversed and lines\reversed
        for bonusSpot, tiles_feeder in zip(range(4), (turs, reversedTurs, lines, reversedLines)):
            sumForBonus = 0
            for line in tiles_feeder:
                t0,t1,t2,t3 = line
                if t0>= t1:
                    sumForBonus = t0 + t1
                    if t1 >= t2:
                        sumForBonus += t2
                        if t2 >= t3:
                            sumForBonus += t3
            bonus[bonusSpot] = sumForBonus
            
        linesBonus = max(bonus[0:2])
        tursBonus = max(bonus[2:4])
        return NORMALIZE_13(linesBonus + tursBonus)
            
            
    def h14(self, board):
        ''' this heuristic is manDistance between same tiles. supposed to figure out things like this:
                consider something like that:
        [1024, 512, 256, 4]
        [256,  4,   2,   4]
        [.................]
        [.................]
        
        '''
        if Miniboard.Max(board)[0] < 128:
            return NORMALIZE_14(-1500) 
        punish = 0
        foundPunish = False
        boardSorted = Miniboard.sort_board_by_highest_number(board)
        for index in range(STOP_BEFORE_COMPUTER_BURNS_FAT):
            if not boardSorted: break
            tile, x, y = boardSorted.pop(0)
            if tile < 64: break
            for nextTile, nx, ny in boardSorted:
                if nextTile < tile: break
                punish -= manhattanDistance(x,y,nx,ny) *(65536 // tile)
        if foundPunish: return NORMALIZE_14(punish)
        else: return NORMALIZE_14(-1500)
            




    def __init__(self):
        '''
        Constructor
        '''
        self.timesForHeuristics = {h : 0 for h in ExpectimaxAgent.heuristicsInUse}
        self.pointsForHeuristics = {h : 0 for h in ExpectimaxAgent.heuristicsInUse}
        self.biggestTile = 8
    
    def getAction(self, boardWithTiles):
        boardWithInt = Miniboard.convertBoardWithTiles(boardWithTiles)
#         emptyTiles = Miniboard.countEmptyTiles(boardWithInt)
#         if emptyTiles > 7:
#             action, score = self.expectimax(boardWithInt, 1, myTurn = True)
        action, score = self.expectimax(boardWithInt, DEPTH, myTurn = True)
        if self.biggestTile == Miniboard.Max(boardWithInt)[0]:
            self.biggestTile *= 2
            self.timesForHeuristics = {h : 0 for h in ExpectimaxAgent.heuristicsInUse}
            self.pointsForHeuristics = {h : 0 for h in ExpectimaxAgent.heuristicsInUse}
        
            
        if score == float("-inf"):
            self.debug_heuristics(boardWithInt)
            print("************")
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
        
        retval = 0
        for h in ExpectimaxAgent.heuristicsInUse:
            start = time()
            score = h(self, board)
            retval += score
            end = time()
            self.timesForHeuristics[h] += (end-start)
            self.pointsForHeuristics[h] += score
            
        return retval

    def debug_heuristics(self, board):
        score = self.pointsForHeuristics
        time = self.timesForHeuristics
        print("biggest tile in the board:", self.biggestTile)
        for h in ExpectimaxAgent.heuristicsInUse:
            print("score:", abs(score[h]),"time:", time[h], "name:", h)


    heuristicsInUse = (h1, h2, h3, h4, h10, h12, h13)
    normalizeHeuristics = {}
