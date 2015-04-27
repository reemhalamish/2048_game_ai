'''
Created on 21 april 2015

@author: Reem
'''
from ai import ExpectimaxAgent
NAMES = ExpectimaxAgent.heuristicsNames

class DataHandler():
    '''
    used to store the data from ended games
    '''


    def __init__(self):
        '''
        Constructor
        '''
        heuristics = set(ExpectimaxAgent.heuristicsInUse)
        for h in ExpectimaxAgent.curHeuToCheck:
            heuristics.add(h)
        
        self.games = {h : 0 for h in heuristics}
        self.won4096 = {h : 0 for h in heuristics}
        self.won2048 = {h : 0 for h in heuristics}
        self.won1024 = {h : 0 for h in heuristics}
        self.scoreMax = {h : 0 for h in heuristics}
        self.scoreSum = {h : 0 for h in heuristics}
        self.gamesImInvolved = 0
    def gameOver(self, heuristics, score, bestTile):
        self.gamesImInvolved += 1
        print(bestTile," best tile. in the game there were", len(heuristics), "heuristics: (game No.", self.gamesImInvolved,")", end = ". ")
        for h in heuristics: print(ExpectimaxAgent.heuristicsNames[h], end = ',')
        print()
        for h in heuristics:
            self.games[h] += 1
            if bestTile >= 4096:
                self.won4096[h] += 1
            if bestTile >= 2048:
                self.won2048[h] += 1
            if bestTile >= 1024:
                self.won1024[h] += 1
            self.scoreMax[h] = max(self.scoreMax[h],  score)
            self.scoreSum[h] += score
    def getData(self, heuristic):
        print("for heuristic ",heuristic, ":")
        print("games played:", self.games[heuristic])
        print("total score:", self.scoreSum[heuristic])
        print("maximum score in one game:", self.scoreMax[heuristic])
        print("total winning 4096:", self.won4096[heuristic])
        print("total winning 2048:", self.won2048[heuristic])
        print("total winning 1024:", self.won1024[heuristic])
        
    def printAllInfo(self):
        self.toFile()
        heuristics = ExpectimaxAgent.heuristicsInUse
        for h in heuristics:
            if self.games[h] == 0: continue
            self.getData(h)
        print("won 1024 game:", {NAMES[h] : self.won1024[h] for h in heuristics if self.won1024[h] > 0})
        print("won 2048 game:", {NAMES[h] : self.won2048[h] for h in heuristics if self.won2048[h] > 0})
        print("won 4096 game:", {NAMES[h] : self.won4096[h] for h in heuristics if self.won4096[h] > 0})
    
    def toFile(self):
        f = open("dataAboutHeuristics.log", "a")
        heuristics = ExpectimaxAgent.heuristicsInUse
        for heuristic in heuristics:
            f.write("for heuristic: "+str(heuristic)+"\n")
            f.write("games played:"+str(self.games[heuristic])+"\n")
            f.write("total score:"+str(self.scoreSum[heuristic])+"\n")
            f.write("maximum score in one game:" + str(self.scoreMax[heuristic])+"\n")
            f.write("total winning 4096:" + str(self.won4096[heuristic])+"\n")
            f.write("total winning 2048:" + str(self.won2048[heuristic])+"\n")
            f.write("total winning 1024:" + str(self.won1024[heuristic])+"\n")
        f.write("won 1024 game: "+str( {h : self.won1024[h] for h in heuristics if self.won1024[h] > 0}) + "\n")
        f.write("won 2048 game: " +str( {h : self.won2048[h] for h in heuristics if self.won2048[h] > 0}) + "\n")
        f.write("won 4096 game: " +str( {h : self.won4096[h] for h in heuristics if self.won4096[h] > 0}) + "\n")
