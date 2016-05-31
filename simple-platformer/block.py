import pygame
from config import *

class Block(pygame.sprite.Sprite):

	def __init__(self, x, y, width, height, blockSpeed):

		## Speed of block
		self.blockSpeed = blockSpeed

		## Call constructor of parent class
		pygame.sprite.Sprite.__init__(self)

		## Image
		self.image = pygame.Surface([width, height])
		self.image.fill((0, 0, 0))

		## Rectangle
		self.rect = self.image.get_rect()
		self.rect[0] = x
		self.rect[1] = y

	## Method to update position of block
	def update(self, loopCount):
		if loopCount % int(FRAME_RATE / 5) == 0:
			self.blockSpeed = -self.blockSpeed ## Reverse speed of block

		## Update speed of block as long as on screen
		self.rect[0] += self.blockSpeed
		if self.rect[0] < -2 or self.rect[0] > GAME_WIDTH * N_SCREENS - self.rect[2] + 4:
			self.rect[0] -= self.blockSpeed

	def render(self, window):
		pygame.draw.rect(window, (0, 0, 0), (self.rect[0], self.rect[1], self.rect[2], self.rect[3]))