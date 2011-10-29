import pygame
from os.path import join, abspath
import sys

def load_image(image_filename, simple=False, colorkey = (255, 0, 255)):
    path = join("images",image_filename)
    
    try:
        img = pygame.image.load(path)
        if not simple:
            img.set_colorkey(colorkey, pygame.locals.RLEACCEL)
            img = img.convert_alpha()
        return img
    except pygame.error, message:
        print('Cannot load image: '+abspath(path))
        sys.exit(0);


def vec_add(v1, v2):
    return Vector(v1.x + v2.x, v1.y + v2.y)

def vec_mult(v, scalar):
    return Vector(v.x * scalar, v.y * scalar)


class Vector:
    # I could overwrite the '+'-operator or make the vector more hardware
    # efficient but i think that would complicate the code too much.

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, vec):
        # self = vec_add(self, vec)  # doesn't work
        self.x += vec.x
        self.y += vec.y

    def mult(self, scalar):
        self.x *= scalar
        self.y *= scalar

    def __str__(self):
        return "Vector(x=%i, y=%i)" % (self.x, self.y)

#    def copy(self):
#        return Vector(self.x, self.y)

