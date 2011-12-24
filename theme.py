from display import Display, ViewPort
from physics import *
from mymath import vec, pi
import random

def rd(l, r):
	return random.random()*(r-l)+l

def only2(world, viewport):
	p1 = PhyPoint(s=(-1 ,0, 0), v=(0, 0, 0), mass=0.2)
	p2 = PhyPoint(s=(1 ,0, 0), v=(0, 0, 0), mass=0.2)
	world.attach(p1);
	world.attach(p2);
	world.attach(Spring(p1, p2, 1.9, 10))
	viewport.s = (0, -50, 20)
	world.attach(FField(f=0.1))

def theme1(world, viewport):
	# attach bodies to world
	n = 35
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
		world.attach(Spring(p1, p2, rd(5,8), 1))
		# world.attach(Stick(p1, p2, norm(p1.s-p2.s)))

	# world.attach(GravityField())
	world.attach(FField(f=0.35))
	viewport.s = (0, -40, 20)

def theme2(world, viewport):
	na = 5
	nb = 5
	da = 2*pi/na
	db = pi/nb
	b = -pi/2
	r = 10.
	ps = []
	while b <= pi/2:
		a = 0
		while a <= 2*pi:
			x = r * cos(b) * cos(a)
			y = r * cos(b) * sin(a)
			z = r * sin(b)
			ps.append(PhyPoint(s=(x,y,z),mass=2, q=5))
			world.attach(ps[-1])
			a += da
		b += db
	for i, j in zip(ps[:-1], ps[1:]):
		world.attach(Stick(i, j, norm(i.s - j.s)))
	world.attach(QField(2.5, 50000))
	viewport.s = (0, -100, 20)


