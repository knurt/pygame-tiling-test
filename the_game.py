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
                    LevelMap.LevelMap.FLOOR: Vector(0, 0),
                    LevelMap.LevelMap.WALL: Vector(32, 0)},
                self.tilesize)

        try:
            self.__sound = pg.mixer.Sound('../sounds/example.wav')
        except:
            print('Cannot load sound: sounds/example.wav')
            
        self.__player1 = Hero.Hero('rpg_sprite_walk.png', self.__level)
        self.__player2 = Hero.Hero('rpg_sprite_walk_other_color.png', self.__level)

        bg = pg.Surface(self.__screen.get_size())
        bg = bg.convert()
        bg.fill((90, 90, 120))
        self__background = bg

        self.__player1.pos = Vector(4 * 32 + 5, 3 * 32 + 5)
        self.__player2.pos = Vector(5 * 32 + 5, 3 * 32 + 5)

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
                self.__player1.state = Hero.Hero.DOWN_WALK
            elif pressed_keys[pg.K_UP]:
                self.__player1.state = Hero.Hero.UP_WALK
            elif pressed_keys[pg.K_LEFT]:
                self.__player1.state = Hero.Hero.LEFT_WALK
            elif pressed_keys[pg.K_RIGHT]:
                self.__player1.state = Hero.Hero.RIGHT_WALK
            else:
                self.__player1.stand()

            if pressed_keys[pg.K_s]:
                self.__player2.state = Hero.Hero.DOWN_WALK
            elif pressed_keys[pg.K_w]:
                self.__player2.state = Hero.Hero.UP_WALK
            elif pressed_keys[pg.K_a]:
                self.__player2.state = Hero.Hero.LEFT_WALK
            elif pressed_keys[pg.K_d]:
                self.__player2.state = Hero.Hero.RIGHT_WALK
            else:
                self.__player2.stand()

            if pressed_keys[pg.K_ESCAPE]:
                done = True

            self.__player1.tick()
            self.__player2.tick()

            ### update display
            self.__level.show(self.__screen, self.offset)
            self.__player1.show(self.__screen, self.offset)
            self.__player2.show(self.__screen, self.offset)
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
            if good + bad > 9999:
                print "good ", good
                print "bad  ", bad
                good = 0
                bad = 0


if __name__ == '__main__':
    game = Game()
    game.loop()
