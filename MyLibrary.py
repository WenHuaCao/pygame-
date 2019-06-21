# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# MyLibrary.py
dict_ = {(0,0):0,(-1, 0): 3, (1, 0): 0, (0, 1): 2, (0, -1): 1, (-1, 1): 2, (-1, -1): 1, (1, -1): 1, (1, 1): 2};
import sys, time, random, math, pygame
from pygame.locals import *
import random
class MySprite(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #extend the base Sprite class
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.direction = list([0,0])
        self.velocity = Point(0.0,0.0) 
        self.moving = False
        self.state = None
        self.tag = None
    #X property
    def _getx(self): return self.rect.x
    def _setx(self,value): self.rect.x = value
    X = property(_getx,_setx)

    #Y property
    def _gety(self): return self.rect.y
    def _sety(self,value): self.rect.y = value
    Y = property(_gety,_sety)

    #position property
    def _getpos(self): return self.rect.topleft
    def _setpos(self,pos): self.rect.topleft = pos
    position = property(_getpos,_setpos)
        

    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0,0,width,height)
        self.columns = columns
        #try to auto-calculate total frames
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate=30):
        #update animation frame number
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        #build current frame only if it changed
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

    def __str__(self):
        return str(self.frame) + "," + str(self.first_frame) + \
               "," + str(self.last_frame) + "," + str(self.frame_width) + \
               "," + str(self.frame_height) + "," + str(self.columns) + \
               "," + str(self.rect)
