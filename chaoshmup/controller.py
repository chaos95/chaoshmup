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
            InputAction("%s Right Thruster" % self.player.name, self.thruster_control(True, Directions.RIGHT), self.thruster_control(False, Directions.RIGHT))
            , InputAction("%s Left Thruster" % self.player.name, self.thruster_control(True, Directions.LEFT), self.thruster_control(False, Directions.LEFT))
            , InputAction("%s Up Thruster" % self.player.name, self.thruster_control(True, Directions.UP), self.thruster_control(False, Directions.UP))
            , InputAction("%s Down Thruster" % self.player.name, self.thruster_control(True, Directions.DOWN), self.thruster_control(False, Directions.DOWN))
            , InputAction("%s Fire Primary" % self.player.name, self.laser_fire(), None)
            , InputAction("%s Fire Secondary" % self.player.name, self.plasma_fire(), None)
            ]
            
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

    def laser_fire(self):
        def control():
            self.player.fire_primary()
        return control

    def plasma_fire(self):
        def control():
            self.player.fire_secondary()
        return control
            
