
# This Class represents the human-controllable hero of the game.

import util
from util import Vector
import LevelMap
from animation import *


class Hero:

    # states:
    # Maybe these should be replaced by the direction-constants below
    (UP_WALK, UP_STAND, DOWN_WALK, DOWN_STAND,
            LEFT_WALK, LEFT_STAND, RIGHT_WALK, RIGHT_STAND) = range(8)
    # directions:
    NO_DIRECTION = Vector(0,0)
    LEFT         = Vector(-1,0)
    RIGHT        = Vector(1,0)
    UP           = Vector(0,-1)
    DOWN         = Vector(0,1)

    def __init__(self, image_filename, levelmap):
        self.levelmap = levelmap

        self.__img = util.load_image(image_filename, False, None)
        order = range(8)
        delay = 4  # each phase of the animation lasts 6 frames
        offset = Vector(0,16)  # the "position-point" of the hero is on
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
        # Coordinates are relative to the map - not to the screen!
        self.pos = Vector(0,0)
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
        
        delta = util.vec_mult(direction, self.speed)
        
        dest_tiles = [self.levelmap.pixel_pos_to_tile_pos(
            util.vec_add(c, delta)) for c in corners]

        tiletypes =\
                [self.levelmap.get_tile_type(t) == LevelMap.LevelMap.FLOOR
                for t in dest_tiles]

        if reduce(lambda a, b: a and b, tiletypes):
            self.pos.add(delta)
        else:
            self.move_to_edge(direction)


    def get_bounds(self):
        # Maybe the use of this function should be replaced by "get_corners"
        return (self.pos.x, self.pos.y, self.size, self.size)


    def get_corners(self, direction):
        upper_left  = self.pos
        upper_right = util.vec_add(self.pos, Vector(self.size-1, 0))
        lower_left  = util.vec_add(self.pos, Vector(0, self.size-1))
        lower_right = util.vec_add(self.pos, Vector(self.size-1, self.size-1))
        
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
        distance_left = self.pos.x % self.levelmap.tilesize
        distance_up = self.pos.y % self.levelmap.tilesize
        if direction == Hero.LEFT:
            self.pos.x -= distance_left
        elif direction == Hero.RIGHT:
            self.pos.x += (self.levelmap.tilesize - self.size - distance_left)
        elif direction == Hero.UP:
            self.pos.y -= distance_up
        elif direction == Hero.DOWN:
            self.pos.y += (self.levelmap.tilesize - self.size - distance_up)
        

    def show(self, screen, offset):
        pos = util.vec_add(self.pos, offset)
        offset_pos = (pos.x, pos.y - 16)

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
        
