# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 16:13:22 2019

@author: Martin
"""

import pyglet
import random
from math import sin, cos, radians, pi
from pyglet.window import key

window = pyglet.window.Window(1250, 1000)
batch = pyglet.graphics.Batch()
bg_batch = pyglet.graphics.Batch()


class All_objects(pyglet.sprite.Sprite):

    def __init__(self, img_file, x=None, y=None):
        self.image_load = pyglet.image.load(img_file)
        # střed otáčení dám na střed obrázku
        self.image_load.anchor_x = self.image_load.width // 2
        self.image_load.anchor_y = self.image_load.height // 2
        # z obrázku vytvořím sprite
        super().__init__(self.image_load,  batch=batch)
        self.x = x if x is not None else random.randint(0, window.width)
        self.y = y if y is not None else random.randint(0, window.height)


class Spaceship(All_objects):

    def __init__(self, x=None, y=None, x_speed=None, y_speed=None, rotation=None):

        self.keys = set()
        super().__init__(
            "obrazkyAST/PNG/raketa1.png", x=window.width / 2, y=77)
        self.x_speed = 0
        self.y_speed = 0
        self.rotation = 0
        self.rozmer = min(self.image.width, self.image.height) / 2

    def tick(self, dt):
        for sym in self.keys:
            if sym == key.RIGHT:
                self.rotation = self.rotation + 10
            elif sym == key.LEFT:
                self.rotation = self.rotation - 10
            elif sym == key.UP:
                self.x_speed = 400
                self.y_speed = 400
                self.x = self.x + dt * self.x_speed * \
                    cos(pi / 2 - radians(self.rotation))
                self.y = self.y + dt * self.y_speed * \
                    sin(pi / 2 - radians(self.rotation))
            elif sym == key.DOWN:
                self.x_speed = 200
                self.y_speed = 200
                self.x = self.x + dt * self.x_speed * \
                    (-cos(pi / 2 - radians(self.rotation)))
                self.y = self.y + dt * self.y_speed * \
                    (-sin(pi / 2 - radians(self.rotation)))


class Meteor(All_objects):

    def __init__(self, x=None, y=None, img_file=None, x_speed=None, y_speed=None, rspeed=None, rozmer=None):

        if img_file is None:
            num = random.choice(range(1, 20))
            img_file = ("obrazkyAST/PNG/Meteors/{}.png".format(num))
        super().__init__(img_file, x, y=window.height + 20)

        self.x_speed = x_speed if x_speed is not None else random.randint(30, 180)
        self.y_speed = y_speed if y_speed is not None else random.randint(-180, -30)
        self.rspeed = rspeed if rspeed is not None else random.randint(-50, 50)
        self.rozmer = min(self.image.width, self.image.height) / 2

    def tick(self, dt):
        self.x = self.x + dt * self.x_speed
        self.y = self.y + dt * self.y_speed
        self.rotation = self.rotation + dt * self.rspeed

        if self.x + self.rozmer > window.width + 200:
            actions.meteors.remove(self)
            self.delete()
        elif self.x + self.rozmer < -200:
            actions.meteors.remove(self)
            self.delete()
        elif self.y + self.rozmer < -200:
            actions.meteors.remove(self)
            self.delete()

    def __del__(self):
        print("Meteor smazán")


class Laser(All_objects):

    def __init__(self, img_file=None, speed=None, rotation=None):

        super().__init__("obrazkyAST/PNG/Effects/fire01.png",
                         x=ship.x, y=ship.y)
        self.anchr_x = self.width // 2
        self.anchor_y = self.height
        self.speed = 1000
        self.rozmer = min(self.image.width, self.image.height) / 2
        self.rotation = ship.rotation

    def tick(self, dt):
        self.x = self.x + dt * self.speed * \
            cos(pi / 2 - radians(self.rotation))
        self.y = self.y + dt * self.speed * \
            sin(pi / 2 - radians(self.rotation))

        if self.y + self.rozmer > window.height + 200:
            actions.lasers.remove(self)
            self.delete()

    def __del__(self):
        print("Laser smazán")

class Actions():

    meteors = []
    lasers = []

    def add_meteor(self, dt=None):
        self.meteors.append(Meteor())

    def add_laser(self, dt=None):
        self.lasers.append(Laser())

    def tick(self, dt):
        # pohnu kamenama
        for meteor in self.meteors:
            meteor.tick(dt)
            distance = ((meteor.x - ship.x)**2 + (meteor.y - ship.y)**2)**0.5
            if distance - meteor.rozmer / 2 - 43 <= 0:
                self.colision()
                """
                label = pyglet.text.Label("Prohrál jsi",
                          font_name="Times New Roman",
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x="center", anchor_y="center")
                """

            for laser in self.lasers:
                laser.tick(dt)
                distance2 = ((meteor.x - laser.x)**2 + (meteor.y - laser.y)**2)**0.5
                if (distance2 - meteor.rozmer) <= 0:
                    self.lasers.remove(laser)
                    laser.delete()
                    self.meteors.remove(meteor)
                    meteor.delete()
                    

    def colision(self):
        pyglet.clock.unschedule(ticky)
        pyglet.clock.unschedule(actions.add_meteor)
        ship.x_speed = 0
        ship.y_speed = 0
        print("Prohrál jsi")
        if ship.sym == key.R:
            self.reset()
        
    def reset(self):
        for meteor in self.meteors:
            self.meteors.remove(meteor)
            meteor.delete()
        ship.x = window.width / 2
        ship.y = 77
        pyglet.clock.schedule_interval(ticky, 1/30)
        pyglet.clock.schedule_interval(actions.add_meteor, 1/3)


def ticky(dt):
    actions.tick(dt)
    ship.tick(dt)

bg = pyglet.image.load("obrazkyAST/Backgrounds/blue.png")
x = 0
bg_sprites = ()

while x < window.width:
    y = 0
    while y < window.height:
        bg_sprites += (pyglet.sprite.Sprite(bg, x=x, y=y, batch=bg_batch),)
        y += bg.height
    x += bg.width

@window.event
def on_key_press(sym, mod):
    ship.keys.add(sym)
    if sym == key.SPACE:
        actions.add_laser()


@window.event
def on_key_release(sym, mod):
    ship.keys.remove(sym)


@window.event
def on_draw():
    window.clear()
    bg_batch.draw()
    batch.draw()
#    label.draw()
    

ship = Spaceship()
actions = Actions()
actions.add_meteor()
actions.add_meteor()
pyglet.clock.schedule_interval(ticky, 1 / 30)
pyglet.clock.schedule_interval(actions.add_meteor, 10 / 3)
pyglet.app.run()
