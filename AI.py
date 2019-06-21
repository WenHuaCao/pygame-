# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pygame.locals import *
from MyLibrary import *
filename = 'p2.png'
filename2 = 'p1.png'
size_of_player = (32,47.5)
size_of_action = 4
size_of_playground = (1200,850)
dict_ = {(0,0):0,(-1, 0): 3, (1, 0): 0, (0, 1): 2, (0, -1): 1, (-1, 1): 2, (-1, -1): 1, (1, -1): 1, (1, 1): 2};
def player2_AI(myball,player,game_over,player_moving,Reference):
    x_bias,y_bias,X,Y = Reference
    TEMP = [0,0]
    player.direction = list(player.direction)
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]: sys.exit()
    if keys[K_UP]: TEMP[0] = -1
    if keys[K_RIGHT]: TEMP[1] = 1
    if keys[K_DOWN]: TEMP[0] = 1
    if keys[K_LEFT]: TEMP[1] = -1
    if keys[K_k] and myball.player == player: myball.kick_off()
    if ([0,0] == TEMP):
        player_moving = False
    else:
        player_moving = True
    if player_moving:
        player.direction = TEMP 
    which_column = dict_[tuple(player.direction)]
        # print(player.direction)
        # print(which_column)
    if not game_over:
    # 根据角色的不同方向，使用不同的动画帧
        player.first_frame = which_column * player.columns
        player.last_frame = player.first_frame + player.columns - 1
        if player.frame < player.first_frame:
            player.frame = player.first_frame
        # print(player.direction)
        if player.X >=0  and player.X <= 70 and player.Y >=255 and player.Y <=260:
            if player.direction[0] == 1:
                player.direction[0] = 0
        if player.X >=70 and player.X <=75 and player.Y >=260 and player.Y <=497:
            if player.direction[1] == -1:
                player.direction[1] =0
        if player.X >=0  and player.X <= 70 and player.Y >=497 and player.Y <=502:
            if player.direction[0] == -1:
                player.direction[0] = 0



        if player.X >=1080 and player.X <= 1200 and player.Y >=255 and player.Y <260:
            if player.direction[0] == 1:
                player.direction[0] = 0
        if player.X > 1075 and player.X <= 1080 and player.Y >=260 and player.Y <  503:
            if player.direction[1] == 1:
                player.direction[1] =0
        if player.X >=1080 and player.X <= 1200 and player.Y >=503 and player.Y <=507:
            if player.direction[0] == -1:
                player.direction[0] = 0
        if not player_moving:
            # 当停止按键（即人物停止移动的时候），停止更新动画帧
            player.frame = player.last_frame= player.first_frame 
            player.moving = False;
        else:
            player.moving = True;
            player.velocity.x = player.direction[1] * 2
            player.velocity.y = player.direction[0]*   2
            player.velocity.x *= 1
            player.velocity.y *= 1
        # x_bias, y_bias = bias(X, Y);
        # print(player.velocity.y)
        if player_moving:
            X += player.velocity.x
            Y += player.velocity.y
            if X < 0: X = 0
            if X > size_of_playground[0] - 48: X = size_of_playground[0] - 48
            if Y < 0: Y = 0
            if Y > size_of_playground[1] - 88: Y = size_of_playground[1] - 88
            player.X = X + x_bias
            player.Y = Y + y_bias
    # Reference = x_bias,y_bias,X,Y
    Reference[0] = x_bias
    Reference[1]= y_bias
    Reference[2] = X
    Reference[3] = Y
            
def player1_AI(myball,player,game_over,player_moving,Reference):
    x_bias,y_bias,X,Y = Reference
    TEMP = [0,0]
    player.direction = list(player.direction)
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]: sys.exit()
    if keys[K_w]: TEMP[0] = -1
    if keys[K_d]: TEMP[1] = 1
    if keys[K_s]: TEMP[0] = 1
    if keys[K_a]: TEMP[1] = -1
    if keys[K_t] and myball.player == player: myball.kick_off()
    if ([0,0] == TEMP):
        player_moving = False
    else:
        player_moving = True
    if player_moving:
        player.direction = TEMP 
    which_column = dict_[tuple(player.direction)]
        # print(player.direction)
        # print(which_column)
    if not game_over:
    # 根据角色的不同方向，使用不同的动画帧
        player.first_frame = which_column * player.columns
        player.last_frame = player.first_frame + player.columns - 1
        if player.frame < player.first_frame:
            player.frame = player.first_frame
        # print(player.direction)
        if player.X >=0  and player.X <= 70 and player.Y >=255 and player.Y <=260:
            if player.direction[0] == 1:
                player.direction[0] = 0
        if player.X >=70 and player.X <=75 and player.Y >=260 and player.Y <=497:
            if player.direction[1] == -1:
                player.direction[1] =0
        if player.X >=0  and player.X <= 70 and player.Y >=497 and player.Y <=502:
            if player.direction[0] == -1:
                player.direction[0] = 0



        if player.X >=1080 and player.X <= 1200 and player.Y >=255 and player.Y <260:
            if player.direction[0] == 1:
                player.direction[0] = 0
        if player.X > 1075 and player.X <= 1080 and player.Y >=260 and player.Y <503:
            if player.direction[1] == 1:
                player.direction[1] =0
        if player.X >=1080 and player.X <= 1200 and player.Y >=503 and player.Y <507:
            if player.direction[0] == -1:
                player.direction[0] = 0
        if not player_moving:
            # 当停止按键（即人物停止移动的时候），停止更新动画帧
            player.frame = player.first_frame = player.last_frame
            player.moving = False;
        else:
            player.moving = True;
            player.velocity.x = player.direction[1] * 2
            player.velocity.y = player.direction[0]*  2
            player.velocity.x *= 1
            player.velocity.y *= 1
        # x_bias, y_bias = bias(X, Y);
        # print(player.velocity.y)
        if player_moving:
            X += player.velocity.x
            Y += player.velocity.y
            if X < 0: X = 0
            if X > size_of_playground[0] - 48: X = size_of_playground[0] - 48
            if Y < 0: Y = 0
            if Y > size_of_playground[1] - 88: Y = size_of_playground[1] - 88
            player.X = X + x_bias
            player.Y = Y + y_bias
    # Reference = x_bias,y_bias,X,Y
    Reference[0] = x_bias
    Reference[1]= y_bias
    Reference[2] = X
    Reference[3] = Y



            