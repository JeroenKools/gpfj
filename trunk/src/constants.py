'''
Constants module for Stratego
Created on 28 jun. 2012

@author: Jeroen Kools and Fedde Burgers
'''

GAME_NAME = 'Stratego'      # Kindral? Praetor?
VERSION = 0.35              # Game version

ICON_DIR = 'uniticons'
ICON_TYPE = 'png'
TERRAIN_DIR = "terrain"
LAND_TEXTURE = "grass3.jpg"
WATER_TEXTURE = "water.jpg"

GRASS_COLOR = "#44AA22"     # Grass color rgb
WATER_COLOR = "#3388AA"     # Water color rgb
DEAD_COLOR = "#567"         # Dead unit cross color
MOVE_ARROW_COLOR = "#FFA"
UNIT_PANEL_COLOR = "#BBB"   # Unit panel rgb

RED_PLAYER_COLOR = "#A00"
SELECTED_RED_PLAYER_COLOR = "#E00"
SHADOW_RED_COLOR = "#600"

BLUE_PLAYER_COLOR = "#00A"
SELECTED_BLUE_PLAYER_COLOR = '#00E'
SHADOW_BLUE_COLOR = "#006"

BOARD_WIDTH = 10            # Board size in tiles, classic Stratego value is 10 
TILE_PIX = 50               # Tile size in pixels, tested between 30 and 60
TILE_BORDER = 3             # Width of the tile highlights/borders
POOLS = 2                   # Number of pools, classic Stratego value is 2
DEBUG = False               # If True, show enemy units' ranks (cheat/debug)