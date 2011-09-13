import pygame
from  os.path import join

def load_image(image_filename, simple=False, colorkey = (255, 0, 255)):
	path = join("..","images",image_filename)
		# If the game runs from within the "src"-directory we first have
		# to go one level up ("..").
	
	try:
		img = pygame.image.load(path)
		if not simple:
			img.set_colorkey(colorkey, pygame.locals.RLEACCEL)
			img = img.convert()
		return img
	except pygame.error, message:
		print('Cannot load image: '+path)
		return None


