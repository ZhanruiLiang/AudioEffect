from numpy import *
from numpy.linalg import *
from mymath import vec, CoorSystem
import random
import cPickle
import config

def new_vec():
	return vec((.0, .0, .0))

class PhyObject(object):
	pass

class PhyPoint(PhyObject):
	# __slots__ = ['s', 'v', 'a', 'mass', 'F', 'q', 'apply', 'update']
	def __init__(self, s=None, v=None, mass=None, q=None):
		if s:
			self.s = vec(s)
		else:
			self.s = new_vec()
		if v:
			self.v = vec(v)
		else:
			self.v = new_vec()
		self.a = new_vec()
		self.mass = mass or .0
		self.q = q or .0
		self.F = new_vec()
	
	def apply(self, F):
		self.F += F

	def update(self, dt):
		if self.mass == 0:
			return
		self.a = self.F / self.mass
		v = self.v
		self.s += (v + dt/2 * self.a) * dt
		self.v += dt * self.a 
		self.F = vec((0.0, 0.0, 0.0))

class PhyShape(PhyObject):
	# __slots__ = ['nodes', 'color']
	def __init__(self, nodes, color=None):
		"""
		nodes: the polygon's nodes, note that this is in 2d plane
		"""
		self.nodes = nodes
		self.color = color or [random.randrange(0xff) for i in xrange(3)]

class ShapeSquare(PhyShape):
	# __slots__ = ['a']
	def __init__(self, a, color=None):
		self.a = a
		nodes = [(-a, -a), (a, -a), (a, a), (-a, a)]
		super(ShapeSquare, self).__init__(nodes, color)

class PhyBody(PhyObject):
	# __slots__ = ['t1', 't2', 't3', 'shape', 'coor']
	def __init__(self, t1, t2, t3, shape=None):
		self.t1 = t1
		self.t2 = t2
		self.t3 = t3
		self.shape = shape
	
	@property
	def coor(self):
		""" The body's coordinate system"""
		t1, t2, t3 = self.t1, self.t2, self.t3
		s = t2.s - t1.s
		s /= norm(s)
		t = t3.s - t1.s
		r = cross(s, t)
		r /= norm(r)
		t = cross(r, s)
		coor = CoorSystem(vstack((s, t, r)), t1.s)
		return coor

class PhyField(PhyObject):
	# __slots__ = ['s', 'r', 'targets', 'apply']
	def __init__(self):
		self.s = vec((0, 0, 0))
		self.r = 100
		self.targets = None

	def apply(self, dt):
		pass

class GravityField(PhyField):
	# __slots__ = ['g']
	def __init__(self, g=9.8):
		self.g = g
		super(GravityField, self).__init__()

	def apply(self, dt):
		s0 = self.s
		for target in self.targets:
			r = target.s - s0
			if norm(r) < self.r:
				target.apply(target.mass * self.g)

class FField(PhyField):
	# __slots__ = ['f']
	def __init__(self, f=0.1):
		super(FField, self).__init__()
		self.f = f

	def apply(self, dt):
		s0 = self.s
		for t in self.targets:
			if norm(t.s - s0) < self.r:
				t.apply(-self.f * t.v)

class QField(PhyField):
	def __init__(self, T, q):
		self.k = 0.1
		self.t = 0
		self.T = T
		self.s = vec((0, 0, 0))
		self.q = q

	def apply(self, dt):
		self.t += dt
		if self.t > self.T:
			self.t = 0
		k = self.k
		# q = self.q * (-sin(2 * pi / self.T * self.t))
		q = self.q
		for tar in self.targets:
			r = tar.s - self.s
			tar.apply(k * q * tar.q / norm(r)**3 * r)

class PhyJoint(PhyObject):
	# __slots__ = ['t1', 't2', 'length', 'update']
	def __init__(self, t1, t2, length):
		self.t1 = t1
		self.t2 = t2
		self.length = length
	def apply(self, dt):
		pass

class Spring(PhyJoint):
	# __slots__ = ['k']
	def __init__(self, t1, t2, l, k):
		super(Spring , self).__init__(t1, t2, l)
		self.k = k
	def apply(self, dt):
		r = self.t2.s - self.t1.s
		F = self.k * (self.length/norm(r) - 1) * r
		self.t2.apply(F)
		self.t1.apply(-F)

class Stick(PhyJoint):
	# __slots__ = []
	kIn = 1000
	kOut = 1000
	def apply(self, dt):
		r = self.t2.s - self.t1.s
		nr = norm(r)
		if nr > self.length:
			k = self.kOut
		else:
			k = self.kIn
		F = k * (self.length/nr - 1) * r
		self.t2.apply(F)
		self.t1.apply(-F)

#TODO delete
debugFile = open('debug', 'w')

class PhyWorld:
	def __init__(self, size, fps):
		"""
		size: (x1, y1, z1, x2, y2, z2)
		fps: the simulate fps
		"""
		self.size = size
		self._fps = fps
		self.dt = 1.0/fps

		self.points = []
		self.bodies = []
		self.joints = []
		self.fields = []

		self.map = {PhyPoint: self.points,
				PhyBody: self.bodies,
				PhyJoint: self.joints,
				PhyField: self.fields}
	def __del__(self):
		debugFile.close()
	
	def save(self, filename=None):
		fn = filename or config.Savefile
		with open(fn, 'wb') as f:
			cPickle.dump(self, f, 0)

	@staticmethod
	def load(filename=None):
		fn = filename or config.Savefile
		with open(fn, 'rb') as f:
			r = cPickle.load(f)
		return r
	
	@property
	def fps(self):
		"The simulate fps"
		return self._fps

	@fps.setter
	def fps(self, fps):
		self._fps = fps
		self.dt = 1.0/fps

	def update(self, dt=None):
		dt = None or self.dt
		# apply all joints
		for i in self.joints:
			i.apply(dt)
		# apply all fields
		for i in self.fields:
			i.apply(dt)
		# update all points
		E = 0
		for i in self.points:
			i.update(dt)
			E += 0.5 * i.mass * norm(i.v)**2

	def attach(self, obj):
		for x in self.map:
			if isinstance(obj, x):
				self.map[x].append(obj)
		if isinstance(obj, PhyField):
			self.fields[-1].targets = self.points
