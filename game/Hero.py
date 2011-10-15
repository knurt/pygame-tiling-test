
# This Class represents the human-controllable hero of the game.

import util
import LevelMap
from Animation import *
import pygame.gfxdraw  # for debugging purposes


class Hero:

    # states:
    # Maybe these should be replaced by the direction-constants below
    (UP_WALK, UP_STAND, DOWN_WALK, DOWN_STAND,
            LEFT_WALK, LEFT_STAND, RIGHT_WALK, RIGHT_STAND) = range(8)
    # directions:
    NO_DIRECTION = (0,0)
    LEFT         = (-1,0)
    RIGHT        = (1,0)
    UP           = (0,-1)
    DOWN         = (0,1)

    def __init__(self, levelmap):
        self.levelmap = levelmap

        self.__img = util.load_image('rpg_sprite_walk.png', False, None)
        order = range(8)
        delay = 4  # each phase of the animation lasts 6 frames
        offset = (0,16)  # the "position-point" of the hero is on
                # his left elbow...
        self.size = 16

        self.__walk_down = Animation(order)
        for down_rect in [ (4+i*24, 0, 16, 31) for i in range(8) ]:
            self.__walk_down.add_frame(self.__img, down_rect, delay, offset)

        self.__walk_up = Animation(order)
        for up_rect in [ (4+i*24, 32, 16, 31) for i in range(8) ]:
            self.__walk_up.add_frame(self.__img, up_rect, delay, offset)

        self.__walk_left = Animation(order)
        for left_rect in [ (4+i*24, 64, 16, 31) for i in range(8) ]:
            self.__walk_left.add_frame(self.__img, left_rect, delay, offset)

        self.__walk_right = Animation(order)
        for right_rect in [ (4+i*24, 96, 16, 31) for i in range(8) ]:
            self.__walk_right.add_frame(self.__img, right_rect, delay, offset)

        # initial values
        self.state = self.DOWN_WALK
        self.x = 0  # Coordinates are relative to the map - not to the screen!
        self.y = 0
        self.speed = 2

    
    def stand(self):
        if self.state == Hero.DOWN_WALK:
            self.state = Hero.DOWN_STAND
        elif self.state == Hero.UP_WALK:
            self.state = Hero.UP_STAND
        elif self.state == Hero.LEFT_WALK:
            self.state = Hero.LEFT_STAND
        elif self.state == Hero.RIGHT_WALK:
            self.state = Hero.RIGHT_STAND


    def tick(self):
        # TODO beautify method (make some lines shorter)

        # Cancel movement, if hero is standing
        if self.state in [Hero.LEFT_STAND, Hero.RIGHT_STAND,
                Hero.UP_STAND, Hero.DOWN_STAND]:
            return
        # Otherwise: Determine direction
        direction = {
                Hero.LEFT_WALK : Hero.LEFT,
                Hero.RIGHT_WALK : Hero.RIGHT,
                Hero.UP_WALK : Hero.UP,
                Hero.DOWN_WALK : Hero.DOWN
                }[self.state]
                
        corners = self.get_corners(direction)
        speed_x = self.speed * direction[0]
        speed_y = self.speed * direction[1]
        dest_tiles = [self.levelmap.pixel_pos_to_tile_pos(
            (c[0]+speed_x, c[1]+speed_y)) for c in corners]

        if reduce(lambda a, b: a and b,
            [self.levelmap.get_tile_type(t) == LevelMap.LevelMap.FLOOR\
                    for t in dest_tiles]):
            self.x += speed_x
            self.y += speed_y
        else:
            self.move_to_edge(direction)


    def get_bounds(self):
        # Maybe the use of this function should be replaced by "get_corners"
        return (self.x, self.y, self.size, self.size)


    def get_corners(self, direction):
        upper_left  = (self.x, self.y)
        upper_right = (self.x + self.size, self.y)
        lower_left  = (self.x, self.y + self.size)
        lower_right = (self.x + self.size, self.y + self.size)
        
        if direction == Hero.LEFT:
            return [upper_left, lower_left]
        elif direction == Hero.RIGHT:
            return [upper_right, lower_right]
        elif direction == Hero.UP:
            return [upper_left, upper_right]
        elif direction == Hero.DOWN:
            return [lower_left, lower_right]
        else:
            return []


    def move_to_edge(self, direction):
        distance_left = self.x % self.levelmap.tilesize
        distance_up = self.y % self.levelmap.tilesize
        if direction == Hero.LEFT:
            self.x -= distance_left
        elif direction == Hero.RIGHT:
            self.x += (self.levelmap.tilesize - self.size - distance_left)
        elif direction == Hero.UP:
            self.y -= distance_up
        elif direction == Hero.DOWN:
            self.y += (self.levelmap.tilesize - self.size - distance_up)
        

    def show(self, screen, offset):
        pos = (self.x + offset[0], self.y + offset[1])
        offset_pos = (pos[0], pos[1] - 16)

        if self.state == Hero.DOWN_WALK:
            self.__walk_down.show(screen, pos)
        elif self.state == Hero.UP_WALK:
            self.__walk_up.show(screen, pos)
        elif self.state == Hero.LEFT_WALK:
            self.__walk_left.show(screen, pos)
        elif self.state == Hero.RIGHT_WALK:
            self.__walk_right.show(screen, pos)
        elif self.state == Hero.DOWN_STAND:
            screen.blit(self.__img, offset_pos, (4, 0, 16, 31))
        elif self.state == Hero.UP_STAND:
            screen.blit(self.__img, offset_pos, (4, 32, 16, 31))
        elif self.state == Hero.LEFT_STAND:
            screen.blit(self.__img, offset_pos, (4, 64, 16, 31))
        elif self.state == Hero.RIGHT_STAND:
            screen.blit(self.__img, offset_pos, (4, 96, 16, 31))
        
        # DEBUG
        # show bounding-box:
        pygame.gfxdraw.rectangle(
                screen,
                (pos[0], pos[1], self.size, self.size),
                (255,0,0))

