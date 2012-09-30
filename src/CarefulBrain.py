'''
Created on Aug 1, 2012

Careful brain

@author: Jeroen Kools
'''

import randomBrain
from random import shuffle, choice
from constants import *

class Brain(randomBrain.Brain):
    def __init__(self, game, army):
        self.army = army
        self.game = game

    def placeArmy(self, armyHeight):
        bombs = self.getUnits("Bomb")
        flag = self.getUnits("Flag")
        
        if self.army.color == "Blue":
            rows = range(armyHeight)
        else:
            rows = range(BOARD_WIDTH - 1, BOARD_WIDTH - armyHeight - 1, -1)
        
        positions = []    
        for n, i in enumerate(rows):
            for j in range(armyHeight-n-1):
                for x in range(BOARD_WIDTH):
                    positions += [(x, i)]
                    
        flagpos = choice(positions)
        flag[0].setPosition(flagpos[0], flagpos[1])
        positions = [pos for pos in positions if pos != flagpos]
        
        d = 1 if self.army.color == "Blue" else -1
        for i in range(3):
            for x in range(max(0, flagpos[0]-2), min(flagpos[0]+3,BOARD_WIDTH)):
                positions += [(x, flagpos[1]+d)]
        
        for bomb in bombs:
            bombpos = choice(positions)
            bomb.setPosition(bombpos[0], bombpos[1])
            positions = [pos for pos in positions if pos != bombpos]
            
        r = randomBrain.Brain(self.game, self.army)
        r.placeArmy(armyHeight)
        
    def getUnits(self, name):
        return [unit for unit in self.army.army if unit.name == name]

    #def findMove(self, gamestate):
        # Find a move given the current board situation
        # Returns (oldPosition, newPosition)
    #    pass
    
    def observe(self, message):
        # Process messages describing enemy moves and other events. Currently unused.
        pass