class Point(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    #X property
    def getx(self): return self.__x
    def setx(self, x): self.__x = x
    x = property(getx, setx)

    #Y property
    def gety(self): return self.__y
    def sety(self, y): self.__y = y
    y = property(gety, sety)

    def __str__(self):
        return "{X:" + "{:.0f}".format(self.__x) + \
            ",Y:" + "{:.0f}".format(self.__y) + "}"


class robot(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #extend the base Sprite class
        self.master_image = None
        self.frame = 0
        self.goal  = None
        self.old_frame = -1
        self.ball = None
        self.leader = None
        self.frame_width = 1
        self.frame_height = 1
        self.goal_pos = None
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.direction = list([0,0])
        self.speed = 3
        self.moving = False
        self.state = "chase"
        self.tag = None
        self.other_group = None
    #X property
    def _getx(self): return self.rect.x
    def _setx(self,value): self.rect.x = value
    X = property(_getx,_setx)

    #Y property
    def _gety(self): return self.rect.y
    def _sety(self,value): self.rect.y = value
    Y = property(_gety,_sety)

    #position property
    def _getpos(self): return self.rect.topleft
    def _setpos(self,pos): self.rect.topleft = pos
    position = property(_getpos,_setpos)
        

    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0,0,width,height)
        self.columns = columns
        #try to auto-calculate total frames
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate=30):
        #update animation frame number
        # print("tag :"+str(self.tag))
        # print(self.direction)
        # print(self.speed)
        self.behavior()
        if self.state == "back":
            self.state ="chase"
        if self.direction == [0,0]:
            self.still()
            return
        self.which_frame()
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        #build current frame only if it changed
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

    def __str__(self):
        return str(self.frame) + "," + str(self.first_frame) + \
               "," + str(self.last_frame) + "," + str(self.frame_width) + \
               "," + str(self.frame_height) + "," + str(self.columns) + \
               "," + str(self.rect)
    def still(self):
        self.frame= self.last_frame = self.first_frame 
    def chase(self):
        self.direction = [self.ball.Y - self.Y ,self.ball.X- self.X]
    def catch(self):
        t = self.detected()
        if t == 2:
            self.direction = [self.goal[1] -self.Y+random.randint(-10,10),self.goal[0]- self.X+random.randint(-10,10)]
            self.ball.kick_off()
            self.state = "chase"
        elif t == 1:
            self.direction = [self.leader.Y -self.Y+random.randint(-10,10),self.leader.X - self.X +random.randint(-10,10)]
            self.ball.kick_off()
            self.state = "chase"
        else:
            self.direction = [self.goal_pos[1] -self.Y,self.goal_pos[0]- self.X]
    #     if detected() == 1:
    #         kick_off()
    # def kick_off(self):
    #     if random.randint(1,10) < 5:
    #         self.direction = [self.leader.Y -self.Y,self.leader.X - self.X ]
    #     self.ball.kick_off(self)
    #     self.state = "chase"
    def distant(self,p):
        return ((self.X - p.X)**2 + (self.Y - p.Y)**2)**(1/2)
    def detected(self):
        if self.X < 400 and self.tag  == 2 and self.X > 100:
            return 2;
        if self.X > 780 and self.tag == 1 and self.X < 1100:
            return 2
        for x in self.other_group:
            if self.distant(x) < 100:
                return 1;
        return 3;
    def which_frame(self):
        which_column = dict_[tuple(self.direction)]
        self.first_frame = which_column * self.columns
        self.last_frame = self.first_frame + self.columns - 1
        if self.frame < self.first_frame:
            self.frame = self.first_frame
    def run(self):
        if self.direction == [0,0]:
            return
        if self.X >=0 and self.X < 70 and self.Y >=260 and self.Y <265:
            if self.direction[0] == 1:
                self.direction[0] = 0
            if self.ball.Y >400:
                self.direction[1] = 1;
        if self.X >= 70 and self.X < 75 and self.Y >=260 and self.Y <265:
            if self.direction == [1,-1]:
                if self.ball.Y > 400:
                    self.direction = [1,0]
                else:
                    self.direction = [0,-1]
        if self.X >70 and self.X <75 and self.Y >=265 and self.Y <492:
            if self.direction[1] == -1:
                self.direction[1] =0
        if self.X >= 70 and self.X < 75 and self.Y >=492 and self.Y <497:
            if self.direction == [-1,-1]:
                if self.ball.Y > 400:
                    self.direction = [0,-1]
                else: self.direction = [-1,0]
        if self.X >=0  and self.X < 70 and self.Y >=492 and self.Y <497:
            if self.direction[0] == -1:
                self.direction[0] = 0
                if self.ball.Y<400:
                    self.direction[1] = 1;
        


        if self.X >=1080 and self.X <= 1200 and self.Y >=260 and self.Y <265:
            if self.direction[0] == 1:
                self.direction[0] = 0
            if self.ball.Y >400:
                self.direction[1] = -1;
        if self.X > 1075 and self.X <= 1080 and self.Y >=260 and self.Y <265:
            if self.direction == [1,1]:
                if self.ball.Y > 400:
                    self.direction = [1,0]
                else:
                    self.direction = [0,1]
        if self.X > 1075 and self.X <= 1080 and self.Y >=265 and self.Y <  498:
            if self.direction[1] == 1:
                self.direction[1] =0
        if self.X > 1075 and self.X<= 1080 and self.Y >=498 and self.Y <502:
            if self.direction == [-1,1]:
                if self.ball.Y > 400:
                    self.direction = [0,1]
                else: self.direction = [-1,0]
        if self.X >=1080 and self.X <= 1200 and self.Y >=498 and self.Y <502:
            if self.direction[0] == -1:
                self.direction[0] = 0
                if self.ball.Y<400:
                    self.direction[1] = -1;
        self.Y += self.direction[0]*self.speed
        self.X += self.direction[1]*self.speed
        # print(str(self.X)+"   "+str(self.Y))
    def back(self):
        self.direction = [0,600 - self.X]
    def behavior(self):
        if self.state =="back":
            self.back()
        elif self.state == "chase":
            self.chase()
        elif self.state == "catch":
            self.catch()
        if self.direction[0]>0:
            self.direction[0]=1
        elif self.direction[0]<0:
            self.direction[0] = -1
        if self.direction[1]>0:
            self.direction[1] =1
        elif self.direction[1]<0:
            self.direction[1] =-1
        # print(self.tag)
        # print(self.direction)
        self.ch_sp()
        self.run()
    def ch_sp(self):
        if self.tag == 1:
            if self.X <600:
                self.speed = 2
            else:self.speed = 1
        else:
            if self.X > 600:
                self.speed = 2
            else :
                self.speed =1
