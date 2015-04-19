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
* consider something like that:
[1024, 512, 256, 4]
[256,  4,   2,   4]
[.................]
[.................]
manDistance between equal tiles?
'''
