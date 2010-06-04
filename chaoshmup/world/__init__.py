import random

import math

import pygame
from pygame.locals import *

from entity import Entity
from weapons import Laser, Plasma

class Ship(Entity):
    THRUST_HORIZ = 500
    THRUST_VERT = 500
    THRUST_ROTATE = 40
    HEALTH = 100
    START_ORIENTATION = 0
    def __init__(self, world):
        Entity.__init__(self, world)
        self.health = self.HEALTH
        self.orientation = self.START_ORIENTATION
        self.rotation = 0
        self.last_orientation = self.orientation
        self.mass = 100

    def update(self, delta):
        Entity.update(self, delta)
        self.orientation += self.rotation * delta
        if self.orientation != self.last_orientation:
            self.image = pygame.transform.rotate(self.images[self.animation[self.frame]], self.orientation)
            center = self.rect.center
            self.rect.size = self.image.get_rect().size
            self.rect.center = center
        self.last_orientation = self.orientation

    def hit(self, weapon):
        self.health -= weapon.damage
        if self.health <= 0:
            self.alive = False

class Enemy(Ship):
    IMAGE_FILE = "images/i_are_spaceship.png"
    def __init__(self, world):
        Ship.__init__(self, world)
        self.rotation = 60
        
    def load_images(self):
        image = pygame.image.load(self.IMAGE_FILE)
        self.images = [image.subsurface(pygame.Rect(48,16,16,16))]

class Player(Entity):
    IMAGE_FILE = "images/i_are_spaceship.png"
    THRUST_HORIZ = 500
    THRUST_VERT = 500
    FRAME_DELAY = 0.1
    def __init__(self, world, name):
        Entity.__init__(self, world)
        self.name = name

    def update(self, delta):
        Entity.update(self, delta)
        self.image = pygame.transform.rotate(self.images[0], self.angle * 5)
        center = self.rect.center

    def load_images(self):
        image = pygame.image.load(self.IMAGE_FILE)
        self.images = [image.subsurface(pygame.Rect(0,0,16,32)),
                       image.subsurface(pygame.Rect(16,0,16,32))]

    def fire_primary(self):
        self.world.lasers.add(Laser(self.world, self, self.rect.midtop))

    def fire_secondary(self):
        self.world.lasers.add(Plasma(self.world, self, self.rect.midtop))


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

    def next_frame(self):
        if self.frame+1 >= len(self.animation):
            self.alive = False
        else:
            self.frame += 1
        return self.images[self.animation[self.frame]]
    
class World(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.players = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.planets = pygame.sprite.Group()
        self.matter = self.players.sprites()[:] + self.enemies.sprites()[:] + self.planets.sprites()[:]

    def gravity(self):
        G = 6.6
        for i in self.matter:
            while len(i.force) > 0:
                i.force.pop()
            for n in self.matter:
                if i != n:
                    i.force.append(( G * n.mass * i.mass) / ((i.rect.centery - n.rect.centery) ** 2 + (i.rect.centerx - n.rect.centerx) ** 2))
                    i.gravitation = sum(i.force)
                    # TODO: figure out how to make this interesting.

    def update(self, delta):
        self.players.update(delta)
        self.enemies.update(delta)
        self.lasers.update(delta)
        self.explosions.update(delta)
        self.planets.update(delta)

        self.matter = self.players.sprites()[:] + self.enemies.sprites()[:] + self.planets.sprites()[:]

        # Collision detection
        laser_enemy = pygame.sprite.groupcollide(self.enemies, self.lasers, False, True)
        for (enemy, lasers) in laser_enemy.iteritems():
            for laser in lasers:
                enemy.hit(laser)
            
        # Cleanup
        enemydead = [x for x in self.enemies.sprites()[:] if not x.alive]
        for x in enemydead:
            self.explosions.add(Explosion(self, x.rect.center))
        self.enemies.remove(enemydead)

        expldead = [x for x in self.explosions.sprites()[:] if not x.alive]
        self.explosions.remove(expldead)

        laserdead = [x for x in self.lasers.sprites()[:] if x.rect.bottom < 0 or x.rect.right < 0 or x.rect.left > self.width or x.rect.top > self.height]
        self.lasers.remove(laserdead)

        # Makeup enemy numbers - this is really only temporary
        makeup = 5 - (len(self.enemies) + len(self.explosions))
        for i in range(makeup):
            self.enemies.add(self.random_enemy())
        
    def clear_callback(self, surf, rect):
        surf.fill((0,0,0), rect)
        
    def draw(self, surface):
        self.explosions.clear(surface, self.clear_callback)
        self.lasers.clear(surface, self.clear_callback)
        self.enemies.clear(surface, self.clear_callback)
        self.players.clear(surface, self.clear_callback)
        
        self.explosions.draw(surface)
        self.lasers.draw(surface)
        self.enemies.draw(surface)
        self.players.draw(surface)

    def random_enemy(self):
        e = Enemy(self)
        e.rect.center = (random.randint(50, self.width-50),
                         random.randint(20, self.height / 2))
        return e
