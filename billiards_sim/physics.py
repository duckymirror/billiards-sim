class World:
    def __init__(self):
        self.balls = []

class Ball:
    def __init__(self, radius, pos, vel):
        self.radius = radius
        self.pos = pos
        self.vel = vel