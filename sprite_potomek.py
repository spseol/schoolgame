#!/usr/bin/env python3
# Soubor:  pokus.py
############################################################################

import pyglet
import random
from math import sin, cos, radians, pi
import glob

from pyglet.window.key import LEFT, RIGHT, UP, DOWN
# from pyglet.window.mouse import LEFT as MouseLEFT

window = pyglet.window.Window(width=1200, height=950)
batch = pyglet.graphics.Batch()   # pro optimalizované vyreslování objektů
bg_batch = pyglet.graphics.Batch()   # pro optimalizované vyreslování objektů


class SpaceObject(pyglet.sprite.Sprite):

    def __init__(self, img_file, x=None, y=None):
        self.image_load = pyglet.image.load(img_file)
        # střed otáčení dám na střed obrázku
        self.image_load.anchor_x = self.image_load.width // 2
        self.image_load.anchor_y = self.image_load.height // 2
        # z obrázku vytvořím sprite
        super().__init__(self.image_load,  batch=batch)
        self.x = x if x is not None else random.randint(0, window.width)
        self.y = y if y is not None else random.randint(0, window.height)


@window.event
def on_key_press(sym, mod):
    obj.x += 10
    obj.y += 10


@window.event
def on_draw():
    window.clear()
    batch.draw()


obj = SpaceObject('obrazkyAST/PNG/Meteors/4.png',)


def ticktack(dt):
    obj.rotation += 1


pyglet.clock.schedule_interval(ticktack, 1/30)
pyglet.app.run()
