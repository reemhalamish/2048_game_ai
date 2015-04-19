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
    for i in range(10):
        main()
    
    
'''
TODO:
at depth=3 the AI is REALLY slow, how can I upgrade it?
more heuristics:
'''