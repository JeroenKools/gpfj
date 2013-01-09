'''
Created on 29 jun. 2012

@author: Jeroen Kools
'''
import Brain
from constants import *
from random import shuffle, choice, randint

BOARD_WIDTH = 0

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
                              self.game.legalMove(unit, direction[0], direction[1])]

                if len(directions) >= 1:
                    move = choice(directions)
                    return ((col, row), move)

        return (None, None) # no legal move - lost!

    def observe(self, armies):
        pass
