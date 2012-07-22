'''
Created on 29 jun. 2012

@author: Jeroen Kools
'''

import Brain
from constants import *
from random import shuffle, choice, randint

class Brain(Brain.Brain):
    def __init__(self, army):
        self.army = army

    def placeArmy(self):

        positions = []

        if self.army.color == "Blue":
            rows = range(4)
        else:
            rows = range(BOARD_WIDTH - 4, BOARD_WIDTH)

        for row in rows:
            for column in range(BOARD_WIDTH):
                positions += [(column, row)]

        shuffle(positions)

        for unit in self.army.army:
            unit.position = positions.pop()

    def findMove(self, gamestate):
        move = None
        order = range(len(self.army.army))
        shuffle(order)

        for i in order:
            if move: break

            unit = self.army.army[i]
            if not unit.canMove or not unit.alive:
                continue

            (col, row) = unit.getPosition()

            if unit.walkFar:
                dist = range(1, BOARD_WIDTH)
                shuffle(dist)
            else:
                dist = [1]

            for d in dist:

                north = (col, row - d)
                south = (col, row + d)
                west = (col - d, row)
                east = (col + d, row)

                directions = [direction for direction in [north, south, west, east] if
                              direction[0] >= 0 and direction[0] < BOARD_WIDTH and
                              direction[1] >= 0 and direction[1] < BOARD_WIDTH and
                              not self.army.getUnit(direction[0], direction[1]) and
                              gamestate.legalMove(unit, direction[0], direction[1])]

                if len(directions) >= 1:
                    move = choice(directions)
                    return ((col, row), move)

        return (None, None) # no legal move - lost!

    def observe(self, armies):
        pass