'''
By Jeroen Kools and Fedde Burgers

Developed for the course "Game Programming" at the University of Amsterdam
2012
'''

from Army import Army, Icons
from constants import *
import Brain, randomBrain, SmartBrain, CarefulBrain

from Tkinter import *
import tkMessageBox
import tkFileDialog
import Image, ImageTk
try:
    import winsound
    playSound = True
except: # not on Windows
    playSound = False

from math import sin, pi
import webbrowser
import os
import pickle
import datetime
from textwrap import fill, dedent, TextWrapper


class Application:
    def __init__(self, root):
        self.root = root
        self.defaultBrainName = "SmartBrain" # Brain used for the first game, can be changed in settings
        self.blueBrain = eval(self.defaultBrainName)
        self.redBrain = 0
        self.blueBrainName = self.defaultBrainName
        self.unitIcons = Icons()

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
        optionMenu.add_command(label="Statistics", command=self.showStats)
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
        Button(toolbar, text="Stats", width=6, command=self.showStats).pack(side=LEFT, padx=2, pady=2)
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
        self.root.protocol("WM_DELETE_WINDOW", self.exit)

        self.firstMove = "Red"
        self.loadStats()
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
        self.armyHeight = min(4, (BOARD_WIDTH - 2) / 2)
        self.braintypes = {"Blue": self.blueBrain,
                           "Red": self.redBrain}
        self.blueArmy = Army("classical", "Blue", BOARD_WIDTH * self.armyHeight)
        self.redArmy = Army("classical", "Red", BOARD_WIDTH * self.armyHeight)
        self.brains = {"Blue": self.braintypes["Blue"].Brain(self, self.blueArmy) if self.braintypes["Blue"] else 0,
                           "Red": self.braintypes["Red"].Brain(self, self.redArmy) if self.braintypes["Red"] else 0}

        if self.brains["Blue"]:
            self.brains["Blue"].placeArmy(self.armyHeight)

        if self.brains["Red"]:
            self.brains["Red"].placeArmy(self.armyHeight)
            self.started = True
        else:
            self.unitsPlaced = 0

        self.drawSidePanels()
        self.drawMap()
        self.setStatusBar("Place your army, or press 'p' for random placement")

    def loadGame(self):
        loadFilename = tkFileDialog.askopenfilename(defaultextension=".sav",
                                                    filetypes =  [('%s saves' % GAME_NAME, '.sav')],
                                                      initialdir = os.getcwd())
        if loadFilename:
            with open(loadFilename, 'r') as f:
                save = pickle.load(f)
                BOARD_WIDTH = save['BOARD_WIDTH']
                self.blueArmy = save['self.blueArmy']
                self.redArmy = save['self.redArmy']
                self.blueBrainName = save['self.blueBrainName']
                self.blueBrain = eval(self.blueBrainName)
                self.braintypes["Blue"] = self.blueBrain
                self.turn = save['self.turn']
                self.won = save['self.won']
                self.started = save['self.started']

                self.brains = {"Blue": self.braintypes["Blue"].Brain(self, self.blueArmy) if self.braintypes["Blue"] else 0,
                               "Red": self.braintypes["Red"].Brain(self, self.redArmy) if self.braintypes["Red"] else 0}
                self.drawMap()
                self.drawSidePanels()
                self.setStatusBar("Game loaded!")

    def saveGame(self):
        saveFilename = tkFileDialog.asksaveasfilename(defaultextension=".sav",
                                                      filetypes = [('%s saves' % GAME_NAME, '.sav')],
                                                      initialdir = os.getcwd())
        if saveFilename:
            with open(saveFilename, 'w') as f:
                pickle.dump({'BOARD_WIDTH': BOARD_WIDTH,
                             'self.blueArmy': self.blueArmy,
                             'self.redArmy': self.redArmy,
                             'self.blueBrainName': self.blueBrainName,
                             'self.turn': self.turn,
                             'self.won': self.won,
                             'self.started': self.started
                             },
                             f)
            self.setStatusBar("Game saved")

    def settings(self):
        self.settingsWindow = Toplevel(width=300)

        lblBrain = Label(self.settingsWindow, text="Opponent Brain")
        self.blueBrainVar = StringVar(self.settingsWindow)
        mnuBrain = OptionMenu(self.settingsWindow, self.blueBrainVar, "randomBrain", "CarefulBrain", "SmartBrain")
        mnuBrain.config(width=20)
        self.blueBrainVar.set(self.blueBrainName)
        lblBrain.grid(column=0, row=0, sticky="ew", ipadx=10, ipady=10)
        mnuBrain.grid(column=1, row=0, sticky="ew", padx=10)
        
        lblDebug = Label(self.settingsWindow, text = "Debug")
        self.debugVar = StringVar(self.settingsWindow)
        mnuDebug = OptionMenu(self.settingsWindow, self.debugVar, "True", "False")
        mnuDebug.config(width=20)
        self.debugVar.set(str(DEBUG))
        lblDebug.grid(column=0, row=1, sticky="ew", ipadx=10, ipady=10)
        mnuDebug.grid(column=1, row=1, sticky="ew", padx=10)

        btnOK = Button(self.settingsWindow, text="OK", command=self.updateSettings)
        btnOK.grid(column=0, row=2, columnspan=2, ipadx=15, pady=8)

    def updateSettings(self):
        global DEBUG
        newBlueBrainName = self.blueBrainVar.get()
        DEBUG = (self.debugVar.get() == "True")
        self.drawMap()
        
        if newBlueBrainName != self.blueBrainName:       
            if tkMessageBox.askyesno("Changed settings", 
                                 "To change the opponent type, you must start a new game \n" +
                                 "Are you sure?"):
                self.blueBrainName = newBlueBrainName
                self.blueBrain = eval(self.blueBrainName)
                self.newGame()
                self.setStatusBar("Selected " + self.blueBrainName)
                
        self.settingsWindow.destroy()
        

    def loadStats(self):
        if os.path.exists('stats.cfg'):
            statsfile = open('stats.cfg', 'r')
            self.stats = pickle.load(statsfile)
            self.stats.lastChecked = datetime.datetime.now()
            statsfile.close()
        else:
            self.stats = Stats(datetime.datetime.now())

    def showStats(self):
        self.stats.refresh()
        t = self.stats.totalRunTime
        hours = t.seconds / 3600
        minutes = (t.seconds % 3600) / 60
        seconds = t.seconds % 60
        timestr = '%s days, %i:%02i:%02i' % (t.days, hours, minutes, seconds)

        self.statsWindow = Toplevel(width=300)
        self.statsWindow.wm_iconbitmap("%s/flag.ico" % ICON_DIR)
        lblNames = Label(self.statsWindow, justify=LEFT,
                         text=dedent("""
                         Games played:
                         Won:
                         Lost:
                         Win percentage:
                         
                         Longest winning streak:
                         Lowest casualties:
                         
                         Total time played:"""))
        lblNames.grid(column=0, row=0, sticky="ew", ipadx=35, ipady=10)

        lblStats = Label(self.statsWindow, justify=RIGHT,
                         text=""" 
                         %i
                         %i
                         %i
                         %.1f%%
                         
                         %i
                         %i
                         
                         %s""" % (self.stats.gamesPlayed, self.stats.gamesWon, self.stats.gamesLost,
                                  100. * self.stats.gamesWon / max(1, self.stats.gamesPlayed),
                                  self.stats.longestStreak,
                                  0, timestr))
        lblStats.grid(column=1, row=0, sticky="ew", ipadx=35, ipady=10)

        btnOK = Button(self.statsWindow, text="OK", command=self.closeStats)
        btnOK.grid(column=0, row=1, columnspan=2, ipadx=15, pady=15)

    def closeStats(self):
        self.statsWindow.destroy()

    def help(self):
        self.helpImage = Image.open("help.png")
        self.helpImage = ImageTk.PhotoImage(self.helpImage)
        self.helpWindow = Toplevel(width=400, height=640)
        lblHelp = Label(self.helpWindow, image=self.helpImage)
        lblHelp.grid(column=0, row=0, sticky="ew")

        btnOK = Button(self.helpWindow, text="OK", command=self.closeHelp)
        btnOK.grid(column=0, row=1, columnspan=2, ipadx=15, pady=8)

    def closeHelp(self):
        self.helpWindow.destroy()

    def visitWebsite(self):
        webbrowser.open("http://code.google.com/p/gpfj")

    def about(self):
        wrapper = TextWrapper(width=60)
        p1 = """\
        %s is a game developed by Jeroen Kools and Fedde Burgers
        for the course 'Game Programming' at the University of Amsterdam in 2012.
        """ % GAME_NAME

        p2 = """\
        The game is inspired by the classic board game Stratego (copyright Hasbro). 
        Sounds by pierrecartoons1979, steveygos93, Erdie and benboncan at freesounds.org 
        """

        text = wrapper.fill(dedent(p1)) + "\n\n" + wrapper.fill(dedent(p2))
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
                self.drawUnit(self.map, unit, x, y)

        for unit in self.blueArmy.army:
            if unit.alive:
                (x, y) = unit.getPosition()
                self.drawUnit(self.map, unit, x, y)

    def drawTile(self, x, y, tileColor):
        """Fill a tile with its background color - Currently unused"""
        self.map.create_rectangle(x * TILE_PIX, y * TILE_PIX, (x + 1) * TILE_PIX, (y + 1) * TILE_PIX, fill=tileColor)

    def drawMoveArrow(self, old, new):
        """Draw an arrow indicating the opponent's move"""
        self.map.create_line(int((old[0] + 0.5) * TILE_PIX), int((old[1] + 0.5) * TILE_PIX),
                             int((new[0] + 0.5) * TILE_PIX), int((new[1] + 0.5) * TILE_PIX),
                             width=3, fill=MOVE_ARROW_COLOR, arrow=LAST, arrowshape="8 10 6")

    def drawSidePanels(self):
        """Draw the unplaced units in the sidebar widget."""
        self.blueUnitPanel.delete(ALL)
        self.redUnitPanel.delete(ALL)

        self.blueUnitPanel.create_rectangle(0, 0, 10 * TILE_PIX, 4 * TILE_PIX, fill=UNIT_PANEL_COLOR)
        self.redUnitPanel.create_rectangle(0, 0, 10 * TILE_PIX, 4 * TILE_PIX, fill=UNIT_PANEL_COLOR)

        unplacedRed = 0
        for unit in self.redArmy.army:
            if unit.isOffBoard():
                x = unplacedRed % 10
                y = unplacedRed / 10
                unit.setPosition(self.offBoard(x), self.offBoard(y))
                self.drawUnit(self.redUnitPanel, unit, x, y)
                unplacedRed += 1

        unplacedBlue = 0
        for unit in self.blueArmy.army:
            if unit.isOffBoard():
                x = unplacedBlue % 10
                y = unplacedBlue / 10
                unit.setPosition(self.offBoard(x), self.offBoard(y))
                self.drawUnit(self.blueUnitPanel, unit, x, y)
                unplacedBlue += 1

    def drawUnit(self, canvas, unit, x, y, color=None):
        if color == None:
            color = RED_PLAYER_COLOR if unit.color == "Red" else BLUE_PLAYER_COLOR

        hilight = SELECTED_RED_PLAYER_COLOR if unit.color == "Red" else SELECTED_BLUE_PLAYER_COLOR
        shadow = SHADOW_RED_COLOR if unit.color == "Red" else SHADOW_BLUE_COLOR

        # draw hilight
        canvas.create_rectangle(x * TILE_PIX, y * TILE_PIX,
                                (x + 1) * TILE_PIX, (y + 1) * TILE_PIX,
                                fill=hilight, outline=None)
        # draw shadow
        canvas.create_rectangle(x * TILE_PIX + TILE_BORDER, y * TILE_PIX + TILE_BORDER,
                                (x + 1) * TILE_PIX, (y + 1) * TILE_PIX,
                                fill=shadow, outline=None, width=0)
        # draw center
        canvas.create_rectangle(x * TILE_PIX + TILE_BORDER, y * TILE_PIX + TILE_BORDER,
                                (x + 1) * TILE_PIX - TILE_BORDER, (y + 1) * TILE_PIX - TILE_BORDER,
                                fill=color, outline=None, width=0)

        if unit.color == "Red" or DEBUG or not unit.alive or self.won or unit.justAttacked:
            unit.justAttacked = False
            canvas.create_image(x * TILE_PIX, y * TILE_PIX, 
                                image=self.unitIcons.getIcon(unit.name), anchor=NW)
            if unit.name != "Bomb" and unit.name != "Flag":
                canvas.create_text(((x + .2) * TILE_PIX, (y + .8) * TILE_PIX),
                                   text=unit.rank, fill=MOVE_ARROW_COLOR)

        if not unit.alive:
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
                    if unit.isMovable() or not self.started:
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

        if y < (BOARD_WIDTH - 4): #TODO: fix for other than standard sizes
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

        (i, j) = self.clickedUnit.getPosition()
        if abs(i - x) > 1 or abs(j - y) > 1:
            self.clickedUnit.isKnown = True

        target = self.getUnit(x, y)
        if target:
            if target.color == self.clickedUnit.color and self.started:
                self.setStatusBar("You can't move there - tile already occupied!")

            elif target.color == self.clickedUnit.color and not self.started: # switch units
                    (xold, yold) = self.clickedUnit.getPosition()
                    target.setPosition(xold, yold)
                    self.clickedUnit.setPosition(x, y)
                    self.clickedUnit = None
                    self.movingUnit = None

                    self.drawMap()
            else:
                self.attack(self.clickedUnit, target)
                if self.started:
                    self.endTurn()
            return

        else:
            self.setStatusBar("Moved %s to (%s, %s)" % (self.clickedUnit, x, y))
            self.clickedUnit.setPosition(x, y)
            self.clickedUnit.hasMoved = True

        self.clickedUnit = None
        self.movingUnit = False

        self.drawMap()

        if self.started:
            self.endTurn()

    def otherPlayer(self, color):
        if color == "Red": return "Blue"
        return "Red"

    def otherArmy(self, color):
        if color == "Red": return self.blueArmy
        return self.redArmy

    def endTurn(self):
        self.turn = self.otherPlayer(self.turn)

        if self.brains[self.turn] and not self.won: # computer player?
            (oldlocation, move) = self.brains[self.turn].findMove()

            # check if the opponent can move
            if move == None:
                self.victory(self.otherPlayer(self.turn), True)
                return

            unit = self.getUnit(oldlocation[0], oldlocation[1])
            unit.hasMoved = True
            enemy = self.getUnit(move[0], move[1])
            if enemy:
                self.attack(unit, enemy)
            else:
                unit.setPosition(move[0], move[1])

            # check if player can move
            tempBrain = randomBrain.Brain(self, self.redArmy)
            playerMove = tempBrain.findMove()
            if playerMove[0] == None:
                self.victory(self.turn, True)
                return

            self.setStatusBar("%s moves unit at (%s,%s) to (%s,%s)" % (self.turn,
                                                                       oldlocation[0], oldlocation[1],
                                                                       move[0], move[1]))
            self.drawMap()
            self.drawSidePanels()
            self.drawMoveArrow(oldlocation, move)

        self.turn = self.otherPlayer(self.turn)

    def legalMove(self, unit, x, y):
        """Check whether a move:
            - does not end in the water
            - does not end off-board
            - is only in one direction
            - is not farther than one step, for non-scouts
            - does not jump over obstacles, for scouts
        """

        if self.isPool(x, y):
            return False

        (ux, uy) = unit.position
        dx = abs(ux - x)
        dy = abs(uy - y)

        if x >= BOARD_WIDTH or y >= BOARD_WIDTH:
            return False

        if not self.started:
            if y < (BOARD_WIDTH - 4):
                return False
            return True

        if unit.walkFar:
            if ux != x and uy != y:
                return False

            if (dx + dy) == 0:
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
        attacker.isKnown = True
        defender.isKnown = True

        if defender.name == "Flag":
            attacker.position = defender.position
            defender.die()
            self.victory(attacker.color)

        elif attacker.canDefuseBomb and defender.name == "Bomb":
            attacker.position = defender.position
            defender.die()
            attacker.justAttacked = True
            text += "The mine was disabled."

        elif attacker.canKillMarshal and defender.name == "Marshal":
            attacker.position = defender.position
            defender.die()
            attacker.justAttacked = True
            text += "The marshal has been assassinated."

        elif attacker.rank > defender.rank:
            attacker.position = defender.position
            defender.die()
            attacker.justAttacked = True
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

            top = Toplevel(width=300)
            top.title("Battle result")
            top.wm_iconbitmap("%s/flag.ico" % ICON_DIR)

            atkImg = ImageTk.PhotoImage(self.unitIcons.getImage(attacker.name, 120))
            atkLbl = Label(top, image=atkImg)
            atkLbl.image = atkImg
            atkLbl.grid(row=0, column=0, sticky=NW)

            defImg = ImageTk.PhotoImage(self.unitIcons.getImage(defender.name, 120))
            defLbl = Label(top, image=defImg)
            defLbl.image = defImg

            message = Label(top, text=text)
            message.grid(row=0, column=1, sticky=NE, ipadx=15, ipady=50)

            defLbl.grid(row=0, column=2, sticky=NE)

            ok = Button(top, text="OK", command=top.destroy)
            ok.grid(row=1, column=1, ipadx=15, ipady=5, pady=5)
            if defender.name == "Bomb":
                if attacker.canDefuseBomb:
                    self.playSound(SOUND_DEFUSE)
                else:
                    self.playSound(SOUND_BOMB)
            elif defender.name == "Marshal" and attacker.canKillMarshal:
                self.playSound(SOUND_ARGH)
            elif attacker.name == "Marshal":
                self.playSound(SOUND_LAUGH)
            else:
                self.playSound(SOUND_COMBAT)
            self.root.wait_window(top)

            #tkMessageBox.showinfo("Battle result", text)

        #self.drawMap()
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
            if unit and unit.alive:
                self.setStatusBar("You clicked on %s %s" % (panel, unit))

                if panel == "red": # clicked player unit
                    self.clickedUnit = unit
                    self.placingUnit = True

                    # highlight unit
                    self.drawUnit(self.redUnitPanel, unit, x, y)

                    self.setStatusBar("Click the map to place this unit")

    def offBoard(self, x):
        """Return negative coordinates used to indicate off-board position. Avoid zero."""
        return -x - 1

    def victory(self, color, noMoves=False):
        self.won = True
        self.drawMap()
        top = Toplevel(width=300)
        top.wm_iconbitmap("%s/flag.ico" % ICON_DIR)
        flagimg1 = Image.open("%s/%s.%s" % (ICON_DIR, "flag", ICON_TYPE))
        flagimg2 = ImageTk.PhotoImage(flagimg1)
        lbl = Label(top, image=flagimg2)
        lbl.image = flagimg2
        lbl.grid(row=0, column=1, sticky=NW)

        if color == "Red":
            top.title("Victory!")
            if noMoves:
                messageTxt = "The enemy army has been immobilized. Congratulations, you win!"
            else:
                messageTxt = "Congratulations! You've captured the enemy flag!"

        else:
            top.title("Defeat!")
            if noMoves:
                messageTxt = "There are no valid moves left. You lose."
            else:
                messageTxt = "Unfortunately, the enemy has captured your flag. You lose."

        self.stats.addGame(color == "Red")
        message = Label(top, text=messageTxt)
        message.grid(row=0, column=0, sticky=NE, ipadx=15, ipady=50)

        ok = Button(top, text="OK", command=top.destroy)
        ok.grid(row=1, column=0, columnspan=2, ipadx=15, ipady=5, pady=5)

        message.configure(width=40, justify=CENTER, wraplength=150)
        self.setStatusBar("%s has won the game!" % color)
        if playSound:
            if color == "Red":
                self.playSound(SOUND_WIN)
            else:
                self.playSound(SOUND_LOSE)

    def playSound(self, name):
        winsound.PlaySound("%s/%s" % (SOUND_DIR, name),
                               winsound.SND_FILENAME | winsound.SND_ASYNC)

    def quickplace(self, event):
        if not self.started:
            tempBrain = randomBrain.Brain(self, self.redArmy)
            tempBrain.placeArmy(self.armyHeight)

            self.drawMap()
            self.drawSidePanels()
            self.setStatusBar("Randomly placed your army!")
            self.started = True

    def exit(self, event=None):
        """Quit program."""
        self.stats.save()
        self.root.quit()

class Stats:
    def __init__(self, lastChecked):
        self.gamesPlayed = 0
        self.gamesWon = 0
        self.gamesLost = 0

        self.currentStreak = 0
        self.longestStreak = 0
        self.lowestCasualties = 0

        self.totalRunTime = datetime.timedelta(0)
        self.lastChecked = lastChecked

    def addGame(self, won):
        self.gamesPlayed += 1
        if won:
            self.gamesWon += 1
            self.currentStreak += 1
            self.longestStreak = max(self.longestStreak, self.currentStreak)
        else:
            self.gamesLost += 1
            self.currentStreak = 0

    def refresh(self):
        self.totalRunTime += (datetime.datetime.now() - self.lastChecked)
        self.lastChecked = datetime.datetime.now()

    def save(self):
        self.refresh()
        with open('stats.cfg', 'w') as f:
            pickle.dump(self, f)


if __name__ == "__main__":
    root = Tk()
    Application(root)
    root.title("%s %s" % (GAME_NAME, VERSION))
    root.wm_iconbitmap("%s/flag.ico" % ICON_DIR)
    root.mainloop()
