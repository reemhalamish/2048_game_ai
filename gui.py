'''
Created on 14 april 2015
@author: Reem
'''
from tkinter import *
from tile import Tile
from game import *
from tkinter.font import BOLD

SIZE_OF_WINDOW = 4 * SIZE_OF_ONE_TILE
FREE_TO_MOVE = True
class GUI(Frame):
    '''
    classdocs
    '''


    def __init__(self, master):
        master.minsize(width=SIZE_OF_WINDOW, height=SIZE_OF_WINDOW)
        master.maxsize(width=SIZE_OF_WINDOW, height=SIZE_OF_WINDOW)
        Frame.__init__(self, master)
        self.board = [[None for i in  range(4)] for j in range(4)]
        self.master = master
        
        # canvas
        self.canvas = Canvas(master, width=SIZE_OF_WINDOW, height=SIZE_OF_WINDOW)
        self.draw_grid()
        
        self.create_new_tile(1, 0)
        self.create_new_tile(2, 1)
        self.create_new_tile(1, 3)
        self.debug_board()
        self.update_turn(Directions.SOUTH)
        self.debug_board()
        self.update_turn(Directions.WEST)
        self.debug_board()

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
        tile.draw()
    def update_turn(self, direction):
        ''' moving all the tiles '''
        dx,dy = Directions.dxdy[direction]
        if direction == Directions.WEST or direction == Directions.NORTH:
            for line in self.board:
                for tile in line:
                    self.move_tile(tile, direction)
        elif direction == Directions.EAST:
            for line in self.board:
                for tile in reversed(line):
                    self.move_tile(tile, direction)
        elif direction == Directions.SOUTH:
            for line in reversed(self.board):
                for tile in line:
                    self.move_tile(tile, direction)
                    
        for line in self.board:
            for tile in line:
                if not tile == None:
                    tile.end_of_turn()
    
    def move_tile(self, tile, direction):
        if tile == None:
            return
        prevX, prevY = tile.getXY()
        tx, ty = tile.getXY()
        dx, dy = Directions.dxdy[direction]
        inBoundaries = lambda x,y : (x >= 0 and x <= 3) and (y >= 0 and y <= 3)
        
        # gravity: move along all the empty tiles
        while (inBoundaries(tx + dx, ty+dy) and self.board[tx + dx][ty+dy] == None):
            tx += dx
            ty += dy
        # coliision: or with the boundary or with another tile
        # if with the boundary - save and exit
        if (not inBoundaries(tx + dx, ty+dy)):
            tile.update_new_place(tx, ty)
            self.board[prevX][prevY] = None
            self.board[tx][ty] = tile
        # else - collision with another. check if can merge
        else:
            anotherTile = self.board[tx+dx][ty+dy]
            if tile.mergable(anotherTile):
                tile.merge(anotherTile)
                self.board[prevX][prevY] = None
                self.board[tx+dx][ty+dy] = tile
            else: # treat like a boundary
                tile.update_new_place(tx, ty)
                self.board[prevX][prevY] = None
                self.board[tx][ty] = tile
        
        
        
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
    def debug_board(self):
        b = self.board
        for y in range(4):
            for x in range(4):
                if b[x][y]:
                    print(b[x][y], end = " ")
                else:
                    print("-", end = " ")
            print()
        print("****************************")