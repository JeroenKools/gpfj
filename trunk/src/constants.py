"""
Constants module
Created on 28 jun. 2012

@author: Jeroen Kools and Fedde Burgers
"""

GAME_NAME = "Kindral"      # Kindral? Praetor? Napoleon? Austerlitz?
VERSION = "0.56"           # Game version

AUTHORS = "Jeroen Kools & Fedde Burgers"
URL = "http://code.google.com/p/gpfj"

## GRAPHICS ##
ICON_DIR = "uniticons"
ICON_TYPE = "png"
TERRAIN_DIR = "terrain"
LAND_TEXTURE = "grass3.jpg"
WATER_TEXTURE = "water.jpg"

GRASS_COLOR = "#44AA22"     # Grass color rgb
WATER_COLOR = "#3388AA"     # Water color rgb
DEAD_COLOR = "#567"         # Dead unit cross color
MOVE_ARROW_COLOR = "#FE6"   # Color of arrow indicating AI move
UNIT_PANEL_COLOR = "#BBB"   # Unit panel rgb

RED_PLAYER_COLOR = "#A00"
SELECTED_RED_PLAYER_COLOR = "#E00"
SHADOW_RED_COLOR = "#600"

BLUE_PLAYER_COLOR = "#00A"
SELECTED_BLUE_PLAYER_COLOR = "#00E"
SHADOW_BLUE_COLOR = "#006"

MOVE_ANIM_STEPS = 10        # number of frames in move animations
MOVE_ANIM_FRAMERATE = 15    # time between animation frames in milliseconds

HELP_BG = "#f0f0f0"
HELP_TITLE_FONT = ("Segoe UI", 12, "bold")
HELP_BODY_FONT = ("Segoe UI", 11)

LAUNCHER_TITLE_FONT = ("Times", 64, "bold italic underline")
LAUNCHER_AUTHOR_FONT = ("Helvetica", 14, "bold")

## AUDIO ##
MUSIC_DIR = "music"
SOUND_DIR = "sounds"
SOUND_WIN = "90140__pierrecartoons1979__win3.wav"
SOUND_LOSE = "73581__benboncan__sad-trombone.wav"
SOUND_COMBAT = "27826__erdie__sword01.wav"
SOUND_BOMB = "explosion.wav"
SOUND_ARGH = "argh2.wav"
SOUND_LAUGH = "laugh.wav"
SOUND_DEFUSE = "creak.wav"
SOUND_OHNO = "ohnoes3.wav"

## GAME PARAMS ##
BOARD_WIDTH = 10        # Board size in tiles, classic Stratego value is 10, tested between 6 and 20. 
TILE_PIX = 50           # Tile size in pixels, tested between 10 and 80. Recommended: 50
TILE_BORDER = 3         # Width of the tile highlights/borders
POOLS = 2               # Number of pools, classic Stratego value is 2

### LAUNCHER SETTINGS
DEFAULTBRAIN = "SurpriseBrain"
DEFAULTDIFFICULTY = "Normal"
FORGETCHANCEEASY = 0.1
DEFAULTSIZE = "Normal"
SIZE_DICT = {           # Preset values for BOARD_WIDTH, POOLS and TILE_PIX, to be selected from launcher menu
             "Small":  [8, 2, 60],
             "Normal": [10, 2, 50],
             "Large":  [14, 3, 50],
             "Extra Large": [20, 4, 40]}


