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
    controllers = {}
    for p in w.players.sprites():
        controllers[p.name] = PlayerController(p)

    action_map = {}

    # TODO: read controls from a config file
    action_map[K_UP] = controllers["Player 1"].input_actions[0]
    action_map[K_LEFT] = controllers["Player 1"].input_actions[1]
    action_map[K_RIGHT] = controllers["Player 1"].input_actions[2]
    action_map[K_RCTRL] = controllers["Player 1"].input_actions[3]
    action_map[K_RSHIFT] = controllers["Player 1"].input_actions[4]

    action_map[K_w] = controllers["Player 2"].input_actions[0]
    action_map[K_a] = controllers["Player 2"].input_actions[1]
    action_map[K_d] = controllers["Player 2"].input_actions[2]
    action_map[K_LCTRL] = controllers["Player 2"].input_actions[3]
    action_map[K_LSHIFT] = controllers["Player 2"].input_actions[4]

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
        if makeup > 0:
            for i in range(makeup):
                w.enemies.add(random_enemy(w))

    # Quit game
    print "Quitting"
    pygame.quit()
