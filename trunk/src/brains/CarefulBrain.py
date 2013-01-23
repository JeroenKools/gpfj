'''
Created on Aug 1, 2012

Careful brain

@author: Jeroen Kools
'''

import randomBrain
from random import shuffle, choice, gauss
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
        self.placeSpy()
        self.placeScouts()

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

        self.frontrow = self.armyHeight - 1 if self.army.color == "Blue" else BOARD_WIDTH - self.armyHeight
        self.backrow = 0 if self.army.color == "Blue" else BOARD_WIDTH - 1
        self.forward = 1 if self.army.color == "Blue" else -1

        for row in range(min(self.frontrow, self.backrow), max(self.frontrow, self.backrow) + 1):
            for column in range(BOARD_WIDTH):
                if row == self.backrow:
                    positions += backrowWeight * [(column, row)]
                elif row == self.frontrow:
                    positions += frontrowWeight * [(column, row)]
                else:
                    positions += [(column, row)]

        # positions around the flag have an extra high probability of getting a bomb        
        if self.flagpos[0] > 0:
            positions += nearFlagWeight * [(self.flagpos[0] - 1, self.flagpos[1])]
        if self.flagpos[0] < (BOARD_WIDTH - 1):
            positions += nearFlagWeight * [(self.flagpos[0] + 1, self.flagpos[1])]
        if self.flagpos[1] != self.frontrow:
            positions += inFrontOfFlagWeight * [(self.flagpos[0], self.flagpos[1] + self.forward)]

        positions = [x for x in positions if x != self.flagpos]

        for bomb in bombs:
            bombpos = choice(positions)
            bomb.setPosition(bombpos[0], bombpos[1])
            positions = [pos for pos in positions if pos != bombpos]

    def placeSpy(self):
        """"Place the Spy on an unoccupied spot. Lean heavily towards the middle of the second or third row."""

        spy = self.getUnits("Spy")[0]
        ylist = [self.backrow + self.forward] * 2 + [self.backrow + 2 * self.forward]
        placed = False

        while not placed:
            x = int(round(gauss(BOARD_WIDTH / 2.0, 1.5)))
            x = max(0, min(BOARD_WIDTH, x))
            y = choice(ylist)
            if self.game.getUnit(x, y):
                continue # already occupied
            else:
                placed = True
                spy.setPosition(x, y)

    def placeScouts(self, number=2):
        """Try to place some scouts at the front line"""
        scouts = self.getUnits("Scout")

        columns = range(BOARD_WIDTH)
        placed = 0
        attempts = 0

        while placed < number and attempts < 1000:
            attempts += 1
            x = choice(columns)
            if not self.game.getUnit(x, self.frontrow) and not self.game.isPoolColumn(x):
                scouts[placed].setPosition(x, self.frontrow)
                placed += 1

    def getUnits(self, name):
        return [unit for unit in self.army.army if unit.name == name]

    def findMove(self):
        """Careful..."""

        move = None
        moves = []
        order = range(len(self.army.army))
        shuffle(order)
        enemyArmy = self.game.otherArmy(self.army.color)
        highestUnknown = enemyArmy.highestUnknown()
        self.threats = self.findThreats()

        # Try these high priority moves first
        methods = [self.keepMarshalSafe, self.hitWeakerUnits, self.scout]
        for method in methods:
            move = method()
            if move:
                #print 'priority move:', method, move
                return move

        # If there are no high priority moves,
        # Find a decent move going through the units in random order 
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
                        if target.isKnown and target.rank < unit.rank and not unit.rank == 10:  # known inferior rank                            
                            if self.game.legalMove(unit, direction[0], direction[1]):
                                #print "you're weaker than me!"
                                return ((col, row), direction)
                        elif not target.isKnown and highestUnknown < unit.rank \
                            and target.hasMoved and not unit.rank == 10: # inferred inferior rank
                            if self.game.legalMove(unit, direction[0], direction[1]):
                                #print "you must be weaker than me!"
                                return ((col, row), direction)
                        elif not target.isKnown and unit.walkFar:       # our unit is a scout
                            dirlist += [direction] * 5
                        #elif not target.isKnown and unit.rank == 5:     # lieutenants are cannon fodder
                        #    dirlist += [direction]
                        elif target.isKnown and target.rank == 99 and unit.canDefuseBomb: # defuse known bomb
                            #print 'I hate bombs!'
                            return ((col, row), direction)
                        elif unit.rank == 10 and target.hasMoved:  # aggressive marshal
                            #print 'checking a marshal move to', direction
                            newNeighborTiles = self.game.getAdjacent(direction[0], direction[1])
                            safe = True
                            # Make sure Marshal isn't walking into a trap
                            for newNeighborTile in newNeighborTiles:
                                newNeighbor = self.game.getUnit(newNeighborTile[0], newNeighborTile[1])
                                if newNeighbor and newNeighbor.color != unit.color:
                                    if not(newNeighbor.isKnown):
                                        safe = False
                                        #print 'not safe there!'
                            if target.isKnown and target.rank == 10:
                                safe = False
                                #print "I'm not committing suicide!"

                            if safe:
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

    def keepMarshalSafe(self):
        "Deal with potential attacks being attempted on our marshal"
        marshal = self.getUnits("Marshal")[0]
        if not(marshal.isKnown) or not(marshal.alive):
            return

        if marshal in [x[0] for x in self.threats]:
            #print 'marshal in danger!!'

            # Find safer tiles - flee!
            mx, my = marshal.getPosition()
            for x, y in self.game.getAdjacent(mx, my):
                #print 'is %i,%i safer?' % (x,y)
                if self.game.getUnit(x, y): continue
                safe = True
                newNeighborTiles = self.game.getAdjacent(x, y)
                for newNeighborTile in newNeighborTiles:
                    newNeighbor = self.game.getUnit(newNeighborTile[0], newNeighborTile[1])
                    if newNeighbor and newNeighbor.color != marshal.color and not(newNeighbor.isKnown):
                        safe = False
                if safe and self.game.legalMove(marshal, x, y):
                    return ((mx, my), (x, y))

            # Intercept threat to Marshal with another unit
            threat = [t[1] for t in self.threats if t[0] == marshal][0]
            threatx, threaty = threat.getPosition()
            for x, y in self.game.getAdjacent(threatx, threaty):
                unit = self.game.getUnit(x, y)
                if unit and unit != marshal and unit.color == marshal.color:
                    return ((x, y), (threatx, threaty))

    def hitWeakerUnits(self):
        for unit in self.army.army:
            if unit.name == "Marshal" or not(unit.canMove) or not(unit.alive): continue
            x, y = unit.getPosition()
            for i, j in self.game.getAdjacent(x, y):
                enemy = self.game.getUnit(i, j)
                if enemy and enemy.color != unit.color and enemy.isKnown and enemy.rank < unit.rank:
                    return((x, y), (i, j))

    def findThreats(self):
        """Return a list of (friendly, enemy) unit tuples, where enemy is a known enemy unit whose rank
        is higher than that of the adjacent friendly unit, or an unknown unit"""

        threats = []
        for enemyUnit in self.game.otherArmy(self.army.color).army:
            x, y = enemyUnit.getPosition()
            for i, j in self.game.getAdjacent(x, y):
                myUnit = self.army.getUnit(i, j)
                if myUnit:
                    if enemyUnit.isKnown:
                        if myUnit.rank < enemyUnit.rank:
                            threats += [(myUnit, enemyUnit)]
                    else:
                        threats += [(myUnit, enemyUnit)]

        return threats

    def scout(self):
        scouts = self.getUnits("Scout")

        for scout in scouts:
            (col, row) = scout.getPosition()
            for dist in range(BOARD_WIDTH, 1, -1):
                north = (col, row - dist)
                south = (col, row + dist)
                west = (col - dist, row)
                east = (col + dist, row)

                # only attack pieces of known weaker strength, or with scouts
                for direction in [north, south, west, east]:
                    if self.game.legalMove(scout, direction[0], direction[1]):
                        unit = self.game.getUnit(direction[0], direction[1])
                        if unit and unit.color != scout.color and unit.hasMoved and not unit.isKnown:
                            #print 'scouting the unknown!!'
                            return ((col, row), direction)

    def observe(self, message):
        # Process messages describing enemy moves and other events. Currently unused.
        pass