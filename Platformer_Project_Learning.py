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

# ------- Init pygame ------------------ #
pygame.init()
screen = pygame.display.set_mode(screen_size, 0, 32)
pygame.display.set_caption('Platformer Prototype')

display = pygame.Surface(display_size) # Will be used with sprites

my_font = pygame.font.SysFont('impact', 30)
clock = pygame.time.Clock()


# ------- Load sprites ----------------- #

	#--Player
player_idle_sprite = pygame.image.load('Sprites/Player/Player_Default_0.png')
player_attack_sprite = pygame.image.load('Sprites/Player/Player_Attack_0.png')

	#-- Ground
grass_sprite = pygame.image.load('Sprites/Ground/Grass.png')
dirt_sprite  = pygame.image.load('Sprites/Ground/Dirt.png')

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






# ------- MAIN LOOP ------------------------------------------------------------ #
while True:
	# --Reset display
	display.fill(DARK_GREY)
	
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


	# --Display tiles
	for i in range(len(tile_grid)):   # *** FOR LOOP SOMEHOW BROKEN. X ALWAYS SHOWN AS 0 IN THIS CASE
		for j in range(len(tile_grid[i])):    # ONLY POSSIBLE WAY IS IF ROW IS 0 AND LOOP INSTA RESETS TO X=0
				# Dirt
			if int(tile_grid[i][j]) == 0:
				display.blit(dirt_sprite, (j*tile_size_x, i*tile_size_y))
				# Grass
			if int(tile_grid[i][j]) == 1:
				display.blit(grass_sprite, (j*tile_size_x, i*tile_size_y))


	# --Display player 
	if player_attacks:
		display.blit(player_attack_sprite, (mouse_x/2 - tile_size_x/2, mouse_y/2 - tile_size_y/2))
	else:										 # Have to divide by two because display is half the
		display.blit(player_idle_sprite, (mouse_x/2 - tile_size_x/2, mouse_y/2 - tile_size_y/2)) # size of screen and is just scaled to screen size


		# Scales display to same size as screen and thus scaling sprite size 
	surf_transform = pygame.transform.scale(display, screen_size)
	screen.blit(surf_transform, (0, 0))
	pygame.display.update()
