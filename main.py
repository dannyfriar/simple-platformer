import pygame
import math
import random
import time
from pygame.locals import *
from player import *
from block import *
from camera import *
from token import *
from config import * # Import global constant variables and level array


##---- CAMERA METHOD - considering including in Camera class ----## 
def complex_camera(camera, target_rect):
	l, _, _, _ = target_rect 	# l = left
	_, t, w, h = camera 	# t = top, w = width, h = height (change this to add up/down scroll)
	l, t, _, _ = -l+HALF_WIDTH, -t, w, h 	# center player

	l = min(0, l) 	# stop scrolling at left edge
	l = max(-(camera.width - GAME_WIDTH), l)	 # stop scrolling at the right edge
    # t = max(-(camera.height - GAME_HEIGHT), t) # stop scrolling at the bottom
    # t = min(0, t)                              # stop scrolling at the top

	return Rect(l, t, w, h)


##---- CREATE LEVEL OBJECTS - blocks and tokens -----##
def create_level(blockList=[], tokenList=[]):
	for y in range(0, len(level1)):
		for x in range(0, len(level1[y])):

			if level1[y][x] == -1: # floor blocks
				blockList.append(Block(x * BLOCK_WIDTH, y * BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT, BLOCK_SPEED_1, image=FLOOR_BLOCK))
				# blockList.append(Block(x * BLOCK_WIDTH, y * BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT, BLOCK_SPEED_1, image=FLOOR_BLOCK))

			if level1[y][x] == 1: # stationary blocks (but not floor)
				blockList.append(Block(x * BLOCK_WIDTH, y * BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT, BLOCK_SPEED_1))

			if level1[y][x] == 2: # moving blocks
				blockList.append(Block(x * BLOCK_WIDTH, y * BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT, BLOCK_SPEED_2))

			if level1[y][x] == 3: # moving blocks opposite direction
				blockList.append(Block(x * BLOCK_WIDTH, y * BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT, -BLOCK_SPEED_2))

			if level1[y][x] == 4: # stationary blocks + token
				blockList.append(Block(x * BLOCK_WIDTH, y * BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT, BLOCK_SPEED_1))
				tokenList.append(Token(x * BLOCK_WIDTH, y * BLOCK_HEIGHT, TOKEN_WIDTH, TOKEN_HEIGHT, BLOCK_SPEED_1))

	blockList = pygame.sprite.Group(blockList)
	tokenList = pygame.sprite.Group(tokenList)
	return [blockList, tokenList]


##---- GAME OVER LOOP ----##
def gameOver():
	gameOver = True
	while gameOver:

		## Display choice
		text = font.render('You died! Space to play again or Esc to quit', 13, (0, 0, 0))
		textx = GAME_WIDTH / 2 - text.get_width() / 2
		texty = GAME_HEIGHT / 2 - text.get_height() / 2
		textx_size = text.get_width()
		texty_size = text.get_height()
		pygame.draw.rect(window, (255, 255, 255), ((textx - 5, texty - 5), (textx_size + 10, texty_size + 10)))
		window.blit(text, (GAME_WIDTH / 2 - text.get_width() / 2, GAME_HEIGHT / 2 - text.get_height() / 2))

		## Check player's keyboard input
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				pygame.display.quit()
				pygame.quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				gameOver = False

		clock.tick(FRAME_RATE)
		pygame.display.flip()

	game_loop()


##----- PAUSE MENU ------##
def pause():
	paused = True
	while paused:

		## Display choice
		pygame.mixer.music.pause()
		text = font.render('Game paused! Space to continue or Esc to quit', 13, (0, 0, 0))
		textx = GAME_WIDTH / 2 - text.get_width() / 2
		texty = GAME_HEIGHT / 2 - text.get_height() / 2
		textx_size = text.get_width()
		texty_size = text.get_height()
		pygame.draw.rect(window, (255, 255, 255), ((textx - 5, texty - 5), (textx_size + 10, texty_size + 10)))
		window.blit(text, (GAME_WIDTH / 2 - text.get_width() / 2, GAME_HEIGHT / 2 - text.get_height() / 2))

		## Check player's keyboard input
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				pygame.display.quit()
				pygame.quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				paused = False
				pygame.mixer.music.unpause()

		clock.tick(FRAME_RATE)
		pygame.display.flip()


##------ GAME LOOP ------##
def game_loop():

	## Set variables
	loopCount = 0                    
	inputMap = [False, False, False] # For key mapping
	gameLoop = True
	paused = False

	## Create objects (blocks, tokens, camera and player)
	blockList = create_level()[0]
	tokenList = create_level()[1]
	camera = Camera(complex_camera, GAME_WIDTH * N_SCREENS, GAME_HEIGHT * N_SCREENS) # Instance of camera
	player = Player(imageN=5) # Instance of player

	## Start music
	pygame.mixer.music.load(START_MUSIC)
	pygame.mixer.music.play(-1)
	pygame.mixer.music.set_volume(0.5)
	# sound.play()

	## Loop
	while gameLoop:
		loopCount += 1 # increment loop counter

		## Event loops
		for event in pygame.event.get():

			if (event.type == pygame.QUIT):
				pygame.display.quit()
				pygame.quit()

			## Key pressed down
			inputMap[2] = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_d:
					inputMap[0] = True
				elif event.key == pygame.K_a:
					inputMap[1] = True
				elif event.key == pygame.K_w:
					inputMap[2] = True
				elif event.key == pygame.K_SPACE:
					paused = True
					pause()

			## Key released
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_d:
					inputMap[0] = False
				elif event.key == pygame.K_a:
					inputMap[1] = False


		window.fill(BLUE)     # Fill window
		camera.update(player) # Update camera

		## Update blocks
		for block in blockList:
			block.update(loopCount)

		## Update player
		player.update(blockList, inputMap, tokenList, loopCount)

		## Draw everything (blocks, tokens and player)
		for block in blockList:
			window.blit(block.image, camera.apply(block))
		for token in tokenList:
			window.blit(token.image, camera.apply(token))
		window.blit(player.image, camera.apply(player))

		## Display player's health
		strHealth = "Health: " + str(player.health)
		text = font.render(strHealth, 1, (FONT_X, FONT_Y, 0))
		textPos = text.get_rect()
		window.blit(text, textPos)

		## Display restart option if player dies
		if player.health == 0:
			gameOver()

		clock.tick(FRAME_RATE)
		pygame.display.flip()


## Initialize PyGame and run game
if __name__ == '__main__':
	pygame.init()
	pygame.mixer.music.set_volume(0.3)
	window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
	pygame.display.set_caption("Platformer")
	clock = pygame.time.Clock()
	font = pygame.font.Font(None, FONT_SIZE)

	game_loop() ## RUN GAME