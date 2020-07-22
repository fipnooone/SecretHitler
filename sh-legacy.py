import pygame
import random
import numpy

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
        self.dead = False
    
    def getInfo(self):
        return self

class Liberal(Player):
    def __init__(self, id_, sex, age, stealth, eloquence, luck, smart):
        super().__init__(id_, sex, age, stealth, eloquence, luck, smart)
        self.img = IMGS["ROLE-MINI-LIBIRAL"]
        self.thoughts = {}
    
    def getThoughts(self):
        return self.thoughts
    
    def changeThoughts(self, thoughts):
        self.thoughts = thoughts

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
        self.on = True
    
    def addPlayer(self, player):
        self.players.append(player)
    
    def getId(self):
        return len(self.players) + 1
    
    def getPlayers(self):
        return self.players
    
    def isOn(self):
        return self.on

def newPlayerInfo():
    return [random.choice([1, 2]), random.randint(14, 45), random.randint(10, 100), random.randint(10, 100), random.randint(10, 100), random.randint(10, 100)]

def grayscale(img):
    arr = pygame.surfarray.array3d(img)
    avgs = [[(r*0.298 + g*0.587 + b*0.114) for (r,g,b) in col] for col in arr]
    arr = numpy.array([[[avg,avg,avg] for avg in col] for col in avgs])
    return pygame.surfarray.make_surface(arr)

