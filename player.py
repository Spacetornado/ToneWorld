import pygame, random, os, glob, math
from settings import *
from utils import *

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, playerList, player_name):
		super().__init__(groups)
		now = pygame.time.get_ticks() / 1000

		self.movement_chance = RAND_MOVE_CHANCE
		self.is_moving = False
		self.is_leaving = False
		self.load_time = now
		self.last_event = now
		self.animation_frame = 0
		self.frame_update_counter = 0
		self.frame_update_delay = random.randint(FRAME_UPDATE_DELAY_MIN, FRAME_UPDATE_DELAY_MAX)
		self.direction = (0, 0)
		self.move_timer = 0
		self.start_move_time = 0
		self._player_name = player_name
		self.image_base = player_name
		self.is_random = False
		self.message_start_time = None
		self._chat_msg = ""
		self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
		image_path = f'ToneImg/ch_{player_name}.png'

		# Check if an image file matching this player's name exists. If not, choose a random player image.
		if not os.path.exists(image_path):
			self.choose_random_player_image(playerList)
			self.is_random = True

		self.image = pygame.image.load(f'ToneImg/ch_{self.image_base}.png').convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)


	@property
	def chat_msg(self):
		"""Get the player's chat message."""
		return self._chat_msg

	@chat_msg.setter
	def chat_msg(self, value):
		"""Set the chat message and set the message_start_time to now."""
		self._chat_msg = value
		if value:
			self.message_start_time = pygame.time.get_ticks() / 1000
			self.update_last_event()

	def draw(self, screen):
		# Draw the player image
		screen.blit(self.image, self.rect)
		# Render the text
		text_surface = self.font.render(self.player_name, True, CHAT_TEXT_COLOR)
		text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.bottom + 10))
		# Create a background rectangle
		background_rect = text_surface.get_rect()
		background_rect.center = text_rect.center
		background_rect.inflate_ip(2, 1)
		# Draw the rectangle and text
		pygame.draw.rect(screen, TEXT_BG_COLOR, background_rect)
		screen.blit(text_surface, text_rect)

	#def change_direction(self):
#		"""Randomly choose a new direction"""
		#while True:
	#		dx = random.uniform(-1, 1)  # Generate a float between -1 and 1
	#		dy = random.uniform(-1, 1)  # Generate a float between -1 and 1
	#		# Check if dx and dy are not within 0.2 of 0
	#		if abs(dx) > 0.2 and abs(dy) > 0.2:
	#			break
	#	self.direction = (dx, dy)
	def change_direction(self):
		"""Randomly choose a new direction at any angle between 0 to 360 degrees"""
		angle = random.uniform(0, 2 * math.pi)  # Generate a random angle in radians
		dx = math.cos(angle)  # Calculate dx based on the cosine of the angle
		dy = math.sin(angle)  # Calculate dy based on the sine of the angle
		self.direction = (dx, dy)

	def set_movement(self):
		self.is_moving = random.random() < self.movement_chance
		if self.is_moving:
			self.change_direction()

			# Set a random movement duration
			self.move_timer = random.uniform(MOVE_MIN_S, MOVE_MAX_S)
			self.start_move_time = pygame.time.get_ticks() / 1000

			# Set a random animation speed
			self.frame_update_delay = random.randint(FRAME_UPDATE_DELAY_MIN, FRAME_UPDATE_DELAY_MAX)
		else:
			self.direction = (0, 0)

	def update_last_event(self):
		"""Update the last event time to the current time."""
		self.last_event = pygame.time.get_ticks() / 1000

	def update(self):
		current_time = pygame.time.get_ticks() / 1000

		if self.is_moving:
			self.update_animation()

			# Check if the move timer has expired
			has_move_expired = current_time - self.start_move_time > self.move_timer
			if not self.is_leaving and has_move_expired:
				self.stop_moving()
			else:
				# Calculate the new position
				new_x = self.rect.x + self.direction[0] * PLAYER_MOVE_SPEED
				new_y = self.rect.y + self.direction[1] * PLAYER_MOVE_SPEED

				# Check if the new position is good (unless the player is leaving)
				if are_coords_good(new_x, new_y) or self.is_leaving:
					# Update the player's position if the new position is good
					self.rect.x = new_x
					self.rect.y = new_y
				else:
					self.stop_moving()
					# Choose a new direction in the opposite X and/or Y direction
					opposite_dx = -self.direction[0] if self.direction[0] != 0 else random.choice([-1, 1])
					opposite_dy = -self.direction[1] if self.direction[1] != 0 else random.choice([-1, 1])
					self.direction = (opposite_dx, opposite_dy)
					if self.rect.x < PLAYER_X_MIN:
						self.rect.x = PLAYER_X_MIN + 1
					if self.rect.x > PLAYER_X_MAX:
						self.rect.x = PLAYER_X_MAX - 1
					if self.rect.y < PLAYER_Y_MIN:
						self.rect.y = PLAYER_Y_MIN + 1
					if self.rect.y > PLAYER_Y_MAX:
						self.rect.y = PLAYER_Y_MAX - 1

	def set_animation_image(self):
		animation_image_path = f'{player_animation_path}/ch_{self.image_base}_{self.animation_frame}.png'
		self.image = pygame.image.load(animation_image_path).convert_alpha()

	def stop_moving(self):
		# Stop moving and load the default image
		self.is_moving = False
		self.animation_frame = 0
		self.set_animation_image()

	def update_animation(self):
		# Only update if moving
		if self.is_moving:
			self.frame_update_counter += 1
			# Update the frame only after every 'frame_update_delay' updates
			if self.frame_update_counter >= self.frame_update_delay:
				# Reset the counter
				self.frame_update_counter = 0
				# Update the player's image based on the current animation frame
				self.set_animation_image()
				# Increment the animation frame, looping back if necessary
				self.animation_frame = (self.animation_frame + 1) % TOTAL_ANIMATION_FRAMES

	def choose_random_player_image(self, playerList):
		# Count the number of random players
		num_random_players = 0
		for player in playerList:
			if player.is_random:
				num_random_players = num_random_players + 1
		# Find image files matching the pattern and choose a random image
		random_char_images = glob.glob('ToneImg/ch_TWRandChar*.png')
		if random_char_images:
			image_path = random.choice(random_char_images)
			self.image_base = get_player_image_name(image_path)
			# Avoid using same random player image repeatedly, but only if there are fewer random characters than available
			if num_random_players < MAX_RANDOM_PLAYERS:
				random_image_in_use = True
				while random_image_in_use:
					image_path = random.choice(random_char_images)
					self.image_base = get_player_image_name(image_path)
					random_image_in_use = False
					# Search all players to see if image in use
					for player in playerList:
						if self.image_base == player.image_base:
							random_image_in_use = True
		else:
			image_path = 'ToneImg/ch_TWDefault.png'
			image_base = 'TWDefault'

	@property
	def player_name(self):
		"""Get the player's name."""
		return self._player_name

	@player_name.setter
	def player_name(self, value):
		"""Set the player's name."""
		self._player_name = value

	@property
	def x(self):
		"""Get the player's x pos."""
		return self.rect.x
	@property
	def y(self):
		"""Get the player's y pos."""
		return self.rect.y


