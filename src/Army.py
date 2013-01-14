from constants import *
from Tkinter import PhotoImage
import Image, ImageTk

class Army:
    ranks = ['marshal', 'general', 'colonel', 'major', 'captain',
             'lieutenant', 'sergeant', 'canDefuseBomb', 'scout', 'spy', 'bomb', 'flag']

    def __init__(self, armyType="classical", color="Red", size=40):
        """Represents a Stratego army as a list of Units."""

        self.armyType = armyType
        self.color = color
        self.flagIsBombProtected = False
        self.livingPossibleMovableRanks = []
        self.livingPossibleUnmovableRanks = []
        self.nrOfMoved = 0
        self.nrOfLiving = 0
        #self.nrOfKnownUnmovable = 0
        self.nrOfUnknownMoved = 0
        self.nrOfKnownMovable = 0
        self.nrOfKnownUnmovable = 0
        self.nrOfMovable = 0
        self.nrOfUnmovable = 0

        self.carefullness = 0.9

        if armyType == "classical":
            self.army = [
                          Flag(),
                          Marshal(),
                          General(),
                          Colonel(), Colonel(),
                          Major(), Major(), Major(),
            ]

            scaled = 0
            rankDict = {Captain: 4 / 31.,
                         Lieutenant: 4 / 31.,
                         Sergeant: 4 / 31.,
                         Miner: 5 / 31.,
                         Scout: 8 / 31.}

            for rank, nr in rankDict.items():
                for i in range(int(round(nr * (size - 9)))):
                    self.army.append(rank())
                    scaled += 1

            for i in range(size - scaled - 9):
                self.army.append(Bomb())

            self.army.append(Spy())

        else:
            pass # TODO: add other army options

        self.nr_of_bombs = 0;

        for unit in self.army:
            if unit.name == 'Bomb':
                self.nr_of_bombs += 1

        for unit in self.army:
            unit.color = self.color
            self.nrOfLiving += 1

        for unit in self.army:
            if unit.canMove:
                self.livingPossibleMovableRanks.append(unit.name)
                self.nrOfMovable += 1
            else:
                self.livingPossibleUnmovableRanks.append(unit.name)
                self.nrOfUnmovable += 1

        for unit in self.army:
            unit.possibleMovableRanks = list(self.livingPossibleMovableRanks)
            unit.possibleUnmovableRanks = list(self.livingPossibleUnmovableRanks)



    def getUnit(self, x, y):
        for unit in self.army:
            if unit.getPosition() == (x, y):
                return unit

    def highestAlive(self):
        highest = 0
        for unit in self.army:
            if unit.rank > Marshal().rank: # ignore bombs and funny stuff
                continue
            if unit.alive and unit.rank > highest:
                highest = unit.rank
        return highest

    def highestUnknown(self):
        """Return the highest possible rank that a unit who's rank is unknown can have"""
        highest = 0
        for unit in self.army:
            if unit.rank > Marshal().rank: # ignore bombs and funny stuff
                continue
            if unit.alive and not unit.isKnown and unit.rank > highest:
                highest = unit.rank
        return highest
    
    def nrAlive(self):
        """Return the number of units in the army that have not been defeated"""
        alive = 0
        for unit in self.army:
            if unit.alive: alive += 1
        return alive

class Unit:
    def __init__(self, position=None):
        self.position = position

        self.walkFar = False        # scout ability
        self.canKillMarshal = False # spy ability
        self.canDefuseBomb = False  # canDefuseBomb ability
        self.canMove = True
        self.alive = True
        self.justAttacked = False   # enemy units who just attacked are revealed
        self.hasMoved = False       # if a unit has moved, the AI remembers
        self.hasMovedFar = False
        self.isKnown = False          # whether the AI already knows this piece's rank 
        self.possibleMovableRanks = []
        self.possibleUnmovableRanks = [] 
        
        self.sortOrder = 0

    def getPosition(self):
        return self.position

    def setPosition(self, x, y):
        self.position = (x, y)

    def isOffBoard(self):
        if self.position is None:
            return True
        if self.position[0] < 0 and self.position[1] < 0:
            return True
        else: return False

    def die(self):
        self.alive = False
        self.position = None
        
    def isMovable(self):
        return self.canMove

    def __str__(self):
        if self.position:
            return "%s at %s" % (self.name, self.position)
        else:
            return "Off-board %s" % (self.name)
        
class Icons:
    def __init__(self, tilepix):
        self.icons = {}
        for rank in ['Marshal', 'General', 'Colonel', 'Major', 'Captain', 'Lieutenant',
                     'Sergeant', 'Miner', 'Scout', 'Bomb', 'Spy', 'Flag']:
            icon = Image.open("%s/%s.%s" % (ICON_DIR, rank, ICON_TYPE))
            icon = icon.resize((2 * tilepix, 2 * tilepix), Image.BICUBIC)
            icon = icon.resize((tilepix, tilepix), Image.ANTIALIAS)
            self.icons[rank] = ImageTk.PhotoImage(icon)
            
    def getIcon(self, rank):
        return self.icons[rank]
    
    def getImage(self, rank, size):   
        img = Image.open("%s/%s.%s" % (ICON_DIR, rank, ICON_TYPE))
        img = img.resize((2 * size, 2 * size), Image.BICUBIC)
        img = img.resize((size, size), Image.ANTIALIAS)
        return img     

class Marshal(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.name = "Marshal"
        self.rank = 10
        self.sortOrder = 1

class General(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.name = "General"
        self.rank = 9
        self.sortOrder = 2

class Colonel(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.name = "Colonel"
        self.rank = 8
        self.sortOrder = 3

class Major(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.name = "Major"
        self.rank = 7
        self.sortOrder = 4

class Captain(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.name = "Captain"
        self.rank = 6
        self.sortOrder = 5

class Lieutenant(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.name = "Lieutenant"
        self.rank = 5
        self.sortOrder = 6

class Sergeant(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.name = "Sergeant"
        self.rank = 4
        self.sortOrder = 7

class Miner(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.name = "Miner"
        self.rank = 3
        self.sortOrder = 8

        self.canDefuseBomb = True

class Scout(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.name = "Scout"
        self.rank = 2
        self.sortOrder = 9

        self.walkFar = True # special scout ability!

class Spy(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.name = "Spy"
        self.rank = 1
        self.sortOrder = 10

        self.canKillMarshal = True

class Bomb(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.name = "Bomb"
        self.rank = 99
        self.sortOrder = 11

        self.canMove = False

class Flag(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.name = "Flag"
        self.rank = 0
        self.sortOrder = 0

        self.canMove = False