def start():
    newGame = Game()
    num_players = random.randint(5, 10)
    print(num_players)

    roles = {
        "liberal": 0,
        "fascist": 0,
        "hitler": 1
    }

    if num_players == 5:
        roles["liberal"] = 3
        roles["fascist"] = 1
        IMGS["TABLE"] = IMGS["TABLE-s"]
    elif num_players == 6:
        roles["liberal"] = 4
        roles["fascist"] = 1
        IMGS["TABLE"] = IMGS["TABLE-s"]
    elif num_players == 7:
        roles["liberal"] = 4
        roles["fascist"] = 2
        IMGS["TABLE"] = IMGS["TABLE-m"]
    elif num_players == 8:
        roles["liberal"] = 5
        roles["fascist"] = 2
        IMGS["TABLE"] = IMGS["TABLE-m"]
    elif num_players == 9:
        roles["liberal"] = 5
        roles["fascist"] = 3
        IMGS["TABLE"] = IMGS["TABLE-l"]
    elif num_players == 10:
        roles["liberal"] = 6
        roles["fascist"] = 3
        IMGS["TABLE"] = IMGS["TABLE-l"]
    
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

    game = True
    move = 0
    laws = ['liberal', 'liberal', 'liberal', 'liberal', 'liberal', 'liberal', 'fascist', 'fascist', 'fascist', 'fascist', 'fascist', 'fascist', 'fascist', 'fascist', 'fascist', 'fascist', 'fascist']
    dropped_laws = []
    random.shuffle(laws)
    
    while newGame.isOn():
        while True:
            clock = pygame.time.Clock()

            screen.blit(IMGS["TABLE"], (0, 0))

            screen.blit(FONTS["GAME-ORIGINAL-NUM"].render(str(move), True, (53, 54, 49)), (1050, 14))
            screen.blit(FONTS["GAME-ORIGINAL-RU"].render('Ход', True, (53, 54, 49)), (1070, 22))
            if len(laws) >= 10:
                screen.blit(FONTS["GAME-ORIGINAL-NUM-LAWS"].render(str(len(laws)), True, (80, 160, 136)), (402, 98))
            else:
                screen.blit(FONTS["GAME-ORIGINAL-NUM-LAWS"].render(str(len(laws)), True, (80, 160, 136)), (412, 98))
            
            if len(dropped_laws) >= 10:
                screen.blit(FONTS["GAME-ORIGINAL-NUM-LAWS"].render(str(len(dropped_laws)), True, (80, 160, 136)), (836, 98))
            else:
                screen.blit(FONTS["GAME-ORIGINAL-NUM-LAWS"].render(str(len(dropped_laws)), True, (80, 160, 136)), (844, 98))

            for i in range(len(newGame.getPlayers())):
                player_rect = pygame.draw.rect(screen, (255, 255, 255), (60, 8 + 60*i, 170, 59))
                color = (53, 54, 49)

                if player_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, (240, 240, 240), (55, 8 + 60*i, 180, 59))

                    screen.blit(FONTS["GAME-ORIGINAL-RU"].render('PLAYER:', True, (53, 54, 49)), (1072 + 14 * (len(str(newGame.getPlayers()[i].getInfo().id)) - 1), 22 + 40))
                    screen.blit(FONTS["GAME-ORIGINAL-NUM"].render(str(newGame.getPlayers()[i].getInfo().id), True, (53, 54, 49)), (1050, 14 + 40))
                    if newGame.getPlayers()[i].getInfo().sex == 1:
                        sex = "Муж."
                    elif newGame.getPlayers()[i].getInfo().sex == 2:
                        sex = "Жен."
                    screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Пол: ' + sex + ', Возраст: ' + str(newGame.getPlayers()[i].getInfo().age), True, (53, 54, 49)), (1055, 22 + 67))
                    if isinstance(newGame.getPlayers()[i], Liberal):
                        screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Партия: Либерал', True, (53, 54, 49)), (1055, 22 + 67 + 17))
                        screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Мысли:', True, (53, 54, 49)), (1055, 22 + 67 + 17*6 + 4))

                        for j in range(len(newGame.getPlayers()[i].getThoughts().keys())):
                            p_ = list(newGame.getPlayers()[i].getThoughts().keys())[j]
                            screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Игрок ' + str(p_.getInfo().id) + ': фашист ~' + str(newGame.getPlayers()[i].getThoughts()[p_]) + '%', True, (53, 54, 49)), (1058, 22 + 67 + 17*7 + 4 + 18*j))

                    elif isinstance(newGame.getPlayers()[i], Fascist):
                        screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Партия: Фашист', True, (53, 54, 49)), (1055, 22 + 67 + 17))
                    elif isinstance(newGame.getPlayers()[i], Hitler):
                        screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Партия: Фашист; Гитлер', True, (53, 54, 49)), (1055, 22 + 67 + 17))
                    screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Хитрость: ' + str(newGame.getPlayers()[i].getInfo().stealth), True, (53, 54, 49)), (1055, 22 + 67 + 17*2))
                    screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Красноречие: ' + str(newGame.getPlayers()[i].getInfo().eloquence), True, (53, 54, 49)), (1055, 22 + 67 + 17*3))
                    screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Удача: ' + str(newGame.getPlayers()[i].getInfo().luck), True, (53, 54, 49)), (1055, 22 + 67 + 17*4))
                    screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Понимание игры: ' + str(newGame.getPlayers()[i].getInfo().smart), True, (53, 54, 49)), (1055, 22 + 67 + 17*5))
                    if newGame.getPlayers()[i].getInfo().dead:
                        screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Мертв.', True, (53, 54, 49)), (1055, 22 + 67 + 17*5))
                

                screen.blit(FONTS["GAME-ORIGINAL"].render('PLAYER', True, color), (60, 20 + 60*i))
                screen.blit(FONTS["GAME-ORIGINAL-NUM"].render(str(newGame.getPlayers()[i].getInfo().id), True, color), (145, 15 + 60*i))

                if newGame.getPlayers()[i].getInfo().dead:
                    color = (153, 153, 153)
                    screen.blit(grayscale(newGame.getPlayers()[i].getInfo().img), (184, 14 + 60*i))
                else:
                    curr_player = newGame.getPlayers()[i]
                    screen.blit(newGame.getPlayers()[i].getInfo().img, (184, 14 + 60*i))
                    
                    if isinstance(curr_player, Liberal):
                        newThoughts = {}
                        for player_ in newGame.getPlayers():
                            if player_.getInfo().id != curr_player.getInfo().id:
                                if len(curr_player.getThoughts()) == 0:
                                    if isinstance(player_, Fascist) or isinstance(player_, Hitler):
                                        newThoughts[player_] = int((100 - player_.getInfo().stealth) - player_.getInfo().eloquence / 5 - player_.getInfo().luck / 5 - player_.getInfo().smart / 5 + curr_player.getInfo().stealth / 8 + curr_player.getInfo().luck / 6 + curr_player.getInfo().smart / 6 + random.randint(-5, 5)) 
                                    else:
                                        newThoughts[player_] = int((100 - player_.getInfo().stealth) / 5 + (100 - player_.getInfo().eloquence) / 6 + (100 - player_.getInfo().luck) / 5 + (100 - player_.getInfo().smart) / 5 - curr_player.stealth / 60 - curr_player.eloquence / 60 - curr_player.luck / 8 - curr_player.smart / 7 + random.randint(-5, 5))
                                    
                                    if newThoughts[player_] > 100:
                                        newThoughts[player_] = 100
                                    elif newThoughts[player_] < 0:
                                        newThoughts[player_] = 0
                                else:
                                    newThoughts = curr_player.getThoughts()
                        curr_player.changeThoughts(newThoughts)

            pygame.display.update()
            screen.fill((255, 255, 255))
            
            clock.tick(40)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    print("Closed")
        
        day += 1

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
        pygame.time.delay(3)

    IMGS["PLAY"] = pygame.image.load('imgs\play.png')
    IMGS["EXIT"] = pygame.image.load('imgs\exit.png')
    IMGS["MENU-BG"] = pygame.image.load('imgs\menu-bg.png')
    IMGS["ROLE-MINI-LIBIRAL"] = pygame.transform.smoothscale(pygame.image.load('imgs\\role-mini-liberal.png'), (47, 47))
    IMGS["ROLE-MINI-FASCIST"] = pygame.transform.smoothscale(pygame.image.load('imgs\\role-mini-fascist.png'), (47, 47))
    IMGS["ROLE-MINI-HITLER"] = pygame.transform.smoothscale(pygame.image.load('imgs\\role-mini-hitler.png'), (47, 47))
    IMGS["TABLE-s"] = pygame.image.load('imgs\\table-s.png')
    IMGS["TABLE-m"] = pygame.image.load('imgs\\table-m.png')
    IMGS["TABLE-l"] = pygame.image.load('imgs\\table-l.png')
    FONTS["MENU"] = pygame.font.Font("files\\font.ttf", 34)
    FONTS["GAME-ORIGINAL"] = pygame.font.Font("files\\font.ttf", 24)
    FONTS["GAME-ORIGINAL-NUM"] = pygame.font.Font("files\\font.ttf", 30)
    FONTS["GAME-ORIGINAL-NUM-LAWS"] = pygame.font.Font("files\\font.ttf", 42)
    FONTS["GAME-ORIGINAL-RU"] = pygame.font.Font("files\\font-ru.otf", 24)
    FONTS["GAME-ORIGINAL-RU-INFO"] = pygame.font.Font("files\\font-ru.otf", 20)

    for i in reversed(range(256)):
        image.set_alpha(i)
        screen.fill((255, 255, 255))
        screen.blit(image, (logo["x"], logo["y"]))
        pygame.display.flip()
        pygame.time.delay(2)

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