import math
import random
import sys


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, point):
        dx = self.x - point.x
        dy = self.y - point.y
        return math.sqrt(dx * dx + dy * dy)

    def __add__(self, rhs):
        return Point(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self, rhs):
        return Vector(self.x - rhs.x, self.y - rhs.y)


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def norm(self):
        return self / self.length()

    def almost_norm(self):
        len = self.length()
        if len == 0.0:
            return Vector(self.x, self.y)
        else:
            return self / len

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def dot(self, rhs):
        return self.x * rhs.x + self.y * rhs.y

    def __add__(self, rhs):
        return Vector(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self, rhs):
        return Vector(self.x - rhs.x, self.y - rhs.y)

    def __mul__(self, rhs):
        return Vector(self.x * rhs, self.y * rhs)

    def __truediv__(self, rhs):
        return Vector(self.x / rhs, self.y / rhs)


class World:
    def __init__(self, width, height, pockets, friction, actions):
        self.balls = []
        self.width = width
        self.height = height
        self.top_pockets = []
        self.bottom_pockets = []
        self.left_pockets = []
        self.right_pockets = []
        self.insert_pockets(pockets)
        self.friction = friction
        self.actions = actions
        self.actions.reverse()

    def insert_pockets(self, pockets):
        for pocket in pockets:
            if pocket.top:
                if pocket.left:
                    self.top_pockets.append([-math.inf, pocket.length])
                    self.left_pockets.append([-math.inf, pocket.length])
                elif pocket.right:
                    self.top_pockets.append([self.width - pocket.length, math.inf])
                    self.right_pockets.append([-math.inf, pocket.length])
                else:
                    self.top_pockets.append([pocket.pos - pocket.length / 2, pocket.pos + pocket.length / 2])
            elif pocket.bottom:
                if pocket.left:
                    self.bottom_pockets.append([-math.inf, pocket.length])
                    self.left_pockets.append([self.height - pocket.length, math.inf])
                elif pocket.right:
                    self.bottom_pockets.append([self.width - pocket.length, math.inf])
                    self.right_pockets.append([self.height - pocket.length, math.inf])
                else:
                    self.bottom_pockets.append([pocket.pos - pocket.length / 2, pocket.pos + pocket.length / 2])
            elif pocket.left:
                self.left_pockets.append([pocket.pos - pocket.length / 2, pocket.pos + pocket.length / 2])
            elif pocket.right:
                self.right_pockets.append([pocket.pos - pocket.length / 2, pocket.pos + pocket.length / 2])
            else:
                raise ValueError()

    def add_ball(self, ball):
        self.balls.append(ball)

    def tick(self, tps):
        for ball in self.balls:
            self.collide_border(ball)
        collisions = self.get_ball_collisions()
        for collision in collisions:
            self.handle_collision(collision[0], collision[1])
        sleeping_count = 0
        for ball in self.balls:
            ball.pos += ball.vel / tps
            ball.vel -= ball.vel.almost_norm() * min(self.friction / tps, ball.vel.length())
            if ball.vel.length() < 0.0001:
                ball.vel = Vector(0, 0)
                sleeping_count += 1
        if sleeping_count == len(self.balls):
            self.next_action()
        self.balls = list(filter(lambda b: not b.removed, self.balls))

    def collide_border(self, ball):
        # Left border
        if ball.pos.x <= ball.radius:
            if any(filter(lambda p: p[0] < ball.pos.y < p[1], self.left_pockets)):
                if ball.pos.x <= 0:
                    ball.removed = True
            else:
                ball.vel.x = -ball.vel.x
        # Right border
        if ball.pos.x >= self.width - ball.radius:
            if any(filter(lambda p: p[0] < ball.pos.y < p[1], self.right_pockets)):
                if ball.pos.x >= self.width:
                    ball.removed = True
            else:
                ball.vel.x = -ball.vel.x

        # Top border
        if ball.pos.y <= ball.radius:
            if any(filter(lambda p: p[0] < ball.pos.x < p[1], self.top_pockets)):
                if ball.pos.y <= 0:
                    ball.removed = True
            else:
                ball.vel.y = -ball.vel.y

        # Bottom border
        if ball.pos.y >= self.height - ball.radius:
            if any(filter(lambda p: p[0] < ball.pos.x < p[1], self.bottom_pockets)):
                if ball.pos.y >= self.height:
                    ball.removed = True
            else:
                ball.vel.y = -ball.vel.y

    def get_ball_collisions(self):
        collisions = []
        for ball in self.balls:
            for other_ball in self.balls:
                if other_ball == ball:
                    continue
                if ball.pos.dist(other_ball.pos) <= ball.radius + other_ball.radius:
                    if not any(filter(lambda c: c[0] == ball and c[1] == other_ball or c[1] == ball and c[0] == other_ball, collisions)):
                        collisions.append((ball, other_ball))

        return collisions

    def handle_collision(self, ball_1, ball_2):
        vel_1 = ball_1.vel - ball_2.vel
        n = ball_2.pos - ball_1.pos
        n0 = n.almost_norm()
        vel_2_new = n0 * n0.dot(vel_1)
        t = Vector(-n.y, n.x)
        t = t * t.dot(vel_1)
        t0 = t.almost_norm()
        vel_1_new = t0 * t0.dot(vel_1)
        ball_1.vel = vel_1_new + ball_2.vel
        ball_2.vel = vel_2_new + ball_2.vel

    def next_action(self):
        if len(self.actions) == 0:
            return
        action = self.actions.pop()
        ball = self.get_ball(action.ball)
        if action.vel is not None:
            ball.vel = action.vel
        else:
            target_ball = self.get_ball(action.push.ball)
            desired_dir = (target_ball.pos - action.push.dest).norm()
            total_radius = ball.radius + target_ball.radius
            target_point = target_ball.pos + desired_dir * total_radius
            if action.push.rail == RAIL_AUTO:
                valid_paths = []
                for rail in [RAIL_TOP, RAIL_BOTTOM, RAIL_LEFT, RAIL_RIGHT, None]:
                    path = self.calculate_path(ball, target_ball, target_point, rail, action.push.vel)
                    if path[1]:
                        valid_paths.append(path)
                result = max(valid_paths, key=lambda p: p[2])
            else:
                result = self.calculate_path(ball, target_ball, target_point, action.push.rail, action.push.vel)
            if not result[1]:
                print("This shot isn't going to hit the ball correctly!", file=sys.stderr)
            ball.vel = result[0] * action.push.vel

    def calculate_path(self, ball, target_ball, target_point, rail, vel):
            if rail == RAIL_TOP:
                curr_pos = Point(ball.pos.x, -ball.pos.y + 2 * ball.radius)
            elif rail == RAIL_BOTTOM:
                curr_pos = Point(ball.pos.x, 2 * self.height - ball.pos.y - 2 * ball.radius)
            elif rail == RAIL_LEFT:
                curr_pos = Point(-ball.pos.x + 2 * ball.radius, ball.pos.y)
            elif rail == RAIL_RIGHT:
                curr_pos = Point(2 * self.width - ball.pos.x - 2 * ball.radius, ball.pos.y)
            else:
                curr_pos = ball.pos

            dir = (target_point - curr_pos).norm()

            if rail == RAIL_TOP or rail == RAIL_BOTTOM:
                final_dir = Vector(dir.x, -dir.y)
            elif rail == RAIL_LEFT or rail == RAIL_RIGHT:
                final_dir = Vector(-dir.x, dir.y)
            else:
                final_dir = dir

            invalid = False
            if rail == RAIL_TOP:
                if final_dir.y != 0:
                    m = final_dir.x / final_dir.y
                    collision_x = m * (ball.radius - ball.pos.y) + ball.pos.x
                    invalid |= 0 <= collision_x < self.width and any(filter(lambda p: p[0] < collision_x < p[1], self.top_pockets))
            elif rail == RAIL_BOTTOM:
                if final_dir.y != 0:
                    m = final_dir.x / final_dir.y
                    collision_x = m * (self.height - ball.radius - ball.pos.y) + ball.pos.x
                    invalid |= 0 <= collision_x < self.width and any(filter(lambda p: p[0] < collision_x < p[1], self.bottom_pockets))
            elif rail == RAIL_LEFT:
                if final_dir.x != 0:
                    m = final_dir.y / final_dir.x
                    collision_y = m * (ball.radius - ball.pos.x) + ball.pos.y
                    invalid |= 0 <= collision_y < self.height and any(filter(lambda p: p[0] < collision_y < p[1], self.left_pockets))
            elif rail == RAIL_RIGHT:
                if final_dir.x != 0:
                    m = final_dir.y / final_dir.x
                    collision_y = m * (self.width - ball.radius - ball.pos.x) + ball.pos.y
                    invalid |= 0 <= collision_y < self.height and any(filter(lambda p: p[0] < collision_y < p[1], self.right_pockets))

            score = self.score_path(curr_pos, target_point, target_ball.pos, vel)
            if invalid or dir.dot(target_point - target_ball.pos) > 0:
                return (final_dir, False, score)
            else:
                return (final_dir, True, score)

    def score_path(self, start_point, target_point, target_ball_pos, vel):
        dist = (target_point - start_point).length()
        collision_vel = math.sqrt(max(2 * -self.friction * dist + vel * vel, 0))
        return (target_ball_pos - target_point).norm().dot((target_point - start_point).norm()) * collision_vel

    def get_ball(self, name):
        try:
            return next(filter(lambda b: b.name == name, self.balls))
        except StopIteration:
            raise ValueError('Ball "{}" couldn\'t be found'.format(name))


class Ball:
    def __init__(self, radius, pos, vel, name=None):
        self.radius = radius
        self.pos = pos
        self.vel = vel
        self.name = name
        self.removed = False

class Pocket:
    def __init__(self, side, diameter, pos):
        if side == 'top_left' or side == 'top_right' or side == 'bottom_left' or side == 'bottom_right':
            assert(pos is None)
            self.length = math.sqrt(diameter * diameter / 2)
            self.pos = 0
        else:
            self.length = diameter
            self.pos = pos
        self.top = side.startswith('top')
        self.bottom = side.startswith('bottom')
        self.left = side.endswith('left')
        self.right = side.endswith('right')

class Action:
    def __init__(self, ball, vel=None, push=None):
        assert(vel is not None or push is not None)
        self.ball = ball
        self.vel = vel
        self.push = push

RAIL_AUTO = "auto"
RAIL_TOP = "top"
RAIL_BOTTOM = "bottom"
RAIL_LEFT = "left"
RAIL_RIGHT = "right"

class PushActionData:
    def __init__(self, ball, dest, vel, rail = None):
        self.ball = ball
        self.dest = dest
        self.vel = vel
        self.rail = rail