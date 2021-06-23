import pygame
import sys
import random
import time
import csv


# ------- Set Parameters --------------- #
fps = 60
screen_size = (1024, 576)
display_size = (screen_size[0]/2, screen_size[1]/2) # Will be scaled to screen size (Use when sprites added)

# ------- Set Colours ------------------ #
WHITE  = (255,255,255)
BLACK  = (0  ,0  ,0  )
RED    = (150,0  ,0  )
GREEN  = (0  ,150,0  )
BLUE   = (0  ,0  ,150)
YELLOW = (230,200,0  )

DARK_GREY = (20 ,20 ,20 )
SUNSET    = (250,214,165)

# ------- Init pygame ------------------ #
pygame.init()                      #    pygame.FULLSCREEN
screen = pygame.display.set_mode(screen_size, 0, 32)
pygame.display.set_caption('Platformer Prototype')

display = pygame.Surface(display_size) # Will be used with sprites

my_font = pygame.font.SysFont('impact', 30)
clock = pygame.time.Clock()


# ------- Load sprites ----------------- #

	#--Background
sunset = pygame.image.load('Sprites/Background/Sunset.png').convert()

	#--Player
player_idle_sprite = [pygame.image.load('Sprites/Player/Default_0.png').convert(),
					  pygame.image.load('Sprites/Player/Default_1.png').convert(),
					  pygame.image.load('Sprites/Player/Default_2.png').convert()]

for i in range(len(player_idle_sprite)):
	player_idle_sprite[i].set_colorkey((0,0,0))

player_attack_sprite = [pygame.image.load('Sprites/Player/Attack_0.png').convert(),
						pygame.image.load('Sprites/Player/Attack_1.png').convert(),
						pygame.image.load('Sprites/Player/Attack_2.png').convert()]

for i in range(len(player_attack_sprite)):
	player_attack_sprite[i].set_colorkey((0,0,0))

	#-- Ground
grass_sprite = pygame.image.load('Sprites/Ground/Grass_new.png').convert()
dirt_sprite  = pygame.image.load('Sprites/Ground/Dirt_new.png').convert()

grass_sprite.set_colorkey((0,0,0)) 
dirt_sprite.set_colorkey((0,0,0))

	#-- Crosshair
crosshair = pygame.image.load('Sprites/Crosshair/Crosshair.png').convert()

crosshair.set_colorkey((255,255,255))

	#-- Tile size
tile_size_x, tile_size_y = dirt_sprite.get_size()


# ------- Map Grid --------------------- #
with open('Grid/Map_Grid.csv') as file:
	reader = csv.reader(file)#, delimiter = ' ')

	tile_grid = []
	for row in reader:
		tile_grid.append(row)


# ------- Init Variables --------------- #
player_attacks = False 
player_y_momentum = 0
	# How much object will speed up downwards every frame
gravity = 0.2
movement_speed = 2
jump_force = -5.5
air_timer = 0
jump_count = 0

player_rect = pygame.Rect((50,50), (player_idle_sprite[0].get_width(), player_idle_sprite[0].get_height()))

moving_right = False
moving_left = False
jumping = False

sprite_tracker = 0
sprite_to_play = 0


# ------- Functions ------------------- #
def collision(player, tiles):
	hit_list = []
	for tile in tiles:
		if player.colliderect(tile):
			hit_list.append(tile)

	return hit_list


def move_player(player, movement, tiles):
	collision_type = {'top' : False, 'bottom' : False, 'right' : False, 'left' : False}

	player.x += movement[0]
	hit_list = collision(player, tiles)
	for tile in hit_list:
		if movement[0] > 0:
				# Pygame function which can set a side of rectangle to a position
				# In this case we set right side of player to left side of tile we are colliding with
			player.right = tile.left
			collision_type['right'] = True
		elif movement[0] < 0:
			player.left = tile.right
			collision_type['left'] = True

	player.y += movement[1]
	hit_list = collision(player, tiles)
	for tile in hit_list:
		if movement[1] > 0 :
			player.bottom = tile.top
			collision_type['bottom'] = True
		elif movement[1] < 0:
			player.top = tile.bottom
			collision_type['top'] = True

	
	return player, collision_type






