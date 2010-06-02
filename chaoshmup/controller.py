from chaoshmup.world import *

import math

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
    TURN_LEFT=5
    TURN_RIGHT=6

class InputController(object):
    def __init__(self):
        self.input_actions = []
        
class PlayerController(InputController):
    def __init__(self, player):
        self.player = player
        self.input_actions = [
            InputAction("%s Right Thruster" % self.player.name, self.thruster_control(True, Directions.RIGHT), self.thruster_control(False, Directions.RIGHT))
            , InputAction("%s Left Thruster" % self.player.name, self.thruster_control(True, Directions.LEFT), self.thruster_control(False, Directions.LEFT))
            , InputAction("%s Up Thruster" % self.player.name, self.thruster_control(True, Directions.UP), self.thruster_control(False, Directions.UP))
            , InputAction("%s Down Thruster" % self.player.name, self.thruster_control(True, Directions.DOWN), self.thruster_control(False, Directions.DOWN))
            , InputAction("%s Fire Primary" % self.player.name, self.laser_fire(), None)
            , InputAction("%s Rotate Left" % self.player.name, self.thruster_control(True, Directions.TURN_LEFT), self.thruster_control(False, Directions.TURN_LEFT))
            , InputAction("%s Rotate Right" % self.player.name, self.thruster_control(True, Directions.TURN_RIGHT), self.thruster_control(False, Directions.TURN_RIGHT))
            ]
            
    def thruster_control(self, switch_on, direction):
        if switch_on:
            thrust_modifier = 1
        else: # switch off
            thrust_modifier = -1
        def control():
            if direction == Directions.RIGHT:
                self.player.velocity_x += math.cos(self.player.angle * math.pi / 36.0) * thrust_modifier * self.player.THRUST_HORIZ
                self.player.velocity_y -= math.sin(self.player.angle * math.pi / 36.0) * thrust_modifier * self.player.THRUST_HORIZ
            elif direction == Directions.LEFT:
                self.player.velocity_x -= math.cos(self.player.angle * math.pi / 36.0) * thrust_modifier * self.player.THRUST_HORIZ
                self.player.velocity_y += math.sin(self.player.angle * math.pi / 36.0) * thrust_modifier * self.player.THRUST_HORIZ
            elif direction == Directions.UP:
                self.player.velocity_x -= math.sin(self.player.angle * math.pi / 36.0) * thrust_modifier * self.player.THRUST_VERT
                self.player.velocity_y -= math.cos(self.player.angle * math.pi / 36.0) * thrust_modifier * self.player.THRUST_VERT
            elif direction == Directions.DOWN:
                self.player.velocity_x += math.sin(self.player.angle * math.pi / 36.0) * thrust_modifier * self.player.THRUST_VERT
                self.player.velocity_y += math.cos(self.player.angle * math.pi / 36.0) * thrust_modifier * self.player.THRUST_VERT
            elif direction == Directions.TURN_RIGHT:
                self.player.angle -= 1
            elif direction == Directions.TURN_LEFT:
                self.player.angle += 1

        return control

    def laser_fire(self):
        def control():
            self.player.fire_primary()
        return control
            
