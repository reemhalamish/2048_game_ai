'''
Created on 14 april 2015
@author: Reem
'''
from miniboard import Miniboard
from tkinter import Frame, Canvas
from tile import Tile
from game import AFTER_FOR_NEW_TURN, Directions, SIZE_OF_ONE_TILE, weighted_choice
from random import choice as choose_uni_from_seq
SIZE_OF_WINDOW = 4 * SIZE_OF_ONE_TILE
class GUI(Frame):
    '''
    classdocs
    '''


    def __init__(self, master, agent = None, dataHandler = None):
        master.minsize(width=SIZE_OF_WINDOW, height=SIZE_OF_WINDOW)
        master.maxsize(width=SIZE_OF_WINDOW, height=SIZE_OF_WINDOW)
        Frame.__init__(self, master)
        self.board = [[None for i in range(4)] for j in range(4)]
        self.master = master
        self.score = 0
        self.ignoreKeys = True
        self.agent = agent
        self.dataHandler = dataHandler
        
        # canvas
        self.canvas = Canvas(master, width=SIZE_OF_WINDOW, height=SIZE_OF_WINDOW)
        self.draw_grid()
        
        # bind keys and functions
        self.master.bind('<Key>', self.key_pressed)

#         self.test_heuristics()
        self.after(AFTER_FOR_NEW_TURN, self.before_turn)

    def create_from_list(self, boardAsList):
        x, y = 0,0
        self.restart_board()
        for tile in boardAsList:
            if tile != None and tile != 0:
                self.create_new_tile(x, y, int(tile))
            x += 1
            if x == 4:
                y += 1
                x = 0

    def draw_grid(self):
        c = self.canvas
        c.grid()
        
        edge_of_screen = 5 * SIZE_OF_ONE_TILE
        for i in range(5):
            height = width = i * SIZE_OF_ONE_TILE
            c.create_line(height, 0, height, edge_of_screen, width = 10)
            c.create_line(0, width, edge_of_screen, width, width = 10)
    def create_new_tile(self, x, y, value = 2):
        tile = Tile(self.canvas, x, y, value)
        self.board[x][y] = tile
#         tile.draw() TODO: restore
        
    def before_turn(self):
        board = self.board
        # 1. get all the empty slots and choose randomly between them
        # 2. choose randomly(0.8) between putting 2 or 4 there
        emptySlots = [(x,y) for x in range(4) for y in range(4) if board[x][y] == None]
        numberToPutInSlot = weighted_choice()
        x,y = choose_uni_from_seq(emptySlots)
        self.create_new_tile(x, y, numberToPutInSlot)
        
        # check that there left some moves here, or it's a game over
        noMoreMoves = True
        for move in Directions.generator():
            if self.is_legal_turn(move):
                noMoreMoves = False
        if noMoreMoves:
            self.display_score_and_exit()
            
        if self.agent:
            self.after(AFTER_FOR_NEW_TURN, self.update_turn, self.agent.getAction(self.board))
        
        self.ignoreKeys = False
        
    def is_legal_turn(self, direction, board = None):
        ''' checks for merges, then for empty tiles right before real tiles '''
        mergeOk = lambda x,y : x != None and y != None and x == y
        if not board:
            board = self.board
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
            
    def update_turn(self, direction):
        ''' moving all the tiles '''
        
        if not self.is_legal_turn(direction):
#             print("not legal!")
            return
        
        if direction == Directions.WEST or direction == Directions.NORTH:
            for line in self.board:
                for tile in line:
                    self.move_tile(tile, direction)
        elif direction == Directions.EAST or direction == Directions.SOUTH:
            for line in reversed(self.board):
                for tile in reversed(line):
                    self.move_tile(tile, direction)
                    
        self.end_of_turn()
        self.before_turn()
