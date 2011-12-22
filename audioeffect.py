import pygame as pg
from display import Display, ViewPort
from physics import *
from mymath import vec
import random

import config

def rd(l, r):
	return random.random()*(r-l)+l

#create world -> world
l = config.WorldSize
world = PhyWorld((-l, -l, -l, l, l, l), config.PhyFPS)

#create viewport
viewport = ViewPort(s=config.CameraPos, w=1024/2, h=768/2, d=400)

#create display -> disp
disp = Display(config.Resolution, world, viewport)

# attach bodies to world
n = 5
# for i in xrange(n):
# 	points = []
# 	for j in xrange(3):
# 		point = PhyPoint()
# 		point.s = vec((rd(0, 10), rd(0, 10), rd(0, 10)))
# 		point.mass = 2
# 		#point.v = vec((rd(-1, 1), rd(-1, 1), rd(-1, 1)))
# 
# 		points.append(point)
# 		world.attach(point)
# 	body = PhyBody(points[0], points[1], points[2], ShapeSquare(1))
# 	world.attach(body)
for i in xrange(n):
	p = PhyPoint()
	p.s = vec((rd(0, 10), rd(0, 10), rd(0, 10)))
	p.v = vec((rd(-1, 1), rd(-1, 1), rd(-1, 1)))
	p.mass = 2
	world.attach(p)
for i in xrange(1,n):
	p1 = world.points[i-1]
	p2 = world.points[i]
	# world.attach(Spring(p1, p2, rd(5,8), 10))
	world.attach(Stick(p1, p2, norm(p1.s-p2.s)))

fps_timer = pg.time.Clock()
quit = False
delta_d = 0
fff=0
while not quit:
	for e in pg.event.get():
		if e.type == pg.QUIT:
			quit = True
		elif e.type == pg.KEYDOWN:
			if e.key == pg.K_UP:
				delta_d = 1
			elif e.key == pg.K_DOWN:
				delta_d = -1
			elif e.key == pg.K_s:
				print "save..."
				world.save("worldsave")
			elif e.key == pg.K_l:
				print "load..."
				world.load("worldsave")

		elif e.type == pg.KEYUP:
			delta_d = 0
	viewport.s[1] += delta_d

	world.update()
	world.update()
	disp.update()
	# raw_input("press enter to continue")
	fps_timer.tick(config.FPS)
	fff += 1
	if fff == 30:
		print 'FPS', fps_timer.get_fps()
		fff = 0
