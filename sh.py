import pygame
import random

pygame.init()
pygame.display.set_caption('SecretHitler Game Simulator')
icon = pygame.image.load('imgs\icon-mini.png')
pygame.display.set_icon(icon)

SCREENSIZE = {
    "w": 800,
    "h": 500
}

IMGS = {}
FONTS = {}

class Player:
    def __init__(self, id_, sex, age, stealth, eloquence, luck, smart):
        self.id = id_
        self.sex = sex
        self.age = age
        self.stealth = stealth
        self.eloquence = eloquence
        self.luck = luck
        self.smart = smart
    
    def getInfo(self):
        return self

class Liberal(Player):
    def __init__(self, id_, sex, age, stealth, eloquence, luck, smart):
        super().__init__(id_, sex, age, stealth, eloquence, luck, smart)
        self.img = IMGS["ROLE-MINI-LIBIRAL"]

class Fascist(Player):
    def __init__(self, id_, sex, age, stealth, eloquence, luck, smart):
        super().__init__(id_, sex, age, stealth, eloquence, luck, smart)
        self.img = IMGS["ROLE-MINI-FASCIST"]

class Hitler(Player):
    def __init__(self, id_, sex, age, stealth, eloquence, luck, smart):
        super().__init__(id_, sex, age, stealth, eloquence, luck, smart)
        self.img = IMGS["ROLE-MINI-HITLER"]

class Game():
    def __init__(self):
        self.players = []
    
    def addPlayer(self, player):
        self.players.append(player)
    
    def getId(self):
        return len(self.players) + 1
    
    def getPlayers(self):
        return self.players

def newPlayerInfo():
    return [random.choice([1, 2]), random.randint(14, 45), random.randint(10, 100), random.randint(10, 100), random.randint(10, 100), random.randint(10, 100)]

def start():
    newGame = Game()
    num_players = random.randint(6, 13)
    print(num_players)

    roles = {
        "liberal": 0,
        "fascist": 0,
        "hitler": 1
    }

    if num_players == 6:
        roles["liberal"] = 4
        roles["fascist"] = 1
    elif num_players == 7:
        roles["liberal"] = 4
        roles["fascist"] = 2
    elif num_players == 8:
        roles["liberal"] = 5
        roles["fascist"] = 2
    elif num_players == 9:
        roles["liberal"] = 5
        roles["fascist"] = 3
    elif num_players == 10:
        roles["liberal"] = 6
        roles["fascist"] = 3
    elif num_players == 11:
        roles["liberal"] = 6
        roles["fascist"] = 4
    elif num_players == 12:
        roles["liberal"] = 7
        roles["fascist"] = 4
    
    rolesList = ["liberal", "fascist", "hitler"]

    playerRole = random.choice(rolesList)
    while roles["liberal"] >= 1 or roles["fascist"] >= 1 or roles["hitler"] >= 1:
        if roles[playerRole] >= 1:
            newPlayer = newPlayerInfo()
            roles[playerRole] -= 1
            if playerRole == "liberal":
                thePlayer = Liberal(newGame.getId(), newPlayer[0], newPlayer[1], newPlayer[2], newPlayer[3], newPlayer[4], newPlayer[5])
            elif playerRole == "fascist":
                thePlayer = Fascist(newGame.getId(), newPlayer[0], newPlayer[1], newPlayer[2], newPlayer[3], newPlayer[4], newPlayer[5])
            elif playerRole == "hitler":
                thePlayer = Hitler(newGame.getId(), newPlayer[0], newPlayer[1], newPlayer[2], newPlayer[3], newPlayer[4], newPlayer[5])
            newGame.addPlayer(thePlayer)
        else:
            rolesList.remove(playerRole)
        playerRole = random.choice(rolesList)


    screen = pygame.display.set_mode((1280, 752))
    screen.fill((255, 255, 255))
    screen.blit(IMGS["TABLE"], (0, 0))

    for i in range(len(newGame.getPlayers())):
        screen.blit(FONTS["GAME-ORIGINAL"].render('PLAYER', True, (53, 54, 49)), (60, 20 + 60*i))
        screen.blit(FONTS["GAME-ORIGINAL-NUM"].render(str(newGame.getPlayers()[i].getInfo().id), True, (53, 54, 49)), (145, 15 + 60*i))
        screen.blit(newGame.getPlayers()[i].getInfo().img, (184, 14 + 60*i))
    
    while True:
        pygame.display.update()
        for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    print("Closed")

