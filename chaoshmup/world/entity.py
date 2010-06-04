import pygame
from pygame.locals import *

class Entity(pygame.sprite.Sprite):
    IMAGE_FILE = ""
    DEFAULT_ANIMATION = "default"
    FRAME_DELAY = 99999999.0
    def __init__(self, world):
        pygame.sprite.Sprite.__init__(self)
        self.world = world
        self.load_images()
        self.load_animations()
        self.animation = self.animations[self.DEFAULT_ANIMATION]
        self.frame = 0
        self.image = self.images[self.animation[self.frame]]
        self.rect = pygame.Rect(0,0,self.image.get_width(),self.image.get_height())
        self.velocity_x = 0
        self.velocity_y = 0
        self.frametime = 0.0
        self.alive = True

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

        # Move
        self.rect = self.rect.move(self.velocity_x * delta, self.velocity_y * delta)