# ------- MAIN LOOP ------------------------------------------------------------ #
while True:

	tile_rects = []

	# --Sprite animation tracker
	if sprite_tracker < 10:
		sprite_to_play = 0
	elif sprite_tracker < 20:
		sprite_to_play = 1
	elif sprite_tracker < 40:
		sprite_to_play = 2
	elif sprite_tracker < 50:
		sprite_to_play = 1
	elif sprite_tracker < 70:
		sprite_to_play = 0
	else:
		sprite_tracker = 0

	sprite_tracker += 1


	# --Reset display
	display.blit(sunset, (0,0))
	
	# --Set fps
	clock.tick(fps)

	# --Get mouse pos
	mouse_x, mouse_y = pygame.mouse.get_pos()

	# --Handle keys/input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			player_attacks = True

		if event.type == pygame.MOUSEBUTTONUP:
			player_attacks = False

		# --Movement keys
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a or event.key == pygame.K_LEFT:
				moving_left = True
			if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
				moving_right = True
			# --Jump
			if event.key == pygame.K_SPACE:
				if air_timer < 6:
					player_y_momentum += jump_force
				# 	jumping = True
				# else:
				# 	jumping = False

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a or event.key == pygame.K_LEFT:
				moving_left = False
			if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
				moving_right = False



	# --Display tiles
	for i in range(len(tile_grid)):   # *** FOR LOOP SOMEHOW BROKEN. X ALWAYS SHOWN AS 0 IN THIS CASE
		for j in range(len(tile_grid[i])):    # ONLY POSSIBLE WAY IS IF ROW IS 0 AND LOOP INSTA RESETS TO X=0
				# Dirt
			if int(tile_grid[i][j]) == 0:
				display.blit(dirt_sprite, (j*tile_size_x, i*tile_size_y))
				# Grass
			if int(tile_grid[i][j]) == 1:
				display.blit(grass_sprite, (j*tile_size_x, i*tile_size_y))

				# Logs position and size (rects) of each tile for use in collision
			if int(tile_grid[i][j]) != -1:
				tile_rects.append(pygame.Rect((j*tile_size_x, i*tile_size_y), (tile_size_x, tile_size_y)))


	# --Display player 
	if player_attacks:
		display.blit(player_attack_sprite[sprite_to_play], (player_rect.x, player_rect.y))
	else:										 # Have to divide by two because display is half the
		display.blit(player_idle_sprite[sprite_to_play], (player_rect.x, player_rect.y)) # size of screen and is just scaled to screen size


	# --Display crosshair          Divided by 2 because display scaled to screen size and its double its size
	display.blit(crosshair, (mouse_x/2 - 3, mouse_y/2 - 3))

	# --Player movement
	player_movement = [0, 0]
	if moving_right:
		player_movement[0] += movement_speed
	elif moving_left:
		player_movement[0] -= movement_speed
		# --Gravity
	player_movement[1] += player_y_momentum
	player_y_momentum += gravity
			# --Caps falling speed
	if player_y_momentum > 5:
		player_y_momentum = 5

	player_rect, collisions = move_player(player_rect, player_movement, tile_rects)

		# --Jumping
	# if jumping:
	# 	player_y_momentum += jump_force
	if collisions['bottom']:
		player_y_momentum = 0
		air_timer = 0
		jumping = False
	elif collisions['top']:
		player_y_momentum = 0
	else:
		air_timer += 1



		# Scales display to same size as screen and thus scaling sprite size 
	surf_transform = pygame.transform.scale(display, screen_size)
	screen.blit(surf_transform, (0, 0))
	pygame.display.update()
