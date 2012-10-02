'''
Constants module
Created on 28 jun. 2012

@author: Jeroen Kools and Fedde Burgers
'''

GAME_NAME = 'Kindral'      # Kindral? Praetor?
VERSION = 0.42              # Game version
DEBUG = False              # If True, show enemy units' ranks (cheat/debug)

## GRAPHICS ##
ICON_DIR = 'uniticons'
ICON_TYPE = 'png'
TERRAIN_DIR = "terrain"
LAND_TEXTURE = "grass3.jpg"
WATER_TEXTURE = "water.jpg"

GRASS_COLOR = "#44AA22"     # Grass color rgb
WATER_COLOR = "#3388AA"     # Water color rgb
DEAD_COLOR = "#567"         # Dead unit cross color
MOVE_ARROW_COLOR = "#FE6"
UNIT_PANEL_COLOR = "#BBB"   # Unit panel rgb

RED_PLAYER_COLOR = "#A00"
SELECTED_RED_PLAYER_COLOR = "#E00"
SHADOW_RED_COLOR = "#600"

BLUE_PLAYER_COLOR = "#00A"
SELECTED_BLUE_PLAYER_COLOR = '#00E'
SHADOW_BLUE_COLOR = "#006"

## AUDIO ##
SOUND_DIR = "sounds"
SOUND_WIN = "90140__pierrecartoons1979__win3.wav"
SOUND_LOSE = "73581__benboncan__sad-trombone.wav"
SOUND_COMBAT = "27826__erdie__sword01.wav"
SOUND_BOMB = "80401__steveygos93__explosion2.wav"
SOUND_ARGH = "argh.wav"
SOUND_LAUGH = "laugh.wav"
SOUND_DEFUSE = "creak.wav"

## GAME PARAMS ##
BOARD_WIDTH = 10        # Board size in tiles, classic Stratego value is 10, tested between 6 and 20. 
TILE_PIX = 50           # Tile size in pixels, tested between 10 and 80. Recommended: 50
TILE_BORDER = 3         # Width of the tile highlights/borders
POOLS = 2               # Number of pools, classic Stratego value is 2

