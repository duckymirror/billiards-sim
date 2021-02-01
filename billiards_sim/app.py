from billiards_sim import physics
from billiards_sim import window

def run():
    window.init(1270, 2540)
    world = physics.World()
    ball = physics.Ball(57.2 / 2, physics.Point(300, 300), physics.Vector(5, 10))
    world.add_ball(ball)
    window.add_ball(window.Ball(ball, (0xFC, 0xEA, 0x23)))
    window.loop(world)
