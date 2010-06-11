# Copyright (c) 2010, Morgan Lokhorst-Blight, Michael Brindle
# All rights reserved. 
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met: 
# 
#  * Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer. 
#  * Redistributions in binary form must reproduce the above copyright 
#    notice, this list of conditions and the following disclaimer in the 
#    documentation and/or other materials provided with the distribution. 
# 
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND ANY 
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE FOR ANY 
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT 
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY 
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH 
# DAMAGE. 

import pygame

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
        self.last_frame = self.frame
        self.image = self.images[self.animation[self.frame]]
        self.rect = pygame.Rect(0,0,self.image.get_width(),self.image.get_height())
        self.acceleration = Vector((0,0))
        self.velocity = Vector((0,0))
        self.frametime = 0.0
        self.alive = True
        self.orientation = self.START_ORIENTATION
        self.last_orientation = self.orientation
        self.rotation = self.START_ROTATION
        self.mass = 0
        self.force = []

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
        self.last_frame = self.frame
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
        if self.orientation != self.last_orientation or self.frame != self.last_frame:
            self.image = pygame.transform.rotate(self.images[self.animation[self.frame]], self.orientation)
            center = self.rect.center
            self.rect.size = self.image.get_rect().size
            self.rect.center = center
        else:
            self.image = pygame.transform.rotate(self.images[self.animation[self.frame-1]], self.orientation)
        self.last_orientation = self.orientation

        # Apply acceleration and clip velocity, apply friction
        self.velocity += self.acceleration.rotated(-self.orientation)
        length = self.velocity.length
        if length > self.MAX_VEL:
            self.velocity = self.velocity.scaled_to(self.MAX_VEL)
        if self.FRICTION_MULTIPLIER != 1 and length > 0 and self.acceleration.length <= 0:
            self.velocity *= self.FRICTION_MULTIPLIER + (1 - self.FRICTION_MULTIPLIER) * delta

        # Move
        self.rect = self.rect.move(self.velocity.x * delta, self.velocity.y * delta)
