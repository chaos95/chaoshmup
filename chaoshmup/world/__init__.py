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
from pygame.locals import *

from entity import Entity
from weapons import LaserRepeater, PlasmaRepeater, PlasmaCannon

class Ship(Entity):
    THRUST_HORIZ = 500
    THRUST_VERT = 500
    THRUST_ROTATE = 40
    HEALTH = 100
    def __init__(self, world):
        Entity.__init__(self, world)
        self.team = None
        self.health = self.HEALTH
        self.mass = 10
        self.weapons = []

    def update(self, delta):
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
        self.mass = 10

    def load_images(self):
        image = pygame.image.load(self.IMAGE_FILE)
        self.images = [image.subsurface(pygame.Rect(48,16,16,16))]

class Planet(Entity):
    IMAGE_FILE = "images/i_are_spaceship.png"
    def __init__(self, world):
        Entity.__init__(self, world)
        self.mass = 1000000

    def load_images(self):
        image = pygame.image.load(self.IMAGE_FILE)
        self.images = [image.subsurface(pygame.Rect(16,16,16,16))]

class Player(Ship):
    IMAGE_FILE = "images/i_are_spaceship.png"
    FRAME_DELAY = 0.1
    def __init__(self, world, name, team):
        Ship.__init__(self, world)
        self.name = name
        self.team = team
        self.weapons = [LaserRepeater(self.world, self),
                        PlasmaCannon(self.world, self)]
        self.mass = 10

    def load_images(self):
        image = pygame.image.load(self.IMAGE_FILE)
        self.images = [image.subsurface(pygame.Rect(0,0,16,32)),
                       image.subsurface(pygame.Rect(16,0,16,32))]


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
        self.matter = self.players.sprites()[:] + self.enemies.sprites()[:] + self.planets.sprites()[:]

#    def gravity(self):
#        G = 1
#        for i in self.matter:
#            while len(i.force_x) > 0:
#                i.force_x.pop()
#            while len(i.force_y) > 0:
#                i.force_y.pop()
#            for n in self.matter:
#                if i != n:
#                    if (i.rect.centerx == n.rect.centerx):
#                        i.force_x.append(( G * n.mass * i.mass) / 1 )
#                    elif (i.rect.centerx != n.rect.centerx):
#                        if (i.rect.centerx - n.rect.centerx) >= 0:
#                            i.force_x.append(( G * n.mass * i.mass) / (i.rect.centerx - n.rect.centerx) ** 2 )
#                        else: # it's negative
#                            i.force_x.append( -1 * (( G * n.mass * i.mass) / (i.rect.centerx - n.rect.centerx) ** 2 ))
#                    if (i.rect.centery == n.rect.centery):
#                        i.force_y.append(( G * n.mass * i.mass) / 1)
#                    elif (i.rect.centery != n.rect.centery):
#                        if (i.rect.centery - n.rect.centery) >= 0:
#                            i.force_y.append(( G * n.mass * i.mass) / (i.rect.centery - n.rect.centery) ** 2 )
#                        else: # it's negative
#                            i.force_y.append( -1 * (( G * n.mass * i.mass) / (i.rect.centery - n.rect.centery) ** 2 ))
#                    i.gravitation_x = sum(i.force_x)
#                    i.gravitation_y = sum(i.force_y)

    def update(self, delta):
        self.players.update(delta)
        self.enemies.update(delta)
        self.projectiles.update(delta)
        self.explosions.update(delta)
        self.planets.update(delta)

        self.matter = self.players.sprites()[:] + self.enemies.sprites()[:] + self.planets.sprites()[:]

        #self.gravity()

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

