'''
Created on 16 april 2015

@author: Reem
'''
from game import SIZE_OF_ONE_TILE, path_for_images
from tkinter import PhotoImage
from PIL import ImageTk
class Tile():
    '''
    represent one tile in the board
    '''


    def __init__(self, canvas, x, y,value = 2, meragble = True):
        '''
        Constructor
        '''
        self.value = value
        self.x = x
        self.y = y
        self.canvas = canvas
        self.image = None
        self.image_in_canvas = None
        self.meragble = meragble # is here to know if this tile has already moved this turn
        self.draw()
        
    def draw(self, x = None, y = None):
        if not x:
            x = self.x
        if not y:
            y = self.y
        x,y = Tile.convertXYinBoardToXYinCanvas(x,y)
        
        picturePath = path_for_images[self.value]
        self.image = ImageTk.PhotoImage(file = picturePath)
        self.image_in_canvas = self.canvas.create_image(x,y, image=self.image)
    def erase(self):
        self.canvas.delete(self.image_in_canvas)
    
    def getXY(self):
        return self.x, self.y
    
    def __update_drawing(self, x = None, y = None):
        self.erase()
        self.draw(x,y)
        
    
    def mergable(self, anotherTile):
        return self.value == anotherTile.value and self.meragble and anotherTile.meragble
    
    def merge(self, anotherTile):
        self.meragble = False
        self.value *= 2
        x, y = anotherTile.getXY()
        self.update_new_place(x,y)
        anotherTile.erase() # the picture in the canvas
        del anotherTile# TODO: need to remove it?
    
    def update_new_place(self, x = None, y = None):
        if (not x == None):
            self.x = x
        if (not y == None):
            self.y = y
        self.__update_drawing(x,y)
        
    
    def end_of_turn(self):
        self.meragble = True
    
    @staticmethod
    def convertXYinBoardToXYinCanvas(x,y):
        x *= SIZE_OF_ONE_TILE
        y *= SIZE_OF_ONE_TILE
        x += 50
        y += 50
        return x,y
    
    def __repr__(self):
        return str(self.value)