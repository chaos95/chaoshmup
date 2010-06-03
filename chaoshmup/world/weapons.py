import pygame
from pygame.locals import *

from chaoshmup.world import Entity

class Laser(Entity):
    IMAGE_FILE = "images/i_are_spaceship.png"
    def __init__(self, world, owner, pos, velocity_x = 0, velocity_y = -1000):
        Entity.__init__(self, world)
        self.owner = owner
        self.rect.center = pos
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.damage = 50

    def load_images(self):
        image = pygame.image.load(self.IMAGE_FILE)
        self.images = [image.subsurface(pygame.Rect(32,16,8,8))]

class Plasma(Laser):
    FRAME_DELAY = 0.05
    DEFAULT_ANIMATION = "throb"
    def __init__(self, world, owner, pos, velocity_x = 0, velocity_y = -250):
        Laser.__init__(self, world, owner, pos, velocity_x, velocity_y)
        self.damage = 100

    def load_images(self):
        image= pygame.image.load(self.IMAGE_FILE)
        self.images = [image.subsurface(pygame.Rect(48,0,8,8)),
                       image.subsurface(pygame.Rect(48,8,8,8)),
                       image.subsurface(pygame.Rect(56,0,8,8)),
                       image.subsurface(pygame.Rect(56,8,8,8))]

    def load_animations(self):
        Laser.load_animations(self)
        self.animations["throb"] = [3,2,1,0,1,2]

