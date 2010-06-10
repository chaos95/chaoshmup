# Copyright (c) 2010, Morgan Lokhorst-Blight 
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

from contrib import vector

from entity import Entity
from weapons import LaserRepeater, PlasmaRepeater, PlasmaCannon

class Ship(Entity):
    THRUST_HORIZ = 500
    THRUST_VERT = 500
    THRUST_ROTATE = 40
    HEALTH = 100
    def __init__(self, world):
        Entity.__init__(self, world)
        self.thrust = 0
        self.team = None
        self.health = self.HEALTH
        self.weapons = []

    def update(self, delta):
        if self.thrust != 0:
            self.acceleration = vector.Vector((0,self.thrust)).rotated(180-self.orientation)
        else:
            self.acceleration = vector.Vector((0,0))
        Entity.update(self, delta)
        for w in self.weapons:
            w.update(delta)

    def hit(self, weapon):
        self.health -= weapon.damage
        if self.health <= 0:
            self.alive = False

class Enemy(Ship):
    START_ORIENTATION = 0
    START_ROTATION = 60
    IMAGE_FILE = "images/i_are_spaceship.png"
    TEAM = "Enemy"
    def __init__(self, world):
        Ship.__init__(self, world)
        self.team = self.TEAM
        self.weapons = [PlasmaRepeater(self.world, self)]
        self.weapons[0].fire()
        
    def load_images(self):
        image = pygame.image.load(self.IMAGE_FILE)
        self.images = [image.subsurface(pygame.Rect(48,16,16,16))]

class Player(Ship):
    IMAGE_FILE = "images/i_are_spaceship.png"
    FRAME_DELAY = 0.1
    def __init__(self, world, name, team):
        Ship.__init__(self, world)
        self.name = name
        self.team = team
        self.weapons = [LaserRepeater(self.world, self),
                        PlasmaRepeater(self.world, self)]

    def load_images(self):
        image = pygame.image.load(self.IMAGE_FILE)
        self.images = [image.subsurface(pygame.Rect(0,0,16,32)),
                       image.subsurface(pygame.Rect(16,0,16,32))]

