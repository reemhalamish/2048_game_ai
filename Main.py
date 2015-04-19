'''
Created on 14 april 2015

@author: Reem
'''

from gui import GUI
import tkinter
from ai import ExpectimaxAgent

def main():
    Agent = ExpectimaxAgent()
    root = tkinter.Tk()
    root.title("2048")
    root.resizable(width=False, height=False)
    gui = GUI(root, agent=Agent)
    gui.focus()
    root.mainloop()

if __name__ == '__main__':
        main()
    
    
'''
TODO:
at depth=3 the AI is REALLY slow, how can I upgrade it?
more heuristics:
* for every tile, search the tile*2 and grant bonuses for closer (i.e. 16,32, 2, 4) os better then (16, 2, 4, 32)
'''