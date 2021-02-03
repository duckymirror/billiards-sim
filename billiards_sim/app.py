from billiards_sim import physics
from billiards_sim import window

WIDTH = 1270
HEIGHT = 2540
BALL_RADIUS = 57.2 / 2

def run():
    window.init(WIDTH, HEIGHT)
    world = physics.World(WIDTH, HEIGHT)
    ball = physics.Ball(BALL_RADIUS, physics.Point(300, 300), physics.Vector(-10, -10))
    world.add_ball(ball)
    window.add_ball(window.Ball(ball, (0xFC, 0xEA, 0x23)))
    ball = physics.Ball(BALL_RADIUS, physics.Point(600, 600), physics.Vector(-5.1, -5))
    world.add_ball(ball)
    window.add_ball(window.Ball(ball, (0xE4, 0x66, 0x15)))
    window.loop(world)
