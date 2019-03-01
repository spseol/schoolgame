# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 16:13:22 2019

@author: Martin
"""

import pyglet
import random
from math import sin, cos, radians, pi
#from pyglet.window import key


window = pyglet.window.Window(1000, 800)
batch = pyglet.graphics.Batch()
#bg_batch = pyglet.graphics.Batch()

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
        

class Meteor(All_objects):
    
    def __init__(self, x=None, y=None, img_file=None, direction=None,speed=None, rspeed=None):
        if img_file is None:
            num=random.choice(range(1,20))
            img_file=("obrazkyAST/PNG/Meteors/{}.png".format(num))
        super().__init__(img_file, x, y=window.height+20)
        
        self.direction=direction if direction is not None else random.randint(150,220)
        self.speed=speed if speed is not None else random.randint(30,80)
        self.rspeed=rspeed if rspeed is not None else random.randint(-50,50)
        
    def tick(self,dt):
        self.x=self.x + dt * self.speed * cos(pi / 2 - radians(self.direction))
        self.y=self.y + dt * self.speed * sin(pi / 2 - radians(self.direction))
        self.rotatin= self.rotation + dt * self.rspeed
        self.bounce()
        
    def bounce(self):
        rozmer=min(self.image.width,self.image.height)/2
        
        if self.x + rozmer >= window.width:
            self.direction=random.randint(190,350)
            return
        if self.x - rozmer  <=0:
            self.direction=random.randint(10,170)
            return
        if self.y + rozmer >= window.height:
            self.direction=random.randint(100,260)
            return
        if self.y - rozmer <=0:
            self.direction=random.randint(-80,80)
            return


class Actions():
    
    meteors=[]
    def add_meteor(self,dt=None):
        self.meteors.append(Meteor())
        
    def tick(self, dt):
        # pohnu kamenama
        for meteor in self.meteors:
            meteor.tick(dt)
def ticky(dt):
    actions.tick(dt)
            
@window.event
def on_key_press(sym, mod):
    global klavesy
    klavesy.add(sym)


@window.event
def on_draw():
    window.clear()
    batch.draw()

actions=Actions()
actions.add_meteor()
actions.add_meteor()
pyglet.clock.schedule_interval(ticky, 1/30)
pyglet.clock.schedule_interval(actions.add_meteor, 10/3)
pyglet.app.run()