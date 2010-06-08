import random

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
                        PlasmaCannon(self.world, self)]

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

    def update(self, delta):
        self.players.update(delta)
        self.enemies.update(delta)
        self.projectiles.update(delta)
        self.explosions.update(delta)

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

