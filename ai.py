'''
Created on 18 april 2015

@author: Reem
'''
from miniboard import Miniboard, tileIsInBoundaries
from time import time
from game import BOUNDARYS, flipping30
from random import random
from turtledemo.forest import randomize
DEPTH = 4
PATTERN_FOR_SNAKE = ((0,1,2,3,3,2,1,0,0,1,2,3,3,2,1,0), (0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3))
manhattanDistance = lambda x1,y1,x2,y2 : abs(y2-y1) + abs(x2-x1)
spreadXY = lambda x,y : [(x-1,y), (x+1, y), (x,y-1), (x,y+1)]
STOP_BEFORE_COMPUTER_BURNS_FAT = 7

NORMALIZE_1 = lambda x : x//2
NORMALIZE_2 = 8
NORMALIZE_3 = 1
NORMALIZE_4 = 8
NORMALIZE_5 = 8
NORMALIZE_6 = 32
NORMALIZE_8 = lambda x : x//4
NORMALIZE_9 = 1
NORMALIZE_10 = 32
NORMALIZE_11 = 8
NORMALIZE_12 = lambda x : x//4
NORMALIZE_13 = lambda x : x//2
NORMALIZE_14 = lambda x : x//2
NORMALIZE_15 = 3
NORMALIZE_18 = lambda x : x//2
NORMALIZE_20 = lambda x : 2 * x
NORMALIZE_21 = lambda x : x



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
            neighbour = board[3][i]
            if cur == neighbour: bonus += cur
            
            cur = board[i][3]
            neighbour = board[i][3]
            if cur == neighbour: bonus += cur
            
        return bonus * NORMALIZE_5
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
        return bonus * NORMALIZE_11
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
            elif t3 >= t2:
            # the first is smaller then the second - try the other side! (i.e. --> [4,8,15,256] )
                sumLine = t3 + t2
                if t2 >= t1:
                    sumLine += t1
                    if t1 >= t0:
                        sumLine += t0
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
            elif t3 >= t2:
            # the first is smaller then the second - try the other side! (i.e. --> [4,8,15,256] )
                sumTur = t3 + t2
                if t2 >= t1:
                    sumTur += t1
                    if t1 >= t0:
                        sumTur += t0
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
            
    def h15(self, board):
        ''' stop things like [0, 64, 32, 8] '''
        punish = 0
        turs = zip(board[0], board[1], board[2], board[3])
        reversedTurs = zip(reversed(board[0]), reversed(board[1]), reversed(board[2]), reversed(board[3]))
        lines = board
        reversedLines = reversed(board)
        for changed_board in (turs, reversedTurs, lines, reversedLines):
            for tiles_feeder in changed_board:
                t0,t1,t2 = tiles_feeder[0:3]
                if t1 > t2 and t1 > t0:
                    punish -= t1
        return punish * NORMALIZE_15
            
    def h16(self, board):
        ''' 
        monotonicity on the whole screen.
        for each dot, see how far is it from (0,0)
        '''
        x,y, punish = 0,0,0
        for tile, xt,yt in Miniboard.generator(board):
            punish -= tile * manhattanDistance(x,y,xt,yt)
        return punish
    def h17(self, board, runnningMazeX = None, runnningMazeY = None):
        ''' hard-coded snakes beginnig from (0,0) '''
        if not runnningMazeX: runnningMazeX = PATTERN_FOR_SNAKE[0]
        if not runnningMazeY: runnningMazeY = PATTERN_FOR_SNAKE[1]
        tile = biggest = Miniboard.Max(board)[0]
        bonusX, bonusY = 0, 0
        worth = 2 ** 16
        # x way
        for x, y in zip(runnningMazeX, runnningMazeY):
            board[x][y] = tile
            bonusX += (tile * worth)
            worth //= 2
            
        # y way
        tile = biggest
        worth = 2 ** 16
        for y,x in zip(runnningMazeX, runnningMazeY):
            board[x][y] = tile
            bonusY += tile * worth
            worth //= 2
        
        return max(bonusX, bonusY)
    
    def h18(self,board):
        ''' snakes from whetever corner! '''
        bonus = []
        snake = ExpectimaxAgent.h17
        x, y = PATTERN_FOR_SNAKE
        bonus.append(snake(self,board, x, y))
        bonus.append(snake(self,board, flipping30(x), y))
        bonus.append(snake(self,board, x, flipping30(y)))
        bonus.append(snake(self,board, flipping30(x), flipping30(y)))
        return NORMALIZE_18(max(bonus))
    
    def h18a(self,board):
        ''' snakes from the best corner! '''
        NORMALIZE = 2
        tile, xt, yt = Miniboard.Max(board)
        if xt in (1,2) or yt in (1,2):
            xt = min(xt, 3-xt)
            yt = min(yt, 3-yt)
            return -(xt+yt) * tile
            
        snake = ExpectimaxAgent.h17
        x, y = PATTERN_FOR_SNAKE
        if xt == 0:
            if yt == 0:
                return snake(self,board, x, y)//NORMALIZE # from (0,0)
            else:
                return snake(self,board, x, flipping30(y))//NORMALIZE # from (0,3)
        else:
            if yt == 0:
                return snake(self,board, flipping30(x), y)//NORMALIZE # from (3,0)
            else:
                return snake(self,board, flipping30(x), flipping30(y))//NORMALIZE # from(3,3)
        return 0
    
    def h19(self, board):
        ''' specialized gravity - more points for ordinated lines like [64,32,8,0] '''         
        bonus = 0
        turs = zip(board[0], board[1], board[2], board[3])
        reversedTurs = zip(reversed(board[0]), reversed(board[1]), reversed(board[2]), reversed(board[3]))
        lines = board
        reversedLines = reversed(board)
        for changed_board in (turs, reversedTurs, lines, reversedLines):
            for tiles_feeder in changed_board:
                lastTile = 0
                for tile in tiles_feeder:
                    if tile > lastTile: break
                    bonus += tile
                    lastTile = tile
        return bonus
        
    def h20(self, board):
        '''
gets bonus for every tile in the x's, half a bonus for y's -
xxxx
yyyy
0000
0000
in order to make the heavy tiles get into one side
        '''
        return max((sum(board[0]) + sum(board[1]) // 2,
                    sum(board[3]) + sum(board[2]) // 2,
                    sum([board[i][0] for i in range(4)]) + sum([board[i][1] for i in range(4)]) // 2,
                    sum([board[i][3] for i in range(4)]) + sum([board[i][2] for i in range(4)]) // 2
                    ))
                    
    
    def h21(self, board):
        ''''' an upgrade of 20 - 
        make the heavy tiles get into one side,
        double the bonus for every ordered tile
        double the bonus for the corners '''
        line_feeders = ((board[0],board[1]), (board[3], board[2]), ([board[i][0] for i in range(4)], [board[i][1] for i in range(4)]), ([board[i][3] for i in range(4)], [board[i][2] for i in range(4)]))
        bonus = 0
        for first_line, second_line in line_feeders:
            # if first line is sorted - double the bonus
            myBonus = 8 * sum(first_line) + sum(second_line) //2
            lastTile = float("inf")
            for tile in first_line:
                if tile <= lastTile:
                    myBonus += tile
                    lastTile = tile 
                else: break
            lastTile = float("inf")
            for tile in reversed(first_line):
                if tile <= lastTile:
                    myBonus += tile
                    lastTile = tile 
                else: break
            bonus += 10 * (first_line[0] + first_line[3])
            bonus = max(bonus, myBonus)
            
        return NORMALIZE_21(bonus)
    def h22(self, board):
        ''' creating snakes all over the board.
        checks for neighbours with a largeness 
        between (x/2 , 2*x) for every x tile in the board '''
        bonusX = bonusY = 0
        for tile, x, y in Miniboard.generator(board):
            x1, y1 = x+1, y+1
            if tileIsInBoundaries(x1,y):
                nextTile = board[x1][y]
                if tile == nextTile or tile*2 == nextTile or nextTile*2 == tile:
                    bonusX += tile
            if tileIsInBoundaries(x,y1):
                nextTile = board[x][y1]
                if tile == nextTile or tile*2 == nextTile or nextTile*2 == tile:
                    bonusY += tile
                    
        return max(bonusX, bonusY)
        
    def h23(self, board):
        ''' the first found A* heuristic, including the other heuristics with weights '''
        return ((self.h10(board) * 16) + \
                (self.h11(board) * 32) + \
                (self.h12(board) * 8)  + \
                (self.h5(board) * 8)   + \
                (self.h20(board) * 32) + \
                (self.h13(board) * 32) + \
                (self.h19(board) * 32) + \
                (self.h8(board) * 16)  + \
                (self.h1(board) * 32))
                
    def h24(self, board):
        ''' the second found A* heuristic, including the other heuristics with weights '''
        return ((self.h10(board) * 16) + \
                (self.h12(board) * 32)  + \
                (self.h20(board) * 16) + \
                (self.h13(board) * 64) + \
                (self.h8(board) * 64)  + \
                (self.h1(board) * 32))
         
    def h25(self, board):
        ''' the third found A* heuristic, including the other heuristics with weights '''
        return ((self.h10(board) * 32) + \
                (self.h12(board) * 64)  + \
                (self.h20(board) * 32) + \
                (self.h13(board) * 64) + \
                (self.h8(board) * 16)  + \
                (self.h1(board) * 64))
        
    def h26(self, board):
        ''' the fourth found A* heuristic, including the other heuristics with weights '''
        return sum(w * h(self,board) for h,w in {h1: 64, h8 : 26, h12:64, h13: 64, h20:42}.items())
        
    

    def __init__(self, heuristics = None):
        '''
        Constructor
        '''
        if not heuristics:
            heuristics = ExpectimaxAgent.curHeuToCheck
        self.heuristicsInUse = heuristics
        self.timesForHeuristics = {h : 0 for h in self.heuristicsInUse}
        self.pointsForHeuristics = {h : 0 for h in self.heuristicsInUse}
        self.biggestTile = 8
    
    def getAction(self, boardWithTiles):
        boardWithInt = Miniboard.convertBoardWithTiles(boardWithTiles)
