from billiards_sim import physics
from billiards_sim import window

def run():
    window.init(1270, 2540)
    window.add_ball(window.Ball(physics.Ball(57.2 / 2, (300, 300), (0, 0)), (0xFC, 0xEA, 0x23)))
    window.loop()
