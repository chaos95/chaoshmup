import random

import pygame
from pygame.locals import *

class Entity(pygame.sprite.Sprite):
    IMAGE_FILE = ""
    def __init__(self, world):
        pygame.sprite.Sprite.__init__(self)
        self.world = world
        self.base_image = pygame.image.load(self.IMAGE_FILE)
        self.image = self.base_image
        self.rect = pygame.Rect(0,0,self.image.get_width(),self.image.get_height())
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self, delta):
        self.rect = self.rect.move(self.velocity_x * delta, self.velocity_y * delta)

class Enemy(Entity):
    IMAGE_FILE = "images/enemy.png"
    def __init__(self, world):
        Entity.__init__(self, world)
        self.rotation = 0

    def update(self, delta):
        Entity.update(self, delta)
        self.rotation += delta * 60
        self.image = pygame.transform.rotate(self.base_image, self.rotation)
        center = self.rect.center
        self.rect.size = self.image.get_rect().size
        self.rect.center = center


class Laser(Entity):
    IMAGE_FILE = "images/laser.png"
    def __init__(self, world, owner, pos, velocity_x = 0, velocity_y = -1000):
        Entity.__init__(self, world)
        self.owner = owner
        self.rect.center = pos
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y


class Player(Entity):
    IMAGE_FILE = "images/player.png"
    THRUST_HORIZ = 500
    THRUST_VERT = 500
    def __init__(self, world, name):
        Entity.__init__(self, world)
        self.name = name

    def fire_primary(self):
        self.world.lasers.add(Laser(self.world, self, self.rect.midtop))


class Explosion(pygame.sprite.Sprite):
    IMAGE_FILE = "images/explosion.png"
    LIFESPAN = 300
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(self.IMAGE_FILE)
        self.rect = pygame.Rect((0,0), self.image.get_rect().size)
        self.rect.center = pos
        self.lifetime = 0
        self.alive = True

    def update(self, delta):
        self.lifetime += delta * 1000
        if self.lifetime >= self.LIFESPAN:
            self.alive = False

class World(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.players = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

    def update(self, delta):
        self.players.update(delta)
        self.enemies.update(delta)
        self.lasers.update(delta)
        self.explosions.update(delta)

        expldead = [x for x in self.explosions.sprites()[:] if not x.alive]
        self.explosions.remove(expldead)

        # Collision detection
        laser_enemy = pygame.sprite.groupcollide(self.enemies, self.lasers, True, True)
        for enemy in [x for (x,y) in laser_enemy.iteritems() if len(y) > 0]:
            self.explosions.add(Explosion(x.rect.center))

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
        
