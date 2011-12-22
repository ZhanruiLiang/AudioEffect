import pygame as pg
import config
from display import Display, ViewPort
from physics import *
from mymath import vec
import random

def rd(l, r):
	return random.random()*(r-l)+l

#create world -> world
l = config.WorldSize
world = PhyWorld((-l, -l, -l, l, l, l), config.FPS)

#create viewport
viewport = ViewPort(s=config.CameraPos, w=1024/2, h=768/2)

#create display -> disp
disp = Display(config.Resolution, world, viewport)

# attach bodies to world
n = 5
for i in xrange(n):
	points = []
	for j in xrange(3):
		point = PhyPoint()
		point.s = vec((rd(-10, 10), rd(0, 10), rd(0, 10)))
		point.v = vec((rd(-1, 1), rd(-1, 1), rd(-1, 1)))
		points.append(point)
		world.attach(point)
	body = PhyBody(points[0], points[1], points[2], ShapeSquare(1))
	world.attach(body)

fps_timer = pg.time.Clock()
quit = False
while not quit:
	for e in pg.event.get():
		if e.type == pg.QUIT:
			quit = True
	world.update()
	disp.update()
	fps_timer.tick(config.FPS)
