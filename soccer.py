# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import itertools, sys, time, random, math, pygame
from pygame.locals import *
from MyLibrary import *
from football import *
from IO import*






def bias(x, y):
    x = x + 16
    y = y + 24
    x_cent = 0
    y_cent = 0
    if (x >= 100 and x <= 700):
        x_cent = -1 * x + 100
    elif (x > 700):
        x_cent = -600
    else:
        x_cent = 0
    if (y >= 75 and y <= 525):
        y_cent = -1 * y + 75
    elif (y > 525):
        y_cent = -450
    else:
        y_cent = 0
    return x_cent, y_cent


def draw_background(screen):
    rc = (255, 255, 255)
    rp = (600, 400)
    rr = 80
    width = 5
    screen.fill((0,100,0))
    pygame.draw.circle(screen, rc, rp, rr, width)
    pygame.draw.rect(screen, (255, 255, 255), (10, 10, 600, 790), 5)
    pygame.draw.rect(screen, (255, 255, 255), (600, 10, 590, 790), 5)
    pygame.draw.rect(screen, (255, 255, 255), (10, 150, 300, 500), 5)
    pygame.draw.rect(screen, (255, 255, 255), (890, 150, 300, 500), 5)

def draw_ball_goal(screen):
    goal1 = pygame.image.load("goal1.bmp").convert()
    goal2 = pygame.image.load("goal2.bmp").convert()
    screen.blit(goal1,(8,305))
    screen.blit(goal2,(1121,305))


