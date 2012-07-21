'''
Created on 29 jun. 2012

@author: Jeroen Kools
'''

import Brain
from constants import *
from random import shuffle, choice

class Brain(Brain.Brain):
    def __init__(self, army):
        self.army = army

    def placeArmy(self):

        positions = []

        if self.army.color == "Blue":
            rows = range(4)
        else:
            rows = range(BOARD_WIDTH, BOARD_WIDTH - 4)

        for row in rows:
            for column in range(BOARD_WIDTH):
                positions += [(column, row)]

        shuffle(positions)

        for unit in self.army.army:
            unit.position = positions.pop()

    def doMove(self, gamestate):
        move = None

        while not move:
            unit = choice(self.army.army)
            if not unit.canMove or not unit.alive:
                continue

            (col, row) = unit.getPosition()

            north = (col, row - 1)
            south = (col, row + 1)
            west = (col - 1, row)
            east = (col + 1, row)

            directions = [direction for direction in [north, south, west, east] if
                          direction[0] >= 0 and direction[0] < BOARD_WIDTH and
                          direction[1] >= 0 and direction[1] < BOARD_WIDTH and
                          not self.army.getUnit(direction[0], direction[1]) and
                          gamestate.legalMove(unit, direction[0], direction[1])]

            if len(directions) >= 1:
                move = choice(directions)

                enemy = gamestate.getUnit(move[0], move[1])
                if enemy:
                    gamestate.attack(unit, enemy)
                else:
                    unit.setPosition(move[0], move[1])
                return ("(%s,%s)" % (col, row), move)

    def observe(self, armies):
        pass