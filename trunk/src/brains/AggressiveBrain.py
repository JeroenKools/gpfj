'''
Created on 15 jan. 2013

@author: Junuxx

TO DO: Will be a brain that likes to take risks and attacks. Currently just inherits randomBrain
'''

import randomBrain

class Brain(randomBrain.Brain):
    def __init__(self, game, army, BOARD_WIDTH):
        randomBrain.Brain.__init__(self, game, army, BOARD_WIDTH)
    
    # TODO: Aggressively place strong units at the front line
    # def placeArmy(self):
    
    def findMove(self):
        # Moves in order of priority
        methods = [self.huntKnown, self.huntUnknown]
        for method in methods:
            move = method()
            if move: return move
            
        tempBrain = randomBrain.Brain(self.game, self.army)
        return tempBrain.findMove()
    
    def huntKnown(self):
        knownUnits =[unit for unit in self.game.otherArmy(self.army.color).army if unit.isKnown]
        
        for unit in knownUnits:
            pass

    def huntUnknown(self):
        pass
    
    def findNearestEnemies(self,x,y):
        pass
    
    def findPath(self,fromX,fromY, toX, toY):
        return