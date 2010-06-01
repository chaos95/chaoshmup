import random

import pygame
from pygame.locals import *

from chaoshmup.world import *
from chaoshmup.controller import *


WINDOWWIDTH = 640
WINDOWHEIGHT = 480

def initialise():
    pygame.init()
    pygame.font.init()
    random.seed()

    return pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))


def generate_world():
    w = World(WINDOWWIDTH, WINDOWHEIGHT)

    p = Player(w, "Player 1")
    p.rect.center = (WINDOWWIDTH * 1 / 4, WINDOWHEIGHT * 3 / 4)
    w.players.add(p)

    p = Player(w, "Player 2")
    p.rect.center = (WINDOWWIDTH * 3 / 4, WINDOWHEIGHT * 3 / 4)
    w.players.add(p)
    
    return w

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
    # TODO: Figure out better controls for turning the thing.
    action_map[K_j] = controllers[0].input_actions[5]
    action_map[K_k] = controllers[0].input_actions[6]

    action_map[K_d] = controllers[1].input_actions[0]
    action_map[K_a] = controllers[1].input_actions[1]
    action_map[K_w] = controllers[1].input_actions[2]
    action_map[K_s] = controllers[1].input_actions[3]
    action_map[K_LCTRL] = controllers[1].input_actions[4]
    # TODO: Figure out better controls for turning the thing.
    action_map[K_q] = controllers[1].input_actions[5]
    action_map[K_e] = controllers[1].input_actions[6]


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
        delta_ms = clock.tick(60)
        delta = delta_ms / 1000.0
        w.update(delta)

    # Quit game
    print "Quitting"
    pygame.quit()
