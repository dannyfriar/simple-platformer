import pygame
from config import *
from spritesheet import *

class Player(pygame.sprite.Sprite):

	def __init__(self, x=START_X, y=START_Y, color=BLACK, width=PLAYER_WIDTH, height=PLAYER_HEIGHT, 
		imageFile=PLAYER_IMG, imageN=1):

		## Player variables
		self.vY = 0
		self.falling = True
		self.onGround = False
		self.vX = 0
		self.health = MAX_HEALTH

		## Constructor of parent class
		pygame.sprite.Sprite.__init__(self)

		# ## Image (simple rectangle)
		# self.image = pygame.Surface([width, height])
		# self.image.fill(color)

		##----- Image from spritesheet
		## Load spritesheet
		spritesheet = SpriteSheet(imageFile, imageN, width, height)
		self.numImages = spritesheet.numImages
		self.player_img = spritesheet.get_all_images()

		## Display first image from spritesheet
		self.cImage = 0
		self.image = self.player_img[self.cImage]

		## Rectangle
		self.rect = self.image.get_rect()
		self.rect[0] = x
		self.rect[1] = y
		self.rect[2] = width
		self.rect[3] = height


	## Jump method
	def jump(self):
		if self.onGround == False:
			return

		self.vY = JUMP_SPEED
		self.onGround = False


	## Method to update x, y positions of player
	def update(self, blockList, inputMap, tokenList, loopCount):

		##---- Y MOVEMENT ----##
		## Update y velocity based on keyboard input
		if inputMap[2]:
			self.jump()

		## Update falling
		if self.vY < 0:
			self.falling = True

		## Check for top collision
		topCollision = False
		self.onGround = False
		yColBlock = 0
		blockSpeed = 0
		for block in blockList:
			if self.rect.colliderect(block) == True:
				if self.vY <= 0 and self.rect.bottom <= block.rect.bottom:
					topCollision = True
					yColBlock = block.rect[1] # Save position of block causing collision
					blockSpeed = block.blockSpeed # Save vY of block causing collision
				break

		## Stop block falling if collision with ground
		if topCollision == True:
			if self.falling == True:
				self.falling = False
				self.onGround = True
				self.vY = 0
				self.rect[1] = yColBlock - self.rect[3] + 1

		## Update y vY of player - cap this at certain value (NEED TO DO THIS)
		if self.onGround == False:
			self.vY += GRAVITY

		## Update y position of player
		self.rect[1] -= self.vY


		##---- X MOVEMENT----##
		## Update from key input
		self.vX = 0
		if inputMap[0]:
			self.vX += MOVE_SPEED
		if inputMap[1]:
			self.vX -= MOVE_SPEED

		## Account for speed of block if moving
		if topCollision == True and blockSpeed != 0:
			self.vX += blockSpeed

		# ## Check for side collision (x vY update in main game loop)
		# sideCollision = 0
		# if topCollision == False:
		# 	for block in blockList:
		# 		if self.rect.colliderect(block) == True:
		# 			if self.vX > 0:
		# 				sideCollision = 1
		# 			elif self.vX < 0:
		# 				sideCollision = -1

		# ## Update x vY as a result of side collision (to make player rebound slightly)
		# if sideCollision != 0:
		# 	self.vX = 0

		## Update x position of player but keep on screen
		self.rect[0] += self.vX
		if self.rect[0] < -2 or self.rect[0] > GAME_WIDTH * N_SCREENS - self.rect[2] + 4:
			self.rect[0] -= self.vX


		##--- UPDATE HEALTH ---##
		## Decrement health every second
		if loopCount % int(FRAME_RATE / 10) == 0:
			self.health -= 1

		## Add to health if token collected
		tokenHitList = pygame.sprite.spritecollide(self, tokenList, True)
		for token in tokenHitList:
			self.health += 20

		## Make sure health doesn't exceed max value
		if self.health > MAX_HEALTH:
			self.health = MAX_HEALTH


		##--- ANIMATION ---##
		if self.vX != 0:
			## Get next sprite unless at end of sprite sheet i.e. animate
			if (self.cImage >= self.numImages - 1):
				self.cImage = 0
			else:
				self.cImage += 1

		## Get the corresponding player image	
		self.image = self.player_img[self.cImage]


	def render(self, window):
		# pygame.draw.rect(window, (0, 0, 0), (self.rect[0], self.rect[1], self.rect[2], self.rect[3])) # Draw simple rectangle
		window.blit(self.image, (self.rect[0], self.rect[1], self.rect[2], self.rect[3])) # Draw image