class robot_B(robot):
    def __init__(self):
        robot.__init__(self)
        self.wonder = None
        self.speed =1
    def wondering(self):
        if self.X > self.wonder+1 or self.X <self.wonder -1 :
            self.direction = [560-self.Y,self.wonder- self.X]
        elif self.Y <280:
            self.direction = [560-self.Y,0]
        elif self.Y > 550:
            self.direction = [270-self.Y,0]
    def behavior(self):
        if self.state =="back":
            self.back()
        elif (self.ball.X > 600 and self.tag == 1) or (self.ball.X < 600 and self.tag == 2):
            self.wondering()
        else:
            if self.state == "chase":
                self.chase()
            elif self.state == "catch":
                self.catch()
        if self.direction[0]>0:
            self.direction[0]=1
        elif self.direction[0]<0:
            self.direction[0] = -1
        if self.direction[1]>0:
            self.direction[1] =1
        elif self.direction[1]<0:
            self.direction[1] =-1
        self.run()
    def catch(self):
        if random.randint(1,10)<5:
            self.direction = [self.goal[1] -self.Y,self.goal[0]- self.X]
            self.ball.kick_off()
            self.state = "chase"
        else:
            self.direction = [self.leader.Y -self.Y,self.leader.X - self.X ]
            self.ball.kick_off()
            self.state = "chase"


class defence(robot):
    def __init__(self):
        robot.__init__(self)
        self.wonder = None
        self.speed = 2
        self.shoot = False
        self.delay = 0
        self.direction= [1,0]
    def wondering(self):
        self.speed = 1
        if self.X != self.wonder:
            self.direction = [390-self.Y,self.wonder- self.X]
        if self.Y <305:
            self.direction = [460-self.Y,self.wonder- self.X]
        elif self.Y > 459:
            self.direction = [306-self.Y,self.wonder- self.X]
    def df(self):
        if self.shoot == True:
            self.speed = 0
            self.direction = [0,1]
            return 
        self.speed = 3
        self.direction[0] = self.ball.Y - self.Y
        if self.Y <=305:
            self.direction[0] = 1
        if self.Y >= 459 :
            self.direction[0] = -1
        self.direction[1] = 0
    def start_shoot(self):
        self.direction = [random.randint(-1,1),1]
        self.ball.kick_off()
        self.shoot = False
        self.delay = 0
    def behavior(self):
        if self.shoot == True:
            self.delay += 1
        self.direction = list(self.direction)
        if self.ball.X <310 and self.ball.Y >150 and self.ball.Y <649 and self.delay <=30:
            self.df()
        elif self.ball.X <310 and self.ball.Y >150 and self.ball.Y <649 and self.delay>30:
            self.start_shoot()
        else:
            self.wondering()
        if self.direction[0]>0:
            self.direction[0] =1
        elif self.direction[0]<0:
            self.direction[0] = -1
        if self.direction[1]>0:
            self.direction[1] =1
        elif self.direction[1]<0:
            self.direction[1] =-1
        self.run()
class defence2(robot):
    def __init__(self):
        robot.__init__(self)
        self.wonder = None
        self.speed = 2
        self.shoot = False
        self.delay = 0
        self.direction= [1,0]
    def wondering(self):
        self.speed = 1
        if self.X != self.wonder:
            self.direction = [390-self.Y,self.wonder- self.X]
        if self.Y <305:
            self.direction = [460-self.Y,self.wonder- self.X]
        elif self.Y > 459:
            self.direction = [306-self.Y,self.wonder- self.X]
    def df(self):
        if self.shoot == True:
            self.speed = 0
            self.direction = [0,-1]
            return 
        self.speed = 3
        self.direction[0] = self.ball.Y - self.Y
        if self.Y <=305:
            self.direction[0] = 1
        if self.Y >= 459 :
            self.direction[0] = -1
        self.direction[1] = 0
    def start_shoot(self):
        self.direction = [random.randint(-1,1),-1]
        self.ball.kick_off()
        self.shoot = False
        self.delay = 0
    def behavior(self):
        if self.shoot == True:
            self.delay += 1
        self.direction = list(self.direction)
        if self.ball.X >930 and self.ball.Y >150 and self.ball.Y <649 and self.delay <=30:
            self.df()
        elif self.ball.X >930 and self.ball.Y >150 and self.ball.Y <649 and self.delay>30:
            self.start_shoot()
        else:
            self.wondering()
        if self.direction[0]>0:
            self.direction[0] =1
        elif self.direction[0]<0:
            self.direction[0] = -1
        if self.direction[1]>0:
            self.direction[1] =1
        elif self.direction[1]<0:
            self.direction[1] =-1
        self.run()
