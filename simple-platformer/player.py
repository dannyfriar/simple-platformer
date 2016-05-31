import pygame
from config import *

class Player(pygame.sprite.Sprite):

	def __init__(self, x, y, color, width, height):

		## Player variables
		self.velocity = 0
		self.falling = True
		self.onGround = False
		self.moveX = 0
		self.health = MAX_HEALTH

		## Constructor of parent class
		pygame.sprite.Sprite.__init__(self)

		## Image
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
		# self.images = pygame.image.load("res/playersprites.png")
		# self.numImages = 16
		# self.cImage = 0

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

		self.velocity = JUMP_SPEED
		self.onGround = False


	## Method to update x, y positions of player
	def update(self, blockList, inputMap, tokenList, loopCount):

		##---- Y MOVEMENT ----##
		## Update y velocity based on keyboard input
		if inputMap[2]:
			self.jump()

		## Update falling
		if self.velocity < 0:
			self.falling = True

		## Check for top collision
		topCollision = False
		self.onGround = False
		yColBlock = 0
		blockSpeed = 0
		for block in blockList:
			if self.rect.colliderect(block) == True:
				if self.velocity <= 0 and self.rect.bottom <= block.rect.bottom:
					topCollision = True
					yColBlock = block.rect[1]     ## Save position of block causing collision
					blockSpeed = block.blockSpeed ## Save velocity of block causing collision
				break

		## Stop block falling if collision with ground
		if topCollision == True:
			if self.falling == True:
				self.falling = False
				self.onGround = True
				self.velocity = 0
				self.rect[1] = yColBlock - self.rect[3] + 1

		## Update y velocity of player - cap this at certain value (NEED TO DO THIS)
		if self.onGround == False:
			self.velocity += GRAVITY

		self.rect[1] -= self.velocity ## Update y position of player


		##---- X MOVEMENT----##
		## Update from key input
		self.moveX = 0
		if inputMap[0]:
			self.moveX += MOVE_SPEED
		if inputMap[1]:
			self.moveX -= MOVE_SPEED

		## Account for speed of block if moving
		if topCollision == True and blockSpeed != 0:
			self.moveX += blockSpeed

		# ## Check for side collision (x velocity update in main game loop)
		# sideCollision = 0
		# if topCollision == False:
		# 	for block in blockList:
		# 		if self.rect.colliderect(block) == True:
		# 			if self.moveX > 0:
		# 				sideCollision = 1
		# 			elif self.moveX < 0:
		# 				sideCollision = -1

		# ## Update x velocity as a result of side collision (to make player rebound slightly)
		# if sideCollision != 0:
		# 	self.moveX = 0

		## Update x position of player but keep on screen
		self.rect[0] += self.moveX
		if self.rect[0] < -2 or self.rect[0] > GAME_WIDTH * N_SCREENS - self.rect[2] + 4:
			self.rect[0] -= self.moveX


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
		# if self.moveX != 0:
		# 	## Get next sprite unless at end of sprite sheet i.e. animate
		# 	if (self.cImage >= self.numImages - 1):
		# 		self.cImage = 0
		# 	else:
		# 		self.cImage += 1


	def render(self, window):
		pygame.draw.rect(window, (0, 0, 0), (self.rect[0], self.rect[1], self.rect[2], self.rect[3]))