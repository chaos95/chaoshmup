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

from chaoshmup.world import *

# Controller layer
class InputAction(object):
    def __init__(self, description, down_func, up_func):
        self.description = description
        self.down_func = down_func
        self.up_func = up_func

class Directions(object):
    RIGHT=0
    LEFT=1
    UP=2
    DOWN=3

class InputController(object):
    def __init__(self):
        self.input_actions = []
        
class PlayerController(InputController):
    def __init__(self, player):
        self.player = player
        self.input_actions = [
            InputAction("%s Forward Thruster" % self.player.name, self.thruster_fire(), self.thruster_release())
            , InputAction("%s Rotate Anti-clockwise" % self.player.name, self.rotate_ccw(), self.rotate_cw())
            , InputAction("%s Rotate Clockwise" % self.player.name, self.rotate_cw(), self.rotate_ccw())
            , InputAction("%s Fire Primary" % self.player.name, self.primary_fire(), self.primary_release())
            , InputAction("%s Fire Secondary" % self.player.name, self.secondary_fire(), self.secondary_release())
            ]
            
    def thruster_fire(self):
        def control():
            self.player.thrust = 200
        return control

    def thruster_release(self):
        def control():
            self.player.thrust = 0
        return control

    def rotate_ccw(self):
        def control():
            self.player.rotation += 360
        return control

    def rotate_cw(self):
        def control():
            self.player.rotation -= 360
        return control

    def primary_fire(self):
        def control():
            self.player.weapons[0].fire()
        return control

    def secondary_fire(self):
        def control():
            self.player.weapons[1].fire()
        return control

    def primary_release(self):
        def control():
            self.player.weapons[0].release()
        return control

    def secondary_release(self):
        def control():
            self.player.weapons[1].release()
        return control
            
