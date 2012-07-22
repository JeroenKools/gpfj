'''
Constants module for Stratego
Created on 28 jun. 2012

@author: Jeroen Kools and Fedde Burgers
'''

GAME_NAME = 'Stratego'      # Kindral? Praetor?
VERSION = 0.31              # Game version

ICON_DIR = 'uniticons'
ICON_TYPE = 'png'
TERRAIN_DIR = "terrain"
LAND_TEXTURE = "grass3.jpg"
WATER_TEXTURE = "water.jpg"

GRASS_COLOR = "#44AA22"     # Grass color rgb
WATER_COLOR = "#3388AA"     # Water color rgb
DEAD_COLOR = "#567"         # Dead unit cross color
UNIT_PANEL_COLOR = "#BBB"   # Unit panel rgb
RED_PLAYER_COLOR = "#A00"
SELECTED_RED_PLAYER_COLOR = "#e00"
BLUE_PLAYER_COLOR = "#00A"

BOARD_WIDTH = 10            # Board size in tiles, classic Stratego value is 10 
TILE_PIX = 50               # Tile size in pixels
POOLS = 2                   # Number of pools, classic Stratego value is 2
DEBUG = False               # If True, show enemy units' ranks