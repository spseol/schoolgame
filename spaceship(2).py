# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 09:15:01 2018

@author: Martin
"""

import pyglet
import random
from math import sin, cos, radians, pi
from pyglet.window import key

window = pyglet.window.Window(1000, 800)
batch = pyglet.graphics.Batch()
klavesy=set()


class Stone(object):
    
    def __init__(self,x=None, y=None,direction=None,speed=None, rspeed=None):
        
        self.x=x if x is not None else random.randint(0, window.width)
        self.y=y if y is not None else random.randint(0,window.height)
        
        self.direction=direction if direction is not None else random.randint(0,359)
        
        self.speed=speed if speed is not None else random.randint(30,180)
        self.rspeed=rspeed if rspeed is not None else random.randint(-100,100)
        
        num=random.choice(range(1,20))
        self.image=pyglet.image.load("obrazkyAST/PNG/meteors/{}.png".format(num))
        self.image.anchor_x=self.image.width // 2
        self.image.anchor_y=self.image.height // 2
        
        self.sprite=pyglet.sprite.Sprite(self.image, batch=batch)
        self.sprite.x=self.x
        self.sprite.y=self.y
    
    def tick(self,dt):
        self.bounce()
        self.x=self.x + dt * self.speed * cos(pi / 2 - radians(self.direction))
        self.sprite.x=self.x
        self.y=self.y + dt * self.speed * sin(pi / 2 - radians(self.direction))
        self.sprite.y=self.y
        self.sprite.rotatin= self.sprite.rotation + 0.01 * self.rspeed
        
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
stones=[] 
       
for i in range(30):
    stone=Stone()
    pyglet.clock.schedule_interval(stone.tick, 1/30)
    stones.append(stone)

class Spaceship(object):
    
    def __init__(self, x=None, y=None, x_speed=None, y_speed=None, rotation=None):
        self.x=window.width/2
        self.y=window.height/2
        self.x_speed=0
        self.y_speed=0
        self.rotation=0

        self.image=pyglet.image.load("obrazkyAST/PNG/raketa1.png")
        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.width // 2
        self.sprite = pyglet.sprite.Sprite(self.image, batch=batch)
        
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.rozmer = min(self.image.width, self.image.height)/2
        
    def tick(self,dt):
        for sym in klavesy:
            if sym==key.RIGHT:
                self.rotation=self.rotation + 10
            elif sym==key.LEFT:
                self.rotation=self.rotation - 10    
            elif sym==key.UP:
                self.x_speed=200
                self.y_speed=200
                self.x=self.x + dt * self.x_speed*cos(pi/2 - radians(self.rotation))
                if self.x +self.rozmer>=window.width or self.x - self.rozmer<=0:
                    self.x=self.sprite.x
                else:
                    self.sprite.x=self.x
                self.y=self.y + dt * self.y_speed*sin(pi/2 - radians(self.rotation))
                if self.y + self.rozmer>=window.height or self.y - self.rozmer<=0:
                    self.y= self.sprite.y
                else:
                    self.sprite.y=self.y
                    
            elif sym==key.DOWN:
                self.x_speed=200
                self.y_speed=200
                self.x=self.x + dt * self.x_speed* (-cos(pi/2 - radians(self.rotation)))
                if self.x +self.rozmer>=window.width or self.x - self.rozmer<=0:
                    self.x=self.sprite.x
                else:
                    self.sprite.x=self.x
                self.y=self.y + dt * self.y_speed*(-sin(pi/2 - radians(self.rotation)))
                if self.y + self.rozmer>=window.height or self.y - self.rozmer<=0:
                    self.y= self.sprite.y
                else:
                    self.sprite.y=self.y  
        self.sprite.rotation=self.rotation            
                
ship=Spaceship()                        
pyglet.clock.schedule_interval(ship.tick, 1 / 30)

@window.event
def on_draw():
    window.clear()
    batch.draw()

@window.event
def on_key_press(sym,mod):
    global klavesy
    klavesy.add(sym)
    
@window.event
def on_key_release(sym, mod):
    global klavesy
    klavesy.remove(sym)

pyglet.app.run()