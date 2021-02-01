class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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
            ball.pos.x += ball.vel.x
            ball.pos.y += ball.vel.y

class Ball:
    def __init__(self, radius, pos, vel):
        self.radius = radius
        self.pos = pos
        self.vel = vel