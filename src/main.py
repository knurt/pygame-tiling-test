#!/usr/bin/env python
#
# Ein simples Tile-basiertes "Spiel" ohne Ziel.
# Ich hab es geschrieben um spaeter mal ein Tutorial dadrueber
# zu machen.
#
# TODO: Wie macht man ordentliche leere 2-Dim-Matrizen, wo die Leveldaten
# rein koennen? ctype zu klompiziert?

import pygame as pg
import pygame.locals

import util
import Hero
import LevelMap


class Game(object):

	def __init__(self):
		self.offset = 80  # Border
		self.tilesize = 32

		pg.init()
		self.__screen = pg.display.set_mode((800, 640))
		pg.display.set_caption('Ich bin der Titel')
		pg.mouse.set_visible(0)

		if not pg.mixer:
			print('Warning, sound diabled')

		self.__hero = Hero.Hero();
		self.__level = LevelMap.LevelMap(
				'images/leveldata.png',
				'images/tileset.png',
				{
					LevelMap.LevelMap.FLOOR : (0, 0),
					LevelMap.LevelMap.WALL : (32, 0)
					}
				)

		try:
			self.__sound = pg.mixer.Sound('sounds/example.wav')
		except:
			print('Cannot load sound: sounds/example.wav')
		
		bg = pg.Surface(self.__screen.get_size())
		bg = bg.convert()
		bg.fill((90, 90, 120))
		self__background = bg

		self.__hero_pos = (80+32+2, 80+32+2)


	def loop(self):
		done = False
		time = pg.time.get_ticks()
		
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

			self.__hero.tick()

			### update display
			self.__level.show(self.__screen, (self.offset, self.offset))

			self.__hero.show(self.__screen)
			pg.display.flip()
			
			# framerate regulation (1000/40 = 25 fps)
			frametime = 50
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


def main():
	game = Game()
	game.loop()


if __name__ == '__main__':
	main()

