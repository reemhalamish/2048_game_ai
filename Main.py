#!/usr/bin/env python
'''
Created on 14 april 2015

@author: Reem
'''

from gui import GUI
import tkinter
from ai import ExpectimaxAgent
<<<<<<< HEAD
TIMES_TO_CHECK_EVERY_RUN = 3
MAXIMUM_HEURISTICS_IN_GAME = 4

def runOneTime(dataSaver=None, heuristics = None):
=======
# from data_handler import DataHandler
TIMES_TO_CHECK_EVERY_RUN = 3
MAXIMUM_HEURISTICS_IN_GAME = 4

def runOneTime(dataSaver = None, heuristics = None):
>>>>>>> 38e04231fa45a38d435d5a5ea8c41da3766d8179
    Agent = ExpectimaxAgent(heuristics)
    root = tkinter.Tk()
    root.title("2048")
    root.resizable(width=False, height=False)
    gui = GUI(root, agent=Agent, dataHandler = dataSaver)
    gui.focus()
    root.mainloop()

def recuresiveRun(heuIndex, heuByNow, dataSaver):
    heuristicsToCheck = ExpectimaxAgent.heuristicsInUse
    if len(heuByNow) >MAXIMUM_HEURISTICS_IN_GAME: return # to much information
    if heuIndex == len(heuristicsToCheck):
        if not heuByNow:return
        for _ in range(TIMES_TO_CHECK_EVERY_RUN):
            runOneTime(dataSaver, heuByNow)
        return
            
    recuresiveRun(heuIndex+1, heuByNow, dataSaver)
    newHeuList = heuByNow[:]
    newHeuList.append(heuristicsToCheck[heuIndex])
    recuresiveRun(heuIndex+1, newHeuList, dataSaver)
    

if __name__ == '__main__':
<<<<<<< HEAD
    for i in range(10):
        runOneTime()
=======
#     for i in range(10):
#        dataSaver = DataHandler()
        runOneTime()
#        dataSaver.printAllInfo()
>>>>>>> 38e04231fa45a38d435d5a5ea8c41da3766d8179
        
    
    
'''
TODO:
at depth=3 the AI is REALLY slow, how can I upgrade it?
more heuristics:
heuristic that gets bonus for every tile in the x's, half a bonus for y's -
xxxx
yyyy
0000
0000
in order to make the heavy tiles get into one side
'''
