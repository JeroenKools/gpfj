'''
Created on Aug 1, 2012

Careful brain

@author: Jeroen Kools
'''

import randomBrain
from random import shuffle, choice
import constants

BOARD_WIDTH = constants.BOARD_WIDTH

class Brain(randomBrain.Brain):
    def __init__(self, game, army, boardwidth=None):
        self.army = army
        self.game = game

        global BOARD_WIDTH
        if boardwidth: BOARD_WIDTH = boardwidth

    def placeArmy(self, armyHeight):
        self.armyHeight = armyHeight
        bombs = self.getUnits("Bomb")
        flag = self.getUnits("Flag")

        if self.army.color == "Blue":
            self.rows = range(self.armyHeight)
        else:
            self.rows = range(BOARD_WIDTH - 1, BOARD_WIDTH - self.armyHeight - 1, -1)

        self.flagpos = self.placeFlag()
        flag[0].setPosition(self.flagpos[0], self.flagpos[1])

        self.placeBombs(bombs)

        # place other pieces randomly!
        r = randomBrain.Brain(self.game, self.army)
        r.placeArmy(self.armyHeight)

    def placeFlag(self):
        positions = []
        for n, i in enumerate(self.rows):
            for _ in range(self.armyHeight - n - 1): # weighted toward back rows 
                for x in range(BOARD_WIDTH):
                    positions += [(x, i)]

        return choice(positions)

    def placeBombs(self, bombs):
        positions = []
        nearFlagWeight = 5
        backrowWeight = 2
        frontrowWeight = 3
        inFrontOfFlagWeight = 10

        frontrow = self.armyHeight - 1 if self.army.color == "Blue" else BOARD_WIDTH - self.armyHeight
        backrow = 0 if self.army.color == "Blue" else BOARD_WIDTH - 1
        forward = 1 if self.army.color == "Blue" else -1

        for row in range(min(frontrow, backrow), max(frontrow, backrow) + 1):
            for column in range(BOARD_WIDTH):
                if row == backrow:
                    positions += backrowWeight * [(column, row)]
                elif row == frontrow:
                    positions += frontrowWeight * [(column, row)]
                else:
                    positions += [(column, row)]

        # positions around the flag have an extra high probability of getting a bomb        
        if self.flagpos[0] > 0:
            positions += nearFlagWeight * [(self.flagpos[0] - 1, self.flagpos[1])]
        if self.flagpos[0] < (BOARD_WIDTH - 1):
            positions += nearFlagWeight * [(self.flagpos[0] + 1, self.flagpos[1])]
        if self.flagpos[1] != frontrow:
            positions += inFrontOfFlagWeight * [(self.flagpos[0], self.flagpos[1] + forward)]

        positions = [x for x in positions if x != self.flagpos]

        for bomb in bombs:
            bombpos = choice(positions)
            bomb.setPosition(bombpos[0], bombpos[1])
            positions = [pos for pos in positions if pos != bombpos]

    def getUnits(self, name):
        return [unit for unit in self.army.army if unit.name == name]

    def findMove(self):
        #print 'careful...'
        move = None
        moves = []
        order = range(len(self.army.army))
        shuffle(order)
        enemyArmy = self.game.otherArmy(self.army.color)
        highestUnknown = enemyArmy.highestUnknown()

        for i in order:
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
                dirlist = []

                # only attack pieces of known weaker strength, or with scouts
                for direction in [north, south, west, east]:
                    target = self.game.getUnit(direction[0], direction[1])
                    if target and target.color != unit.color: # target square occupied by enemy
                        if target.isKnown and target.rank < unit.rank:  # known inferior rank                            
                            if self.game.legalMove(unit, direction[0], direction[1]):
                                #print "you're weaker than me!"
                                return ((col, row), direction)
                        elif not target.isKnown and highestUnknown < unit.rank and target.hasMoved: # inferred inferior rank
                            if self.game.legalMove(unit, direction[0], direction[1]):
                                #print "you must be weaker than me!"
                                return ((col, row), direction)
                        elif not target.isKnown and unit.walkFar:       # our unit is a scout
                            dirlist += [direction] * 5
                        elif not target.isKnown and unit.rank == 5:     # lieutenants are cannon fodder
                            dirlist += [direction]
                        elif target.isKnown and target.rank == 99 and unit.canDefuseBomb: # defuse known bomb
                            #print 'I hate bombs!'
                            return ((col, row), direction)
                        elif unit.rank == 10 and target.isKnown and target.hasMoved:  # aggressive marshal
                            #print "I'm invincible!"
                            return ((col, row), direction)
                        elif unit.rank == 1 and target.rank == 10 and target.isKnown: # spy vs marshall
                            return ((col, row), direction)
                    else:
                        dirlist += [direction]

                # multiply chance for 'forward' direction
                if self.army.color == "Blue":
                    if south in dirlist:
                        dirlist += [south, south, south]
                else:
                    if north in dirlist:
                        dirlist += [north, north, north]

                directions = [direction for direction in dirlist if
                              direction[0] >= 0 and direction[0] < BOARD_WIDTH and
                              direction[1] >= 0 and direction[1] < BOARD_WIDTH and
                              not self.army.getUnit(direction[0], direction[1]) and
                              self.game.legalMove(unit, direction[0], direction[1])]

            if len(directions) >= 1:
                move = choice(directions)
                moves += [((col, row), move)]

        if len(moves) >= 1:
            move = choice(moves)
            return move

        # use randombrain as a last resort - maybe player has encircled us with unknown units?
        #print 'this is my last resort!'
        tempBrain = randomBrain.Brain(self.game, self.army)
        return tempBrain.findMove()

    def observe(self, message):
        # Process messages describing enemy moves and other events. Currently unused.
        pass