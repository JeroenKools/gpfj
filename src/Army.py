from Tkinter import PhotoImage

ICON_DIR = 'uniticons'
ICON_TYPE = 'gif' 

class Army:  
    ranks = ['marshal', 'general', 'colonel', 'major', 'captain', 'lieutenant', 'sergeant', 'miner', 'scout', 'spy', 'bomb', 'flag']
    
    def __init__(self, size = 40):
        
        # Army as dictionary: name is key, entry contains rank, alive, locations. Negative Locations are on the side panel (dead or to be placed)          
        self.army = { 
                     'marshal':    [ 10, [1], [None] ],\
                      'general':    [ 10, [1], [None] ],\
                      'colonel':    [ 10, [1 ,1], [None, None] ],\
                      'major' :     [ 10, [1, 1, 1], [None, None, None] ],\
                      'captain':    [ 10, [1, 1, 1, 1], [None, None, None, None] ],\
                      'lieutenant': [ 10, [1, 1, 1, 1], [None, None, None, None] ],\
                      'sergeant':   [ 10, [1, 1, 1, 1], [None, None, None, None] ],\
                      'miner':      [ 10, [1, 1, 1, 1, 1], [None, None, None, None, None] ],\
                      'scout':      [ 10, [1, 1, 1, 1, 1, 1, 1, 1], [None, None, None, None, None, None, None, None] ],\
                      'spy':        [ 10, [1], [None] ],\
                      'bomb':       [ 10, [1, 1, 1, 1, 1, 1], [None, None, None, None, None, None] ],\
                      'flag':       [ 10, [1], [None] ]
                    }
        
        self.icons = {
                      'marshal':    PhotoImage(file="%s/marshal.%s" % (ICON_DIR, ICON_TYPE)), \
                      'general':    PhotoImage(file="%s/general.%s" % (ICON_DIR, ICON_TYPE)), \
                      'colonel':    PhotoImage(file="%s/colonel.%s" % (ICON_DIR, ICON_TYPE)), \
                      'major':      PhotoImage(file="%s/major.%s" % (ICON_DIR, ICON_TYPE)), \
                      'captain':    PhotoImage(file="%s/captain.%s" % (ICON_DIR, ICON_TYPE)), \
                      'lieutenant': PhotoImage(file="%s/lieutenant.%s" % (ICON_DIR, ICON_TYPE)), \
                      'sergeant':   PhotoImage(file="%s/sergeant.%s" % (ICON_DIR, ICON_TYPE)), \
                      'miner':      PhotoImage(file="%s/miner.%s" % (ICON_DIR, ICON_TYPE)), \
                      'scout':      PhotoImage(file="%s/scout.%s" % (ICON_DIR, ICON_TYPE)), \
                      'spy':        PhotoImage(file="%s/spy.%s" % (ICON_DIR, ICON_TYPE)), \
                      'bomb':       PhotoImage(file="%s/bomb.%s" % (ICON_DIR, ICON_TYPE)), \
                      'flag':       PhotoImage(file="%s/flag.%s" % (ICON_DIR, ICON_TYPE))
                    }
    def offBoard(self, rank, nr):
        position = self.army[rank][2][nr] 
        if position == None: return True
        (x,y) = position
        if x < 0 and y < 0: return True
        return False
    
    def changePosition(self, rank, nr, x, y):
        self.army[rank][2][nr] = (x,y)
             