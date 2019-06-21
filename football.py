# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys, time, random, math, pygame
from pygame.locals import *
from math import pow
class ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_list = []
        self.image = None
        self.frame = 0
        self.old_frame = 0
        self.first_frame = 0
        self.last_frame = 2
        self.direction = list([0,0])
        self.speed = 0;
        self.fetch = False;
        self.f = 1.7
        self.last_time = 0;
        self.player = None
        self.cal = 0
    def _getx(self): return self.rect.x
    def _setx(self,value):self.rect.x = value
    X = property(_getx,_setx)

    #Y property
    def _gety(self):return self.rect.y
    def _sety(self,value):self.rect.y = value
    Y = property(_gety,_sety)

    #position property
    def _getpos(self): return self.rect.topleft
    def _setpos(self,pos): self.rect.topleft = pos
    position = property(_getpos,_setpos)
    def load(self):
        filename = 'ball1.png','ball2.png','ball3.png'
        for x in filename:
        	ball = pygame.image.load(x).convert_alpha()
        	self.image_list.append(ball)
        self.frame = 0;
        self.old_frame = 2;
        self.image = self.image_list[0];
        self.frame_height = self.image_list[0].get_rect().height
        self.frame_width = self.image_list[0].get_rect().width
        self.rect = Rect(0,0,self.frame_width,self.frame_height);
    def update(self,current_time,rate =30):
        if self.fetch and self.player.moving:
            self.speed = (self.player.velocity.x **2 + self.player.velocity.y **2)**(1/2)
        if self.speed == 0 or (self.fetch and self.player.moving == False):
            return
        if current_time > self.last_time + (4-self.speed//4)*20:
        	self.frame += 1
        	self.frame %= 3
        	self.last_time = current_time
        if self.frame != self.old_frame:
        	self.image = self.image_list[self.frame]
        	self.old_frame = self.frame
        # print(self.frame)
    def run(self):
        self.speed -= self.f*0.05;
        self.speed = max(0,self.speed)
        if(self.direction==[0,0]):return;
        # print(self.direction)
        # print(self.speed)
        self.X += ((self.direction[0]*self.speed)/pow((self.direction[1]**2 + self.direction[0]**2),(1/2)))
        self.Y += ((self.direction[1]*self.speed)/pow((self.direction[0]**2 + self.direction[1]**2),(1/2)))
    def fetched(self,player_):
        self.fetch = True;
        if player_ != None:
            self.player = player_
        player = self.player
        if(player.direction[1] >0):
        	self.X = self.player.X + self.player.frame_width*3/4
        else :
        	self.X = self.player.X - self.player.frame_width/3
        self.Y = self.player.Y + self.player.frame_height -self.frame_height;
    def kick_off(self):
        self.speed = 12
        self.direction[0] = self.player.direction[1]
        self.direction[1]  =self.player.direction[0]
        self.player = None
        self.fetch =False
        self.cal = 0
    def check_bound(self,width,height):
        temp = self.X,self.Y
        if self.X < 0:
            self.X =0
            self.direction[0] = abs(self.direction[0])
        if self.Y < 0:
            self.Y = 0
            self.direction[1] = abs(self.direction[1])
        if self.X >width-34:
            self.X= width-34
            self.direction[0] = -1*abs(self.direction[0])
        if self.Y > height-14:
            self.Y = height-14;
            self.direction[1] = -1*abs(self.direction[1])
        if self.X >=0 and self.X <72 and self.Y >300 - 17 and self.Y <315 - 17:
            self.Y = 300-17
            self.direction[1] = -1*abs(self.direction[1])
        if self.X >1110 and self.X <1200 and self.Y >300 - 17 and self.Y <315 - 17:
            self.Y = 300-17
            self.direction[1] = -1*abs(self.direction[1])
        if self.X >=0 and self.X <72 and self.Y >495 and self.Y <510:
            self.Y = 510 
            self.direction[1] = -1*abs(self.direction[1])
        if self.X >1110 and self.X <1200 and self.Y >495 and self.Y <510:
            self.Y = 510
            self.direction[1] = -1*abs(self.direction[1])
        if((self.X,self.Y) != temp):
            # print(str(self.X)+" "+str(self.Y))
            # print(temp)
            self.speed *= 0.8






