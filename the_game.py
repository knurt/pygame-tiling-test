#!/usr/bin/env python

import pygame as pg  # maybe i should leave the "as pg" be...
import pygame.locals  # various constants

from game import util
from game.util import Vector
from game import Hero
from game import LevelMap


class Game(object):

    def __init__(self):
        self.offset = Vector(80, 80)  # Border
        self.tilesize = 32

        pg.init()
        self.__screen = pg.display.set_mode((800, 640))
        pg.display.set_caption('I\'m the Title')
        pg.mouse.set_visible(0)

        if not pg.mixer:
            print('Warning, sound diabled')

        self.__level = LevelMap.LevelMap(
                'leveldata.png',
                'tileset.png',
                {
                    LevelMap.LevelMap.FLOOR : Vector(0, 0),
                    LevelMap.LevelMap.WALL : Vector(32, 0)},
                self.tilesize)

        try:
            self.__sound = pg.mixer.Sound('../sounds/example.wav')
        except:
            print('Cannot load sound: sounds/example.wav')

        self.__hero = Hero.Hero(self.__level);
        
        bg = pg.Surface(self.__screen.get_size())
        bg = bg.convert()
        bg.fill((90, 90, 120))
        self__background = bg

        self.__hero.pos = Vector(4*32+5, 3*32+5)


    def loop(self):
        done = False
        time = pg.time.get_ticks()
        
        # DEBUG
        # Counters for frames that took to long
        good = 0
        bad = 0

        while not done:

            ### event handling
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True

            pressed_keys = pg.key.get_pressed()

            ### game logic
            if pressed_keys[pg.K_DOWN]:
                self.__hero.state = Hero.Hero.DOWN_WALK
            elif pressed_keys[pg.K_UP]:
                self.__hero.state = Hero.Hero.UP_WALK
            elif pressed_keys[pg.K_LEFT]:
                self.__hero.state = Hero.Hero.LEFT_WALK
            elif pressed_keys[pg.K_RIGHT]:
                self.__hero.state = Hero.Hero.RIGHT_WALK
            else:
                self.__hero.stand()

            if pressed_keys[pg.K_ESCAPE]:
                done = True

            self.__hero.tick()

            ### update display
            self.__level.show(self.__screen, self.offset)
            self.__hero.show(self.__screen, self.offset)
            pg.display.flip()
            
            # framerate regulation (e.g. 1000ms/40mspf = 25 fps)
            frametime = 50  # milliseconds per frame
            oldtime = time
            time = pg.time.get_ticks()
            diff = time - oldtime
            if diff > frametime:
                bad += 1
            else:
                pg.time.delay(frametime - diff)
                good += 1
            if good+bad > 9999:
                print "good ",good
                print "bad  ",bad
                good = 0
                bad = 0


if __name__ == '__main__':
    game = Game()
    game.loop()

