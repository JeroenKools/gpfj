'''
Created on 29 jun. 2012

Template brain

@author: Jeroen Kools
'''

class Brain:
    def __init__(self, game, army):
        self.army = army
        self.game = game

    def placeArmy(self):
        # Place units on board; give a (valid) position to all units in self.army
        # Return None
        pass

    def findMove(self, gamestate):
        # Find a move given the current board situation
        # Returns (oldPosition, newPosition)
        pass

    def observe(self, message):
        # Process messages describing enemy moves and other events. Currently unused.
        pass