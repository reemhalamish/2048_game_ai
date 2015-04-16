'''
Created on 14 april 2015

@author: Reem
'''

from gui import GUI
import tkinter

def main():
    root = tkinter.Tk()
    root.title("2048")
    root.resizable(width=False, height=False)
    gui = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
    
    
'''
TODO:
1. create method before_turn() in GUI that creates one random 2 or 4 square
    it can use create_new_tile(self, x, y, value = 2)
2. create a listener to the arrows that will call update_turn(direction) 
    it should be with a getAction I think. maybe in another class?
'''