def main():
    screen = pygame.display.set_mode((SCREENSIZE["w"], SCREENSIZE["h"]))
    screen.fill((255, 255, 255))

    logo = {
        "LOGOIMG": pygame.image.load('imgs\logo.png'),
        "x": int(SCREENSIZE["w"] / 2 - 268/2),
        "y": int(SCREENSIZE["h"] / 2 - 200/2)
    }

    image = logo["LOGOIMG"]

    for i in range(256):
        image.set_alpha(i)
        screen.fill((255, 255, 255))
        screen.blit(image, (logo["x"], logo["y"]))
        pygame.display.flip()
        pygame.time.delay(10)

    IMGS["PLAY"] = pygame.image.load('imgs\play.png')
    IMGS["EXIT"] = pygame.image.load('imgs\exit.png')
    IMGS["MENU-BG"] = pygame.image.load('imgs\menu-bg.png')
    IMGS["ROLE-MINI-LIBIRAL"] = pygame.transform.smoothscale(pygame.image.load('imgs\\role-mini-liberal.png'), (47, 47))
    IMGS["ROLE-MINI-FASCIST"] = pygame.transform.smoothscale(pygame.image.load('imgs\\role-mini-fascist.png'), (47, 47))
    IMGS["ROLE-MINI-HITLER"] = pygame.transform.smoothscale(pygame.image.load('imgs\\role-mini-hitler.png'), (47, 47))
    IMGS["TABLE"] = pygame.image.load('imgs\\table.png')
    FONTS["MENU"] = pygame.font.Font("files\\font.ttf", 34)
    FONTS["GAME-ORIGINAL"] = pygame.font.Font("files\\font.ttf", 24)
    FONTS["GAME-ORIGINAL-NUM"] = pygame.font.Font("files\\font.ttf", 30)

    for i in reversed(range(256)):
        image.set_alpha(i)
        screen.fill((255, 255, 255))
        screen.blit(image, (logo["x"], logo["y"]))
        pygame.display.flip()
        pygame.time.delay(4)

    while True:
        a = "NONE"
        screen.blit(IMGS["MENU-BG"], (0, 0))
        screen.blit(FONTS["MENU"].render('Start', True, (53, 54, 49)), (int(SCREENSIZE["w"]/4 - 34), int(SCREENSIZE["h"]/2 + 22)))
        screen.blit(FONTS["MENU"].render('Exit', True, (53, 54, 49)), (int(SCREENSIZE["w"] * 0.75 - 26), int(SCREENSIZE["h"]/2 + 22)))
        screen.blit(IMGS["PLAY"], (int(SCREENSIZE["w"]/4 - 50), int(SCREENSIZE["h"]/2 - 80)))
        screen.blit(IMGS["EXIT"], (int(SCREENSIZE["w"] * 0.75 - 50), int(SCREENSIZE["h"]/2 - 80)))

        if IMGS["PLAY"].get_rect().move(int(SCREENSIZE["w"]/4 - 50), int(SCREENSIZE["h"]/2 - 80)).collidepoint(pygame.mouse.get_pos()):
            screen.blit(pygame.transform.smoothscale(IMGS["PLAY"], (106, 106)), (int(SCREENSIZE["w"]/4 - 53), int(SCREENSIZE["h"]/2 - 83)))
            a = "PLAY"
        elif IMGS["EXIT"].get_rect().move(int(SCREENSIZE["w"] * 0.75 - 50), int(SCREENSIZE["h"]/2 - 80)).collidepoint(pygame.mouse.get_pos()):
            screen.blit(pygame.transform.smoothscale(IMGS["EXIT"], (106, 106)), (int(SCREENSIZE["w"] * 0.75 - 53), int(SCREENSIZE["h"]/2 - 83)))
            a = "EXIT"

        pygame.display.update()

        for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    print("Closed")
                elif a != "NONE":
                    if e.type == pygame.MOUSEBUTTONUP:
                        if a == "EXIT":
                            pygame.quit()
                            quit()
                        elif a == "PLAY":
                            start()

main()