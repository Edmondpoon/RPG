import pygame
import images

WIDTH      = 15
HEIGHT     = 15

def COINS(mob, TOTAL_COINS):
    #adds coins to the player total
    VALUES = {"10": 2, "25" : 1, "100": 10, "75" : 10, "150" : 10}
    TOTAL_COINS += VALUES[str(mob.maxhp)]
    return TOTAL_COINS

def generate_store(window, store_font):
    #generates the store
    attacks    = []
    PLACEMENTS = [(27, 100), (157, 100), (287, 100), (417, 100), (547, 100), (36, 60), (38, 190), (325, 60), (325, 190)]
    for attack in range(9):
        attacks.append(images.store_attacks(WIDTH, HEIGHT, PLACEMENTS[attack][0], PLACEMENTS[attack][1], attack))
    return attacks

def maintain_store(window, sprites_list, FONTS):
    #maintains the attacks store
    COSTS_FONT, MENU_FONT, PURCHASE_FONT = FONTS
    PRICES            = [10, 25, 50, 100, 500]
    DAMAGES           = [2, 5, 7, 10, 15]
    PLACEMENTS        = [23, 153, 283, 413, 543]
    BUTTON_PLACEMENTS = [21, 151, 281, 411, 541]
    ATTACKS           = ["attack1", "attack2", "attack3", "attack4", "attack5"]

    window.fill((255, 255, 255))
    #creates the main menu button
    MAINMENU_TEXT     = MENU_FONT.render("Main Menu", True, (0, 0, 0))
    window.blit(MAINMENU_TEXT, (15, 15))

    #shows the amount of coins the player has
    with open("coins.txt", mode = "r") as coin:
        TOTAL_COINS = coin.readlines()
        TOTAL_COINS = TOTAL_COINS[0].split(" ") 
    COINS_TEXT        = MENU_FONT.render("Total coins: " + str(TOTAL_COINS[1]), True, (0, 0, 0))
    window.blit(COINS_TEXT, (450, 15))

    #creates a button to go to the special shop
    SPECIAL_TEXT     = MENU_FONT.render("Specials", True, (0, 0, 0))
    pygame.draw.rect(window, (200, 200, 200), pygame.Rect((520, 455), (100, 35)))
    pygame.draw.polygon(window, (200, 200, 200), [(620, 455), (620, 490), (640, 472)])
    window.blit(SPECIAL_TEXT, (530, 463))

    #displays the cost and damage of each attack
    PRICES_TEXT  = {}
    DAMAGES_TEXT = {}
    for attack in range(len(ATTACKS)):
        PRICES_TEXT[ATTACKS[attack]]  = COSTS_FONT.render("Costs " + str(PRICES[attack]) + " coins", True, (0, 0, 0))    
        DAMAGES_TEXT[ATTACKS[attack]] = COSTS_FONT.render("Does " + str(DAMAGES[attack]) + " damage", True, (0, 0, 0)) 
    for attack in range(len(ATTACKS)):
        window.blit(PRICES_TEXT[ATTACKS[attack]], (PLACEMENTS[attack], 175))
        window.blit(DAMAGES_TEXT[ATTACKS[attack]], (PLACEMENTS[attack], 189))

    #creates a purchase button if attack hasnt been purchased before
    with open("purchases.txt", mode = "r+") as purchases:
        purchasable = purchases.readlines()
        purchasable = purchasable[0].split(" ")
    for attack in range(len(ATTACKS)):
        if "False" in purchasable[attack + 1]:
            pygame.draw.ellipse(window, (200, 200, 200), pygame.Rect((BUTTON_PLACEMENTS[attack], 207), (100, 25)))
            PURCHASE_TEXT = PURCHASE_FONT.render("Purchase", True, (0, 0, 0))
            window.blit(PURCHASE_TEXT, (BUTTON_PLACEMENTS[attack] + 13, 211))
        else:
            pygame.draw.ellipse(window, (0, 0, 0), pygame.Rect((BUTTON_PLACEMENTS[attack], 207), (100, 25)))

    #allows player to equip an unequipped attack
    with open("equipped.txt", mode = "r+") as equip:
        equipped = equip.readlines()
        equipped = equipped[0].split(" ")
    for attack in range(len(ATTACKS)):
        if "True" in equipped[attack + 1]:
            EQUIPPED_TEXT = PURCHASE_FONT.render("Equipped", True, (255, 255, 255))
            window.blit(EQUIPPED_TEXT, (BUTTON_PLACEMENTS[attack] + 13, 211))
        elif "False" in equipped[attack + 1]:
            EQUIP_TEXT = PURCHASE_FONT.render("Equip", True, (255, 255, 255))
            window.blit(EQUIP_TEXT, (BUTTON_PLACEMENTS[attack] + 28, 211))

    #updates screen and attacks
    sprites_list.draw(window)
    pygame.display.flip()

    if pygame.mouse.get_pressed() == (True, False, False):
        position = pygame.mouse.get_pos()
        if position[0] > 15 and position[0] < 123 and position[1] > 14 and position[1] < 32:
            #returns to main menu
            return False, "attacks", False, False
        elif position[0] > 520 and position[0] < 640 and position[1] > 455 and position[1] < 490:
            return True, "specials", None, False
        else:
            #purchases/equips attack
            for attack in range(len(ATTACKS)):
                if position[0] > BUTTON_PLACEMENTS[attack] + 1 and position[0] < BUTTON_PLACEMENTS[attack] + 98 and position[1] > 207 and position[1] < 232:
                    with open("purchases.txt", mode = "r") as purchase:
                        purchasable = purchase.readlines()
                        purchasable = purchasable[0].split(" ")
                        if PRICES[attack] <= int(TOTAL_COINS[1]) and "False" in purchasable[attack + 1]:
                            with open("coins.txt", mode = "r+") as coins:
                                COIN = coins.readlines()
                                COIN = COIN[0].split(" ")
                                temp = []
                                temp2 = ""
                                for item in range(len(COIN)):
                                    if item == 0:
                                        temp.append("PLACEHOLDER")
                                    elif item <= 2:
                                        temp.append(COIN[item])
                                temp[1] = int(temp[1]) - PRICES[attack]
                                coins.truncate(0)
                                for item in temp:
                                    temp2 += str(item) + " "
                                coins.write(temp2)
                            with open("equipped.txt", mode = "r+") as equip:
                                equipped = equip.readlines()
                                equipped = equipped[0].split(" ")
                                temp  = []
                                temp2 = ""
                                for item in equipped:
                                    temp.append(item)
                                temp[attack + 1] = "False"
                                equip.truncate(0)
                                for item in temp:
                                    temp2 += item + " "
                                equip.write(temp2)
                            with open("purchases.txt", mode = "r+") as purchases:
                                purchasable = purchases.readlines()
                                purchasable = purchasable[0].split(" ")
                                temp  = []
                                temp2 = ""
                                for item in purchasable:
                                    temp.append(item)
                                temp[attack + 1] = "True"
                                purchases.truncate(0)
                                for item in temp:
                                    temp2 += item + " "
                                purchases.write(temp2)

                        elif "True" in purchasable[attack + 1]:
                            with open("equipped.txt", mode = "r+") as equip:
                                EQUIP = equip.readlines()
                                EQUIP = EQUIP[0].split(" ")
                                if "False" in EQUIP[attack + 1] and attack < 5:
                                    temp  = []
                                    temp2 = ""
                                    for item in equipped:
                                        temp.append(item)
                                    for item in range(len(temp)):
                                        if "True" in temp[item] and item <= 5:
                                            temp[item] = "False"
                                    temp[attack + 1] = "True"
                                    equip.truncate(0)
                                    for item in temp:
                                        temp2 += item + " "
                                    equip.write(temp2)


    return True, "attacks", True, None



