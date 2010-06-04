import pygame
from pygame.locals import *

from contrib import vector

from chaoshmup.world import Entity

class Laser(Entity):
    IMAGE_FILE = "images/i_are_spaceship.png"
    MAX_VEL=1000
    def __init__(self, world, owner, pos, acceleration=(0,-1000)):
        Entity.__init__(self, world)
        self.owner = owner
        self.rect.center = pos
        self.acceleration = vector.Vector(acceleration)
        self.damage = 50

    def load_images(self):
        image = pygame.image.load(self.IMAGE_FILE)
        self.images = [image.subsurface(pygame.Rect(32,16,8,8))]

class Plasma(Laser):
    FRAME_DELAY = 0.05
    DEFAULT_ANIMATION = "throb"
    MAX_VEL=250
    def __init__(self, world, owner, pos, acceleration=(0,-1000)):
        Laser.__init__(self, world, owner, pos, acceleration)
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

