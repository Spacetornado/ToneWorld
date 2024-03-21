import pygame, sys, random, os, textwrap, math
from player import Player
from settings import *
from utils import *
from debug import *

#region functions
###################################################################################
## Functions                                                                     ##
###################################################################################
def create_player(players, name):
    # Generate random coordinates within the specified range
    random_x = random.randint(SPAWN_X_MIN, SPAWN_X_MAX)
    random_y = random.randint(SPAWN_Y_MIN, SPAWN_Y_MAX)
    # A hack to prevent players from spawning on the chess board, couches, walls, etc.
    while False == are_coords_good(random_x, random_y):
        random_x = random.randint(SPAWN_X_MIN, SPAWN_X_MAX)
        random_y = random.randint(SPAWN_Y_MIN, SPAWN_Y_MAX)

    # Create the player at the random location
    player = Player(pos=(random_x, random_y), groups=all_sprites, playerList=players, player_name=name)
    return player

def make_player_inactive(player, timestamp):
    print("Moving from players to inactive_players: " + player.player_name)
    move_towards_door(player)
    player.is_leaving = True
    player.is_moving = True
    inactive_players.append(player)
    players.remove(player)
    game_msg("goodbye " + player.player_name + "! ToneWorld will miss you <3", timestamp)

def move_towards_door(player, target_x=EXIT_X, target_y=EXIT_Y):
    # Calculate the vector from the player to the door
    dx = target_x - player.x
    dy = target_y - player.y

    # Normalize the vector
    distance = math.hypot(dx, dy)  # More concise way to calculate distance
    if distance != 0:
        dx = (dx / distance)
        dy = (dy / distance)
    else:
        dx, dy = 0, 0

    player.direction = (dx, dy)
    p_name = player.player_name
    #print("Player direction: dx: " + str(dx) + " dy: " + str(dy) + " (" + p_name + ")")

def game_msg(new_text, timestamp):
    if len(game_text) >= 3:
        # Remove the oldest text (first item in the list)
        game_text.pop(0)
        game_text_timestamps.pop(0)

    # Add the new text and its timestamp
    game_text.append(new_text)
    game_text_timestamps.append(timestamp)

def draw_text_with_shadow(screen, text, font, color, shadow_color, x, y, shadow_offset):
    # Render the shadow
    shadow_text = font.render(text, True, shadow_color)
    shadow_rect = shadow_text.get_rect(center=(x + shadow_offset, y + shadow_offset))
    screen.blit(shadow_text, shadow_rect)

    # Render the actual text
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect(center=(x, y))
    screen.blit(rendered_text, text_rect)

def set_event_timer(timer_duration):
    global event_num
    event_id = pygame.USEREVENT + event_num
    pygame.time.set_timer(event_id, timer_duration * 1000)
    event_num += 1

def calculate_average_distance(players):
    if len(players) < 2:
        return 0
    total_distance = 0
    count = 0
    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            # Calculate the Euclidean distance between players i and j
            dx = players[i].x - players[j].x
            dy = players[i].y - players[j].y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            total_distance += distance
            count += 1
    # Return average distance
    average_distance = total_distance / count
    return average_distance

def set_movement_chance(players):
    avg_distance = calculate_average_distance(players)

    base_chance = RAND_MOVE_CHANCE
    if avg_distance < 80:
        base_chance += 0.3
    elif avg_distance < 150:
        base_chance += 0.2
    elif avg_distance < 200:
        base_chance += 0.1

    # Check proximity and adjust movement chance
    for player in players:
        close_to_another = any(
            math.sqrt((player.x - other.x)**2 + (player.y - other.y)**2) < PLAYER_CLOSENESS_THRESHOLD
            for other in players if other != player
        )
        if close_to_another:
            player.movement_chance = 0.9
        else:
            player.movement_chance = base_chance

    # Example of moving players based on their movement chance
    for player in players:
        if random.random() < player.movement_chance:
            # Move the player
            pass  # Implement your movement logic here
#endregion

# Initialize the game
###################################################################################
pygame.init()

