class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, rhs):
        return Point(self.x + rhs.x, self.y + rhs.y)

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class World:
    def __init__(self):
        self.balls = []

    def add_ball(self, ball):
        self.balls.append(ball)
    
    def tick(self):
        for ball in self.balls:
            ball.pos += ball.vel

class Ball:
    def __init__(self, radius, pos, vel):
        self.radius = radius
        self.pos = pos
        self.vel = vel