def begin_a_game(n1,n2):
    nn = 0
    filename = 'p2.png'
    filename2 = 'p1.png'
    size_of_player = (32,47.5)
    size_of_action = 4
    size_of_playground = (1920,1080)
    dict_ = {(-1, 0): 3, (1, 0): 0, (0, 1): 2, (0, -1): 1, (-1, 1): 3, (-1, -1): 1, (1, -1): 0, (1, 1): 2};
    x_bias = 0
    y_bias = 0
    kick_off = 0
    player_group = pygame.sprite.Group()
    player_group1 = pygame.sprite.Group()
    player_group2 = pygame.sprite.Group()
    player = MySprite()
    X, Y = random.randint(250,500),random.randint(350-25,450-25)
    # x_bias, y_bias = bias(X, Y);
    player.load(filename, size_of_player[0], size_of_player[1], size_of_action)
    player.position = X + x_bias, Y + y_bias
    player.direction = 1,0
    player.tag  =1
    player_group.add(player)
    player_group1.add(player)

    player2 = MySprite()
    X2,Y2 = random.randint(700,950),random.randint(350-25,450-25)
    player2.load(filename2, size_of_player[0], size_of_player[1], size_of_action)
    player2.position = X2 + x_bias, Y2 + y_bias
    player2.direction = 1,0
    player2.tag = 2
    player_group.add(player2)
    player_group2.add(player2)

    b_X,b_Y = 1200/2,800/2;
    ball_group = pygame.sprite.Group()
    myball = ball()
    myball.load()
    myball.position = b_X+x_bias,b_Y+y_bias
    ball_group.add(myball)

    
    p1 = robot()
    p1.leader = player
    p1.ball = myball
    p1.goal_pos = [892,399]
    p1.tag = 1
    p1.goal = [1120,405]
    p1.other_group = player_group2
    p1.load("p3.png", size_of_player[0], size_of_player[1], size_of_action)
    p1.X,p1.Y = random.randint(250,500),random.randint(50-25,350-25)
    p1.direction = 1,0
    player_group1.add(p1)
    player_group.add(p1)
    
    pp2 = robot_B()
    pp2.leader = p1
    pp2.ball = myball
    pp2.goal_pos = [892,399]
    pp2.goal = [1120,405]
    pp2.tag = 1
    pp2.wonder = 300;
    pp2.other_group = player_group2
    pp2.load("p3.png", size_of_player[0], size_of_player[1], size_of_action)
    pp2.X,pp2.Y = random.randint(250,500),random.randint(450-25,750-25)
    pp2.direction = 1,0
    player_group1.add(pp2)
    player_group.add(pp2)

    d1 = defence()
    d1.leader = player
    d1.ball = myball
    d1.wonder = 85
    d1.tag = 1
    d1.other_group = player_group2
    d1.load("p3.png", size_of_player[0], size_of_player[1], size_of_action)
    d1.X,d1.Y = 85,390
    d1.direction = 1,0
    player_group1.add(d1)
    player_group.add(d1)
    
    t = robot()
    t.leader = player2
    t.ball = myball
    t.tag = 2
    t.other_group = player_group1
    t.goal_pos = [309,389]
    t.goal = [70,405]
    t.load("p4.png", size_of_player[0], size_of_player[1], size_of_action)
    t.X,t.Y = random.randint(700,950),random.randint(50-25,350-25)
    t.direction = 1,0
    player_group2.add(t)
    player_group.add(t)
    r = t;
    t = robot_B()
    t.leader = r
    t.goal = [70,405]
    t.ball = myball
    t.wonder = 900
    t.tag = 2
    t.other_group = player_group1
    t.goal_pos = [309,389]
    t.load("p4.png", size_of_player[0], size_of_player[1], size_of_action)

    t.X,t.Y = random.randint(700,950),random.randint(450-25,750-25)
    t.direction = 1,0
    player_group2.add(t)
    player_group.add(t)

    d2 = defence2()
    d2.leader = player2
    d2.ball = myball
    d2.wonder = 1070
    d2.tag = 2
    d2.other_group = player_group1
    d2.load("p4.png", size_of_player[0], size_of_player[1], size_of_action)
    d2.X,d2.Y = 1070,390
    d2.direction = 1,0
    player_group2.add(d2)
    player_group.add(d2) 


    game_over = False
    player_moving = False
    player2_moving =False
    while True:
        timer.tick(50)
        ticks = pygame.time.get_ticks()
        myball.cal +=1;
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if nn == 0.00001:
            keys = pygame.key.get_pressed()
            if keys[K_ESCAPE]: sys.exit()
            if keys[K_SPACE]:nn+=0.00001
            continue

        nn+=0.00001
        mx, my = pygame.mouse.get_pos()
        # print(str(mx)+" "+str(my))
        # print(myball.position)
        Reference = [x_bias,y_bias,X,Y]
        player1_AI(myball,player,game_over,player_moving,Reference)
        x_bias,y_bias,X,Y = Reference
        Reference = [x_bias,y_bias,X2,Y2]
        player2_AI(myball,player2,game_over,player2_moving,Reference)
        x_bias,y_bias,X2,Y2 = Reference
        # print(d1.shoot)
        if d1.shoot == True or d2.shoot == True:
            p1.state = "back"
            pp2.state = "back"
            r.state =  "back"
            t.state =  "back"
        player_group.update(ticks, 30)
        
        if myball.cal > 10:
            the_player = None
            if myball.player == None:
                the_player = pygame.sprite.spritecollideany(myball,player_group);
                if  the_player != None:
                    if pygame.sprite.collide_circle_ratio(1)(the_player,myball):
                        myball.fetched(the_player);
                        the_player.state = "catch"
                        if the_player == d1 or the_player == d2:
                            the_player.shoot =True;
            elif myball.player.tag ==1:
                the_player = pygame.sprite.spritecollideany(myball,player_group2);
                if  the_player != None:
                    if pygame.sprite.collide_circle_ratio(1)(the_player,myball):
                        if the_player != d1 and the_player != d2:
                            myball.player.state = "chase"
                            the_player.state = "catch"
                            myball.fetched(the_player)
            elif myball.player.tag ==2:
                the_player = pygame.sprite.spritecollideany(myball,player_group1);
                if  the_player != None:
                    if pygame.sprite.collide_circle_ratio(1)(the_player,myball):
                        if the_player != d1 and the_player != d2:
                            myball.player.state = "chase"
                            the_player.state = "catch"
                            myball.fetched(the_player)

            # the_player = pygame.sprite.spritecollideany(myball,player_group);
            # if  the_player != None:
            #     if pygame.sprite.collide_circle_ratio(0.65)(the_player,myball):
            #         print("*********************************************************")
            #         if(myball.player!=None):
            #             player_group.add(myball.player);
            #             ball_group.remove(myball.player);
            #         myball.fetched(the_player);
            #         player_group.remove(the_player)
            #         ball_group.add(the_player)
        myball.check_bound(1200,800)
        if(myball.fetch):
            myball.fetched(None)
            print("kick_off")
        else: myball.run()
        # print(str(myball.X)+" "+str(myball.Y))
        ball_group.update(ticks,60)
        print(str(myball.X)+" "+str(myball.Y))
        if myball.X < 60 and myball.Y >315 - 17  and myball.Y <495:
            return 2
        elif myball.X > 1110 and myball.Y >315 - 17  and myball.Y <495:
            return 1
        draw_background(screen)
        if(myball.player!=None and myball.player.direction[0]>0):
            player_group.draw(screen)
            ball_group.draw(screen)
        else:
            ball_group.draw(screen)
            player_group.draw(screen)
        font = pygame.font.SysFont("", 150)
        text_surface = font.render(str(n1)+" : "+str(n2), True, (0, 0, 255))
        screen.blit(text_surface, (500, 10))
        draw_ball_goal(screen)
        pygame.display.update()
def myinit():
    screen = pygame.display.set_mode((769,563))
    g1 = pygame.image.load("g1.jpg").convert()
    g2 = pygame.image.load("hh.png").convert()
    t = 0
    timer = pygame.time.Clock()
    while(1):
        timer.tick(30)
        ticks = pygame.time.get_ticks();
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(g1,(0,0))
        t+= 1
        print(t)
        if t > 66:
            break;
        pygame.display.update()
    while(1):
        timer.tick(30)
        ticks = pygame.time.get_ticks();
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                mouse_up = event.button
                mouse_up_x,mouse_up_y = event.pos
                if mouse_up_x > 245 and mouse_up_x < 469 and mouse_up_y> 368 and mouse_up_y < 470:
                    return
        screen.blit(g2,(0,0))
        pygame.display.update()
    
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("简单足球")
    font = pygame.font.Font(None, 36)
    myinit()
    timer = pygame.time.Clock()
    n1 = 0
    n2 =0
    screen = pygame.display.set_mode((1200, 800))
    for x in range(10000):
        t = begin_a_game(n1,n2);
        if t == 1:
            n1 +=1
        else:
            n2 += 1

