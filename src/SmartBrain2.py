'''
Created on 29 jun. 2012

@author: Fedde Burgers
'''
import Brain
from constants import *
from random import shuffle, choice, randint
import constants

BOARD_WIDTH = constants.BOARD_WIDTH

class Brain(Brain.Brain):
    def __init__(self, game, army, boardwidth=None):
        self.game = game
        self.army = army

        global BOARD_WIDTH
        if boardwidth: BOARD_WIDTH = boardwidth

    def placeArmy(self, armyHeight):
        if (armyHeight>3):
            tactic = randint(1,4)
        else: 
            tactic = randint(0,1)
        #tactic = 2
        
        positions = []
        bombPos = []
        scoutPos = []
        sergPos = []

        if self.army.color == "Blue":
            rows = range(armyHeight)
            backrow = 0
            frontrow = armyHeight-1
            direction = 1
        else:
            rows = range(BOARD_WIDTH - armyHeight, BOARD_WIDTH)
            backrow = BOARD_WIDTH
            frontrow = BOARD_WIDTH - armyHeight
            direction = -1

        for row in rows:
            for column in range(BOARD_WIDTH):
                if self.army.getUnit(column, row) == None:
                    positions += [(column, row)]
        
        shuffle(positions)

        ####################################################################################################################################
        #Tactic 0: Just put the flag in the back row
        if tactic == 0:
            xpos = randint(0, BOARD_WIDTH-1)
            flagPos = (xpos, backrow)

        ####################################################################################################################################
        elif tactic == 1:
            #Tactic 1: Flag in a back corner and 2 bombs around it. And if possible a boobytrap bomb cluster in other corner
            side = randint(0,3)
            self.army.flagIsBombProtected = True

            if side == 0: 
                flagPos  = (0, backrow) 
                bombPos += [(1, backrow)] 
                bombPos += [(0, backrow + direction)]
            elif side == 1:
                flagPos = (BOARD_WIDTH-1, backrow)
                bombPos += [(BOARD_WIDTH-2, backrow)] 
                bombPos += [(BOARD_WIDTH-1, backrow + direction)]
            elif side == 2: 
                flagPos  = (0, backrow)
                sergPos = [(BOARD_WIDTH-1, backrow)]
                bombPos += [(1, backrow)] 
                bombPos += [(0, backrow + direction)]
                if (armyHeight > 3):
                    bombPos += [(BOARD_WIDTH-2, backrow)] 
                    bombPos += [(BOARD_WIDTH-1, backrow + direction)]
            else:
                flagPos = (BOARD_WIDTH-1, backrow)
                sergPos = [(0, backrow)]
                bombPos += [(BOARD_WIDTH-2, backrow)] 
                bombPos += [(BOARD_WIDTH-1, backrow + direction)]
                if (armyHeight > 3):
                    bombPos += [(1, backrow)] 
                    bombPos += [(0, backrow + direction)]

        ####################################################################################################################################
        elif tactic == 2: # Flag in a corner and 6 bombs and sergeants around it
            side = randint(0,1)
            self.army.flagIsBombProtected = True

            if side == 0: 
                flagPos  = (0, backrow) 
                bombPos += [(1, backrow)]
                sergPos += [(2, backrow)]
                bombPos += [(3, backrow)]
                bombPos += [(0, backrow + direction)]
                sergPos += [(1, backrow + direction)]
                bombPos += [(2, backrow + direction)]
                sergPos += [(0, backrow + direction * 2)]
                bombPos += [(1, backrow + direction * 2)]
                bombPos += [(0, backrow + direction * 3)]
            elif side == 1:
                flagPos = (BOARD_WIDTH-1, backrow)
                bombPos += [(BOARD_WIDTH-2, backrow)]
                sergPos += [(BOARD_WIDTH-3, backrow)]
                bombPos += [(BOARD_WIDTH-4, backrow)]
                bombPos += [(BOARD_WIDTH-1, backrow + direction)]
                sergPos += [(BOARD_WIDTH-2, backrow + direction)]
                bombPos += [(BOARD_WIDTH-3, backrow + direction)]
                sergPos += [(BOARD_WIDTH-1, backrow + direction * 2)]
                bombPos += [(BOARD_WIDTH-2, backrow + direction * 2)]
                bombPos += [(BOARD_WIDTH-1, backrow + direction * 3)]
       ####################################################################################################################################
        elif tactic == 3: #Flag on back row and 3 bombs around it
            xpos = randint(2, BOARD_WIDTH-3)
            self.army.flagIsBombProtected = True
            
            flagPos = (xpos, backrow)
            bombPos += [(xpos-1, backrow)]
            bombPos += [(xpos+1, backrow)]
            bombPos += [(xpos, backrow + direction)]
            

        ####################################################################################################################################
        elif tactic == 4: #Flag behind a lake and some bombs around it
            posFlagCol = []

            for column in range(BOARD_WIDTH):
                if positions.index((column, frontrow)) > 0 and self.game.isPool(column, frontrow + direction):
                    posFlagCol += [column]

            xpos = posFlagCol[randint(0, len(posFlagCol)-1)]

            flagPos = (xpos, frontrow)
            bombPos += [(xpos-1, frontrow)]
            bombPos += [(xpos+1, frontrow)]
            bombPos += [(xpos, frontrow - direction)]
        ####################################################################################################################################
        ####################################################################################################################################

        positions.remove(flagPos)
        for bp in bombPos:
            positions.remove(bp)
        for sp in scoutPos:
            positions.remove(sp)
        for sergp in sergPos:
            positions.remove(sergp)

        # Bombs and flag are placed (possibly with some other pieces) and now the rest of the pieces is placed semi-random:


        # Scouts and bombs on front row and not behind the lakes:
        for column in range(BOARD_WIDTH):
            if positions.__contains__((column, frontrow)) and not self.game.isPool(column, frontrow + direction):
                bool = randint(0,1)
                if bool == 0 and self.army.nr_of_bombs-len(bombPos) > 1:
                    bombPos += [(column, frontrow)]
                else:
                    scoutPos += [(column, frontrow)]
                positions.remove((column, frontrow))
                
        for unit in self.army.army:
            if unit.isOffBoard():
                if unit.name == 'Flag':
                    unit.position = flagPos
                elif unit.name == 'Bomb' and bombPos:
                    unit.position = bombPos.pop()
                elif unit.name == 'Scout' and scoutPos:
                    unit.position = scoutPos.pop()
                elif unit.name == 'Sergeant' and sergPos:
                    unit.position = sergPos.pop()
                elif len(positions) >0:
                    unit.position = positions.pop()
                else:
                    unit.position = (0, 3)
        pass

    def findMove(self):
        move = None
        moves = []
        priorityKillingMoves = [] #Kills that should always have priority: miners or Marshall with spy
        alreadyKnownKillingMoves = []
        alreadyMovedKillingMoves = [] 
        alreadyMovedNotKillingMoves = []
        defuseBombMoves = []
        notMovedKillingMoves = []
        notMovedNotKillingMoves = []
        order = range(len(self.army.army))
        shuffle(order)
        enemyArmy = self.game.otherArmy(self.army.color)
        highestUnknown = enemyArmy.highestUnknown()
        
        # Probability that an unknown and unmoved piece is movable:
        nrOfPieces = enemyArmy.nrOfMovable + enemyArmy.nrOfUnmovable
        nrOfNotMovedMovable = enemyArmy.nrOfMovable - enemyArmy.nrOfKnownMovable - enemyArmy.nrOfUnknownMoved
        nrOfNotMovedUnmovable = enemyArmy.nrOfUnmovable - enemyArmy.nrOfKnownUnmovable
        nrOfNotMoved = nrOfNotMovedMovable + nrOfNotMovedUnmovable
        probNotMovedIsMovable =  nrOfNotMovedMovable / nrOfNotMoved
        probNotMovedIsNotMovable = nrOfNotMovedUnmovable / nrOfNotMoved
        
        probUnknownUnmovedIsMovable = (len(enemyArmy.livingPossibleMovableRanks) - enemyArmy.nrOfMoved) / (enemyArmy.nrOfLiving - enemyArmy.nrOfMoved)

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

                # 
                for direction in [north, south, west, east]:
                    target = self.game.getUnit(direction[0], direction[1])
                    if self.game.legalMove(unit, direction[0], direction[1]) and target and target.color != unit.color and direction[0] >= 0 and direction[0] < BOARD_WIDTH and direction[1] >= 0 and direction[1] < BOARD_WIDTH: # target is enemy and known
                        dist2Flag = abs(target.position[0]-self.army.army[0].position[0]) + abs(target.position[1]-self.army.army[0].position[1])
                        if target.isKnown:
                            if dist2Flag < 3 and target.rank < unit.rank:
                                priorityKillingMoves += [((col,row), direction)]*7
                            elif target.rank == 3 and unit.rank>target.rank and self.army.flagIsBombProtected:
                                priorityKillingMoves += [((col,row), direction)]*3
                            elif target.rank == 10 and unit.rank == 1:
                                priorityKillingMoves += [((col,row), direction)]
                            elif target.rank < unit.rank:
                                if unit.isKnown:
                                    alreadyKnownKillingMoves += [((col,row), direction)]
                                elif unit.hasMoved:
                                    alreadyMovedKillingMoves += [((col,row), direction)]
                                else:
                                    notMovedKillingMoves += [((col,row), direction)]
                        elif highestUnknown < unit.rank and target.hasMoved:
                            if unit.hasMoved:
                                alreadyMovedKillingMoves += [((col,row), direction)]
                            else:
                                notMovedKillingMoves += [((col,row), direction)]
                        #elif 
                        elif not target.isKnown and unit.walkFar:       # our unit is a scout
                            if unit.hasMoved:
                                alreadyMovedKillingMoves += [((col,row), direction)]
                            else:
                                notMovedKillingMoves += [((col,row), direction)]
                        elif not target.isKnown and unit.rank == 5:     # lieutenants are cannon fodder
                            if unit.hasMoved:
                                alreadyMovedKillingMoves += [((col,row), direction)]
                            else:
                                notMovedKillingMoves += [((col,row), direction)]
                        elif target.isKnown and target.rank == 99 and unit.canDefuseBomb: # defuse known bomb
                            #print 'I hate bombs!'
                            defuseBombMoves += [(col,row), direction]
                        elif unit.rank == 10 and target.isKnown and target.hasMoved:  # aggressive marshal
                            #print "I'm invincible!"
                            if unit.hasMoved:
                                alreadyMovedKillingMoves += [((col,row), direction)]
                            else:
                                notMovedKillingMoves += [((col,row), direction)]
                    elif self.game.legalMove(unit, direction[0], direction[1]) and not target and direction[0] >= 0 and direction[0] < BOARD_WIDTH and direction[1] >= 0 and direction[1] < BOARD_WIDTH:
                        if unit.hasMoved:
                            if (self.army.color == "Blue" and direction == south) or (self.army.color == "Red" and direction == north):
                                alreadyMovedNotKillingMoves += [((col,row), direction)]*3
                            else:
                                alreadyMovedNotKillingMoves += [((col,row), direction)]
                        else:
                            if (self.army.color == "Blue" and direction == south) or (self.army.color == "Red" and direction == north):
                                notMovedNotKillingMoves += [((col,row), direction)]*3
                            else:
                                notMovedNotKillingMoves += [((col,row), direction)]

        if len(priorityKillingMoves) >= 1:
            move = choice(priorityKillingMoves)
            return move
        elif len(defuseBombMoves) >= 1:
            move = choice(defuseBombMoves)
            return move
        elif len(alreadyKnownKillingMoves) >= 1:
            move = choice(alreadyKnownKillingMoves)
            return move
        elif len(alreadyMovedKillingMoves) >= 1:
            move = choice(alreadyMovedKillingMoves)
            return move
        elif len(alreadyMovedNotKillingMoves) >= 1:
            move = choice(alreadyMovedNotKillingMoves)
            return move
        elif len(notMovedKillingMoves) >= 1:
            move = choice(notMovedKillingMoves)
            return move
        elif len(notMovedNotKillingMoves) >= 1:
            move = choice(notMovedNotKillingMoves)
            return move

                    
                                     
        # use randombrain as a last resort - maybe player has encircled us with unknown units?
        #print 'this is my last resort!'
        tempBrain = randomBrain.Brain(self.game, self.army)
        return tempBrain.findMove()

    def observe(self, armies):
        pass
