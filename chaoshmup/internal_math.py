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

import math

def sign(foo):
    if foo >= 0:
        return 1
    else:
        return -1

def tuple_xy_add(foo):
    bar = 0
    baz = 0
    for i in range(0,len(foo)):
        bar += foo[i][0]
        baz += foo[i][1]
    return bar, baz

def uni_gravity(G, cray, boff):
    # newton's law of universal gravitation
    # F = GMm/r^2
    if (cray.rect.centery - boff.rect.centery) == 0 and (cray.rect.centerx - boff.rect.centerx) == 0:
        force = G * (cray.mass * boff.mass)
    else:
        force = G * (cray.mass * boff.mass) / ((cray.rect.centery - boff.rect.centery) ** 2 + (cray.rect.centerx - boff.rect.centerx) ** 2)

    #cray.orientation = math.degrees(math.atan2((cray.rect.centerx - boff.rect.centerx) , (cray.rect.centery - boff.rect.centery)))

    return ((math.cos(math.atan2((cray.rect.centerx - boff.rect.centerx), (cray.rect.centery - boff.rect.centery))) * force), (sign(boff.rect.centery - cray.rect.centery) * math.sin(math.atan2((cray.rect.centerx - boff.rect.centerx), (cray.rect.centery - boff.rect.centery))) * force))
