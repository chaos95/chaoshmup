# Copyright (c) 2010, Michael Brindle
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

import pygame

from entity import Entity

class black_hole(Entity):
    IMAGE_FILE = "images/black_hole.png" # hurpa derp
    def __init__(self, world):
        Entity.__init__(self, world)
        self.mass = 1000000 # 1 million units - it's a black hole.

    def update(self, delta):
        Entity.update(self, delta)

class star(Entity):
    IMAGE_FILE = "images/star.png"
    def __init__(self, world):
        Entity.__init__(self, world)
        self.mass = 100000 # 100 thousand - it's a freaking star

    def update(self, delta):
        Entity.update(self, delta)

class gas_giant(Entity):
    IMAGE_FILE = "mages/blackhole.png"
    def __init__(self, world):
        Entity.__init__(self, world)
        self.mass = 10000 # 10 thousand - it's a gas giant

    def update(self, delta):
        Entity.update(self, delta)

class planet(Entity):
    IMAGE_FILE = "images/planet.png"
    def __init__(self, world):
        Entity.__init__(self, world)
        self.mass = 1000 # 1 thousand - meh

    def update(self, delta):
        Entity.update(self, delta)
