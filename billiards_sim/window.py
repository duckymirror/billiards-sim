import pygame, sys
from pygame.locals import *

pygame.init()

balls = pygame.sprite.Group()
all_pockets = pygame.sprite.Group()

FramesPerSec = pygame.time.Clock()

WHITE = (255, 255, 255)
BLUE = (25, 25, 205)
BACKGROUND = (0x02, 0xC3, 0x7D)
POCKET_COLOR = (0x97, 0x99, 0x9B)

SCALE = 1.0 / 3
BORDER_THICKNESS = 10

DISPLAYSURF = None

table_size = (None, None)
paused = False

def init(width, height, pockets):
    global table_size
    table_size = (width, height)
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode((int(width * SCALE + 2 * BORDER_THICKNESS), int(height * SCALE + 2 * BORDER_THICKNESS)))
    DISPLAYSURF.fill(BACKGROUND)
    pygame.display.set_caption("Billiards")
    global all_pockets
    all_pockets = pockets

class Table(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((table_size[0] * SCALE + 2 * BORDER_THICKNESS, table_size[1] * SCALE + 2 * BORDER_THICKNESS))
        self.surf.fill(BACKGROUND)
        border_left = Rect(0, 0, BORDER_THICKNESS, table_size[1] * SCALE + 2 * BORDER_THICKNESS)
        pygame.draw.rect(self.surf, BLUE, border_left)
        border_top = Rect(0, 0, table_size[0] * SCALE + 2 * BORDER_THICKNESS, BORDER_THICKNESS)
        pygame.draw.rect(self.surf, BLUE, border_top)
        border_right = Rect(table_size[0] * SCALE + BORDER_THICKNESS, 0, table_size[0] * SCALE + 2 * BORDER_THICKNESS, table_size[1] * SCALE + 2 * BORDER_THICKNESS)
        pygame.draw.rect(self.surf, BLUE, border_right)
        border_bottom = Rect(0, table_size[1] * SCALE + BORDER_THICKNESS, table_size[0] * SCALE + 2 * BORDER_THICKNESS, table_size[1] * SCALE + 2 * BORDER_THICKNESS)
        pygame.draw.rect(self.surf, BLUE, border_bottom)

    def draw(self, surface):
        surface.blit(self.surf, (0, 0))

class Pocket(pygame.sprite.Sprite):
    def __init__(self, pocket):
        self.pocket = pocket
    
    def draw(self, surface):
        if self.pocket.top and self.pocket.left:
            x = 0
            y = 0
            width = BORDER_THICKNESS + self.pocket.length * SCALE
            height = BORDER_THICKNESS
            pygame.draw.rect(surface, POCKET_COLOR, (x, y, width, height))
            width = BORDER_THICKNESS
            height = BORDER_THICKNESS + self.pocket.length * SCALE
            pygame.draw.rect(surface, POCKET_COLOR, (x, y, width, height))
        elif self.pocket.top and self.pocket.right:
            x = table_size[0] * SCALE + BORDER_THICKNESS - self.pocket.length * SCALE
            y = 0
            width = table_size[0] * SCALE + BORDER_THICKNESS
            height = BORDER_THICKNESS
            pygame.draw.rect(surface, POCKET_COLOR, (x, y, width, height))
            x = table_size[0] * SCALE + BORDER_THICKNESS
            height = BORDER_THICKNESS + self.pocket.length * SCALE
            pygame.draw.rect(surface, POCKET_COLOR, (x, y, width, height))
        elif self.pocket.top:
            x = BORDER_THICKNESS + self.pocket.pos * SCALE - self.pocket.length / 2 * SCALE
            y = 0
            width = self.pocket.length * SCALE
            height = BORDER_THICKNESS
            pygame.draw.rect(surface, POCKET_COLOR, (x, y, width, height))
        elif self.pocket.bottom and self.pocket.left:
            x = 0
            y = BORDER_THICKNESS + table_size[1] * SCALE
            width = BORDER_THICKNESS + self.pocket.length * SCALE
            height = BORDER_THICKNESS
            pygame.draw.rect(surface, POCKET_COLOR, (x, y, width, height))
            y = table_size[1] * SCALE + BORDER_THICKNESS - self.pocket.length * SCALE
            width = BORDER_THICKNESS
            height = self.pocket.length * SCALE + BORDER_THICKNESS
            pygame.draw.rect(surface, POCKET_COLOR, (x, y, width, height))
        elif self.pocket.bottom and self.pocket.right:
            x = table_size[0] * SCALE + BORDER_THICKNESS - self.pocket.length * SCALE
            y = table_size[1] * SCALE + BORDER_THICKNESS
            width = self.pocket.length * SCALE + BORDER_THICKNESS
            height = BORDER_THICKNESS
            pygame.draw.rect(surface, POCKET_COLOR, (x, y, width, height))
            x = table_size[0] * SCALE + BORDER_THICKNESS
            y = table_size[1] * SCALE + BORDER_THICKNESS - self.pocket.length * SCALE
            width = BORDER_THICKNESS
            height = self.pocket.length * SCALE + BORDER_THICKNESS
            pygame.draw.rect(surface, POCKET_COLOR, (x, y, width, height))
        elif self.pocket.bottom:
            x = BORDER_THICKNESS + self.pocket.pos * SCALE - self.pocket.length / 2 * SCALE
            y = table_size[1] * SCALE + BORDER_THICKNESS
            width = self.pocket.length * SCALE
            height = BORDER_THICKNESS
            pygame.draw.rect(surface, POCKET_COLOR, (x, y, width, height))
        elif self.pocket.left:
            x = 0
            y = BORDER_THICKNESS + self.pocket.pos * SCALE - self.pocket.length / 2 * SCALE
            width = BORDER_THICKNESS
            height = self.pocket.length * SCALE
            pygame.draw.rect(surface, POCKET_COLOR, (x, y, width, height))
        elif self.pocket.right:
            x = table_size[0] * SCALE + BORDER_THICKNESS
            y = BORDER_THICKNESS + self.pocket.pos * SCALE - self.pocket.length / 2 * SCALE
            width = BORDER_THICKNESS
            height = self.pocket.length * SCALE
            pygame.draw.rect(surface, POCKET_COLOR, (x, y, width, height))

class Ball(pygame.sprite.Sprite):
    def __init__(self, ball, color):
        super().__init__()
        self.ball = ball
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.ball.pos.x * SCALE) + BORDER_THICKNESS, int(self.ball.pos.y * SCALE) + BORDER_THICKNESS), int(self.ball.radius * SCALE))

def add_ball(ball):
    global balls
    balls.add(ball)

def handle_keydown(event):
    if event.key == pygame.K_SPACE:
        global paused
        paused = not paused

def loop(world, fps, tpf, start_paused):
    global paused
    paused = start_paused if start_paused is not None else False
    table = Table()
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                handle_keydown(event)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        if not paused:
            for _ in range(tpf):
                world.tick(fps * tpf)

        DISPLAYSURF.fill(BACKGROUND)
        table.draw(DISPLAYSURF)
        global balls
        balls = list(filter(lambda b: not b.ball.removed, balls))
        for ball in balls:
            ball.draw(DISPLAYSURF)
        for pocket in all_pockets:
            pocket.draw(DISPLAYSURF)
        pygame.display.update()
        FramesPerSec.tick(fps)
