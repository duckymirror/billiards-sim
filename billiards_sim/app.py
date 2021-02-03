import yaml
import sys
from billiards_sim import physics
from billiards_sim import window

WIDTH_KEY = 'width'
HEIGHT_KEY = 'height'
BALL_RADIUS_KEY = 'radius'
FPS_KEY = 'fps'
TPF_KEY = 'tpf'
BALLS_KEY = 'balls'
POS_KEY = 'pos'
VEL_KEY = 'vel'
COLOR_KEY = 'col'
POCKETS_KEY = 'pockets'
POCKET_SIDE_KEY = 'side'
POCKET_POS_KEY = 'pos'
POCKET_DIAMETER_KEY = 'diameter'

def run():
    yaml_path = sys.argv[1]
    data = None
    with open(yaml_path) as f:
        data = yaml.load(f, Loader=yaml.Loader)
        data = {} if data is None else data
    ball_radius = data.get(BALL_RADIUS_KEY, 57.2 / 2)
    fps = data.get(FPS_KEY, 60)
    tpf = data.get(TPF_KEY, 5)
    width = data.get(WIDTH_KEY, 1270)
    height = data.get(HEIGHT_KEY, 2540)

    pockets = []
    ui_pockets = []
    if POCKETS_KEY in data:
        for pocket in data[POCKETS_KEY]:
            pocket = physics.Pocket(pocket[POCKET_SIDE_KEY], pocket[POCKET_DIAMETER_KEY], pocket.get(POCKET_POS_KEY, None))
            pockets.append(pocket)
            ui_pockets.append(window.Pocket(pocket))

    window.init(width, height, ui_pockets)
    world = physics.World(width, height, pockets)
    if BALLS_KEY in data:
        for ball in data[BALLS_KEY]:
            pos = ball[POS_KEY]
            vel = ball[VEL_KEY]
            color = ball[COLOR_KEY]
            ph_ball = physics.Ball(ball_radius, physics.Point(pos[0], pos[1]), physics.Vector(vel[0], vel[1]))
            world.add_ball(ph_ball)
            window.add_ball(window.Ball(ph_ball, (color[0], color[1], color[2])))
    window.loop(world, fps, tpf)
