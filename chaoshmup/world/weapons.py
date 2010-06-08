import pygame
from pygame.locals import *

from contrib import vector

from chaoshmup.world import Entity

class Projectile(Entity):
    DAMAGE = 1
    def __init__(self, world, owner, pos, heading=0, acceleration=(0,1000)):
        Entity.__init__(self, world)
        self.owner = owner
        self.rect.center = pos
        self.acceleration = vector.Vector(acceleration).rotated(-heading)
        self.damage = self.DAMAGE

class LaserBolt(Projectile):
    IMAGE_FILE = "images/i_are_spaceship.png"
    MAX_VEL=1000
    DAMAGE = 50
    def load_images(self):
        image = pygame.image.load(self.IMAGE_FILE)
        self.images = [image.subsurface(pygame.Rect(32,16,8,8))]

class PlasmaBall(Projectile):
    IMAGE_FILE = "images/i_are_spaceship.png"
    FRAME_DELAY = 0.05
    DEFAULT_ANIMATION = "throb"
    MAX_VEL=250
    DAMAGE=100
    def load_images(self):
        image= pygame.image.load(self.IMAGE_FILE)
        self.images = [image.subsurface(pygame.Rect(48,0,8,8)),
                       image.subsurface(pygame.Rect(48,8,8,8)),
                       image.subsurface(pygame.Rect(56,0,8,8)),
                       image.subsurface(pygame.Rect(56,8,8,8))]

    def load_animations(self):
        Projectile.load_animations(self)
        self.animations["throb"] = [3,2,1,0,1,2]

class Weapon(Entity):
    PROJECTILE_TYPE = None
    def __init__(self, world, owner):
        self.world = world
        self.owner = owner

    def fire(self):
        if self.PROJECTILE_TYPE is None:
            return

        self.world.projectiles.add(self.PROJECTILE_TYPE(self.world, self.owner,
                                                        self.owner.position, self.owner.rotation))

    def release(self):
        pass

    def update(self, delta):
        pass

class RepeaterWeapon(Weapon):
    RATE_OF_FIRE = 0.0
    def __init__(self, world, owner):
        Weapon.__init__(self, world, owner)
        self.firing = False
        self.reload = 0.0
        
    def fire(self):
        self.firing = True

    def release(self):
        self.firing = False

    def update(self, delta):
        if not self.firing:
            return
        self.reload += delta
        if self.reload >= self.RATE_OF_FIRE:
            if self.PROJECTILE_TYPE is None:
                return

            self.world.projectiles.add(
                self.PROJECTILE_TYPE(self.world, self.owner,
                                     self.owner.position, self.owner.orientation))
            self.reload = 0.0
    
class LaserRepeater(RepeaterWeapon):
    PROJECTILE_TYPE = LaserBolt
    RATE_OF_FIRE = 0.1

class PlasmaRepeater(RepeaterWeapon):
    PROJECTILE_TYPE = PlasmaBall
    RATE_OF_FIRE = 1.0

class PlasmaCannon(Weapon):
    PROJECTILE_TYPE = PlasmaBall