#         emptyTiles = Miniboard.countEmptyTiles(boardWithInt)
#         if emptyTiles > 7:
#             action, score = self.expectimax(boardWithInt, 1, myTurn = True)
#         try:
        action, score = self.expectimax(boardWithInt, myTurn = True)    
    
        if self.biggestTile == Miniboard.Max(boardWithInt)[0]:
            self.biggestTile *= 2
            self.timesForHeuristics = {h : 0 for h in self.heuristicsInUse}
            self.pointsForHeuristics = {h : 0 for h in self.heuristicsInUse}
        
        if (score == float("-inf")):
            self.debug_heuristics(boardWithInt)
            print("~~~~")

        return action
#         
#         except TypeError:
#             self.debug_heuristics(boardWithInt)
#             print("************")
#             return None
        
        
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
            return -99999999 # TODO: maybe change the number
        
        retval = 0
        for h in self.heuristicsInUse:
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
        for h in self.heuristicsInUse:
            print("score:", abs(score[h]),"time:", time[h], "name:", h)
        Miniboard.debug_board(board)

    def get_heuristics(self):
        return self.heuristicsInUse



        '''
        REACHED 4096:
        
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
NORMALIZE_15 = 3
heuristicsInUse = (h1, h2, h3, h4, h10, h13, h15)
'''

    '''
1024, 256, 64, 32, 16, 8, 8, 8, 4, 4, 4, 4, 2, 2, 2, 2, 
128, 64, 32, 32, 16, 16, 16, 8, 8, 4, 4, 4, 4, 4, 4, 2, 
2048, 512, 256, 64, 64, 32, 32, 16, 8, 8, 8, 4, 4, 2, 2, 2, 
2048, 128, 64, 32, 32, 16, 16, 8, 8, 8, 4, 4, 4, 2, 2, 2, 
    heuristicsInUse = (h18, h1, h5, h9, h10) #(h16,h15, h10, h1, h5, h17) #(h1, h2, h3, h4, h10, h13, h15)
'''
    ''' heuristicsInUse = (h19, h18, h1, h5, h10) # scored 50% of 2048 with NORMALIZED_5 = 1 '''
    
    heuristicsInUse =(h1,h2,h3,h4,h5,h6,h7,h8,h9,h10,h11,h12,h13,h14,h15,h18,h19,h20,h21,h22)#(h19, h18, h1, h5, h10, h21) #  (h20, h1, h5, h11) #(h19, h18, h1, h5, h10) #(h16,h15, h10, h1, h5, h17) #(h1, h2, h3, h4, h10, h13, h15)
    heuristicsNames = { 
                        h1 : 'h1', 
                        h2 : 'h2', 
                        h3 : 'h3', 
                        h4 : 'h4', 
                        h5 : 'h5', 
                        h6 : 'h6', 
                        h7 : 'h7', 
                        h8 : 'h8', 
                        h9 : 'h9', 
                        h10 : 'h10', 
                        h11 : 'h11', 
                        h12 : 'h12', 
                        h13 : 'h13', 
                        h14 : 'h14', 
                        h15 : 'h15', 
                        h16 : 'h16', 
                        h17 : 'h17', 
                        h18 : 'h18', 
                        h18a : 'h18a', 
                        h19 : 'h19', 
                        h20 : 'h20', 
                        h21 : 'h21', 
                        h22 : 'h22', 
                        h23 : 'A* first heuristic',
                        h24 : 'A* second heuristic',
                        h25 : 'A* third heuristic',
                        h26 : 'A* fourth heuristic'
                       }
    heuristicsWon4096 = (h1, h8, h10, h12, h13, h20)
    heuristicsWon2048 = (h1, h19)
    heuristicOK2048   = (h1, h5, h8, h10, h11, h12, h13, h18, h19, h20)
    heuristicsWon1024 = (h1, h5, h8, h10, h11, h12, h13, h20)
    curHeuToCheck     = (h26,) #(h1, h8, h12, h13, h20)
    curHeuWeights     = {h26 : 1} #{h1: 64, h8 : 26, h12:64, h13: 64, h20:42}
    
h1 = ExpectimaxAgent.h1
h2 = ExpectimaxAgent.h2
h3 = ExpectimaxAgent.h3
h4 = ExpectimaxAgent.h4
h5 = ExpectimaxAgent.h5
h6 = ExpectimaxAgent.h6
h7 = ExpectimaxAgent.h7
h8 = ExpectimaxAgent.h8
h9 = ExpectimaxAgent.h9
h10 = ExpectimaxAgent.h10
h11 = ExpectimaxAgent.h11
h12 = ExpectimaxAgent.h12
h13 = ExpectimaxAgent.h13
h14 = ExpectimaxAgent.h14
h15 = ExpectimaxAgent.h15
h16 = ExpectimaxAgent.h16
h17 = ExpectimaxAgent.h17
h18 = ExpectimaxAgent.h18
h19 = ExpectimaxAgent.h19
h20 = ExpectimaxAgent.h20
h21 = ExpectimaxAgent.h21
h22 = ExpectimaxAgent.h22
h23 = ExpectimaxAgent.h23
h24 = ExpectimaxAgent.h24
h25 = ExpectimaxAgent.h25
h26 = ExpectimaxAgent.h26