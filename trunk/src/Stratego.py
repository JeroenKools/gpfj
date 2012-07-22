'''
Stratego
By Jeroen Kools and Fedde Burgers

Developed for the course "Game Programming" at the University of Amsterdam
2012
'''

from Army import Army
from constants import *
import Brain, randomBrain

from Tkinter import *
import tkMessageBox
from PIL import Image, ImageTk

from math import sin, pi
import webbrowser
from textwrap import fill, dedent


class Application:
    def __init__(self, root):
        self.root = root

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
        Button(toolbar, text="Settings", width=6, command=self.settings).pack(side=LEFT, padx=2, pady=2)
        Button(toolbar, text="Stats", width=6, command=self.statistics).pack(side=LEFT, padx=2, pady=2)
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

        self.sidePanel.pack(side=RIGHT, fill=Y)
        self.sidePanel.bind("<Button-1>", self.panelClick)
        for child in self.sidePanel.winfo_children():
            child.bind("<Button-1>", self.panelClick)

        # Create map 
        self.boardsize = BOARD_WIDTH * TILE_PIX
        grassImage = Image.open("%s/%s" % (TERRAIN_DIR, LAND_TEXTURE))
        grassImage = grassImage.resize((BOARD_WIDTH * TILE_PIX, BOARD_WIDTH * TILE_PIX), Image.BICUBIC)
        self.grassImage = ImageTk.PhotoImage(grassImage)
        waterImage = Image.open("%s/%s" % (TERRAIN_DIR, WATER_TEXTURE))
        waterImage = waterImage.resize((TILE_PIX, TILE_PIX), Image.BICUBIC)
        self.waterImage = ImageTk.PhotoImage(waterImage)
        self.mapFrame = Frame(root, relief=SUNKEN, bd=2)
        self.mapFrame.pack(side=RIGHT, fill=BOTH, expand=1)
        self.map = Canvas(self.mapFrame, width=self.boardsize, height=self.boardsize)
        self.map.pack(side=RIGHT, fill=BOTH, expand=1)

        # Key bindings
        root.bind("<Escape>", self.exit)
        self.map.bind("<Button-1>", self.mapClick)
        self.root.bind("<Button-3>", self.rightClick)
        self.root.bind("p", self.quickplace)

        self.braintypes = {"Blue": randomBrain,
                           "Red": 0}
        self.firstMove = "Red"

        self.newGame()

    def newGame(self):
        # TODO: lose ongoing game confirmation  

        # interaction vars
        self.clickedUnit = None
        self.placingUnit = False
        self.movingUnit = False
        self.turn = self.firstMove
        self.won = False
        self.started = False

        # Initialize armies and brains
        self.blueArmy = Army("classical", "Blue")
        self.redArmy = Army("classical", "Red")
        self.brains = {"Blue": self.braintypes["Blue"].Brain(self.blueArmy) if self.braintypes["Blue"] else 0,
                           "Red": self.braintypes["Red"].Brain(self.redArmy) if self.braintypes["Red"] else 0}

        if self.brains["Blue"]:
            self.brains["Blue"].placeArmy()

        if self.brains["Red"]:
            self.brains["Red"].placeArmy()
            self.started = True
        else:
            self.unitsPlaced = 0

        self.drawSidePanels()
        self.drawMap()

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
        webbrowser.open("http://code.google.com/p/gpfj")

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
        self.map.delete(ALL)

        # fill entire map with green
        #self.map.create_rectangle(0, 0, self.boardsize, self.boardsize, fill=GRASS_COLOR)
        self.map.create_image(0, 0, image=self.grassImage, anchor=NW)

        # draw water
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_WIDTH):
                if self.isPool(x, y):
                    self.map.create_image(x * TILE_PIX, y * TILE_PIX, image=self.waterImage, anchor=NW)
                    #self.drawTile(x, y, WATER_COLOR)

        # draw lines
        for i in range(BOARD_WIDTH - 1):
            x = TILE_PIX * (i + 1)
            self.map.create_line(x, 0, x, self.boardsize, fill="black")
            self.map.create_line(0, x, self.boardsize, x, fill="black")

        for unit in self.redArmy.army:
            if unit.alive:
                (x, y) = unit.getPosition()
                self.drawUnit(self.map, unit, x, y, RED_PLAYER_COLOR)

        for unit in self.blueArmy.army:
            if unit.alive:
                (x, y) = unit.getPosition()
                self.drawUnit(self.map, unit, x, y, BLUE_PLAYER_COLOR)

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
                self.drawUnit(self.redUnitPanel, unit, x, y, RED_PLAYER_COLOR, unit.alive)
                unplacedRed += 1

        unplacedBlue = 0
        for unit in self.blueArmy.army:
            if unit.isOffBoard():
                x = unplacedBlue % 10
                y = unplacedBlue / 10
                unit.setPosition(self.offBoard(x), self.offBoard(y))
                if not unit.alive:
                    self.drawUnit(self.blueUnitPanel, unit, x, y, BLUE_PLAYER_COLOR, False)
                unplacedBlue += 1

    def drawUnit(self, canvas, unit, x, y, color, alive=True):
        canvas.create_rectangle(x * TILE_PIX, y * TILE_PIX,
                                (x + 1) * TILE_PIX, (y + 1) * TILE_PIX,
                                fill=color, outline=None)
        if unit.color == "Red" or DEBUG or not alive:
            canvas.create_image(x * TILE_PIX, y * TILE_PIX, image=unit.getIcon(), anchor=NW)

        if not alive:
            canvas.create_line(x * TILE_PIX, y * TILE_PIX,
                               (x + 1) * TILE_PIX, (y + 1) * TILE_PIX,
                               width=3, fill=DEAD_COLOR, capstyle=ROUND)
            canvas.create_line(x * TILE_PIX, (y + 1) * TILE_PIX,
                               (x + 1) * TILE_PIX, y * TILE_PIX,
                               width=3, fill=DEAD_COLOR, capstyle=ROUND)

    def isPool(self, x, y):
        """Check whether there is a pool at tile (x,y)."""

        # uneven board size + middle row or even board size + middle 2 rows
        if  (BOARD_WIDTH % 2 == 1 and y == BOARD_WIDTH / 2) or \
            ((BOARD_WIDTH % 2 == 0) and (y == BOARD_WIDTH / 2 or y == (BOARD_WIDTH / 2) - 1)):

            if sin(2 * pi * (x + .5) / BOARD_WIDTH * (POOLS + 0.5)) < 0:
                return True
            else:
                return False

    def rightClick(self, event):
        self.clickedUnit = None
        self.movingUnit = False
        self.drawMap()
        self.drawSidePanels()
        self.setStatusBar("")

    def mapClick(self, event):
        """Process clicks on the map widget."""

        x = event.x / TILE_PIX
        y = event.y / TILE_PIX

        if self.isPool(x, y):
            type = 'water'
        else:
            type = 'land'

        if self.placingUnit:
            self.placeUnit(x, y)

        elif self.movingUnit and not self.won:
            self.moveUnit(x, y)

        else:
            # find clicked unit
            unit = self.getUnit(x, y)

            if unit:
                if unit.color == "Blue":
                    self.setStatusBar("You clicked an enemy unit at (%s, %s)" % (x, y))
                    return

                else:
                    if unit.isMovable():
                        self.movingUnit = True
                        self.clickedUnit = unit
                        self.drawUnit(self.map, unit, x, y, SELECTED_RED_PLAYER_COLOR)

            else:
                unit = "no unit at (%s, %s)" % (x, y)

            self.setStatusBar("You clicked a %s tile with %s" % (type, unit))

    def placeUnit(self, x, y):
        if self.isPool(x, y):
            self.setStatusBar("You can't place units in the water!")
            return

        if self.getUnit(x, y):
            self.setStatusBar("Can't place %s there, spot already taken!" % self.clickedUnit.name)
            return

        if y < (BOARD_WIDTH - 4):
            self.setStatusBar("Must place unit in the first 4 rows")
            return

        self.clickedUnit.setPosition(x, y)
        self.setStatusBar("Placed %s" % self.clickedUnit)
        self.placingUnit = False
        self.clickedUnit = None
        self.unitsPlaced += 1
        if self.unitsPlaced == len(self.redArmy.army):
            self.started = True

        self.drawSidePanels()
        self.drawMap()

    def moveUnit(self, x, y):
        if not self.legalMove(self.clickedUnit, x, y):
            self.setStatusBar("You can't move there!")
            return

        target = self.getUnit(x, y)
        if target:
            if target.color == self.clickedUnit.color:
                self.setStatusBar("You can't move there - tile already occupied!")
            else:
                self.attack(self.clickedUnit, target)

        else:
            self.setStatusBar("Moved %s to (%s, %s)" % (self.clickedUnit, x, y))
            self.clickedUnit.setPosition(x, y)

        self.clickedUnit = None
        self.movingUnit = False

        self.drawMap()

        if self.started:
            self.endTurn()

    def endTurn(self):
        self.turn = "Blue" if self.turn == "Red" else "Blue"

        if self.brains[self.turn] and not self.won: # computer player?
            (oldlocation, move) = self.brains[self.turn].doMove(self)
            self.setStatusBar("%s moves unit at %s to %s" % (self.turn, oldlocation, move))

            self.drawMap()
            self.drawSidePanels()

        self.turn = "Blue" if self.turn == "Red" else "Blue"

    def legalMove(self, unit, x, y):
        """Check whether a move:
            - does not end in the water
            - is only in one direction
            - is not farther than one step, for non-scouts
            - does not jump over obstacles, for scouts
        """

        if self.isPool(x, y):
            return False

        (ux, uy) = unit.position
        dx = abs(ux - x)
        dy = abs(uy - y)

        if not self.started:
            if y < (BOARD_WIDTH - 4):
                return False
            return True

        if unit.walkFar:
            if ux != x and uy != y:
                return False

            if uy == y:
                x0 = min(x, ux)
                x1 = max(x, ux)
                for i in range(x0 + 1, x1):
                    if self.isPool(i, y) or self.getUnit(i, y):
                        return False

            elif ux == x:
                y0 = min(y, uy)
                y1 = max(y, uy)
                for i in range(y0 + 1, y1):
                    if self.isPool(x, i) or self.getUnit(x, i):
                        return False

        else:
            if (dx + dy) != 1:
                return False

        return True

    def attack(self, attacker, defender):

        text = "A %s %s attacked a %s %s. " % (attacker.color, attacker.name, defender.color, defender.name)

        if defender.name == "Flag":
            attacker.position = defender.position
            defender.die()
            self.victory(attacker.color)

        elif attacker.canDefuseBomb and defender.name == "Bomb":
            attacker.position = defender.position
            defender.die()
            text += "The mine was disabled."

        elif attacker.canKillMarshal and defender.name == "Marshal":
            attacker.position = defender.position
            defender.die()
            text += "The marshal has been assassinated."

        elif attacker.rank > defender.rank:
            attacker.position = defender.position
            defender.die()
            text += "The %s was defeated." % defender.name

        elif attacker.rank == defender.rank:
            attacker.die()
            defender.die()
            text += "Both units died."

        else:
            attacker.die()
            text += "The %s was defeated." % attacker.name

        if not self.won:
            text = fill(dedent(text), 60)
            tkMessageBox.showinfo("Battle result", text)

        self.drawMap()
        self.drawSidePanels()
        self.clickedUnit = None
        self.movingUnit = False

    def getUnit(self, x, y):
        return self.redArmy.getUnit(x, y) or self.blueArmy.getUnit(x, y)

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
            if unit:
                self.setStatusBar("You clicked on %s %s" % (panel, unit))

                if panel == "red": # clicked player unit
                    self.clickedUnit = unit
                    self.placingUnit = True

                    # highlight unit
                    self.drawUnit(self.redUnitPanel, unit, x, y, SELECTED_RED_PLAYER_COLOR)

                    self.setStatusBar("Click the map to place this unit")

    def offBoard(self, x):
        """Return negative coordinates used to indicate off-board position. Avoid zero."""
        return -x - 1

    def victory(self, color):
        self.won = True
        top = Toplevel(width=300)
        flagimg1 = Image.open("%s/%s.%s" % (ICON_DIR, "flag", ICON_TYPE))
        flagimg2 = ImageTk.PhotoImage(flagimg1)
        lbl = Label(top, image=flagimg2)
        lbl.image = flagimg2
        lbl.grid(row=0, column=1, sticky=NW)

        if color == "Red":
            top.title("Victory!")
            message = Label(top, text="Congratulations! You've captured the enemy flag!")

        else:
            top.title("Defeat!")
            message = Label(top, text="Unfortunately, the enemy has captured your flag. You lose.")

        message.grid(row=0, column=0, sticky=NE, ipadx=15, ipady=50)

        ok = Button(top, text="OK", command=top.destroy)
        ok.grid(row=1, column=0, columnspan=2, ipadx=15, ipady=5, pady=5)

        message.configure(width=40, justify=CENTER, wraplength=150)
        self.setStatusBar("%s has won the game!" % color)

    def quickplace(self, event):
        if not self.started:
            tempBrain = randomBrain.Brain(self.redArmy)
            tempBrain.placeArmy()

            self.drawMap()
            self.drawSidePanels()
            self.setStatusBar("Randomly placed your army!")
            self.started = True

    def exit(self, event=None):
        """Quit program."""

        self.root.quit()

if __name__ == "__main__":
    root = Tk()
    Application(root)
    root.title("%s %s" % (GAME_NAME, VERSION))
    root.wm_iconbitmap("%s/flag.ico" % ICON_DIR)
    root.mainloop()
