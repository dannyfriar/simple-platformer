import pygame
from config import *

class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """
    sprite_sheet = None


    def __init__(self, fileName, numImages, width, height):

    	## Load the spritesheet image
        self.spriteSheet = pygame.image.load(fileName)

        ## Load the charactersitics of the invidual images within the sheet
        self.numImages = numImages
        self.width = width
        self.height = height


    ## Grab a single image from a larger spritesheet - takes the x, y locations and width,height of the image
    def get_single_image(self, index):

	    ## Create a new blank image
	    image = self.spriteSheet.subsurface((self.width*index, 0, self.width, self.height))

	    # ## Assuming black works as the transparent color
	    # image.set_colorkey(constants.BLACK)

	    return image


    ## Load all images from spritesheet into list
    def get_all_images(self):

    	imageList = []
    	for i in range(0, self.numImages):
    		imageList.append(self.get_single_image(i))

    	return imageList