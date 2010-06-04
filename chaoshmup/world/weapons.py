import math

import pygame
from pygame.locals import *

from chaoshmup.world import Entity

class Laser(Entity):
    IMAGE_FILE = "images/i_are_spaceship.png"
    def __init__(self, world, owner, pos, velocity_x = 0, velocity_y = -1000):
        Entity.__init__(self, world)
        self.owner = owner
        self.rect.center = pos
        self.velocity_x = math.sin(owner.angle * math.pi / 36.0) * velocity_y
        self.velocity_y = math.cos(owner.angle * math.pi / 36.0) * velocity_y
        self.damage = 50

    def load_images(self):
        image = pygame.image.load(self.IMAGE_FILE)
        self.images = [image.subsurface(pygame.Rect(32,16,8,8))]

    def update(self, delta):
        Entity.update(self, delta)
        self.image = pygame.transform.rotate(self.images[0], self.owner.angle * 5)

class Plasma(Laser):
    FRAME_DELAY = 0.05
    DEFAULT_ANIMATION = "throb"
    def __init__(self, world, owner, pos, velocity_x = 0, velocity_y = -250):
        Laser.__init__(self, world, owner, pos, velocity_x, velocity_y)
        # So... at angles of +-1 (5 degrees in program), plasma doesn't angle.
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

    def update(self, delta):
        Entity.update(self, delta)
        self.image = pygame.transform.rotate(self.images[0], self.owner.angle * 5)

