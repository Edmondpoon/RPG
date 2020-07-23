import pygame
import spawn
import random
import collision
import images

WIDTH  = 15
HEIGHT = 15

#creates a wizard mob
def wizard(mobs, player):
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

#creates a boss mob
def boss(mobs, player):
    mob      = images.mob("boss", WIDTH, HEIGHT)
    entities = [player]
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
def spawn_mobs(mobs, player, sprites_list, WAVES):
    if WAVES % 5 != 0:
        num_mobs = random.randint(1, 6)
        for mob in range(num_mobs):
            spawn = random.random()
            if spawn  <= 0.4:
                sprites_list.add(wizard(mobs, player))
            elif spawn < 1.0:
                sprites_list.add(tank(mobs, player))
    else:
        sprites_list.add(boss(mobs, player))

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

#creates the map
def map(window, sprites_list, player_hp, mobs, VARIABLES, FONTS, COINS_EARNED, WAVES):
    BORDER, DEAD, STORE                          = VARIABLES
    WORD_FONT, HP_FONT, DEATH_FONT, OPTIONS_FONT, FONT_25 = FONTS

    if STORE == False:
        window.fill((255, 255, 255))
        #draws black sidebar
        pygame.draw.rect(window, (0, 0, 0), pygame.Rect((500, 0), (150, 500)))
        #draws the hp bar background
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect((520, 81), (110, 30)))
        WAVE_TEXT = FONT_25.render("Current wave: " + str(WAVES), True, (200, 200, 200))
        window.blit(WAVE_TEXT, (510, 20))

    #changes the length of the player hp bar depedning on the player's hp
    if int(player_hp) <= 50 and int(player_hp) > 0:
        percentage = int(player_hp) / 50
        hp_size    = int( 100 * percentage)
        pygame.draw.rect(window, (255, 0, 0), pygame.Rect((525, 86), (hp_size, 20)))

        enemy_hp_bar = WORD_FONT.render("Enemy hp", True, (255, 255, 255))
        window.blit(enemy_hp_bar, (510, 200))
        background_placements = [233, 273, 313, 353, 393, 433]
        hp_placements         = [238, 278, 318, 358, 398, 438]
        hp_value_placements   = [240, 280, 320, 360, 400, 440]
        for value in background_placements[:len(mobs)]:
            pygame.draw.rect(window, (255, 255, 255), pygame.Rect((520, value), (110, 30)))
        for mob in range(len(mobs)):
            if int(mobs[mob].hp) <= mobs[mob].maxhp and int(mobs[mob].hp) > 0:
                mob_hp = HP_FONT.render(str(mobs[mob].hp) + " / " + str(mobs[mob].maxhp), True, (200, 200, 200))
                percentage = int(mobs[mob].hp) / mobs[mob].maxhp
                hp_size    = int( 100 * percentage)
                pygame.draw.rect(window, (255, 0, 0), pygame.Rect((525, hp_placements[mob]), (hp_size, 20)))
                if int(mobs[mob].maxhp) < 100:
                    window.blit(mob_hp, (545, hp_value_placements[mob]))
                else: 
                    window.blit(mob_hp, (532, hp_value_placements[mob]))

        if int(player_hp) > 0:
            hp_bar = WORD_FONT.render("Player hp", True, (255, 255, 255))
            window.blit(hp_bar, (510, 50))
            hp = HP_FONT.render(str(player_hp) + " / 50", True, (200, 200, 200))
            window.blit(hp, (545, 88))

    elif int(player_hp) <= 0 and STORE == False:
        with open("coins.txt", mode = "r+") as coins:
            COIN  = coins.readlines()
            COIN  = COIN[0].split(" ")
            temp  = []
            temp2 = ""
            for item in range(3):
                if item == 0:
                    temp.append("PLACEHOLDER")
                else:
                    temp.append(COIN[item])
            temp[1] = int(temp[1]) + COINS_EARNED + (5 * int(WAVES))
            coins.truncate(0)
            for item in temp:
                temp2 += str(item) + " "
            coins.write(temp2)

        for sprite in sprites_list:
            sprite.kill()
        window.fill((0, 0, 0))
        ending_text     = DEATH_FONT.render("You died", True, (255, 255, 255))
        store_text      = OPTIONS_FONT.render("Store", True, (255, 255, 255))
        play_again_text = OPTIONS_FONT.render("Play again", True, (255, 255, 255))
        pygame.draw.rect(window, (0, 0, 0), pygame.Rect((274, 300), (89, 37)))
        pygame.draw.rect(window, (0, 0, 0), pygame.Rect((234, 370), (174, 37)))
        window.blit(ending_text, (175, 100))
        window.blit(store_text, (275, 300))
        window.blit(play_again_text, (235, 370))
        pygame.display.flip()
        return True, True, 0

    if BORDER == False:
        spawn.generate_wall(sprites_list, BORDER)
    sprites_list.draw(window)
    pygame.display.flip()
    return True, False, COINS_EARNED
