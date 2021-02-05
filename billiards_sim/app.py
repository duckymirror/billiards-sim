import yaml
import sys
from billiards_sim import physics
from billiards_sim import window

WIDTH_KEY = 'width'
HEIGHT_KEY = 'height'
BALL_RADIUS_KEY = 'radius'
FPS_KEY = 'fps'
TPF_KEY = 'tpf'
INVERT_Y_KEY = 'invert_y'
PAUSED_KEY = 'paused'
BALLS_KEY = 'balls'
POS_KEY = 'pos'
VEL_KEY = 'vel'
COLOR_KEY = 'col'
BALL_NAME_KEY = 'name'
POCKETS_KEY = 'pockets'
POCKET_SIDE_KEY = 'side'
POCKET_POS_KEY = 'pos'
POCKET_DIAMETER_KEY = 'diameter'
FRICTION_KEY = 'friction'
ACTIONS_KEY = 'actions'
ACTIONS_BALL_KEY = 'ball'
ACTIONS_VEL_KEY = 'vel'
ACTIONS_PUSH_KEY = 'push'
ACTIONS_PUSH_BALL_KEY = 'ball'
ACTIONS_PUSH_DEST_KEY = 'dest'
ACTIONS_PUSH_VEL_KEY = 'vel'
ACTIONS_PUSH_RAIL_KEY = 'rail'

def run():
    yaml_path = sys.argv[1]
    data = None
    with open(yaml_path) as f:
        data = yaml.load(f, Loader=yaml.Loader)
        data = {} if data is None else data
    ball_radius = data.get(BALL_RADIUS_KEY, 57.2 / 2)
    fps = data.get(FPS_KEY, 60)
    tpf = data.get(TPF_KEY, 10)
    width = data.get(WIDTH_KEY, 1270)
    height = data.get(HEIGHT_KEY, 2540)
    invert_y = data.get(INVERT_Y_KEY, True)
    paused = data.get(PAUSED_KEY)

    friction = data.get(FRICTION_KEY, 0)

    pockets = []
    ui_pockets = []
    if POCKETS_KEY in data:
        for pocket in data[POCKETS_KEY]:
            pos = pocket.get(POCKET_POS_KEY, None)
            side = pocket[POCKET_SIDE_KEY]
            if invert_y and (pos == 'left' or pos == 'right'):
                pos = -pos
            pocket = physics.Pocket(side, pocket[POCKET_DIAMETER_KEY], pos)
            pockets.append(pocket)
            ui_pockets.append(window.Pocket(pocket))

    actions = []
    if ACTIONS_KEY in data:
        for action in data[ACTIONS_KEY]:
            ball = str(action[ACTIONS_BALL_KEY])
            vel = action.get(ACTIONS_VEL_KEY, None)
            vel = None if vel is None else physics.Vector(vel[0], vel[1])
            if vel is not None and invert_y:
                vel.y = -vel.y
            push = action.get(ACTIONS_PUSH_KEY, None)
            if push is not None:
                pushed_ball = push[ACTIONS_PUSH_BALL_KEY]
                dest = push[ACTIONS_PUSH_DEST_KEY]
                if invert_y:
                    dest[1] = height - dest[1]
                abs_vel = push[ACTIONS_PUSH_VEL_KEY]
                rail = push.get(ACTIONS_PUSH_RAIL_KEY, None)
                push = physics.PushActionData(pushed_ball, physics.Point(dest[0], dest[1]), abs_vel, rail)
            actions.append(physics.Action(ball, vel, push))

    window.init(width, height, ui_pockets)
    world = physics.World(width, height, pockets, friction, actions)
    if BALLS_KEY in data:
        for ball in data[BALLS_KEY]:
            pos = ball[POS_KEY]
            vel = ball[VEL_KEY]
            if invert_y:
                pos[1] = height - pos[1]
                vel[1] = -vel[1]
            color = ball[COLOR_KEY]
            name = ball.get(BALL_NAME_KEY, None)
            ph_ball = physics.Ball(ball_radius, physics.Point(pos[0], pos[1]), physics.Vector(vel[0], vel[1]), name)
            world.add_ball(ph_ball)
            window.add_ball(window.Ball(ph_ball, (color[0], color[1], color[2])))
    window.loop(world, fps, tpf, paused)
