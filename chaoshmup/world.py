import random

import math

import pygame
from pygame.locals import *

class Entity(pygame.sprite.Sprite):
    IMAGE_FILE = ""
    START_FRAME = 0
    FRAME_DELAY = 99999999.0
    def __init__(self, world):
        pygame.sprite.Sprite.__init__(self)
        self.world = world
        self.load_images()
        self.frame = self.START_FRAME
        self.image = self.images[self.frame]
        self.rect = pygame.Rect(0,0,self.image.get_width(),self.image.get_height())
        self.velocity_x = 0
        self.velocity_y = 0
        self.angle = 0
        self.frametime = 0.0

    def load_images(self):
        self.images = [pygame.image.load(self.IMAGE_FILE)]

    def next_frame(self):
        if self.frame+1 >= len(self.images):
            self.frame = 0
        else:
            self.frame += 1
        return self.images[self.frame]

    def update(self, delta):
        self.frametime += delta
        if self.frametime >= self.FRAME_DELAY:
            self.image = self.next_frame()
            self.frametime = 0.0
        self.rect = self.rect.move(self.velocity_x * delta, self.velocity_y * delta)

class Enemy(Entity):
    IMAGE_FILE = "images/i_are_spaceship.png"
    def __init__(self, world):
        Entity.__init__(self, world)
        self.rotation = 0

    def load_images(self):
        image = pygame.image.load(self.IMAGE_FILE)
        self.images = [image.subsurface(pygame.Rect(48,16,16,16))]

    def update(self, delta):
        Entity.update(self, delta)
        self.rotation += delta * 60
        self.image = pygame.transform.rotate(self.images[0], self.rotation)
        center = self.rect.center
        self.rect.size = self.image.get_rect().size
        self.rect.center = center


class Laser(Entity):
    IMAGE_FILE = "images/i_are_spaceship.png"
    def __init__(self, world, owner, pos, velocity_x = 0, velocity_y = -1000):
        Entity.__init__(self, world)
        self.owner = owner
        self.rect.center = pos
        self.velocity_x = math.sin(owner.angle * math.pi / 12.0) * velocity_y
        self.velocity_y = math.cos(owner.angle * math.pi / 12.0) * velocity_y

    def load_images(self):
        image = pygame.image.load(self.IMAGE_FILE)
        self.images = [image.subsurface(pygame.Rect(32,16,8,8))]

    def update(self, delta):
        Entity.update(self, delta)
        self.image = pygame.transform.rotate(self.images[0], self.owner.angle * 10)


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
        self.image = pygame.transform.rotate(self.images[0], self.angle * 15)
        center = self.rect.center

    def load_images(self):
        image = pygame.image.load(self.IMAGE_FILE)
        self.images = [image.subsurface(pygame.Rect(0,0,16,32)),
                       image.subsurface(pygame.Rect(16,0,16,32))]

    def fire_primary(self):
        self.world.lasers.add(Laser(self.world, self, self.rect.midtop))


class Explosion(Entity):
    IMAGE_FILE = "images/i_are_spaceship.png"
    FRAME_DELAY = 0.3
    def __init__(self, world, pos):
        Entity.__init__(self, world)
        self.rect.center = pos
        self.alive = True

    def load_images(self):
        image = pygame.image.load(self.IMAGE_FILE)
        self.images = [image.subsurface(pygame.Rect(0,32,16,16)),
                       image.subsurface(pygame.Rect(16,32,16,16)),
                       image.subsurface(pygame.Rect(32,32,16,16)),
                       image.subsurface(pygame.Rect(48,32,16,16))]

    def update(self, delta):
        Entity.update(self, delta)
        if self.frame >= len(self.images)-1:
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

        # Cleanup
        expldead = [x for x in self.explosions.sprites()[:] if not x.alive]
        self.explosions.remove(expldead)

        laserdead = [x for x in self.lasers.sprites()[:] if x.rect.bottom < 0 or x.rect.right < 0 or x.rect.left > self.width or x.rect.top > self.height]
        self.lasers.remove(laserdead)

        # Collision detection
        laser_enemy = pygame.sprite.groupcollide(self.enemies, self.lasers, True, True)
        for enemy in [x for (x,y) in laser_enemy.iteritems() if len(y) > 0]:
            self.explosions.add(Explosion(self, x.rect.center))

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
        
