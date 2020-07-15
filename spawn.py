import pygame
import random
import collision
import images

WIDTH  = 15
HEIGHT = 15

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
