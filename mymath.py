from numpy import *
norm = linalg.norm

class vec(array):
	def __init__(self, *args):
		array.__init__(self, *args, dtype=double)

class CoorSystem(matrix, object):
	__slots__ = ['transform', 'origin']
	def __init__(self, M, origin):
		matrix.__init__(self, M, dtype=double)
		if self.shape != (3, 3):
			raise Exception("Wrong coordinate system shape, should be (3, 3)")
		self.origin = origin

	def transform(self, c2, x):
		"""
		c1 * y = c2 * x
		"""
		c1 = self
		return solve(c1, c2 * x + c2.origin - c1.origin)) + c1.origin

	def apply(self, x):
		return self * x + self.origin

def rotate_about_axis(x, p, u, angle):
	pass

PixelPerMeter = 1366/0.32
PPM = PixelPerMeter
MeterPerPixel = 1/PixelPerMeter
MPP = MeterPerPixel
