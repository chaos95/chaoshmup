import os
import random

import pygame
from pygame.locals import *

from chaoshmup.world import *
from chaoshmup.controller import *


WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FRAMERATE = 60

def initialise():
    pygame.init()
    pygame.font.init()
    random.seed()

    return pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))


def generate_world():
    w = World(WINDOWWIDTH, WINDOWHEIGHT)

    p = Player(w, "Player 1", "Players")
    p.rect.center = ((WINDOWWIDTH * 1) / 4, (WINDOWHEIGHT * 3) / 4)
    w.players.add(p)

    p = Player(w, "Player 2", "Players")
    p.rect.center = ((WINDOWWIDTH * 3) / 4, (WINDOWHEIGHT * 3) / 4)
    w.players.add(p)
    
    return w

def random_enemy(w):
    e = Enemy(w)
    e.position = (random.randint(50, WINDOWWIDTH-50),
                  random.randint(20, WINDOWHEIGHT / 2))
    return e

def screenshot_action(screen):
    def action():
        scrnums = [int(x[len("screenshot_"):-len(".png")])
                   for x in os.listdir(os.getcwd())
                   if x.startswith("screenshot_") and x.endswith(".png")]
        if scrnums:
            highest = max(scrnums)
        else:
            highest = 0
        newfilename = "screenshot_%d.png" % (highest+1)
        print "Taking screenshot and saving as %s" % newfilename
        pygame.image.save(screen,newfilename)
    return action

def main():
    # Initialise modules
    print "Initialising"
    screen = initialise()

    # Generate world
    print "Generating world"
    w = generate_world()

    # Set up controllers
    print "Setting up controls"
    controllers = []
    for p in w.players.sprites():
        controllers.append(PlayerController(p))

    action_map = {}

    # TODO: read controls from a config file
    action_map[K_RIGHT] = controllers[0].input_actions[0]
    action_map[K_LEFT] = controllers[0].input_actions[1]
    action_map[K_UP] = controllers[0].input_actions[2]
    action_map[K_DOWN] = controllers[0].input_actions[3]
    action_map[K_SPACE] = controllers[0].input_actions[4]
    action_map[K_RALT] = controllers[0].input_actions[5]

    action_map[K_d] = controllers[1].input_actions[0]
    action_map[K_a] = controllers[1].input_actions[1]
    action_map[K_w] = controllers[1].input_actions[2]
    action_map[K_s] = controllers[1].input_actions[3]
    action_map[K_LCTRL] = controllers[1].input_actions[4]
    action_map[K_LALT] = controllers[1].input_actions[5]

    action_map[K_F12] = InputAction("Take Screenshot",screenshot_action(screen),None)

    # Game loop
    print "Starting game loop"
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    fpsrect = pygame.Rect(0,0,0,0)
    delta = 0.0

    playing = True
    while playing:
        # Draw screen
        w.draw(screen)
        screen.fill((0,0,0),fpsrect)
        fps = font.render("FPS: %.2f" % (clock.get_fps()), 1, (255, 255, 255))
        fpsrect = fps.get_rect()
        screen.blit(fps, fpsrect)

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                # Escape key is magic, bypasses normal input handling
                if event.key == K_ESCAPE:
                    playing = False
                elif event.key in action_map and action_map[event.key].down_func:
                    action_map[event.key].down_func()
            elif event.type == KEYUP:
                if event.key in action_map and action_map[event.key].up_func:
                    action_map[event.key].up_func()

        # Update world
        delta_ms = clock.tick(FRAMERATE)
        delta = delta_ms / 1000.0
        w.update(delta)

        # Makeup enemy numbers - this is really only temporary
        makeup = 15 - (len(w.enemies) + len(w.explosions))
        for i in range(makeup):
            w.enemies.add(random_enemy(w))

    # Quit game
    print "Quitting"
    pygame.quit()
