from constants import *
from Tkinter import PhotoImage


class Army:
    ranks = ['marshal', 'general', 'colonel', 'major', 'captain',
             'lieutenant', 'sergeant', 'miner', 'scout', 'spy', 'bomb', 'flag']

    def __init__(self):
        """Represents a Stratego army as a list of Units."""

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

    def getUnit(self, x, y):
        for unit in self.army:
            if unit.getPosition() == (x, y):
                return unit

class Unit:
    def __init__(self, position=None):
        self.position = position
        self.alive = True
        self.walkFar = False        # scout ability
        self.killMarshall = False    # spy ability

    def getPosition(self):
        return self.position

    def isOffBoard(self):
        if self.position is None:
            return True
        else: return False

    def setPosition(self, x, y):
        self.position = (x, y)

    def die(self):
        self.alive = False
        self.position = None

    def getIcon(self):
        return self.icon

    def __str__(self):
        if self.position:
            return "%s at %s" % (self.name, self.position)
        else:
            return "Off-board %s" % (self.type)

class Marshal(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.moving = True
        self.rank = 10
        self.name = "Marshal"
        self.icon = PhotoImage(file="%s/%s.%s" % (ICON_DIR, self.name, ICON_TYPE))

class General(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.moving = True
        self.rank = 9
        self.name = "General"
        self.icon = PhotoImage(file="%s/%s.%s" % (ICON_DIR, self.name, ICON_TYPE))

class Colonel(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.moving = True
        self.rank = 8
        self.name = "Colonel"
        self.icon = PhotoImage(file="%s/%s.%s" % (ICON_DIR, self.name, ICON_TYPE))

class Major(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.moving = True
        self.rank = 7
        self.name = "Major"
        self.icon = PhotoImage(file="%s/%s.%s" % (ICON_DIR, self.name, ICON_TYPE))

class Captain(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.moving = True
        self.rank = 6
        self.name = "Captain"
        self.icon = PhotoImage(file="%s/%s.%s" % (ICON_DIR, self.name, ICON_TYPE))

class Lieutenant(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.moving = True
        self.rank = 5
        self.name = "Lieutenant"
        self.icon = PhotoImage(file="%s/%s.%s" % (ICON_DIR, self.name, ICON_TYPE))

class Sergeant(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.moving = True
        self.rank = 4
        self.name = "Sergeant"
        self.icon = PhotoImage(file="%s/%s.%s" % (ICON_DIR, self.name, ICON_TYPE))

class Miner(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.moving = True
        self.rank = 3
        self.name = "Miner"
        self.icon = PhotoImage(file="%s/%s.%s" % (ICON_DIR, self.name, ICON_TYPE))

class Scout(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.moving = True
        self.moveFar = True # special scout ability!
        self.rank = 2
        self.name = "Scout"
        self.icon = PhotoImage(file="%s/%s.%s" % (ICON_DIR, self.name, ICON_TYPE))

class Spy(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.moving = True
        self.killMarshall = True
        self.rank = 1
        self.name = "Spy"
        self.icon = PhotoImage(file="%s/%s.%s" % (ICON_DIR, self.name, ICON_TYPE))

class Bomb(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.moving = False
        self.rank = 99
        self.name = "Bomb"
        self.icon = PhotoImage(file="%s/%s.%s" % (ICON_DIR, self.name, ICON_TYPE))

class Flag(Unit):
    def __init__(self, position=None):
        Unit.__init__(self, position)
        self.moving = False
        self.rank = 0
        self.name = "Flag"
        self.icon = PhotoImage(file="%s/%s.%s" % (ICON_DIR, self.name, ICON_TYPE))
