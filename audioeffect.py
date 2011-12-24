import pygame as pg
from display import Display, ViewPort
from physics import *
from mymath import vec
import random
import theme

import config

#create world -> world
l = config.WorldSize
world = PhyWorld((-l, -l, -l, l, l, l), config.PhyFPS)

#create viewport
viewport = ViewPort(s=config.CameraPos, w=1024/2, h=768/2, d=400)

#create display -> disp
disp = Display(config.Resolution, world, viewport)

theme.theme2(world, viewport)

fps_timer = pg.time.Clock()
quit = False
delta_d = 0
delta_angle = 0
fff=0
while not quit:
	for e in pg.event.get():
		if e.type == pg.QUIT:
			quit = True
		elif e.type == pg.KEYDOWN:
			if e.key == pg.K_UP:
				delta_d = 5
			elif e.key == pg.K_DOWN:
				delta_d = -5
			elif e.key == pg.K_s:
				print "save..."
				world.save("worldsave")
			elif e.key == pg.K_l:
				print "load..."
				world = PhyWorld.load("worldsave")
				disp.world = world
			elif e.key == pg.K_LEFT:
				delta_angle = pi/20
			elif e.key == pg.K_RIGHT:
				delta_angle = -pi/20

		elif e.type == pg.KEYUP:
			delta_d = 0
			delta_angle = 0
	viewport.s[1, 0] += delta_d
	viewport.rotate((0, 0, 0), (0, 0, 1), delta_angle)

	for i in xrange(config.PhyFPS/config.FPS):
		world.update()
	disp.update()
	# raw_input("press enter to continue")
	fps_timer.tick(config.FPS)
	fff += 1
	if fff == 30:
		print 'FPS', fps_timer.get_fps()
		fff = 0
