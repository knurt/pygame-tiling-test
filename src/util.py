import pygame

def load_image(path):
	
	colorkey = (255, 0, 255)
	try:
		img = pygame.image.load(path)
		img.set_colorkey(colorkey, pygame.locals.RLEACCEL)
		img = img.convert()
		return img
	except pygame.error, message:
		print('Cannot load image: '+path)
		return None


