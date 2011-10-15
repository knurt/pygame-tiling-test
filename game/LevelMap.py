import os.path
import util
import array
import pygame

class LevelMap:
    VOID, WALL, FLOOR = range(3)

    def __init__(self, mapfile, tilefile,
            tilemapping, tilesize):
        self.tilesize = tilesize

        self.table = array.array('b')
        self.mapwidth = 0
        self.mapheight = 0

        # In my opinion the name should be "splittext".
        _, ending = os.path.splitext(mapfile)
        
        # There are different filetypes for levels supported.
        if ending == '.png':
            lvl_img = util.load_image(mapfile, True)
            # prepare for pixel acces:
            lvl_img = pygame.PixelArray(lvl_img)
            
            self.mapwidth = len(lvl_img)
            self.mapheight = len(lvl_img[0])

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
            sys.exit(0)

        # Prepare tileset
        self.__tileset = util.load_image(tilefile)
        self.__tilemapping = tilemapping
    

    def pixel_pos_to_tile_pos(self, pos):
        # Coordinates of the tile the pixel is on:
        tile_x = pos[0] / self.tilesize
        tile_y = pos[1] / self.tilesize

        return (tile_x, tile_y)


    def pixel_pos_to_tile_offset(self, pos):
        # Distances in x and y dimension from the grid:
        offset_x = pos[0] % self.tilesize
        offset_y = pos[1] % self.tilesize

        return (offset_x, offset_y)


    def get_tile_type(self, pos):
        index = pos[0]*self.mapheight + pos[1]
        return self.table[index]


    def show(self, screen, offset):
        TILESIZE = 32  # TODO There is already a member for that

        index = 0
        for x in range(self.mapwidth):
            for y in range(self.mapheight):
                pos = self.__tilemapping[self.table[index]]
                screen.blit(
                        self.__tileset,
                        (x*TILESIZE + offset[0], y*TILESIZE + offset[1]),
                        (pos[0], pos[1], TILESIZE, TILESIZE))
                index += 1