#region Global settings
# Fonts and line heights
###################################################################################
pygame.font.init()
font = pygame.font.Font(FONT_NAME, FONT_SIZE)
larger_font = pygame.font.Font(FONT_NAME, LARGER_FONT_SIZE)
largerer_font = pygame.font.Font(FONT_NAME, LARGERER_FONT_SIZE)
largest_font = pygame.font.Font(FONT_NAME, LARGEST_FONT_SIZE)
line_height = font.size("Test text")[1]
larger_line_height = larger_font.size("Test text")[1]
largest_line_height = largest_font.size("Test text")[1]

# Icon
icon = pygame.image.load('ToneImg/ToneWorldIcon.png')
pygame.display.set_icon(icon)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Caption
pygame.display.set_caption('ToneWorld (twitch.tv/tonedefff)')

# Clock
clock = pygame.time.Clock()

# Background image
background_image = pygame.image.load('ToneImg/ToneWorld.jpg')
chatMessagesFile = "C:\\StreamCode\\ChatProcessing\\chatMessages.json"
# Sprite group
all_sprites = pygame.sprite.Group()
# Lists
#######################################################################################################################
players = []
inactive_players = []
chat_messages = []
game_text = []
game_text_timestamps = []
# Events
#######################################################################################################################
event_num = 1
# Player movement
EVENT_MOVEMENT = pygame.USEREVENT + event_num
pygame.time.set_timer(EVENT_MOVEMENT, TIMER_PLAYER_MOVE * 1000)
event_num += 1
# Chat messages
EVENT_CHAT = event_num + 1
pygame.time.set_timer(EVENT_CHAT, TIMER_CHAT * 1000)
event_num += 1
# Cleanup -- Inactive players, expired game messages
EVENT_CLEANUP = event_num + 1
pygame.time.set_timer(EVENT_CLEANUP, TIMER_CLEANUP * 1000)
event_num += 1
# Move inactive players towards door
EVENT_INACTIVE_PLAYER_MOVE = event_num + 1
pygame.time.set_timer(EVENT_INACTIVE_PLAYER_MOVE, TIMER_INACTIVE_PLAYER_MOVE * 1000)
event_num += 1

#endregion

#region Testing code
#######################################################################################################################
desiredTestPlayers = 2
# Create a new player and add to the list
if desiredTestPlayers > 0:
    tonedefff_player = create_player(players, "Tonedefff")
    players.append(tonedefff_player)
if desiredTestPlayers > 1:
    brb_player = create_player(players, "BackRankBot")
    players.append(brb_player)
if desiredTestPlayers > 2:
    info_player = create_player(players, "infomatters")
    players.append(info_player)
if desiredTestPlayers > 3:
    naunii_player = create_player(players, "Nauniime")
    players.append(naunii_player)
if desiredTestPlayers > 4:
    moo_player = create_player(players, "MooChunks")
    players.append(moo_player)
if desiredTestPlayers > 5:
    mad_player = create_player(players, "madzilla_816")
    players.append(mad_player)
if desiredTestPlayers > 6:
    diva_player = create_player(players, "chess_diva")
    players.append(diva_player)
if desiredTestPlayers > 7:
    joshi_player = create_player(players, "ajitesh_joshi")
    players.append(joshi_player)
if desiredTestPlayers > 8:
    aj_player = create_player(players, "AJdaking47")
    players.append(aj_player)
if desiredTestPlayers > 9:
    paladin_player = create_player(players, "paladin_archer")
    players.append(paladin_player)
if desiredTestPlayers > 10:
    kev_player = create_player(players, "kevinc3445")
    players.append(kev_player)
if desiredTestPlayers > 11:
    noor_player = create_player(players, "noor_zaidan")
    players.append(noor_player)
#endregion