def maintain_store2(window, sprites_list, FONTS):
    #maintains the special store
    COSTS_FONT, MENU_FONT, PURCHASE_FONT, FONT_25 = FONTS
    PRICES              = [250, 1000, 750 , 1200]
    PRICES2             = [0, 0, 0, 0, 0, 0, 250, 1000, 750, 1200]
    BUTTON_PLACEMENTS   = [0, 0, 0, 0, 0, 0, 148, 280, 150, 280]
    COSTPLACEMENTS_Y    = [80, 80, 210, 210]
    ABILITYPLACEMENTS_Y = [98, 98, 228, 228]
    PLACEMENTS_X        = [125, 420, 125, 420]
    SPECIALS            = ["special1", "special2", "special3", "special4"]
    ABILITIES           = ["Heals hp", "Unlimited shots (5 seconds)", "Gain 15 coins", "Double damage (5 seconds)"]

    window.fill((255, 255, 255))
    #creates the main menu button
    MAINMENU_TEXT     = MENU_FONT.render("Main Menu", True, (0, 0, 0))
    window.blit(MAINMENU_TEXT, (15, 15))

    #shows the amount of coins the player has
    with open("coins.txt", mode = "r") as coin:
        TOTAL_COINS = coin.readlines()
        TOTAL_COINS = TOTAL_COINS[0].split(" ") 
    COINS_TEXT        = MENU_FONT.render("Total coins: " + str(TOTAL_COINS[1]), True, (0, 0, 0))
    window.blit(COINS_TEXT, (450, 15))

    #creates a button to go to the attack shop
    ATTACK_TEXT     = MENU_FONT.render("Attacks", True, (0, 0, 0))
    pygame.draw.rect(window, (200, 200, 200), pygame.Rect((520, 455), (100, 35)))
    pygame.draw.polygon(window, (200, 200, 200), [(620, 455), (620, 490), (640, 472)])
    window.blit(ATTACK_TEXT, (540, 463))

    #displays the cost and ability of each special move
    PRICES_TEXT  = {}
    ABILITY_TEXT = {}
    for special in range(len(SPECIALS)):
        PRICES_TEXT[SPECIALS[special]]  = FONT_25.render("Costs " + str(PRICES[special]) + " coins", True, (0, 0, 0))    
        ABILITY_TEXT[SPECIALS[special]] = FONT_25.render(ABILITIES[special], True, (0, 0, 0)) 
    for special in range(len(SPECIALS)):
        window.blit(PRICES_TEXT[SPECIALS[special]], (PLACEMENTS_X[special], COSTPLACEMENTS_Y[special]))
        window.blit(ABILITY_TEXT[SPECIALS[special]], (PLACEMENTS_X[special], ABILITYPLACEMENTS_Y[special]))

    #creates a purchase button if special move hasnt been purchased before
    with open("purchases.txt", mode = "r+") as purchases:
        purchasable = purchases.readlines()
        purchasable = purchasable[0].split(" ")
    for special in range(10):
        if special > 5:
            if "False" in purchasable[special] and special < 8:
                pygame.draw.ellipse(window, (200, 200, 200), pygame.Rect((30, BUTTON_PLACEMENTS[special]), (85, 25)))
                PURCHASE_TEXT = PURCHASE_FONT.render("Purchase", True, (0, 0, 0))
                window.blit(PURCHASE_TEXT, (38, BUTTON_PLACEMENTS[special] + 6))
            elif "False" in purchasable[special]:
                pygame.draw.ellipse(window, (200, 200, 200), pygame.Rect((323, BUTTON_PLACEMENTS[special]), (85, 25)))
                PURCHASE_TEXT = PURCHASE_FONT.render("Purchase", True, (0, 0, 0))
                window.blit(PURCHASE_TEXT, (331, BUTTON_PLACEMENTS[special] + 6))
            elif "True" in purchasable[special] and special < 8:
                pygame.draw.ellipse(window, (0, 0, 0), pygame.Rect((32, BUTTON_PLACEMENTS[special]), (85, 25)))
            else:
                pygame.draw.ellipse(window, (0, 0, 0), pygame.Rect((325, BUTTON_PLACEMENTS[special]), (85, 25)))

    #allows player to equip an unequipped special
    with open("equipped.txt", mode = "r+") as equip:
        equipped = equip.readlines()
        equipped = equipped[0].split(" ")
    for special in range(10):
        if special > 5:
            if "True" in equipped[special] and special < 8:
                EQUIPPED_TEXT = PURCHASE_FONT.render("Equipped", True, (255, 255, 255))
                window.blit(EQUIPPED_TEXT, (40, BUTTON_PLACEMENTS[special] + 6))
            elif "True" in equipped[special]:
                EQUIPPED_TEXT = PURCHASE_FONT.render("Equipped", True, (255, 255, 255))
                window.blit(EQUIPPED_TEXT, (333, BUTTON_PLACEMENTS[special] + 6))
            elif "False" in equipped[special] and special < 8:
                EQUIP_TEXT = PURCHASE_FONT.render("Equip", True, (255, 255, 255))
                window.blit(EQUIP_TEXT, (53, BUTTON_PLACEMENTS[special] + 6))
            elif "False" in equipped[special]:
                EQUIP_TEXT = PURCHASE_FONT.render("Equip", True, (255, 255, 255))
                window.blit(EQUIP_TEXT, (348, BUTTON_PLACEMENTS[special] + 6))

    #updates screen and special moves
    sprites_list.draw(window)
    pygame.display.flip()

    if pygame.mouse.get_pressed() == (True, False, False):
        position = pygame.mouse.get_pos()
        if position[0] > 15 and position[0] < 123 and position[1] > 14 and position[1] < 32:
            #returns to main menu
            return False, "attacks", False, False
        elif position[0] > 520 and position[0] < 640 and position[1] > 455 and position[1] < 490:
            return True, "attacks", False, None
        else:
            #purchases/equips special
            for special in range(len(BUTTON_PLACEMENTS)):
                if special > 5 and special < 8:
                    if position[0] > 30 and position[0] < 115 and position[1] > BUTTON_PLACEMENTS[special] and position[1] < BUTTON_PLACEMENTS[special] + 25:
                        with open("purchases.txt", mode = "r") as purchase:
                            purchasable = purchase.readlines()
                            purchasable = purchasable[0].split(" ")
                            if PRICES2[special] <= int(TOTAL_COINS[1]) and "False" in purchasable[special]:
                                with open("coins.txt", mode = "r+") as coins:
                                    COIN = coins.readlines()
                                    COIN = COIN[0].split(" ")
                                    temp = []
                                    temp2 = ""
                                    for item in range(len(COIN)):
                                        if item == 0:
                                            temp.append("PLACEHOLDER")
                                        elif item <= 2:
                                            temp.append(COIN[item])
                                    temp[1] = int(temp[1]) - PRICES2[special]
                                    coins.truncate(0)
                                    for item in temp:
                                        temp2 += str(item) + " "
                                    coins.write(temp2)
                                with open("equipped.txt", mode = "r+") as equip:
                                    equipped = equip.readlines()
                                    equipped = equipped[0].split(" ")
                                    temp  = []
                                    temp2 = ""
                                    for item in equipped:
                                        temp.append(item)
                                    temp[special] = "False"
                                    equip.truncate(0)
                                    for item in temp:
                                        temp2 += item + " "
                                    equip.write(temp2)
                                with open("purchases.txt", mode = "r+") as purchases:
                                    purchasable = purchases.readlines()
                                    purchasable = purchasable[0].split(" ")
                                    temp  = []
                                    temp2 = ""
                                    for item in purchasable:
                                        temp.append(item)
                                    temp[special] = "True"
                                    purchases.truncate(0)
                                    for item in temp:
                                        temp2 += item + " "
                                    purchases.write(temp2)

                            elif "True" in purchasable[special]:
                                with open("equipped.txt", mode = "r+") as equip:
                                    EQUIP = equip.readlines()
                                    EQUIP = EQUIP[0].split(" ")
                                    if "False" in EQUIP[special] and special > 5:
                                        temp  = []
                                        temp2 = ""
                                        for item in equipped:
                                            temp.append(item)
                                        for item in range(len(temp)):
                                            if "True" in temp[item] and item > 5:
                                                temp[item] = "False"
                                        temp[special] = "True"
                                        equip.truncate(0)
                                        for item in temp:
                                            temp2 += item + " "
                                        equip.write(temp2)
                elif special >= 8:
                    if position[0] > 323  and position[0] < 408 and position[1] > BUTTON_PLACEMENTS[special] and position[1] < BUTTON_PLACEMENTS[special] + 25:
                        with open("purchases.txt", mode = "r") as purchase:
                            purchasable = purchase.readlines()
                            purchasable = purchasable[0].split(" ")
                            if PRICES2[special] <= int(TOTAL_COINS[1]) and "False" in purchasable[special]:
                                with open("coins.txt", mode = "r+") as coins:
                                    COIN = coins.readlines()
                                    COIN = COIN[0].split(" ")
                                    temp = []
                                    temp2 = ""
                                    for item in range(len(COIN)):
                                        if item == 0:
                                            temp.append("PLACEHOLDER")
                                        elif item <= 2:
                                            temp.append(COIN[item])
                                    temp[1] = int(temp[1]) - PRICES2[special]
                                    coins.truncate(0)
                                    for item in temp:
                                        temp2 += str(item) + " "
                                    coins.write(temp2)
                                with open("equipped.txt", mode = "r+") as equip:
                                    equipped = equip.readlines()
                                    equipped = equipped[0].split(" ")
                                    temp  = []
                                    temp2 = ""
                                    for item in equipped:
                                        temp.append(item)
                                    temp[special] = "False"
                                    equip.truncate(0)
                                    for item in temp:
                                        temp2 += item + " "
                                    equip.write(temp2)
                                with open("purchases.txt", mode = "r+") as purchases:
                                    purchasable = purchases.readlines()
                                    purchasable = purchasable[0].split(" ")
                                    temp  = []
                                    temp2 = ""
                                    for item in purchasable:
                                        temp.append(item)
                                    temp[special] = "True"
                                    purchases.truncate(0)
                                    for item in temp:
                                        temp2 += item + " "
                                    purchases.write(temp2)

                            elif "True" in purchasable[special]:
                                with open("equipped.txt", mode = "r+") as equip:
                                    EQUIP = equip.readlines()
                                    EQUIP = EQUIP[0].split(" ")
                                    if "False" in EQUIP[special] and special > 5:
                                        temp  = []
                                        temp2 = ""
                                        for item in equipped:
                                            temp.append(item)
                                        for item in range(len(temp)):
                                            if "True" in temp[item] and item > 5:
                                                temp[item] = "False"
                                        temp[special] = "True"
                                        equip.truncate(0)
                                        for item in temp:
                                            temp2 += item + " "
                                        equip.write(temp2)

    return True, "specials", None, True
