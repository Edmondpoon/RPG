import pygame
def Spawn(mobs, new_spawn):
    for mob in mobs:
        #checks if the new spawn will be on top of another mob
        #must check whether mob is a wizard or tank since they are different sizes
        if pygame.sprite.collide_rect(mob, new_spawn):
            return True
    return False

def movement(mobs, mover):
    for mob in mobs:
        if pygame.sprite.collide_rect(mob, mover):
            return [True, mob]
    return [False, None]
