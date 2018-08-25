import os


class GameConstants:

    SCREEN_SIZE = (800, 600)
    FPS = 60
    INTERVAL = .15  # animation interval

    STARTING_SCENE = 0

    """ Define Types """
    ALL_GAME_OBJECTS = 0
    PLAYER_GAME_OBJECTS = 1
    COMPUTER_GAME_OBJECTS = 2

    """ SCREEN DIVISION CONSTANTS """
    # X
    BATTLE_AREA_PLAYER_BORDER = int(SCREEN_SIZE[0]*3/8)  # 300
    BATTLE_AREA_COMPUTER_BORDER = (SCREEN_SIZE[0] - BATTLE_AREA_PLAYER_BORDER)  # 500
    # Y
    BATTLE_AREA_TOP = int(SCREEN_SIZE[1]/3)  # 200
    BATTLE_AREA_BOTTOM = int(SCREEN_SIZE[1]*2/3)  # 400

    PADX = 50
    PADY = 25

    """ PLAYER AREA """
    PLAYERS_BACK_COLUMN = int(SCREEN_SIZE[0]*3/32)  # 75
    PLAYERS_FRONT_COLUMN = int(SCREEN_SIZE[0]*6/32 + PADX)  # 225
    PLAYERS_TOP_ROW = int(SCREEN_SIZE[1]*5/12 - 3*PADY)  # 100
    PLAYERS_MIDDLE_ROW = int(SCREEN_SIZE[1]/2 - 2*PADY)  # 300
    PLAYERS_BOTTOM_ROW = int(SCREEN_SIZE[1]*7/12 - PADY)  # 400

    # Playing Scene CENTER Positions
    PLAYER_TOP_BACK = (PLAYERS_BACK_COLUMN, PLAYERS_TOP_ROW)  # (75, 250)
    PLAYER_MIDDLE_BACK = (PLAYERS_BACK_COLUMN, PLAYERS_MIDDLE_ROW)  # (75, 300)
    PLAYER_BOTTOM_BACK = (PLAYERS_BACK_COLUMN, PLAYERS_BOTTOM_ROW)  # (75, 350)

    PLAYER_TOP_FRONT = (PLAYERS_FRONT_COLUMN, PLAYERS_TOP_ROW)  # (225, 250)
    PLAYER_MIDDLE_FRONT = (PLAYERS_FRONT_COLUMN, PLAYERS_MIDDLE_ROW)  # (225, 250)
    PLAYER_BOTTOM_FRONT = (PLAYERS_FRONT_COLUMN, PLAYERS_BOTTOM_ROW)  # (225, 250)

    """ COMPUTER AREA """
    COMPUTER_BACK_COLUMN = int(SCREEN_SIZE[0] - PLAYERS_BACK_COLUMN)  # 800 - 75 = 725
    COMPUTER_FRONT_COLUMN = int(SCREEN_SIZE[0] - PLAYERS_FRONT_COLUMN)  # 800 - 225 = 575

    # Playing Scene CENTER Positions
    COMPUTER_TOP_BACK = (COMPUTER_BACK_COLUMN, PLAYERS_TOP_ROW)
    COMPUTER_MIDDLE_BACK = (COMPUTER_BACK_COLUMN, PLAYERS_MIDDLE_ROW)
    COMPUTER_BOTTOM_BACK = (COMPUTER_BACK_COLUMN, PLAYERS_BOTTOM_ROW)

    COMPUTER_TOP_FRONT = (COMPUTER_FRONT_COLUMN, PLAYERS_TOP_ROW)
    COMPUTER_MIDDLE_FRONT = (COMPUTER_FRONT_COLUMN, PLAYERS_MIDDLE_ROW)
    COMPUTER_BOTTOM_FRONT = (COMPUTER_FRONT_COLUMN, PLAYERS_BOTTOM_ROW)

    """ Menus """
    PLAYER_UNITS_MENU_WIDTH = PLAYERS_FRONT_COLUMN + 1 * PADX
    COMPUTER_UNITS_MENU_WIDTH = SCREEN_SIZE[0] - COMPUTER_FRONT_COLUMN + PADX

    """ SPRITES """
    DARK_LAIR = os.path.join("Assets", "Graphics", "dark_lair.png")
    CAVE_TILE = os.path.join("Assets", "Graphics", "cave_tile.png")

    """ COLORS """
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BRIGHT_RED = (255, 0, 0)
    RED = (155, 0, 0,)
    BRIGHT_GREEN = (0, 255, 0)
    GREEN = (0, 155, 0)
    BRIGHT_BLUE = (0, 0, 255)
    BLUE = (0, 0, 155)
    BRIGHT_YELLOW = (255, 255, 0)
    YELLOW = (155, 155, 0)
    BRIGHT_GRAY = (128, 128, 128)
    DARK_GRAY = (40, 40, 40)

