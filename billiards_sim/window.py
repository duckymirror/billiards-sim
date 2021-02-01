import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 30
FramesPerSec = pygame.time.Clock()

WHITE = (255, 255, 255)
BLUE = (25, 25, 205)
BACKGROUND = (0x02, 0xC3, 0x7D)

SCALE = 1.0 / 3
BORDER_THICKNESS = 10

table_size = (None, None)

def init(width, height):
    global table_size
    table_size = (width, height)
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode((int(width * SCALE + 2 * BORDER_THICKNESS), int(height * SCALE + 2 * BORDER_THICKNESS)))
    DISPLAYSURF.fill(BACKGROUND)
    pygame.display.set_caption("Billiards")

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

def loop():
    table = Table()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        DISPLAYSURF.fill(BACKGROUND)
        table.draw(DISPLAYSURF)
        pygame.display.update()
        FramesPerSec.tick(FPS)
