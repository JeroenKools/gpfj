from constants import *
from Tkinter import PhotoImage


class Army:
    ranks = ['marshal', 'general', 'colonel', 'major', 'captain',
             'lieutenant', 'sergeant', 'miner', 'scout', 'spy', 'bomb', 'flag']

    def __init__(self, armyType="classical"):
        """Represents a Stratego army as a list of Units."""

        if armyType == "classical":
            self.army = [
                          Marshal(),
                          General(),
                          Colonel(), Colonel(),
                          Major(), Major(), Major(),
                          Captain(), Captain(), Captain(), Captain(),
                          Lieutenant(), Lieutenant(), Lieutenant(), Lieutenant(),
                          Sergeant(), Sergeant(), Sergeant(), Sergeant(),
                          Miner(), Miner(), Miner(), Miner(), Miner(),
                          Scout(), Scout(), Scout(), Scout(), Scout(), Scout(), Scout(), Scout(),
                          Spy(),
                          Bomb(), Bomb(), Bomb(), Bomb(), Bomb(), Bomb(),
                          Flag()
            ]
        else:
            pass # TODO: add other army options

    def getUnit(self, x, y):
        for unit in self.army:
            if unit.getPosition() == (x, y):
                return unit

class Unit:
    def __init__(self, position=None):
        self.position = position
        self.icon = PhotoImage(file="%s/%s.%s" % (ICON_DIR, self.name, ICON_TYPE))

        self.walkFar = False        # scout ability
        self.killMarshall = False   # spy ability
        self.canMove = True
        self.alive = True

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

    def getIcon(self):
        return self.icon

    def isMovable(self):
        return self.canMove

    def __str__(self):
        if self.position:
            return "%s at %s" % (self.name, self.position)
        else:
            return "Off-board %s" % (self.type)

class Marshal(Unit):
    def __init__(self, position=None):
        self.name = "Marshal"
        self.rank = 10
        Unit.__init__(self, position)

class General(Unit):
    def __init__(self, position=None):
        self.name = "General"
        self.rank = 9
        Unit.__init__(self, position)

class Colonel(Unit):
    def __init__(self, position=None):
        self.name = "Colonel"
        self.rank = 8
        Unit.__init__(self, position)


class Major(Unit):
    def __init__(self, position=None):
        self.name = "Major"
        self.rank = 7
        Unit.__init__(self, position)

class Captain(Unit):
    def __init__(self, position=None):
        self.name = "Captain"
        self.rank = 6
        Unit.__init__(self, position)

class Lieutenant(Unit):
    def __init__(self, position=None):
        self.name = "Lieutenant"
        self.rank = 5
        Unit.__init__(self, position)

class Sergeant(Unit):
    def __init__(self, position=None):
        self.name = "Sergeant"
        self.rank = 4
        Unit.__init__(self, position)

class Miner(Unit):
    def __init__(self, position=None):
        self.name = "Miner"
        self.rank = 3
        Unit.__init__(self, position)

class Scout(Unit):
    def __init__(self, position=None):
        self.name = "Scout"
        self.rank = 2
        Unit.__init__(self, position)

        self.moveFar = True # special scout ability!

class Spy(Unit):
    def __init__(self, position=None):
        self.name = "Spy"
        self.rank = 1
        Unit.__init__(self, position)

        self.killMarshall = True

class Bomb(Unit):
    def __init__(self, position=None):
        self.name = "Bomb"
        self.rank = 99
        Unit.__init__(self, position)

        self.canMove = False

class Flag(Unit):
    def __init__(self, position=None):
        self.name = "Flag"
        self.rank = 0
        Unit.__init__(self, position)

        self.canMove = False
