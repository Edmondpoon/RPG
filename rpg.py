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
    mob      = images.mob("W", WIDTH, HEIGHT)
    entities = mobs[:]
    entities.append(player)
    mob.rect.x          = random.randint(38, 433)
    mob.rect.y          = random.randint(38, 417)
    FLAG          = collision.Spawn(entities, mob)
    while FLAG == True:
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
    while FLAG == True: 
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
    WAVES    = 3
    mobs     = []
    attacks  = {}
    run      = True
    p1       = player()
    sprites_list.add(p1)
    while run:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            p1.move_left(VEL, p1, mobs)  
        if keys[pygame.K_RIGHT]:
            p1.move_right(VEL, p1, mobs)
        if keys[pygame.K_UP]:
            p1.move_up(VEL, p1, mobs)
        if keys[pygame.K_DOWN]:
            p1.move_down(VEL, p1, mobs)
        
        if WAVES != 0 and mobs == []:
            WAVES -= 1
            spawn_mobs(mobs, p1, sprites_list, mob_dict)
        #else:
            #for mob in mobs:
                #mob.move(VEL)

        if pygame.mouse.get_pressed() == (True, False, False):
            position = pygame.mouse.get_pos()
            attack   = images.player_attack(WIDTH, HEIGHT, p1.rect.x, p1.rect.y)
            if position[0] > p1.rect.x and position[1] > p1.rect.y:
                #fourth quadrant
                RUN   = position[0] - p1.rect.x
                RISE  = position[1] - p1.rect.y
                SLOPE = RISE / RUN
                attacks[attack] = ["quadrant4", SLOPE]
                sprites_list.add(attack)            
            elif position[0] < p1.rect.x and position[1] < p1.rect.y:
                #second quadrant
                RUN   = p1.rect.x - position[0]
                RISE  = p1.rect.y - position[1]
                SLOPE = RISE / RUN
                attacks[attack] = ["quadrant2", SLOPE]
                sprites_list.add(attack)            
            elif position[0] < p1.rect.x and position[1] > p1.rect.y:
                #third quadrant
                RUN   = p1.rect.x - position[0]
                RISE  = position[1] - p1.rect.y
                SLOPE = RISE / RUN
                attacks[attack] = ["quadrant3", SLOPE]
                sprites_list.add(attack)            
            elif position[0] > p1.rect.x and position[1] < p1.rect.y: 
                #first quadrant 
                RUN   = position[0] - p1.rect.x
                RISE  = p1.rect.y - position[1]
                SLOPE = RISE / RUN
                attacks[attack] = ["quadrant1", SLOPE]
                sprites_list.add(attack)             
            elif position[0] == p1.rect.x and posision[1] > p1.rect.y:
                #y-axis bottom
                attacks[attack] = ["verticaldown", VEL]
                sprites_list.add(attack)            
            elif position[0] == p1.rect.x and position[1] < p1.rect.y:
                #y-axis top
                attacks[attack] = ["verticalup", VEL]
                sprites_list.add(attack)            
            elif position[0] > p1.rect.x and position[1] == p1.rect.y:
                #x-axis right
                attacks[attack] = ["horizontalright", VEL]
                sprites_list.add(attack)            
            elif position[0] < p1.rect.x and position[1] == p1.rect.y:
                #x-axis left
                attacks[attack] = ["horizontalleft", VEL] 
                sprites_list.add(attack)            

        for attack in attacks.keys():
            if attacks[attack][0] == "quadrant1":
                attack.quadrant1(attacks[attack][1], mobs, attack, sprites_list)
            elif attacks[attack][0] == "quadrant2":
                attack.quadrant2(attacks[attack][1], mobs, attack, sprites_list)
            elif attacks[attack][0] == "quadrant3":
                attack.quadrant3(attacks[attack][1], mobs, attack, sprites_list)
            elif attacks[attack][0] == "quadrant4":
                attack.quadrant4(attacks[attack][1], mobs, attack, sprites_list)
            elif attacks[attack][0] == "verticaldown":
                attack.verticaldown(attacks[attack][1], mobs, attack, sprites_list)
            elif attacks[attack][0] == "verticalup":
                attack.verticalup(attacks[attack][1], mobs, attack, sprites_list)
            elif attacks[attack][0] == "horizontalright":
                attack.horizontalright(attacks[attack][1], mobs, attack, sprites_list)
            elif attacks[attack][0] == "horizontalleft":
                attack.horizontalleft(attacks[attack][1], mobs, attack, sprites_list)

        sprites_list.update()
        map(window, sprites_list, BORDER, WALL_REMOVED)
        clock.tick(60)

    pygame.quit()
clock=pygame.time.Clock()
play()
