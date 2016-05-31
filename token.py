import pygame
from config import *
from block import *

class Token(Block):

	def __init__(self, x, y, width, height, blockSpeed, image=PILL):

		## Call constructor of block class
		Block.__init__(self, x, y, width, height, blockSpeed, image)

		## Displace token to sit above (and in middle of) corresponding platform
		self.rect[0] = self.rect[0] + int(BLOCK_WIDTH / 2) - int(TOKEN_WIDTH / 2)
		self.rect[1] = self.rect[1] - DISPLACE_TOKEN