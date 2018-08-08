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
    PLAYERS_TOP_ROW = int(SCREEN_SIZE[1]*5/12 - 2 * PADY)  # 100
    PLAYERS_MIDDLE_ROW = int(SCREEN_SIZE[1]/2 - PADY)  # 300
    PLAYERS_BOTTOM_ROW = int(SCREEN_SIZE[1]*7/12)  # 400

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

    """ SPRITES """
    DARK_LAIR = os.path.join("Assets", "Graphics", "dark_lair.png")
    CAVE_TILE = os.path.join("Assets", "Graphics", "cave_tile.png")

    GAME_SCENE_MENU = os.path.join("Assets", "Graphics", "game_scene_menu.png")

    TRIANGLE_TOP_DOWN_SHEET = os.path.join("Assets", "Graphics", "triangle_top_down_sprite_sheet.png")
    TRIANGLE_TOP_DOWN_SIZE = (int(33 * 0.5), int(59 * 0.5))

    ADVENTURER_SPRITE_SHEET = os.path.join("Assets", "Graphics", "adventurer_sprite_sheet.png")
    ADVENTURER_SIZE = (50 * 3, 37 * 3)
    ADVENTURER_SPEED = (15, 15)

    DARK_SPRITE_SHEET = os.path.join("Assets", "Graphics", "dark_sprite_sheet.png")

    SKELETON_SPRITE_SHEET = os.path.join("Assets", "Graphics", "skeleton_sprite_sheet.png")
    SKELETON_SIZE = (100 * 1, 74 * 1)
    SKELETON_SPEED = (15, 15)

    SLIME_SPRITE_SHEET = os.path.join("Assets", "Graphics", "slime_sprite_sheet.png")
    SLIME_SIZE = (100 * 1, 74 * 1)
    SLIME_SPEED = (15, 15)

    """ COLORS """
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BRIGHT_GREEN = (0, 255, 0)  # lime

    TEXT_SIZE_SMALL = 17
