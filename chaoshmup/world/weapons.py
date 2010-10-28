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

import random

import pygame

from contrib import vector

from chaoshmup.world import Entity

class Projectile(Entity):
    DAMAGE = 1
    def __init__(self, world, owner, pos, heading=0, acceleration=(0,1000)):
        Entity.__init__(self, world)
        self.owner = owner
        self.rect.center = pos
        self.orientation = heading
        self.acceleration = vector.Vector(acceleration).rotated(180-heading)
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
    def __init__(self, world, owner, pos, heading=0, acceleration=(0,1000)):
        Projectile.__init__(self, world, owner, pos, heading, acceleration)
        self.frame = random.randint(0,len(self.animation)-1)

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
                                                        self.owner.position, self.owner.orientation))

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

    def spawn_projectile(self):
        self.world.projectiles.add(
            self.PROJECTILE_TYPE(self.world, self.owner,
                                 self.owner.position, self.owner.orientation))

    def update(self, delta):
        self.reload += delta
        if self.reload >= self.RATE_OF_FIRE:
            if self.PROJECTILE_TYPE is None:
                return

            if self.firing:
                self.spawn_projectile()
            self.reload = 0.0

class FanWeapon(RepeaterWeapon):
    ARC = 0.0
    NUM_PROJECTILES = 0
    def calc_angle(self, i):
        half_arc = self.ARC / 2.0
        return i * self.ARC / (self.NUM_PROJECTILES - 1) - half_arc
    def spawn_projectile(self):
        proj = []
        for i in range(self.NUM_PROJECTILES):
            proj.append(self.PROJECTILE_TYPE(self.world, self.owner,
                                             self.owner.position,
                                             self.owner.orientation + self.calc_angle(i)))
        self.world.projectiles.add(proj)
    
class LaserRepeater(RepeaterWeapon):
    PROJECTILE_TYPE = LaserBolt
    RATE_OF_FIRE = 0.1

class PlasmaRepeater(RepeaterWeapon):
    PROJECTILE_TYPE = PlasmaBall
    RATE_OF_FIRE = 1.0

class PlasmaCannon(Weapon):
    PROJECTILE_TYPE = PlasmaBall

class LaserFan(FanWeapon):
    PROJECTILE_TYPE = LaserBolt
    RATE_OF_FIRE = 0.1
    ARC = 60.0
    NUM_PROJECTILES = 5
