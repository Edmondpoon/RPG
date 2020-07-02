import os
import images
import collision 
import pygame
import random
import time

pygame.init()
window = pygame.display.set_mode((500, 500))
sprites_list = pygame.sprite.Group()

BORDER       = False
WALL_REMOVED = False
WIDTH        = 15
HEIGHT       = 15
VEL          = 5

#creates a wizard mob
def wizard(mobs, player, mob_dict):
    mob      = images.mob("T", WIDTH, HEIGHT)
    entities = mobs[:]
    entities.append(player)
    mob.rect.x          = random.randint(38, 433)
    mob.rect.y          = random.randint(38, 417)
    FLAG          = collision.Spawn(entities, mob)
    while FLAG == False:
        mob.rect.x = random.randint(38, 433)
        mob.rect.y = random.randint(38, 417)
        FLAG = collision.Spawn(entities, mob)
    mobs.append(mob)
    return mob

#creates a tank mob
def tank(mobs, player): 
    mob      = images.mob("T", WIDTH, HEIGHT)
    entities = mobs[:]
    entities.append(player)
    mob.rect.x          = random.randint(38, 433)
    mob.rect.y          = random.randint(38, 417)
    FLAG          = collision.Spawn(entities, mob)
    while FLAG == False: 
        mob.rect.x = random.randint(38, 433)
        mob.rect.y = random.randint(38, 417)
        FLAG = collision.Spawn(entities, mob)

    mobs.append(mob)
    return mob

#spawns a random amount of wizards and tanks
def spawn_mobs(mobs, player, sprites_list, mob_dict):
    num_mobs = random.randint(5, 10)
    for mob in range(num_mobs):
        spawn = random.random()
        if spawn  <= 0.4:
            sprites_list.add(wizard(mobs, player, mob_dict))
        elif spawn < 1.0:
            sprites_list.add(tank(mobs, player))

#creates a player sprite
def player():
    POSx = random.randint(38, 433)
    POSy = random.randint(38, 417)
    return images.tree(WIDTH, HEIGHT, POSx, POSy)

#generates wall
def generate_wall(sprites_list, BORDER):
    left_wall   = images.side_wall(40, 10000, 0, 0)
    right_wall  = images.side_wall(40, 500, 460, 0)
    top_wall    = images.top_wall(500, 40, 0, 0)
    bottom_wall = images.top_wall(40, 500, 0, 460)
    for wall in [left_wall, right_wall, top_wall, bottom_wall]:
        sprites_list.add(wall)
    BORDER = True

#removes wall sprites from sprites list
def remove_wall(sprites_list, WALL_REMOVED):
    left_wall   = images.side_wall(40, 10000, 0, 0)
    right_wall  = images.side_wall(40, 500, 460, 0)
    top_wall    = images.top_wall(500, 40, 0, 0)
    bottom_wall = images.top_wall(40, 500, 0, 460)
    for wall in [left_wall, right_wall, top_wall, bottom_wall]:
        sprites_list.remove(wall)   
    WALL_REMOVED = True

#creates the map
def map(window, sprites_list, BORDER, WALL_REMOVED):
    window.fill((255, 255, 255))
    if BORDER == False:
        generate_wall(sprites_list, BORDER)
    sprites_list.draw(window)
    if WALL_REMOVED == False:
        remove_wall(sprites_list, WALL_REMOVED)
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
        if keys[pygame.K_RIGHT]:
            p1.move_right(VEL)
        if keys[pygame.K_UP]:
            p1.move_up(VEL)
        if keys[pygame.K_DOWN]:
            p1.move_down(VEL)

        if WAVES != 0 and mobs == []:
            WAVES -= 1
            spawn_mobs(mobs, p1, sprites_list, mob_dict)
        #else:
            #for mob in mobs:
                #mob.move(VEL)

        sprites_list.update()
        map(window, sprites_list, BORDER, WALL_REMOVED)
        clock.tick(60)

    pygame.quit()
clock=pygame.time.Clock()
play()
