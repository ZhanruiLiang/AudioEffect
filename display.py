import pygame.display as pgdisplay
# from pygame import locals
import pygame as pg
from mymath import *
import config

worldCoor = CoorSystem(eye(3), vec([0, 0, 0]))
@vectorize
def vint(x):
	return int(x)

class Display(object):
	def __init__(self, resolution, world, viewport=None):
		pgdisplay.init()
		self.screen = pgdisplay.set_mode(resolution, pg.DOUBLEBUF)
		# self.screen = pgdisplay.set_mode(resolution, pg.DOUBLEBUF|pg.FULLSCREEN)
		pgdisplay.set_caption('PyAudioEffect')
		self.world = world
		self.viewport = viewport
	
	def draw_grid(self):
		"""
		draw grid for debug
		"""
		z = 0
		a = 20
		sep = 2
		gridColor = pg.Color("blue")
		w2s = self.viewport.world_to_screen
		x = -a
		while x <= a:
			p1 = w2s(mat((x, -a, z)).T)[0]
			p2 = w2s(mat((x, a, z)).T)[0]
			if x != 0:
				pg.draw.aaline(self.screen, gridColor, vint(p1), vint(p2))
			else:
				pg.draw.aaline(self.screen, pg.Color("red"), vint(p1), vint(p2))
			x += sep
		y = -a
		while y <= a:
			w2s = self.viewport.world_to_screen
			p1 = w2s(mat((-a, y, z)).T)[0]
			p2 = w2s(mat((a, y, z)).T)[0]
			if y != 0:
				pg.draw.aaline(self.screen, gridColor, vint(p1), vint(p2))
			else:
				pg.draw.aaline(self.screen, pg.Color("red"), vint(p1), vint(p2))
			y += sep


	def update(self):
		"""
		redraw
		"""
		self.screen.fill(config.bgcolor)
		w2s = self.viewport.world_to_screen
		# draw grid for debug
		# self.draw_grid()

		# draw bodies
		# for b in self.world.bodies:
		# 	polygon = []
		# 	fflag = 0
		# 	for node in b.shape.nodes:
		# 		p, flag = w2s(b.coor.apply(mat((node[0], node[1], 0)).T))
		# 		fflag = fflag or flag
		# 		polygon.append(p)
		# 	if fflag:
		# 		pg.draw.polygon(self.screen, b.shape.color, polygon)

		# draw points
		for point in self.world.points:
			p, flag = w2s(point.s.T)
			if flag:
				pg.draw.circle(self.screen, pg.Color("blue"), vint(p), 2)

		# draw joints
		jointColor = (0x22, 0xff, 0)
		for j in self.world.joints:
			p1, flag1 = w2s(j.t1.s.T)
			p2, flag2 = w2s(j.t2.s.T)
			if flag1 or flag2:
				pg.draw.aaline(self.screen, jointColor, vint(p1), vint(p2))

		pgdisplay.flip()

	def __del__(self):
		pgdisplay.quit()

class ViewPort(object):
	def __init__(self, s, w, h, d=0):
		"""
		s: the position
		w, h: half width and height(in pixel)
		d: the distance(in meter)
		"""
		self.w, self.h, self.d = w, h, d
		self._zoom = 1.0
		self.coor = CoorSystem((
				(MPP, 0, 0), 
				(0, 0, MPP),
				(0, -MPP, 0)), s)
	
	@property
	def s(self):
		return self.coor.origin

	@s.setter
	def s(self, value):
		if type(value) != matrix:
			self.coor.origin = mat(value).T
		else:
			self.coor.origin = value

	def zoom(self, scale):
		self._zoom = scale
	
	def rotate(self, s, n, angle):
		"""
		"""
		#TODO
		coor = self.coor.M
		s = mat(s).T
		n = mat(n).T
		i = self.s + coor[:, 0]
		j = self.s + coor[:, 1]
		k = self.s + coor[:, 2]
		sp = rotate_about_axis(self.s, s, n, angle)
		i, j, k = ((rotate_about_axis(x, s, n, angle) - sp) for x in (i,j,k))
		self.coor.M = hstack((i, j, k))
		self.coor.origin = sp

	def watch(self, p):
		"""
		rotatate to watch the position p
		"""
		#TODO
		pass

	def world_to_screen(self, p):
		"""
		Convert world coordinate to the screen coordinate, `p` is the coordinate.
		"""
		d = self.d or 1e8
		# TODO: add zoom effect
		np = self.coor.transform(worldCoor, p)
		x, y, z = np[0, 0], np[1, 0], np[2, 0]
		k = d / (d + z)
		return (self.w + k * x, self.h + k * y), (z >= 0)

