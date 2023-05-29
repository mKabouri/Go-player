# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''
import math
import time
import Goban
import random
import numpy as np
import itertools
from playerInterface import *

import sys

class myPlayer(PlayerInterface):

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None
        self.limitTime = 10
        self.begin = 0
        
    def getPlayerName(self):
        return "(:TeaDrinker:)"

 #####################################################################################
 
 
    """ 
    This alphaBeta algorithm extract score and the move associated.
    """
    def alphaBeta(self, player, profondeur, alpha=-math.inf, beta=math.inf):
        now = time.time()
        
        if profondeur == 0 or self._board.is_game_over() or (now - self.begin >= self.limitTime):
            return self.combineHeuristics(), None #Evaluate board
        if player:
            max_score = -math.inf
            best_moves = []
            for move in self._board.legal_moves():
                self._board.push(move)
                eval = self.alphaBeta(not player, profondeur-1, alpha, beta)[0]
                self._board.pop()
                if eval > max_score:
                    max_score = eval
                    best_moves.clear()
                    best_moves.append(move)
                    alpha = max(alpha, eval)
                    if beta <= alpha: # prune
                        break
            best_move = random.choice(best_moves)
            return max_score, best_move
        else:
            min_score = math.inf
            best_moves = []
            for move in self._board.legal_moves():
                self._board.push(move)
                eval = self.alphaBeta(not player, profondeur-1, alpha, beta)[0]
                self._board.pop()
                if eval < min_score:
                    min_score = eval
                    best_moves.clear()
                    best_moves.append(move)
                    beta = min(beta, eval)
                    if beta <= alpha: #prune
                        break
            best_move = random.choice(best_moves)
            return min_score, best_move

 #####################################################################################

    def playMove(self): #use iterative deepening
        profondeur = 1
        self.begin = time.time()        
        best_score, best_move = -1, -1
        while (True):
            now = time.time()
            if (time.time() - self.begin < self.limitTime):
                best_score, best_move = self.alphaBeta(True, profondeur) 
                print("Heuristic value : ", best_score) 
            print("Depth (%d): heuriticScore = %f (%s seconds)" % (profondeur, best_score, time.time() - now))     
            if (time.time() - self.begin >= self.limitTime):               
                break
            profondeur+=1
        return best_move
    
 #####################################################################################

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS"
        move = self.playMove()
        self._board.push(move)

        # New here: allows to consider internal representations of moves
        print("I am playing ", self._board.move_to_str(move))
        print("My current board :")
        self._board.prettyPrint()
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move)

    def playOpponentMove(self, move):
        print("Opponent played ", move)  # New here
        #  the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move))

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")

 #####################################################################################
    # First heuristic
    def nbStonesHeuristic(self):
        if self._mycolor == self._board._BLACK:
            return self._board._nbBLACK - self._board._nbWHITE
        return self._board._nbWHITE - self._board._nbBLACK
    
    # Second heuristic
    def nbLibertiesHeuristic(self):
        return sum(self._board._stringLiberties[self._board._getStringOfStone(i)]
                   if self._board[i] == self._mycolor 
                   else -self._board._stringLiberties[self._board._getStringOfStone(i)] 
                   for i in range(len(self._board)) if self._board[i] != self._board._EMPTY)

    # Third heuristic    
    def __validNeighbor(self, row, col):
        return row >= 0 and row < 9 and col >= 0 and col < 9

    def __getAdjacentPoints(self, row, col):
        neighbors = ((row+1, col), (row-1, col), (row, col+1), (row, col-1))
        return [c for c in neighbors if self.__validNeighbor(c[0], c[1])]
    
    def getGroups(self):
        visited = set()
        groups = []
        for i in range(self._board._BOARDSIZE):
            for j in range(self._board._BOARDSIZE):
                if (i, j) not in visited and self._board[self._board.flatten((i, j))] != 0 and self._board[self._board.flatten((i, j))] == self._mycolor:
                    group = set()
                    queue = [(i, j)]
                    while queue:
                        row, col = queue.pop(0)
                        if (row, col) not in visited:
                            visited.add((row, col))
                            group.add((row, col))
                            for neighbor in self.__getAdjacentPoints(row, col):
                                if neighbor not in visited and self._board[self._board.flatten(neighbor)] == self._board[self._board.flatten((i, j))]:
                                    queue.append(neighbor)
                    groups.append(group)
        return groups

    def __areAdjacent(self, points):
        for p1 in points:
            for p2 in points:
                if p1 == p2:
                    continue
                distance = np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
                if distance == 1:
                    return True
        return False
    
    def getConnections(self):
        connections = {}
        groups = self.getGroups()
        for i, group1 in enumerate(groups):
            for j, group2 in enumerate(groups):
                if i != j:
                    if any(self.__areAdjacent(points) for points in itertools.product(group1, group2)):
                        connections[(i, j)] = 1
                    else:
                        connections[(i, j)] = 0
        return connections
    
    def nbConnectionsHeuristic(self):
        weights = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 32, 7: 64, 8: 128, 9: 256}
        score = 0
        groups = self.getGroups()
        for i, group1 in enumerate(groups):
            for j, group2 in enumerate(groups):
                if i != j:
                    if self._mycolor == self._board._BLACK:
                        if self.getConnections().get((i, j), 0) > 0:
                            if self._board[self._board.flatten(list(group1)[0])] == self._board._BLACK:
                                distance = self.getDistance(group1, group2)
                                weight = weights.get(distance, 0)
                                score += weight
                            else:
                                distance = self.getDistance(group1, group2)
                                weight = weights.get(distance, 0)
                                score -= weight
                    else:
                        if self.getConnections().get((i, j), 0) > 0:
                            if self._board[self._board.flatten(list(group1)[0])] == self._board._WHITE:
                                distance = self.getDistance(group1, group2)
                                weight = weights.get(distance, 0)
                                score += weight
                            else:
                                distance = self.getDistance(group1, group2)
                                weight = weights.get(distance, 0)
                                score -= weight
        return score
            
    # Combine the three heuristics: (Joue sur les poids de chaque terme à tester)
    def combineHeuristics(self):
        return 3*self.nbStonesHeuristic() + self.nbLibertiesHeuristic() + self.nbConnectionsHeuristic()


