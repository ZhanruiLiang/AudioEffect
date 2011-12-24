from numpy import *
norm = linalg.norm

def vec(v):
	return mat(v, dtype=double)

def mcross(a, b):
	return cross(a.T, b.T).T

class CoorSystem(object):
	__slots__ = ['transform', 'origin', 'M']
	def __init__(self, M, origin):
		self.M = matrix(M)
		if self.M.shape != (3, 3):
			raise Exception("Wrong coordinate system shape, should be (3, 3)")
		self.origin = mat(origin).T
		if self.origin.shape != (3, 1):
			raise Exception("Wrong coordinate system origin point, should be (3, 1)")


	def transform(self, c2, x):
		"""
		c1 * y = c2 * x
		"""
		# result = linalg.solve(self.M, c2.M * x + c2.origin - self.origin)
		result = self.M.I * (c2.M * x + c2.origin - self.origin)
		return result

	def apply(self, x):
		return self.M * x + self.origin

def rotate_about_axis(p, s, n, angle):
	"""
	p: current pos
	s: origin
	n: normal vector
	angle: rota angle in rad
	"""
	np = ((p-s).T*n/norm(n))[0,0]*n
	t= p - s - np
	l = norm(t)
	if l == 0:
		return p
	t /= l
	r = mcross(n, t)
	r /= norm(r)
	pp = s + np + cos(angle) * l * t + sin(angle) * l * r
	return pp

PixelPerMeter = 1366/20.32
PPM = PixelPerMeter
MeterPerPixel = 1/PixelPerMeter
MPP = MeterPerPixel
