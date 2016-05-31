import pygame
from pygame.locals import *

pygame.init()
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test")
BLUE = (50, 60, 200)

## Block
class Block(pygame.sprite.Sprite):

	def __init__(self, image="res/dark_block1.png"):
		pygame.sprite.Sprite.__init__(self)

		## Load block image
		self.image = pygame.image.load(image)

	def render(self, window):
		window.blit(self.image, (100, 100))


## Gameloop
while True:
	for event in pygame.event.get():
		if (event.type == pygame.QUIT):
			pygame.display.quit()
			pygame.quit()

	window.fill(BLUE)

	## Display block
	my_block = Block()
	my_block.render(window)

	pygame.display.flip()