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

    # default abilities
    walkFar = False        # scout ability
    canKillMarshal = False # spy ability
    canDefuseBomb = False  # canDefuseBomb ability
    canMove = True
    sortOrder = 0

    def __init__(self, position=None):
        self.position = position

        self.alive = True
        self.justAttacked = False   # enemy units who just attacked are revealed
        self.hasMoved = False       # if a unit has moved, the AI remembers
        self.hasMovedFar = False
        self.isKnown = False          # whether the AI already knows this piece's rank 
        self.possibleMovableRanks = []
        self.possibleUnmovableRanks = []

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
            return "a %s at %s" % (self.name, self.position)
        else:
            return "Off-board %s" % (self.name)

class Icons:
    def __init__(self, tilepix):
        self.icons = {}
        for rank in ['Marshal', 'General', 'Colonel', 'Major', 'Captain', 'Lieutenant',
                     'Sergeant', 'Miner', 'Scout', 'Bomb', 'Spy', 'Flag']:
            icon = Image.open("%s/%s.%s" % (ICON_DIR, rank.lower(), ICON_TYPE))
            icon = icon.resize((2 * tilepix, 2 * tilepix), Image.BICUBIC)
            icon = icon.resize((tilepix, tilepix), Image.ANTIALIAS)
            self.icons[rank] = ImageTk.PhotoImage(icon)

    def getIcon(self, rank):
        return self.icons[rank]

    def getImage(self, rank, size):
        img = Image.open("%s/%s.%s" % (ICON_DIR, rank.lower(), ICON_TYPE))
        img = img.resize((2 * size, 2 * size), Image.BICUBIC)
        img = img.resize((size, size), Image.ANTIALIAS)
        return img

class Marshal(Unit):
    name = "Marshal"
    rank = 10
    sortOrder = 1
    def __init__(self, position=None):
        Unit.__init__(self, position)

class General(Unit):
    name = "General"
    rank = 9
    sortOrder = 2
    def __init__(self, position=None):
        Unit.__init__(self, position)

class Colonel(Unit):
    name = "Colonel"
    rank = 8
    sortOrder = 3
    def __init__(self, position=None):
        Unit.__init__(self, position)

class Major(Unit):
    name = "Major"
    rank = 7
    sortOrder = 4
    def __init__(self, position=None):
        Unit.__init__(self, position)

class Captain(Unit):
    name = "Captain"
    rank = 6
    sortOrder = 5
    def __init__(self, position=None):
        Unit.__init__(self, position)

class Lieutenant(Unit):
    name = "Lieutenant"
    rank = 5
    sortOrder = 6
    def __init__(self, position=None):
        Unit.__init__(self, position)

class Sergeant(Unit):
    name = "Sergeant"
    rank = 4
    sortOrder = 7
    def __init__(self, position=None):
        Unit.__init__(self, position)

class Miner(Unit):
    name = "Miner"
    rank = 3
    sortOrder = 8

    canDefuseBomb = True

    def __init__(self, position=None):
        Unit.__init__(self, position)

class Scout(Unit):
    name = "Scout"
    rank = 2
    sortOrder = 9

    walkFar = True # special scout ability!    

    def __init__(self, position=None):
        Unit.__init__(self, position)

class Spy(Unit):
    name = "Spy"
    rank = 1
    sortOrder = 10

    canKillMarshal = True

    def __init__(self, position=None):
        Unit.__init__(self, position)

class Bomb(Unit):
    name = "Bomb"
    rank = 99
    sortOrder = 11

    canMove = False

    def __init__(self, position=None):
        Unit.__init__(self, position)

class Flag(Unit):
    name = "Flag"
    rank = 0
    sortOrder = 0

    canMove = False

    def __init__(self, position=None):
        Unit.__init__(self, position)
