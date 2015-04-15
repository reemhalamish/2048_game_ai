'''
Created on 14 april 2015
@author: Reem
'''
from tkinter import *

SIZE_OF_ONE_TILE = 100
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
        self.board = [[(0, FREE_TO_MOVE) for i in  range(4)] for j in range(4)]
        
        self.master = master
        
        # canvas
        self.canvas = Canvas(master, width=SIZE_OF_WINDOW, height=SIZE_OF_WINDOW)
        self.draw_grid()
        

    def draw_grid(self):
        c = self.canvas
        c.grid()
        
        edge_of_screen = 5 * SIZE_OF_ONE_TILE
        for i in range(5):
            height = width = i * SIZE_OF_ONE_TILE
            c.create_line(height, 0, height, edge_of_screen)
            c.create_line(0, width, edge_of_screen, width)
    def draw_new_tile(self, x, y, value):
        pass
    def move_tile(self, direction): # גם האיחוד יהיה כאן, או שנעשה פונקציה אחרת?
        pass
    def replace_tile_value(self, x,y, newValue):
        pass
    def update_turn(self, direction):
        pass
    def getTileValue(self,x,y):
        return self.board[x][y]
    def erase_all(self):
        pass
    def draw_all(self, board):
        pass