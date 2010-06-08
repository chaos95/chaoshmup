import pygame
from pygame.locals import *

from contrib.vector import Vector

def sign(val):
    if val >= 0:
        return 1
    else:
        return -1

class Entity(pygame.sprite.Sprite):
    IMAGE_FILE = ""
    DEFAULT_ANIMATION = "default"
    FRAME_DELAY = 99999999.0
    MAX_VEL = 500
    FRICTION_MULTIPLIER = 0.5
    START_ORIENTATION = 180
    START_ROTATION = 0
    def __init__(self, world):
        pygame.sprite.Sprite.__init__(self)
        self.world = world
        self.load_images()
        self.load_animations()
        self.animation = self.animations[self.DEFAULT_ANIMATION]
        self.frame = 0
        self.image = self.images[self.animation[self.frame]]
        self.rect = pygame.Rect(0,0,self.image.get_width(),self.image.get_height())
        self.acceleration = Vector((0,0))
        self.velocity = Vector((0,0))
        self.frametime = 0.0
        self.alive = True
        self.orientation = self.START_ORIENTATION
        self.last_orientation = self.orientation
        self.rotation = self.START_ROTATION

    @property
    def position(self):
        return Vector(self.rect.center)
    @position.setter
    def position(self,newpos):
        self.rect.center = tuple(newpos)

    def load_images(self):
        self.images = [pygame.image.load(self.IMAGE_FILE)]

    def load_animations(self):
        self.animations = {"default": range(len(self.images))}

    def next_frame(self):
        if self.frame+1 >= len(self.animation):
            self.animation_complete()
        else:
            self.frame += 1
        return self.images[self.animation[self.frame]]

    def animation_complete(self):
        self.frame = 0

    def update(self, delta):
        # Animate
        self.frametime += delta
        if self.frametime >= self.FRAME_DELAY:
            self.image = self.next_frame()
            self.frametime = 0.0

        # Rotate
        self.orientation += self.rotation * delta
        if self.orientation != self.last_orientation:
            self.image = pygame.transform.rotate(self.images[self.animation[self.frame]], self.orientation)
            center = self.rect.center
            self.rect.size = self.image.get_rect().size
            self.rect.center = center
        self.last_orientation = self.orientation

        # Apply acceleration and clip velocity, apply friction
        self.velocity += self.acceleration
        length = self.velocity.length
        if length > self.MAX_VEL:
            self.velocity = self.velocity.scaled_to(self.MAX_VEL)
        if self.FRICTION_MULTIPLIER != 1 and length > 0 and self.acceleration.length <= 0:
            self.velocity *= self.FRICTION_MULTIPLIER + (1 - self.FRICTION_MULTIPLIER) * delta

        # Move
        self.rect = self.rect.move(self.velocity.x * delta, self.velocity.y * delta)
