from numpy import *
norm = linalg.norm

def vec(v):
	return mat(v, dtype=double)

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
		result = linalg.solve(self.M, c2.M * x + c2.origin - self.origin)
		return result

	def apply(self, x):
		return self.M * x + self.origin

def rotate_about_axis(x, p, u, angle):
	pass

PixelPerMeter = 1366/20.32
PPM = PixelPerMeter
MeterPerPixel = 1/PixelPerMeter
MPP = MeterPerPixel
