import os.path
import util
import array
import pygame

class LevelMap:
	VOID, WALL, FLOOR = range(3)

	def __init__(self, mapfile, tilefile, tilemapping):

		self.table = array.array('b')
		self.width = 0
		self.height = 0

		# In my opinion the name should be "splittext".
		_, ending = os.path.splitext(mapfile)
		
		# There are different filetypes for levels supported.
		if ending == '.png':
			lvl_img = pygame.image.load(mapfile)
			# prepare for pixel acces:
			lvl_img = pygame.PixelArray(lvl_img)
			
			self.width = len(lvl_img)
			self.height = len(lvl_img[0])
			print("%d * %d"%(self.height,self.width))

			for row in lvl_img:
				for color in row:
					if color == 0x999999:
						self.table.append(self.WALL)
					elif color == 0xffffff:
						self.table.append(self.FLOOR)
					else: # or 0x000000:
						self.table.append(self.VOID)
		else:
			raise IOError("Error: File suffix '%s'\
					not supported for map-data." % ending)

		# Prepare tileset
		self.__tileset = util.load_image(tilefile)
		self.__tilemapping = tilemapping


	def show(self, screen, offset):
		TILESIZE = 32

		index = 0
		for x in range(self.width):
			for y in range(self.height):
				pos = self.__tilemapping[self.table[index]]
				screen.blit(
						self.__tileset,
						(x*TILESIZE + offset[0], y*TILESIZE + offset[1]),
						(pos[0], pos[1], TILESIZE, TILESIZE))
				index += 1


