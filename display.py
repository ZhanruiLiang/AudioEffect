import pygame.display as pgdisplay
# from pygame import locals
import pygame as pg
from mymath import *

worldCoor = CoorSystem(eye(3), vec(0, 0, 0))

class Display(object):
	def __init__(self, resolution=(1024, 768), world, viewport=None):
		pgdisplay.init()
		self.screen = pgdisplay.set_mode(resolution, pg.DOUBLEBUF)
		# self.screen = pgdisplay.set_mode(resolution, pg.DOUBLEBUF|pg.FULLSCREEN)
		pgdisplay.set_caption('PyAudioEffect')
		self.world = world
		self.viewport = viewport

	def update(self):
		"""
		redraw
		"""
		self.screen.fill(config.bgcolor)
		w2s = self.viewport.world_to_screen

		# draw bodies
		for b in self.world.bodies:
			polygon = []
			for node in b.shape.nodes:
				p = mat((node[0], node[1], 0))
				polygon.append(w2s(b.coor.apply(p)))
			pg.draw.polygon(self.screen, b.shape.color, polygon)

		# draw joints
		jointColor = (0xff, 0xff, 0)
		for j in self.world.joints:
			p1 = w2s(j.t1.s)
			p2 = w2s(j.t2.s)
			pg.draw.aaline(self.screen, jointColor, p1, p2)

		pgdisplay.flip()

	def __del__(self):
		pgdisplay.quit()

class ViewPort(object):
	__slots__ = ['s', 'w', 'h', 'd', 'surface']


	def __init__(self, s, w, h, d=0):
		"""
		s: the position
		w, h: half width and height(in pixel)
		d: the distance(in meter)
		"""
		self.w0, self.h0, self.d0 = w, h, d
		self.w, self.h, self.d = w, h, d
		self._zoom = 1.0
		self.coor = mat((
				(MPP, 0, 0), 
				(0, 0, -MPP),
				(0, MPP, 0)), s)
	
	@property
	def s(self):
		return self.coor.origin

	@s.setter
	def s(self, value):
		self.coor.origin = value

	def zoom(self, scale):
		self._zoom = scale
	
	def rotate_to(self, s, focus):
		"""
		rotate the camera to position `s`, but always focus on `focus`
		"""
		#TODO
		pass

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
		np = self.coor.transform(worldCoor, p)
		return [i for i in np[0,:2]]

