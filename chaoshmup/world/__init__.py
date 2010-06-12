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

import math

import pygame

from entity import Entity
from ship import Enemy, Player
from mass import *
from chaoshmup.internal_math import *

class Explosion(Entity):
    IMAGE_FILE = "images/i_are_spaceship.png"
    FRAME_DELAY = 0.3
    def __init__(self, world, pos):
        Entity.__init__(self, world)
        self.rect.center = pos

    def load_images(self):
        image = pygame.image.load(self.IMAGE_FILE)
        self.images = [image.subsurface(pygame.Rect(0,32,16,16)),
                       image.subsurface(pygame.Rect(16,32,16,16)),
                       image.subsurface(pygame.Rect(32,32,16,16)),
                       image.subsurface(pygame.Rect(48,32,16,16))]

    def animation_complete(self):
        self.alive = False
    
class World(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.players = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.planets = pygame.sprite.Group()
        self.black_holes = pygame.sprite.Group()

    def gravity(self, delta):
        G = .0066 # some semblence of a universal gravitational constant.
        self.matter = self.players.sprites()[:] + self.enemies.sprites()[:] + self.planets.sprites()[:] # I'll add stars, planets, etc. later
        for cray in self.matter:
            while len(cray.force) > 0:
                cray.force.pop()
            for boff in self.matter:
                if cray != boff:
                    cray.force.append(uni_gravity(G, cray, boff))
            foo = tuple_xy_add(cray.force)
            cray.velocity += (delta * foo[0] / cray.mass, delta * foo[1] / cray.mass)

    def update(self, delta):
        self.players.update(delta)
        self.enemies.update(delta)
        self.projectiles.update(delta)
        self.explosions.update(delta)
        self.planets.update(delta)

        # Keep players on the screen
        for p in self.players.sprites() + self.enemies.sprites():
            if p.rect.right > self.width:
                p.rect.right = self.width
            if p.rect.left < 0:
                p.rect.left = 0
            if p.rect.bottom > self.height:
                p.rect.bottom = self.height
            if p.rect.top < 0:
                p.rect.top = 0

        # Collision detection
        projectile_enemy = pygame.sprite.groupcollide(self.enemies, self.projectiles, False, False)
        for (enemy, projectiles) in projectile_enemy.iteritems():
            for projectile in projectiles:
                if projectile.owner.team != enemy.team:
                    enemy.hit(projectile)
                    self.projectiles.remove(projectile)
            
        # Cleanup
        enemydead = [x for x in self.enemies.sprites()[:] if not x.alive]
        for x in enemydead:
            self.explosions.add(Explosion(self, x.rect.center))
        self.enemies.remove(enemydead)

        expldead = [x for x in self.explosions.sprites()[:] if not x.alive]
        self.explosions.remove(expldead)

        projectiledead = [x for x in self.projectiles.sprites()[:] if x.rect.bottom < 0 or x.rect.right < 0 or x.rect.left > self.width or x.rect.top > self.height]
        self.projectiles.remove(projectiledead)

    def clear_callback(self, surf, rect):
        surf.fill((0,0,0), rect)
        
    def draw(self, surface):
        self.explosions.clear(surface, self.clear_callback)
        self.projectiles.clear(surface, self.clear_callback)
        self.enemies.clear(surface, self.clear_callback)
        self.players.clear(surface, self.clear_callback)
        
        self.explosions.draw(surface)
        self.projectiles.draw(surface)
        self.enemies.draw(surface)
        self.players.draw(surface)