#region Main game loop
#########################################################################
game_running = True
while game_running:

    current_time = pygame.time.get_ticks() / 1000

    # Events
    ###################################################################################################################
    for event in pygame.event.get():

        # Quit
        ###############################################################################################################
        if event.type == pygame.QUIT:
            game_running = False


        # Mouse click
        ###############################################################################################################
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click was on any player
            for player in players:
                if player.rect.collidepoint(event.pos):
                    if event.button == 1:
                        print("Left clicked " + player.player_name)
                        make_player_inactive(player, current_time)
                    elif event.button == 3:
                        print("Right clicked " + player.player_name)
                        player.rect.x = TEST_X
                        player.rect.y = TEST_Y
                    break


        # Movement
        ###############################################################################################################
        elif event.type == EVENT_MOVEMENT:
            set_movement_chance(players)
            for player in players:
                player.set_movement()


        # Cleanup
        ###############################################################################################################
        elif event.type == EVENT_CLEANUP:
            # Move players from the players list to the inactive_players list when they have become inactive
            for player in players[:]:
                #print(player.player_name)
                if player.player_name != "Tonedefff" and player.player_name != "BackRankBot":
                    if current_time - player.last_event > PLAYER_EXPIRATION_MINS * 60:
                        make_player_inactive(player, current_time)

            #print(f"Players: {len(players)}. Inactive: {len(inactive_players)}")
            # Remove old game messages
            # Create new lists for messages and timestamps that are not expired
            new_game_text = []
            new_game_text_timestamps = []
            # Loop through all game text messages and their timestamps
            for text, timestamp in zip(game_text, game_text_timestamps):
                if current_time - timestamp <= GAME_MSG_EXPIRATION_SECS:
                    new_game_text.append(text)
                    new_game_text_timestamps.append(timestamp)
            # Update the original lists
            game_text = new_game_text
            game_text_timestamps = new_game_text_timestamps


        # Move inactive players towards door
        ###############################################################################################################
        elif event.type == EVENT_INACTIVE_PLAYER_MOVE:
            for inactive_player in inactive_players:
                move_towards_door(inactive_player)


        # Read chat messages
        ###############################################################################################################
        elif event.type == EVENT_CHAT:
            # Read chat messages
            chat_messages = read_json_with_retry(chatMessagesFile)

            # Process each chat message
            ###########################
            for message in chat_messages:
                if not message.get('processed'):
                    username = message.get("username")
                    msg = message.get("message")

                    # Check if this is a new player that should be added
                    ####################################################
                    if username and len(players) < MAX_TOTAL_PLAYERS:
                        # Check if this username is already a player
                        if not any(player.player_name == username for player in players):
                            # Create and add a new player
                            new_player = create_player(players, username)
                            players.append(new_player)
                            game_msg("welcome to ToneWorld, " + username + "!", current_time)

                    # Loop through each player and find the one who chatted this, and set it as their chat_msg
                    ##########################################################################################
                    for player in players:
                        if player.player_name == username:
                            # Shorten the message if it's over the max
                            player.chat_msg = msg[:MAX_CHAT_LENGTH-2] + ".." if len(msg) > MAX_CHAT_LENGTH else msg
                            message['processed'] = True

                    # ToneWorld commands
                    ##########################################################################################
                    # !twrandom
                    if msg == "!twrandom":
                        player.choose_random_player_image(players)
                    elif msg == "!twpoop":
                        game_msg(username + " poops.", current_time)

            # Write the updated messages back to the file
            #############################################
            if len(chat_messages) > 0:
                write_json_with_retry(chatMessagesFile, chat_messages)

    #################
    # End events loop
    #################


    # Draw ToneWorld background
    ###################################################################################################################
    screen.blit(background_image, (0, 0))


    # Update and draw each player
    ###################################################################################################################
    for player in players:
        player.draw(screen=screen)
        player.update()
        screen.blit(player.image, player.rect)


    # Update and draw inactive players
    ###################################################################################################################
    for player in inactive_players[:]:  # Iterate over a copy of the list
        player.draw(screen=screen)
        # Check if player is near the door, or off the screen
        if ((player.x > EXIT_X - 30 and player.x < EXIT_X + 30 and
             player.y > EXIT_Y - 20 and player.y < EXIT_Y + 20) or
            (player.x < 0 or player.x > WIDTH + PLAYER_SIZE or
             player.y < 0 or player.y > HEIGHT + PLAYER_SIZE)):
            print("Removing player from inactive_players: " + player.player_name)
            inactive_players.remove(player)
        else:
            player.update()


    # Display the latest 3 game messages at top of screen
    ###################################################################################################################
    y = GAME_TEXT_Y
    # Get the last three messages, reverse them so the last one is first
    reversed_game_text = game_text[-3:][::-1]
    # Loop through the game messages
    for i, text in enumerate(reversed_game_text):
        if i == 0:
            msg_font = largest_font
            msg_color = GAME_TEXT_COLOR
            msg_shadow = SHADOW_OFFSET
            msg_line_height = largest_line_height
        elif i == 1:
            msg_font = largerer_font
            msg_color = GAME_TEXT_DARKER_COLOR
            msg_shadow = SHADOW_OFFSET - 1
            msg_line_height = larger_line_height
        else:
            msg_font = larger_font
            msg_color = GAME_TEXT_DARKER_COLOR
            msg_shadow = SHADOW_OFFSET - 1
            msg_line_height = larger_line_height

        draw_text_with_shadow(screen, text, msg_font, msg_color, SHADOW_COLOR, WIDTH / 2, y, msg_shadow)
        y += msg_line_height


    # Draw chat messages in speech bubbles.
    ###################################################################################################################
    for player in players:

        # Check if the player has a chat message that should be displayed
        if player.chat_msg != "" and player.message_start_time:

            # Stop displaying the message after it's been displayed the max amount of time
            time_since_message = current_time - player.message_start_time
            msg_display_timeout = MSG_DISPLAY_TIME
            # Display the message for more time the longer the message is
            msg_length = len(player.chat_msg)
            if msg_length > 90:
                msg_display_timeout += 6
            elif msg_length > 60:
                msg_display_timeout += 4
            elif msg_length > 30:
                msg_display_timeout += 2

            if time_since_message > msg_display_timeout:
                player.chat_msg = ""

            else:
                # Load the correct speech bubble depending on which side of the screen the player is on (left/right)
                if player.x < WIDTH / 2:
                    speech_bubble_image = pygame.image.load("ToneImg/SpeechBubble1.png")
                    bubble_pos_x = player.x + 30
                else:
                    speech_bubble_image = pygame.image.load("ToneImg/SpeechBubble2.png")
                    bubble_pos_x = player.x - 100
                # Make sure the y value is not too high or low
                bubble_pos_y = player.y - speech_bubble_image.get_height()
                if bubble_pos_y < SPEECH_BUBBLE_Y_MIN:
                    bubble_pos_y = SPEECH_BUBBLE_Y_MIN
                speech_bubble_height = speech_bubble_image.get_height()
                if bubble_pos_y > HEIGHT - speech_bubble_height:
                    bubble_pos_y = HEIGHT - speech_bubble_height

                bubble_pos = (bubble_pos_x, bubble_pos_y)

                # Chat speech bubble
                #######################################################################################################
                # Wrap the text into multiple lines (if it's longer than a certain length)
                wrapped_text = textwrap.wrap(player.chat_msg, width=CHAT_TEXT_WRAP)

                # Calculate the total height of the text block
                total_text_height = line_height * len(wrapped_text)
                # Initial y position for text
                text_y = bubble_pos[1] + 10
                # Draw the speech bubble first and then text, so the text is on top
                screen.blit(speech_bubble_image, bubble_pos)
                # Move the text down a bit if there's only one line of text
                if len(wrapped_text) <= 1:
                    text_y = text_y + line_height
                # Loop through and display each line of text
                for line in wrapped_text:
                    # Render each line of the message
                    text_surface = font.render(line, True, CHAT_COLOR)
                    # Calculate the position to center the text in the bubble
                    text_x = bubble_pos[0] + (speech_bubble_image.get_width() - text_surface.get_width()) // 2
                    text_pos = (text_x, text_y)
                    # Draw the text line
                    screen.blit(text_surface, text_pos)
                    # Move text_y down for the next line
                    text_y += line_height

    if DISPLAY_FPS:
        fps = clock.get_fps()
        fps_text = font.render(f"{int(fps)} fps", True, CHAT_TEXT_COLOR)
        screen.blit(fps_text, (screen.get_width() - fps_text.get_width() - 10, 10))

    # Draw the entire frickin' screen
    pygame.display.update()
    clock.tick(FPS)

    # MAIN GAME LOOP END
    ###################################################################################################################
#endregion

pygame.quit()