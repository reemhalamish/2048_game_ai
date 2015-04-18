'''
Created on 18 April 2015

@author: Reem
'''
from game import Directions, PROB_FOR_TWO_NORMALIZED


class Miniboard():
    '''
    represents the board (and a couple of good methods) without the gui part
    '''


    def __init__(self, tilesAsList = []):
        '''
        Constructor
        '''
        self.score = 0
        self.board = self.board = [[None for i in range(4)] for j in range(4)]
        Miniboard.debug_board(self.board)
        x, y = 0,0
        for tile in tilesAsList:
            if tile != None and tile != 0:
                self.board[x][y] = tile
            x += 1
            if x == 4:
                y += 1
                x = 0

    def encapsulateIntoState(self):
        return self.board
    
    @staticmethod
    def getNextStatesOfMyTurn(board):
        ''' gets a state - a board - and yields tuples (move,nextState) '''
        for direction in Directions.generator():
            if Miniboard.isLegalAction(board, direction):
                nextBoard = Miniboard.calculateNextBoardUsing(direction, board)
                yield(direction, nextBoard)

    @staticmethod
    def isLegalAction(board, direction):
        mergeOk = lambda x,y : x != None and y != None and x == y
        # first of all - if there are two close tiles that can be attached - it's a legal turn
        if direction == Directions.NORTH or direction == Directions.SOUTH:
            for line in board:
                tile0, tile1, tile2, tile3 = line
                if mergeOk(tile0,tile1) \
                or mergeOk(tile1, tile2) \
                or mergeOk(tile2,tile3):
                    return True
        if direction == Directions.WEST or direction == Directions.EAST:
            for tile0, tile1, tile2, tile3 in zip(board[0], board[1], board[2], board[3]):
                if mergeOk(tile0,tile1) \
                or mergeOk(tile1, tile2) \
                or mergeOk(tile2,tile3):
                    return True

        # secondly - check for instances of empty tiles right before other tiles
        if direction == Directions.WEST:
            for line in zip(board[0], board[1], board[2], board[3]):
                foundNone = False
                for tile in line:
                    if tile == None:
                        foundNone = True
                    elif foundNone: # there is a tile after a None - it will move! so this turn is good
                        return True
        elif direction == Directions.EAST:# or direction == Directions.SOUTH:
            for line in zip(board[0], board[1], board[2], board[3]):
                foundNone = False
                for tile in reversed(line):
                    if tile == None:
                        foundNone = True
                    elif foundNone: # there is a tile after a None - it will move! so this turn is good
                        return True
        elif direction == Directions.NORTH:
            for tur in board:
                foundNone = False
                for tile in tur:
                    if tile == None:
                        foundNone = True
                    elif foundNone: # there is a tile after a None - it will move! so this turn is good
                        return True
        elif direction == Directions.SOUTH:
            for tur in board:
                foundNone = False
                for tile in reversed(tur):
                    if tile == None:
                        foundNone = True
                    elif foundNone: # there is a tile after a None - it will move! so this turn is good
                        return True
        
        # reached here? sign that you haven't found anything
        return False

    @staticmethod
    def calculateNextBoardUsing(direction, oldBoard):
        ''' returns the new board '''
        board = [tur[:] for tur in oldBoard]
        if direction == Directions.WEST or direction == Directions.NORTH:
            for x in range(4):
                for y in range(4):
                    Miniboard.move_tile(x,y, direction, board)
        elif direction == Directions.EAST or direction == Directions.SOUTH:
            for x in range(3,-1,-1):
                for y in range(3,-1,-1):
                    Miniboard.move_tile(x,y, direction, board)
        
        # move_tile() changed merged tiles - i.e. from (4) to (-4) so we need to flip it 
        for x in range(4):
                for y in range(4):
                    if board[x][y] != None:
                        board[x][y] = abs(board[x][y])
        return board
                    
    @staticmethod
    def move_tile(prevX, prevY, direction, board):
        tile = board[prevX][prevY]
        if tile == None:
            return
        tx, ty = prevX, prevY
        dx, dy = Directions.dxdy[direction]
        tileIsInBoundaries = lambda x,y : (x >= 0 and x <= 3) and (y >= 0 and y <= 3)
        tilesCanMerge = lambda t,T : t != None and T != None and t == T
        
        # gravity: move along all the empty tiles
        while (tileIsInBoundaries(tx + dx, ty+dy) and board[tx + dx][ty+dy] == None):
            tx += dx
            ty += dy
        
        # coliision: or with the boundary or with another tile
        
        # if with the boundary - save and exit
        if (not tileIsInBoundaries(tx + dx, ty+dy)):
            board[prevX][prevY] = None
            board[tx][ty] = tile
        # else - collision with another. check if can merge
        else:
            anotherTile = board[tx+dx][ty+dy]
            if tilesCanMerge(tile,anotherTile):
                anotherTile *= -2
                board[tx+dx][ty+dy] = anotherTile
                board[prevX][prevY] = None
            else: # treat like a boundary
                board[prevX][prevY] = None
                board[tx][ty] = tile

    @staticmethod
    def getNextStatesForRandomPlacements(board):
        ''' gets a state - a board - and yields tuples (probability, nextState) '''
        emptySlots = [(x,y) for x in range(4) for y in range(4) if board[x][y] == None]
        if not emptySlots:
            return None
            # game over
        probabilityForOnePlacement = 1 / len(emptySlots)
        prob2 = PROB_FOR_TWO_NORMALIZED
        prob4 = 1 - prob2
        for x,y in emptySlots:
            newBoard2 = [tur[:] for tur in board]
            newBoard2[x][y] = 2
            prob = probabilityForOnePlacement * prob2
            yield (prob, newBoard2)
            newBoard4 = [tur[:] for tur in board]
            prob = probabilityForOnePlacement * prob4
            yield (prob, newBoard4)
                
    @staticmethod
    def score_for_board(board):
        score = 0
        for x in range(4):
            for y in range(4):
                tile = board[x][y]
                if not tile: continue
                # for any number 2^n , the score for it is (n-1)*(2^n)
                n = tile.bit_length() - 1 # extract n from 2^n
                score += (n-1) * tile
        return score
    
    @staticmethod
    def debug_board(board):
        for y in range(4):
            for x in range(4):
                if board[x][y]:
                    print(board[x][y], end = " "* (4 - len(str((board[x][y])))))
                else:
                    print("-", end = " "*3)
            print()
        print("****************************")
        
    @staticmethod
    def convertBoardWithTiles(board):
        retval = [[None for i in range(4)] for j in range(4)]
        for y in range(4):
            for x in range(4):
                if board[x][y] != None:
                    retval[x][y] = int(board[x][y])
        return retval
        
def test_miniboard():
    m = Miniboard([0,0,2,2,0,0,4,0,0,0,0,0,8])
    state = m.encapsulateIntoState()
    m.debug_board(state)
    nextBoards = m.getNextStatesOfMyTurn(state)
    print("next ones:")
    for b in nextBoards:
        print(b[0],":")
        print("score:", m.score_for_board(b[1]))
        m.debug_board(b[1])
if __name__ == '__main__':
            test_miniboard()