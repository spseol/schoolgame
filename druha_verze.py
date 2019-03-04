# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 16:13:22 2019

@author: Martin
"""

import pyglet
import random
from math import sin, cos, radians, pi
from pyglet.window import key

window = pyglet.window.Window(1000, 800)
batch = pyglet.graphics.Batch()

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
        
        self.keys=set()
        super().__init__("obrazkyAST/PNG/raketa1.png", x=window.width/2, y=77)
        self.x_speed=0
        self.y_speed=0
        self.rotation=0
        self.rozmer = min(self.image.width, self.image.height)/2
        
    def tick(self,dt):
        for sym in self.keys:
            if sym==key.RIGHT:
                self.rotation=self.rotation + 10
            elif sym==key.LEFT:
                self.rotation=self.rotation - 10    
            elif sym==key.UP:
                self.x_speed = 900
                self.y_speed = 900
                self.x=self.x + dt * self.x_speed*cos(pi/2 - radians(self.rotation))
                self.y=self.y + dt * self.y_speed*sin(pi/2 - radians(self.rotation))
            elif sym==key.DOWN:
                self.x_speed=200
                self.y_speed=200
                self.x=self.x + dt * self.x_speed* (-cos(pi/2 - radians(self.rotation)))
                self.y=self.y + dt * self.y_speed*(-sin(pi/2 - radians(self.rotation)))
        
class Meteor(All_objects):
    
    def __init__(self, x=None, y=None, img_file=None, direction=None,speed=None, rspeed=None, rozmer=None):
        if img_file is None:
            num=random.choice(range(1,20))
            img_file=("obrazkyAST/PNG/Meteors/{}.png".format(num))
        super().__init__(img_file, x, y=window.height+20)
        
        self.direction=direction if direction is not None else random.randint(150,220)
        self.speed=speed if speed is not None else random.randint(300,800)
        self.rspeed=rspeed if rspeed is not None else random.randint(-50,50)
        self.rozmer=min(self.image.width,self.image.height)/2

    def __del__():
        print(id(self))
        
    def tick(self, dt):
        self.x=self.x + dt * self.speed * cos(pi / 2 - radians(self.direction))
        self.y=self.y + dt * self.speed * sin(pi / 2 - radians(self.direction))
        self.rotatin= self.rotation + dt * self.rspeed
        
        if self.x + self.rozmer> window.width + 200:
            del(self)
        elif self.x + self.rozmer < -200:
            del(self)
        elif self.y + self.rozmer < -200:
            del(self)


class Actions():

    meteors=[]
    def add_meteor(self,dt=None):
        self.meteors.append(Meteor())
              
    def tick(self, dt):
        # pohnu kamenama
        for meteor in self.meteors:
            meteor.tick(dt)
            distance = ((meteor.x - ship.x)**2 + (meteor.y - ship.y)**2)**0.5
            if distance - meteor.rozmer/2 <=0:
                self.colision()
                
    def colision(self):
        pyglet.clock.unschedule(ticky)
        pyglet.clock.unschedule(actions.add_meteor)  
        ship.x_speed=0
        ship.y_speed=0
        print("Prohrál jsi")          
        
def ticky(dt):
    actions.tick(dt)
    ship.tick(dt)
            
@window.event
def on_key_press(sym, mod):
    ship.keys.add(sym)

@window.event
def on_key_release(sym, mod):
    ship.keys.remove(sym)

@window.event
def on_draw():
    window.clear()
    batch.draw()

ship=Spaceship()
actions=Actions()
actions.add_meteor()
actions.add_meteor()
pyglet.clock.schedule_interval(ticky, 1/30)
pyglet.clock.schedule_interval(actions.add_meteor, 10/3)
pyglet.app.run()
