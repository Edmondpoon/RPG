import pygame
def Spawn(mobs, new_spawn):
    for mob in mobs:
        #checks if the new spawn will be on top of another mob
        if pygame.sprite.collide_rect(mob, new_spawn):
            return True
    return False

def movement(mobs, mover):
    #checks if mob/player with come into contact with another sprite
    for mob in mobs:
        if pygame.sprite.collide_rect(mob, mover):
            return [True, mob]
    return [False, None]

def attack_movement(mobs, attack):
    #checks if attack comes into contact with mobs
    for mob in mobs:
        if pygame.sprite.collide_rect(mob, attack):
            return [True, mob]
    return [False, None]
