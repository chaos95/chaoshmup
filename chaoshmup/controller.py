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

class WeaponInputAction(InputAction):
    def __init__(self, description, weapon):
        InputAction.__init__(self, description, weapon.fire, weapon.release)
        self._weapon = weapon

    @property
    def weapon(self):
        return self._weapon

    @weapon.setter
    def weapon(self, value):
        self._weapon = value
        self.down_func = self._weapon.fire
        self.up_func = self._weapon.release

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
        self.current_weapon = 0
        self.input_actions = [
            InputAction("%s Right Thruster" % self.player.name, self.thruster_control(True, Directions.RIGHT), self.thruster_control(False, Directions.RIGHT))
            , InputAction("%s Left Thruster" % self.player.name, self.thruster_control(True, Directions.LEFT), self.thruster_control(False, Directions.LEFT))
            , InputAction("%s Up Thruster" % self.player.name, self.thruster_control(True, Directions.UP), self.thruster_control(False, Directions.UP))
            , InputAction("%s Down Thruster" % self.player.name, self.thruster_control(True, Directions.DOWN), self.thruster_control(False, Directions.DOWN))
            , WeaponInputAction("%s Fire Primary" % self.player.name, self.player.weapons[self.current_weapon])
            , InputAction("%s Switch Weapon" % self.player.name, self.switch_weapon, None)
            ]
            

    def switch_weapon(self):
        self.current_weapon += 1
        if self.current_weapon >= len(self.player.weapons):
            self.current_weapon = 0
        # update weapon actions
        for a in [act for act in self.input_actions if hasattr(act, 'weapon')]:
            a.weapon = self.player.weapons[self.current_weapon]

    def thruster_control(self, switch_on, direction):
        if switch_on:
            def control():
                if direction == Directions.RIGHT:
                    self.player.acceleration += (self.player.THRUST_HORIZ, 0)
                elif direction == Directions.LEFT:
                    self.player.acceleration -= (self.player.THRUST_HORIZ, 0)
                elif direction == Directions.UP:
                    self.player.acceleration -= (0, self.player.THRUST_VERT)
                elif direction == Directions.DOWN:
                    self.player.acceleration += (0, self.player.THRUST_VERT)
        else:
            def control():
                if direction == Directions.RIGHT:
                    self.player.acceleration -= (self.player.THRUST_HORIZ, 0)
                elif direction == Directions.LEFT:
                    self.player.acceleration += (self.player.THRUST_HORIZ, 0)
                elif direction == Directions.UP:
                    self.player.acceleration += (0, self.player.THRUST_VERT)
                elif direction == Directions.DOWN:
                    self.player.acceleration -= (0, self.player.THRUST_VERT)

        return control
