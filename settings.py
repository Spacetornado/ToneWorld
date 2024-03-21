# Screen settings
WIDTH = 1024
HEIGHT = 585
FPS = 60
DISPLAY_FPS = False

# Exit location
EXIT_X = 560
EXIT_Y = 100

# Test object location (right click)
TEST_X = 250
TEST_Y = 125

# Timers
TIMER_CHAT = 1
TIMER_PLAYER_MOVE = 2
TIMER_INACTIVE_PLAYER_MOVE = 1
TIMER_CLEANUP = 5

# Player settings
MAX_RANDOM_PLAYERS = 8
MAX_TOTAL_PLAYERS = 12
PLAYER_SIZE = 96
PLAYER_ROTATION_MAX = 7 # 7, 10, 15 or 25
player_animation_path = f"ToneImg/animated_players_{PLAYER_ROTATION_MAX}"
PLAYER_EXPIRATION_MINS = 10 # Minutes inactive until a player is forced to leave
PLAYER_CLOSENESS_THRESHOLD = 50 # Distance in pixels where 2 players are considered to be too close to each other
# Player spawn location minimums/maximums
TEST_SPAWNS = False
SPAWN_X_MIN = 300
SPAWN_X_MAX = 550
SPAWN_Y_MIN = 250
SPAWN_Y_MAX = 350
if TEST_SPAWNS:
    SPAWN_X_MIN = 50
    SPAWN_X_MAX = 600
    SPAWN_Y_MIN = 50
    SPAWN_Y_MAX = 600
PLAYER_X_MIN = 50
PLAYER_X_MAX = WIDTH - PLAYER_SIZE - 15
PLAYER_Y_MIN = 200
PLAYER_Y_MAX = HEIGHT - PLAYER_SIZE - 15
# Player animation
PLAYER_MOVE_SPEED = 1
RAND_MOVE_CHANCE = 0.2
MOVE_MIN_S = 0.8
MOVE_MAX_S = 1.8
TOTAL_ANIMATION_FRAMES = 8
FRAME_UPDATE_DELAY_MIN = 6
FRAME_UPDATE_DELAY_MAX = 9
# Edge buffers
PLAYER_BUFFER_X = 50
PLAYER_BUFFER_TOP_Y = 100
PLAYER_BUFFER_BOTTOM_Y = 100

# Message/chat settings
GAME_MSG_EXPIRATION_SECS = 30 # Seconds before removing a message from game_msgs list
MSG_DISPLAY_TIME = 4
CHAT_TEXT_WRAP = 28
MAX_CHAT_LENGTH = 120

# Fonts
FONT_NAME = "Rajdhani-SemiBold.ttf"
FONT_SIZE = 16
LARGER_FONT_SIZE = 18
LARGERER_FONT_SIZE = 22
LARGEST_FONT_SIZE = 28

# Colors
CHAT_TEXT_COLOR = (210, 210, 240)
GAME_TEXT_COLOR = (230, 20, 133)
GAME_TEXT_DARKER_COLOR = (200, 50, 100)
TEXT_BG_COLOR = (25, 25, 55)
CHAT_COLOR = (25, 25, 75)
SHADOW_COLOR = (30, 10, 20)

# Text shadow offset
SHADOW_OFFSET = 3

# Minimum Y positions
GAME_TEXT_Y = 20 # Min Y position of game messages
SPEECH_BUBBLE_Y_MIN = 50 # Min Y position of player speech bubbles