#         self.after(AFTER_FOR_NEW_TURN, self.before_turn) TODOL restore it

        
    def end_of_turn(self):
        for line in self.board:
            for tile in line:
                if not tile == None:
                    tile.end_of_turn()
        
        self.ignoreKeys = True
    
    def move_tile(self, tile, direction, board = None):
        if tile == None:
            return
        if not board:
            board = self.board
        prevX, prevY = tile.getXY()
        tx, ty = tile.getXY()
        dx, dy = Directions.dxdy[direction]
        inBoundaries = lambda x,y : (x >= 0 and x <= 3) and (y >= 0 and y <= 3)
        
        # gravity: move along all the empty tiles
        while (inBoundaries(tx + dx, ty+dy) and board[tx + dx][ty+dy] == None):
            tx += dx
            ty += dy
        # coliision: or with the boundary or with another tile

        # if with the boundary - save and exit
        if (not inBoundaries(tx + dx, ty+dy)):
            tile.update_new_place(tx, ty)
            board[prevX][prevY] = None
            board[tx][ty] = tile
        # else - collision with another. check if can merge
        else:
            anotherTile = self.board[tx+dx][ty+dy]
            if tile.mergable(anotherTile):
                tile.merge(anotherTile)
                self.score += int(tile)
                board[prevX][prevY] = None
                board[tx+dx][ty+dy] = tile
            else: # treat like a boundary
                tile.update_new_place(tx, ty)
                board[prevX][prevY] = None
                board[tx][ty] = tile
        
    def getTile(self,x,y):
        return self.board[x][y]
    def erase_all(self):
        for line in self.board:
            for tile in line:
                if tile:
                    tile.erase()
    def draw_all(self, board):
        for line in self.board:
            for tile in line:
                if tile:
                    tile.draw()
                    
    def restart_board(self):
        self.board = [[None for i in range(4)] for j in range(4)]
    
                    
    def display_score_and_exit(self):
#         print("Game over! your score:",self.score)
#         print("you have about 10 seconds to review the game")
        TEN_SEC_UNTIL_EXIT = 1000 
        self.after(TEN_SEC_UNTIL_EXIT, self.exit_fast)
    
    def exit_fast(self):
#         self.printTilesSorted()
#         self.debug_board()
        if self.dataHandler:
            heuristics = self.agent.get_heuristics()
            score = self.score
            bestTile = max([int(self.getTile(x, y)) for x in range(4) for y in range(4) if self.getTile(x, y)])
            self.dataHandler.gameOver(heuristics, score, bestTile)
        self.master.destroy()
    
    def key_pressed(self, event):
        if event.keysym == 'Escape':
            self.exit_fast()
        elif event.keysym == 'q':
            self.exit_fast()
        elif event.keysym == 'z':
            self.debug_board()
        elif self.ignoreKeys:
            return
        
        elif event.keysym == 'Right':
            self.update_turn(Directions.EAST)
        elif event.keysym == 'Left':
            self.update_turn(Directions.WEST)
        elif event.keysym == 'Up':
            self.update_turn(Directions.NORTH)
        elif event.keysym == 'Down':
            self.update_turn(Directions.SOUTH)


    def debug_board(self, board = None):
        print("****************************")

        b = board if board else self.board
        for y in range(4):
            for x in range(4):
                if b[x][y]:
                    print(b[x][y], end = " "* (6 - len(str((b[x][y])))))
                else:
                    print("-", end = " "*5)
            print()
        
    def printTilesSorted(self):
        board = Miniboard.convertBoardWithTiles(self.board)
        sortedList = Miniboard.sort_board_by_highest_number(board)
        for tile in sortedList:
            print(tile[0], end = ", ")
        print()
        
        
    def test_legal_turn(self):
        self.create_from_list([0,0,0,0,2,4,2,4])
        self.debug_board()
        for d in Directions.generator():
            print(d, self.is_legal_turn(d))
        
    def test_heuristics(self):
        self.create_from_list([0,0,2,0,0,0,0,2,0,0,0,4,2,2,16,32])
        print(self.agent.getAction(self.board))
        self.debug_board()