'''
Stratego
By Jeroen Kools and Fedde Burgers

Developed for the course "Game Programming" at the University of Amsterdam
2012
'''

from Tkinter import *
from math import sin, pi
from Army import Army
import tkMessageBox
from constants import *
from textwrap import fill, dedent

class StrategoGUI:
    def __init__(self, root):
        self.root = root
        root.bind("<Escape>", self.exit)

        # Initialize armies
        self.blueArmy = Army()
        self.redArmy = Army()

        # Create menu bar
        menuBar = Menu(root)

        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="New Game", command=self.newGame)
        fileMenu.add_command(label="Load Game", command=self.loadGame)
        fileMenu.add_command(label="Save Game", command=self.saveGame)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.exit)
        menuBar.add_cascade(label="File", menu=fileMenu)

        optionMenu = Menu(menuBar, tearoff=0)
        optionMenu.add_command(label="Settings", command=self.settings)
        optionMenu.add_command(label="Statistics", command=self.statistics)
        menuBar.add_cascade(label="Options", menu=optionMenu)

        helpmenu = Menu(menuBar, tearoff=0)
        helpmenu.add_command(label="Help", command=self.help)
        helpmenu.add_command(label="Visit Website", command=self.visitWebsite)
        helpmenu.add_command(label="About", command=self.about)
        menuBar.add_cascade(label="Help", menu=helpmenu)

        root.config(menu=menuBar)

        # Create toolbar        
        toolbar = Frame(root)
        Button(toolbar, text="New", width=6, command=self.newGame).pack(side=LEFT, padx=2, pady=2)
        Button(toolbar, text="Load", width=6, command=self.loadGame).pack(side=LEFT, padx=2, pady=2)
        Button(toolbar, text="Save", width=6, command=self.saveGame).pack(side=LEFT, padx=2, pady=2)
        Button(toolbar, text="Settings", width=6, command=self.newGame).pack(side=LEFT, padx=2, pady=2)
        Button(toolbar, text="Stats", width=6, command=self.newGame).pack(side=LEFT, padx=2, pady=2)
        toolbar.pack(side=TOP, fill=X)

        # Create status bar
        self.statusBar = Label(root, text="", bd=1, relief=SUNKEN, anchor=W)
        self.statusBar.pack(side=BOTTOM, fill=X)
        self.setStatusBar("Welcome!")

        # Create side panel
        self.sidePanel = Frame(root, relief=SUNKEN, bd=2)

        Label(self.sidePanel, width=20, text="Blue").pack(side=TOP, pady=3)
        self.blueUnitPanel = Canvas(self.sidePanel, height=4 * TILE_PIX, width=10 * TILE_PIX)
        self.blueUnitPanel.pack(side=TOP)

        Label(self.sidePanel, width=20, text="Red").pack(side=BOTTOM, pady=4)
        self.redUnitPanel = Canvas(self.sidePanel, height=4 * TILE_PIX, width=10 * TILE_PIX)
        self.redUnitPanel.pack(side=BOTTOM)

        self.drawSidePanels()
        self.sidePanel.pack(side=RIGHT, fill=Y)
        self.sidePanel.bind("<Button-1>", self.panelClick)
        for child in self.sidePanel.winfo_children():
            child.bind("<Button-1>", self.panelClick)

        # Create map 
        self.boardsize = BOARD_WIDTH * TILE_PIX
        self.mapFrame = Frame(root, relief=SUNKEN, bd=2)
        self.mapFrame.pack(side=RIGHT, fill=BOTH, expand=1)
        self.map = Canvas(self.mapFrame, width=self.boardsize, height=self.boardsize)
        self.map.pack(side=RIGHT, fill=BOTH, expand=1)
        self.map.bind("<Button-1>", self.mapClick)
        self.drawMap()

    def newGame(self):
        tkMessageBox.showinfo("%s %s" % (GAME_NAME, VERSION), "To be implemented!")

    def loadGame(self):
        tkMessageBox.showinfo("%s %s" % (GAME_NAME, VERSION), "To be implemented!")

    def saveGame(self):
        tkMessageBox.showinfo("%s %s" % (GAME_NAME, VERSION), "To be implemented!")

    def settings(self):
        tkMessageBox.showinfo("%s %s" % (GAME_NAME, VERSION), "To be implemented!")

    def statistics(self):
        tkMessageBox.showinfo("%s %s" % (GAME_NAME, VERSION), "To be implemented!")

    def help(self):
        tkMessageBox.showinfo("%s %s" % (GAME_NAME, VERSION), "To be implemented!")

    def visitWebsite(self):
        tkMessageBox.showinfo("%s %s" % (GAME_NAME, VERSION), "To be implemented!")

    def about(self):
        text = """\
        Stratego is a game developed by Jeroen Kools and Fedde Burgers
        for the course 'Game Programming' at the University of Amsterdam in 2012.
        """

        text = fill(dedent(text), 60)
        tkMessageBox.showinfo("%s %s" % (GAME_NAME, VERSION), text)

    def setStatusBar(self, newText):
        """Change the text in the status bar."""

        self.statusBar.config(text=newText)

    def drawMap(self):
        """Draw the tiles and units on the map."""

        # fill with green
        self.map.create_rectangle(0, 0, self.boardsize, self.boardsize, fill=GRASS_COLOR)

        # draw lines
        for i in range(BOARD_WIDTH - 1):
            x = TILE_PIX * (i + 1)
            self.map.create_line(x, 0, x, self.boardsize, fill="black")
            self.map.create_line(0, x, self.boardsize, x, fill="black")

        # draw water
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_WIDTH):
                if self.isPool(x, y):
                    self.drawTile(x, y, WATER_COLOR)

        # TODO: draw units on map
        for unit in self.redArmy.army:
            pass

        for unit in self.blueArmy.army:
            pass

    def drawTile(self, x, y, tileColor):
        """Fill a tile with its background color."""

        self.map.create_rectangle(x * TILE_PIX, y * TILE_PIX, (x + 1) * TILE_PIX, (y + 1) * TILE_PIX, fill=tileColor)

    def drawSidePanels(self):
        """Draw the unplaced units in the sidebar widget."""

        self.blueUnitPanel.create_rectangle(0, 0, 10 * TILE_PIX, 4 * TILE_PIX, fill=UNIT_PANEL_COLOR)
        self.redUnitPanel.create_rectangle(0, 0, 10 * TILE_PIX, 4 * TILE_PIX, fill=UNIT_PANEL_COLOR)

        unplacedRed = 0
        for unit in self.redArmy.army:
            if unit.isOffBoard():
                x = unplacedRed % 10
                y = unplacedRed / 10
                unit.setPosition(self.offBoard(x), self.offBoard(y))
                self.redUnitPanel.create_image(x * TILE_PIX, y * TILE_PIX, image=unit.getIcon(), anchor=NW)
                unplacedRed += 1


    def isPool(self, x, y):
        """Check whether there is a pool at tile (x,y)."""

        # uneven board size + middle row or even board size + middle 2 rows
        if  (BOARD_WIDTH % 2 == 1 and y == BOARD_WIDTH / 2) or \
            ((BOARD_WIDTH % 2 == 0) and (y == BOARD_WIDTH / 2 or y == (BOARD_WIDTH / 2) - 1)):

            if sin(2 * pi * (x + .5) / BOARD_WIDTH * (POOLS + 0.5)) < 0:
                return True
            else:
                return False

    def mapClick(self, event):
        """Process clicks on the map widget."""

        x = event.x / TILE_PIX
        y = event.y / TILE_PIX

        if self.isPool(x, y):
            type = 'water'
        else:
            type = 'land'

        unit = 'no unit'

        self.setStatusBar("You clicked (%s, %s); a %s tile with %s" % (x, y, type, unit))

    def panelClick(self, event):
        """Process mouse clicks on the side panel widget."""
        x = event.x / TILE_PIX
        y = event.y / TILE_PIX

        if event.widget == self.redUnitPanel:
            panel = "red"
            army = self.redArmy
        elif event.widget == self.blueUnitPanel:
            panel = "blue"
            army = self.blueArmy
        else:
            panel = ""

        if panel:
            unit = army.getUnit(self.offBoard(x), self.offBoard(y))
            self.setStatusBar("You clicked on %s %s" % (panel, unit))

            # TODO: unit placement
            # 1. check whether unit is unplaced or dead
            # 2. highlight unit and give help text in status bar
            # 3. update map and panel when unit is placed

    def offBoard(self, x):
        return -x - 1

    def exit(self, event=None):
        """Quits program."""

        self.root.quit()

if __name__ == "__main__":
    root = Tk()
    StrategoGUI(root)
    root.title("Stratego %s" % VERSION)
    #root.iconbitmap("icon") # TODO: window icon
    root.mainloop()
