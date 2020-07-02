import pygame
def Spawn(mobs, test):
    for mob in mobs:
        #checks if the new spawn will be on top of another mob
        #must check whether mob is a wizard or tank since they are different sizes

        if pygame.sprite.collide_rect(mob, test):
            return False
    return True

