import os
import images
import collision 
import pygame
import random
import time

pygame.init()
window = pygame.display.set_mode((500, 500))
sprites_list = pygame.sprite.Group()

WALL   = 0
WIDTH  = 15
HEIGHT = 15
VEL    = 1

def wizard(mobs, player, mob_dict):
    entities = mobs[:]
    entities.append(player)
    POSx          = random.randint(38, 433)
    POSy          = random.randint(38, 417)
    FLAG          = collision.Spawn(entities, POSx, POSy)
    while FLAG == False: 
        POSx = random.randint(38, 433)
        POSy = random.randint(38, 417)
        FLAG = collision.Spawn(entities, POSx, POSy)
    mob      = images.mob("W", WIDTH, HEIGHT, POSx, POSy)
    mobs.append(mob)
    return mob

def tank(mobs, player): 
    entities = mobs[:]
    entities.append(player)
    POSx          = random.randint(38, 433)
    POSy          = random.randint(38, 417)
    FLAG          = collision.Spawn(entities, POSx, POSy)
    while FLAG == False: 
        POSx = random.randint(38, 433)
        POSy = random.randint(38, 417)
        FLAG = collision.Spawn(entities, POSx, POSy)
    mob      = images.mob("T", WIDTH, HEIGHT, POSx, POSy)
    mobs.append(mob)
    return mob



def spawn_mobs(mobs, player, sprites_list, mob_dict):
    num_mobs = random.randint(5, 10)
    for mob in range(num_mobs):
        spawn = random.random()
        if spawn  <= 0.4:
            sprites_list.add(wizard(mobs, player, mob_dict))
        elif spawn < 1.0:
            sprites_list.add(tank(mobs, player))

def player():
    POSx = random.randint(38, 433)
    POSy = random.randint(38, 417)
    return images.tree(WIDTH, HEIGHT, POSx, POSy)

def map(window, sprites_list, num_wall):
    window.fill((255, 255, 255))
    if num_wall == 0:
        left_wall = images.side_wall(40, 10000, 0, 0)
        right_wall = images.side_wall(40, 500, 460, 0)
        top_wall = images.top_wall(500, 40, 0, 0)
        bottom_wall = images.top_wall(40, 500, 0, 460)
        for wall in [left_wall, right_wall, top_wall, bottom_wall]:
            sprites_list.add(wall)
        num_wall += 1
    sprites_list.draw(window)
    for wall in [left_wall, right_wall, top_wall, bottom_wall]:
        sprites_list.remove(wall)   
    pygame.display.flip()

def play():
    mob_dict = {}
    WAVES  = 3
    mobs = []
    run  = True
    p1   = player()
    sprites_list.add(p1)
    while run:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            p1.move_left(VEL)           
            print(p1.rect.x, p1.rect.y)
        if keys[pygame.K_RIGHT]:
            p1.move_right(VEL)
            print(p1.rect.x, p1.rect.y)
        if keys[pygame.K_UP]:
            p1.move_up(VEL)
            print(p1.rect.x, p1.rect.y)
        if keys[pygame.K_DOWN]:
            p1.move_down(VEL)
            print(p1.rect.x, p1.rect.y)

        if WAVES != 0 and mobs == []:
            WAVES -= 1
            spawn_mobs(mobs, p1, sprites_list, mob_dict)
        #else:
            #for mob in mobs:
                #mob.move(VEL)

        sprites_list.update()
        map(window, sprites_list, WALL)
        clock.tick(60)

    pygame.quit()
clock=pygame.time.Clock()
play()
