import pygame
import random
import numpy
import time
import traceback
import pygame.gfxdraw
from threading import Thread

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
        self.vote = None
        self.dead = False
    
    def getInfo(self):
        return self
    
    def voteJa(self):
        self.vote = True
    
    def voteRes(self):
        self.vote = None
    
    def voteNein(self):
        self.vote = False
    
    def getVote(self):
        return self.vote
    
    def kill(self):
        self.dead = True

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
        self.thoughts = {}
    
    def getThoughts(self):
        return self.thoughts
    
    def changeThoughts(self, thoughts):
        self.thoughts = thoughts

class Game():
    def __init__(self):
        self.players = []
        self.on = True
        self.move = 0
        self.laws = ['liberal', 'liberal', 'liberal', 'liberal', 'liberal', 'liberal', 'fascist', 'fascist', 'fascist', 'fascist', 'fascist', 'fascist', 'fascist', 'fascist', 'fascist', 'fascist', 'fascist']
        self.dropped_laws = []
        self.applied_laws = {
            "liberal": 0,
            "fascist": 0
        }
        self.president = {
            "candidate": None,
            "current": None,
            "was": None
        }
        self.cancellor = {
            "candidate": None,
            "current": None,
            "was": None
        }
        self.logs = ""
        self.logs2 = ""
        self.showVotes = False
        self.voteCounter = 0
        random.shuffle(self.laws)
    
    def applyLaw(self, law):
        if law == "liberal":
            self.applied_laws["liberal"] += 1
        elif law == "fascist":
            self.applied_laws["fascist"] += 1

    def dropLaw(self, law):
        self.dropped_laws.append(law)

    def addPlayer(self, player):
        self.players.append(player)
    
    def getId(self):
        return len(self.players) + 1
    
    def getPlayers(self):
        return self.players
    
    def isOn(self):
        return self.on
    
    def nextMove(self):
        self.move += 1
    
    def votes(self, president, forced = False):
        if isinstance(president, Liberal):
            cancellor = None
            for k in president.getThoughts().keys():
                if not k.getInfo().dead and k != self.cancellor["was"]:
                    if cancellor == None:
                        cancellor = k
                    elif president.getThoughts()[k] < president.getThoughts()[cancellor] and president != k:
                        cancellor = k
                    elif president.getThoughts()[cancellor] == president.getThoughts()[k] and president != k:
                        if random.choice([False, True]):
                            cancellor = k
            self.log("Президент выбрал канцлером Player " + str(cancellor.id))

            self.cancellor["candidate"] = cancellor
        
        elif isinstance(president, Hitler):
            cancellor = None
            for k in president.getThoughts().keys():
                if k.getInfo().dead == False and k != self.cancellor["was"]:
                    if cancellor == None:
                        cancellor = k
                    elif president.getThoughts()[k] > president.getThoughts()[cancellor]:
                        cancellor = k
                    elif president.getThoughts()[k] == president.getThoughts()[cancellor]:
                        if random.choice([False, True]):
                            cancellor = k
            self.log("Президент выбрал канцлером Player " + str(cancellor.id))

            self.cancellor["candidate"] = cancellor
        
        elif isinstance(president, Fascist):
            if random.randint(0, 100) <= 35 and not isinstance(self.cancellor["was"], Hitler):
                for player in self.getPlayers():
                    if isinstance(player, Hitler):
                        self.cancellor["candidate"] = player
                        break
            elif random.randint(0, 100) <= 15:
                for player in self.getPlayers():
                    if isinstance(player, Liberal) and player != self.cancellor["was"]:
                        self.cancellor["candidate"] = player
                        break
            else:
                for player in self.getPlayers():
                    if (isinstance(player, Fascist) or isinstance(player, Hitler)) and president != player and player != self.cancellor["was"]:
                        self.cancellor["candidate"] = player
                        break
            self.log("Президент выбрал канцлером Player " + str(self.cancellor["candidate"].id))
        time.sleep(3)
        
        if not forced:
            self.log2("Голосование за: ", "Президент: Player " + str(self.president["candidate"].getInfo().id) + ", Канцлер: Player " + str(self.cancellor["candidate"].getInfo().id))
            time.sleep(3)

            votes = {
                "yes": [],
                "no": []
            }
        
            votePlayers = self.getPlayers()[:]

            while len(votePlayers) != 0:
                p = random.choice(votePlayers)
                if isinstance(p, Liberal) and p.getInfo().dead == False:
                    if p != self.president["candidate"] and p != self.cancellor["candidate"] and (p.getThoughts()[self.president["candidate"]] > random.randint(50, 90) or p.getThoughts()[self.cancellor["candidate"]] > random.randint(50, 90)):
                        p.voteNein()
                        votes["no"].append(p)
                        votePlayers.remove(p)
                    elif p == self.president["candidate"] or p == self.cancellor["candidate"]:
                        p.voteJa()
                        votes["yes"].append(p)
                        votePlayers.remove(p)
                    else:
                        p.voteJa()
                        votes["yes"].append(p)
                        votePlayers.remove(p)
                elif isinstance(p, Hitler) and p.getInfo().dead == False:
                    if p != self.president["candidate"] and p != self.cancellor["candidate"] and (p.getThoughts()[self.president["candidate"]] > random.randint(50, 90) or p.getThoughts()[self.cancellor["candidate"]]):
                        p.voteJa()
                        votes["yes"].append(p)
                        votePlayers.remove(p)
                    elif p == self.president["candidate"] or p == self.cancellor["candidate"]:
                        p.voteJa()
                        votes["yes"].append(p)
                        votePlayers.remove(p)
                    else:
                        p.voteNein()
                        votes["no"].append(p)
                        votePlayers.remove(p)
                elif p.getInfo().dead == False:
                    if (isinstance(self.president["candidate"], Liberal) or isinstance(self.cancellor["candidate"], Liberal)) and random.randint(0, 100) < 15:
                        p.voteJa()
                        votes["yes"].append(p)
                        votePlayers.remove(p)
                    elif isinstance(self.president["candidate"], Liberal) or isinstance(self.cancellor["candidate"], Liberal):
                        p.voteNein()
                        votes["no"].append(p)
                        votePlayers.remove(p)
                    elif p == self.president["candidate"] or p == self.cancellor["candidate"] or isinstance(self.president["candidate"], Hitler) or isinstance(self.cancellor["candidate"], Hitler) or isinstance(self.president["candidate"], Fascist)or isinstance(self.cancellor["candidate"], Fascist):
                        p.voteJa()
                        votes["yes"].append(p)
                        votePlayers.remove(p)
                time.sleep(1)
        
            self.showVotes = True
            time.sleep(.2)
            if len(votes["no"]) == 0 or float(len(votes["yes"]) / len(votes["no"])) > 1.0:
                self.president["current"] = self.president["candidate"]
                self.cancellor["current"] = self.cancellor["candidate"]
                self.log2("Большинство проголосовало за, избранны:", "Президент: Player " + str(self.president["candidate"].getInfo().id) + ", Канцлер: Player " + str(self.cancellor["candidate"].getInfo().id))
                result = True
            else:
                self.log("Большинство проголосовало против")
                self.voteCounter += 1
                result = False
            time.sleep(2)
            for p in self.getPlayers():
                p.voteRes()
            self.showVotes = False
        else:
            result = True

        return result

    def log(self, log_):
        self.logs = log_
        self.logs2 = ""
        print("[LOGS] " + log_)
    
    def log2(self, log_, log2_):
        self.logs = log_
        self.logs2 = log2_
        print("[LOGS] " + log_ + " " + log2_)

    def draw(self, screen):
        while True:
            clock = pygame.time.Clock()

            screen.blit(IMGS["TABLE"], (0, 0))

            if self.voteCounter != 0:
                if self.voteCounter == 1:
                    pygame.gfxdraw.filled_circle(screen, 526, 102, 28, (80, 160, 136))
                if self.voteCounter == 2:
                    pygame.gfxdraw.filled_circle(screen, 526, 102, 28, (80, 160, 136))
                    pygame.gfxdraw.filled_circle(screen, 639, 103, 29, (80, 160, 136))
                if self.voteCounter == 3:
                    pygame.gfxdraw.filled_circle(screen, 526, 102, 28, (80, 160, 136))
                    pygame.gfxdraw.filled_circle(screen, 639, 103, 29, (80, 160, 136))
                    pygame.gfxdraw.filled_circle(screen, 751, 101, 28, (80, 160, 136))
            
            if self.applied_laws["fascist"] != 0:
                for l in range(self.applied_laws["fascist"]):
                    screen.blit(IMGS["LAW-FASCIST"], (314 + 110*l, 308))
            if self.applied_laws["liberal"] != 0:
                for l in range(self.applied_laws["liberal"]):
                    screen.blit(IMGS["LAW-LIBERAL"], (370 + 110*l, 550))

            screen.blit(FONTS["GAME-ORIGINAL-NUM"].render(str(self.move), True, (53, 54, 49)), (1050, 14))
            screen.blit(FONTS["GAME-ORIGINAL-RU"].render('Ход', True, (53, 54, 49)), (1070, 22))
            if len(self.laws) >= 10:
                screen.blit(FONTS["GAME-ORIGINAL-NUM-LAWS"].render(str(len(self.laws)), True, (80, 160, 136)), (402, 98))
            else:
                screen.blit(FONTS["GAME-ORIGINAL-NUM-LAWS"].render(str(len(self.laws)), True, (80, 160, 136)), (412, 98))
            
            if len(self.dropped_laws) >= 10:
                screen.blit(FONTS["GAME-ORIGINAL-NUM-LAWS"].render(str(len(self.dropped_laws)), True, (80, 160, 136)), (836, 98))
            else:
                screen.blit(FONTS["GAME-ORIGINAL-NUM-LAWS"].render(str(len(self.dropped_laws)), True, (80, 160, 136)), (844, 98))

            for i in range(len(self.getPlayers())):
                player_rect = pygame.draw.rect(screen, (255, 255, 255), (60, 8 + 60*i, 170, 59))
                color = (53, 54, 49)

                if player_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, (240, 240, 240), (55, 8 + 60*i, 180, 59))

                    screen.blit(FONTS["GAME-ORIGINAL-RU"].render('PLAYER:', True, (53, 54, 49)), (1072 + 14 * (len(str(self.getPlayers()[i].getInfo().id)) - 1), 22 + 40))
                    screen.blit(FONTS["GAME-ORIGINAL-NUM"].render(str(self.getPlayers()[i].getInfo().id), True, (53, 54, 49)), (1050, 14 + 40))
                    if self.getPlayers()[i].getInfo().sex == 1:
                        sex = "Муж."
                    elif self.getPlayers()[i].getInfo().sex == 2:
                        sex = "Жен."
                    screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Пол: ' + sex + ', Возраст: ' + str(self.getPlayers()[i].getInfo().age), True, (53, 54, 49)), (1055, 22 + 67))
                    
                    plus_ = 0
                    if self.president["current"] == self.getPlayers()[i]:
                        screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Президент', True, (53, 54, 49)), (1055, 22 + 67 + 17))
                        plus_ = 17
                    elif self.cancellor["current"] == self.getPlayers()[i]:
                        screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Канцлер', True, (53, 54, 49)), (1055, 22 + 67 + 17))
                        plus_ = 17
                    elif self.president["was"] == self.getPlayers()[i]:
                        screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Был президентом', True, (53, 54, 49)), (1055, 22 + 67 + 17))
                        plus_ = 17
                    elif self.cancellor["was"] == self.getPlayers()[i]:
                        screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Был канцлером', True, (53, 54, 49)), (1055, 22 + 67 + 17))
                        plus_ = 17

                    if isinstance(self.getPlayers()[i], Liberal):
                        screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Партия: Либерал', True, (53, 54, 49)), (1055, 22 + 67 + 17 + plus_))
                    
                    if self.getPlayers()[i].getInfo().dead:
                        screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Мертв.', True, (53, 54, 49)), (1055, 22 + 67 + 17*6 + plus_))
                        plus_ = 14

                    if isinstance(self.getPlayers()[i], Liberal) or isinstance(self.getPlayers()[i], Hitler):
                        screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Мысли:', True, (53, 54, 49)), (1055, 22 + 67 + 17*6 + 4 + plus_))

                        for j in range(len(self.getPlayers()[i].getThoughts().keys())):
                            p_ = list(self.getPlayers()[i].getThoughts().keys())[j]
                            screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Игрок ' + str(p_.getInfo().id) + ': фашист ~' + str(self.getPlayers()[i].getThoughts()[p_]) + '%', True, (53, 54, 49)), (1058, 22 + 67 + 17*7 + 4 + 18*j + plus_))

                    elif isinstance(self.getPlayers()[i], Fascist):
                        screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Партия: Фашист', True, (53, 54, 49)), (1055, 22 + 67 + 17 + plus_))
                    elif isinstance(self.getPlayers()[i], Hitler):
                        screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Партия: Фашист; Гитлер', True, (53, 54, 49)), (1055, 22 + 67 + 17 + plus_))
                    screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Хитрость: ' + str(self.getPlayers()[i].getInfo().stealth), True, (53, 54, 49)), (1055, 22 + 67 + 17*2 + plus_))
                    screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Красноречие: ' + str(self.getPlayers()[i].getInfo().eloquence), True, (53, 54, 49)), (1055, 22 + 67 + 17*3 + plus_))
                    screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Удача: ' + str(self.getPlayers()[i].getInfo().luck), True, (53, 54, 49)), (1055, 22 + 67 + 17*4 + plus_))
                    screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render('Понимание игры: ' + str(self.getPlayers()[i].getInfo().smart), True, (53, 54, 49)), (1055, 22 + 67 + 17*5 + plus_))

                screen.blit(FONTS["GAME-ORIGINAL"].render('PLAYER', True, color), (60, 20 + 60*i))
                screen.blit(FONTS["GAME-ORIGINAL-NUM"].render(str(self.getPlayers()[i].getInfo().id), True, color), (145, 15 + 60*i))

                if self.getPlayers()[i].getVote() != None:
                    if self.getPlayers()[i].getVote() and self.getPlayers()[i].getInfo().dead == False:
                        if self.showVotes:
                            screen.blit(IMGS["VOTE-JA"], (17, 24 + 60*i))
                            
                        else:
                            screen.blit(grayscale(IMGS["VOTE-JA"]), (17, 24 + 60*i))
                    elif self.getPlayers()[i].getVote() == False and self.getPlayers()[i].getInfo().dead == False:
                        if self.showVotes:
                            screen.blit(IMGS["VOTE-NEIN"], (17, 24 + 60*i))
                        else:
                            screen.blit(grayscale(IMGS["VOTE-NEIN"]), (17, 24 + 60*i))

                if self.president["candidate"] == self.getPlayers()[i]:
                    pygame.gfxdraw.filled_circle(screen, 207, 37 + 60*i, 27, (35, 89, 76))
                elif self.cancellor["candidate"] == self.getPlayers()[i]:
                    pygame.gfxdraw.filled_circle(screen, 207, 37 + 60*i, 27, (199, 107, 56))
                elif self.president["was"] == self.getPlayers()[i]:
                    pygame.gfxdraw.filled_circle(screen, 207, 37 + 60*i, 27, (152, 198, 187))
                elif self.cancellor["was"] == self.getPlayers()[i]:
                    pygame.gfxdraw.filled_circle(screen, 207, 37 + 60*i, 27, (200, 164, 144))

                if self.getPlayers()[i].getInfo().dead:
                    color = (153, 153, 153)
                    screen.blit(grayscale(self.getPlayers()[i].getInfo().img), (184, 14 + 60*i))
                else:
                    curr_player = self.getPlayers()[i]
                    screen.blit(self.getPlayers()[i].getInfo().img, (184, 14 + 60*i))
            
            text_width, text_height = FONTS["GAME-ORIGINAL-RU-INFO"].size(self.logs)
            screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render(self.logs, True, (53, 54, 49)), (int(1280 / 2 - text_width / 2), 150))

            if self.logs2 != "":
                text_width2, text_height2 = FONTS["GAME-ORIGINAL-RU-INFO"].size(self.logs2)
                screen.blit(FONTS["GAME-ORIGINAL-RU-INFO"].render(self.logs2, True, (53, 54, 49)), (int(1280 / 2 - text_width2 / 2), 168))

            pygame.display.update()
            screen.fill((255, 255, 255))
            
            clock.tick(40)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    print("Closed")
    
    def game(self):
        self.log("Game started")
        nextone = None
        forcepresident = None
        lastLaw = 0
        while True:
            self.nextMove()
            self.log("Ход:" + str(self.move))

            if len(self.laws) <= 2:
                self.laws = self.dropped_laws + self.laws
                self.dropped_laws = []
                random.shuffle(self.laws)

            for i in range(len(self.getPlayers())):
                if not self.getPlayers()[i].getInfo().dead:
                    curr_player = self.getPlayers()[i]
                    if isinstance(curr_player, Liberal):
                        newThoughts = {}
                        for player_ in self.getPlayers():
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
                    elif isinstance(curr_player, Hitler):
                        if len(self.getPlayers()) <= 6:
                            newThoughts = {}
                            for player_ in self.getPlayers():
                                if player_.getInfo().id != curr_player.getInfo().id:
                                    if len(curr_player.getThoughts()) == 0:
                                        if isinstance(player_, Fascist):
                                            newThoughts[player_] = 100
                                        else:
                                            newThoughts[player_] = 0
                                    else:
                                        newThoughts = curr_player.getThoughts()
                            curr_player.changeThoughts(newThoughts)
                        else:
                            newThoughts = {}
                            for player_ in self.getPlayers():
                                if player_.getInfo().id != curr_player.getInfo().id:
                                    if len(curr_player.getThoughts()) == 0:
                                        if isinstance(player_, Fascist):
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
            
            time.sleep(1)

            if forcepresident == None:
                if self.president["current"] != None and self.cancellor["current"] != None:
                    self.president["was"] = self.president["current"] 
                    self.cancellor["was"] = self.cancellor["current"] 

                if self.president["was"] == None and self.president["candidate"] == None:
                    self.president["candidate"] = self.getPlayers()[0]
                    self.log2("Выборы, кандидат в президенты", "Player " + str(self.getPlayers()[0].getInfo().id))
                    time.sleep(3)
                    votesResult = self.votes(self.getPlayers()[0])
            
                else:
                    if self.getPlayers().index(self.president["candidate"]) + 1 >= len(self.getPlayers()):
                        nextone = self.getPlayers()[0]
                    else:
                        nextone = self.getPlayers()[self.getPlayers().index(self.president["candidate"]) + 1]
                    self.president["candidate"] = nextone
                    self.log2("Выборы, кандидат в президенты", "Player " + str(nextone.id))
                    time.sleep(3)
                    votesResult = self.votes(nextone)
            else:
                self.president["candidate"] = forcepresident
                votesResult = self.votes(forcepresident, True)
                forcepresident = None

            time.sleep(1)

            if votesResult:
                self.voteCounter = 0

                cards = [self.laws[0], self.laws[1], self.laws[2]]
                self.laws.pop(0)
                self.laws.pop(0)
                self.laws.pop(0)

                self.log("Президент взял 3 карты")
                time.sleep(1)
                #president
                if isinstance(self.president["current"], Liberal):
                    for card in cards:
                        if card == "fascist":
                            self.dropLaw(card)
                            cards.remove(card)
                            break
                    if len(cards) != 2:
                        self.dropLaw(card)
                        cards.remove(card)
                elif isinstance(self.president["current"], Hitler) or isinstance(self.president["current"], Fascist):
                    for card in cards:
                        if card == "liberal":
                            self.dropLaw(card)
                            cards.remove(card)
                            break
                    if len(cards) != 2:
                        self.dropLaw(card)
                        cards.remove(card)
                self.log2("Президент скинул карту,", "Отдал оставшиеся 2 канцлеру")
                time.sleep(1)
                #cancellor
                if isinstance(self.cancellor["current"], Liberal):
                    for card in cards:
                        if card == "fascist":
                            self.dropLaw(card)
                            cards.remove(card)
                            break
                        if len(cards) != 1:
                            self.dropLaw(card)
                            cards.remove(card)
                elif isinstance(self.president["current"], Hitler) or isinstance(self.president["current"], Fascist):
                    for card in cards:
                        if card == "liberal":
                            self.dropLaw(card)
                            cards.remove(card)
                            break
                        if len(cards) != 1:
                            self.dropLaw(card)
                            cards.remove(card)
                self.applyLaw(cards[0])
                self.log2("Канцлер скинул карту,", "Другую положил на стол")
                time.sleep(1)

                if lastLaw != self.applied_laws["fascist"] and (((self.applied_laws["fascist"] == 1 or self.applied_laws["fascist"] == 2) and len(self.getPlayers()) >= 9) or (self.applied_laws["fascist"] == 2 and (len(self.getPlayers()) == 8 or len(self.getPlayers()) == 7))):
                    if isinstance(self.president["current"], Liberal):
                        si = 0
                        suspect = sorted(self.president["current"].getThoughts().items(), key=lambda i: i[1], reverse=True)[si][0]
                        while self.president["current"].getThoughts()[suspect] >= random.randint(75, 100):
                            si += 1
                            suspect = sorted(self.president["current"].getThoughts().items(), key=lambda i: i[1], reverse=True)[si][0]
                        if isinstance(suspect, Liberal):
                            newThoughts = self.president["current"].getThoughts()
                            newThoughts[suspect] = 0
                            for p in self.getPlayers():
                                if (isinstance(p, Liberal) or isinstance(p, Hitler)) and p != self.president["current"] and suspect in p.getThoughts():
                                    newThoughtsP = p.getThoughts()
                                    newThoughtsP[suspect] = int(p.getThoughts()[suspect] - (self.president["current"].getInfo().eloquence / 14  + p.getInfo().luck / 14 + p.getInfo().smart / 14 + suspect.getInfo().eloquence / 14 + p.getInfo().luck / 14 + p.getInfo().smart / 14 + random.randint(-8, 8)))
                                    p.changeThoughts(newThoughtsP)
                        elif isinstance(suspect, Fascist) or isinstance(suspect, Hitler):
                            newThoughts = self.president["current"].getThoughts()
                            newThoughts[suspect] = 100
                            self.president["current"].changeThoughts(newThoughts)
                            for p in self.getPlayers():
                                if (isinstance(p, Liberal) or isinstance(p, Hitler)) and p != self.president["current"] and suspect in p.getThoughts():
                                    newThoughtsP = p.getThoughts()
                                    newThoughtsP[suspect] = int(p.getThoughts()[suspect] + (self.president["current"].getInfo().eloquence / 12  + p.getInfo().luck / 12 + p.getInfo().smart / 12 + random.randint(0, 12)) - (suspect.getInfo().eloquence / 12 + p.getInfo().luck / 12 + p.getInfo().smart / 12 + random.randint(-2, 8)))
                                    p.changeThoughts(newThoughtsP)
                        time.sleep(1)
                        self.log("Президент проверил Player " + str(suspect.id))

                    if isinstance(self.president["current"], Hitler):
                        si = 0
                        suspect = sorted(self.president["current"].getThoughts().items(), key=lambda i: i[1], reverse=True)[si][0]
                        while self.president["current"].getThoughts()[suspect] >= random.randint(75, 100):
                            si += 1
                            suspect = sorted(self.president["current"].getThoughts().items(), key=lambda i: i[1], reverse=True)[si][0]
                        if isinstance(suspect, Liberal):
                            newThoughts = self.president["current"].getThoughts()
                            newThoughts[suspect] = 0
                            self.president["current"].changeThoughts(newThoughts)
                            for p in self.getPlayers():
                                if (isinstance(p, Liberal) or isinstance(p, Hitler)) and p != self.president["current"] and suspect in p.getThoughts():
                                    newThoughtsP = p.getThoughts()
                                    newThoughtsP[suspect] = int(p.getThoughts()[suspect] + (self.president["current"].getInfo().eloquence / 12  + p.getInfo().luck / 12 + p.getInfo().smart / 12 + random.randint(0, 8)) - (suspect.getInfo().eloquence / 12 + p.getInfo().luck / 12 + p.getInfo().smart / 12 + random.randint(-2, 8)))
                                    p.changeThoughts(newThoughtsP)
                        if isinstance(suspect, Fascist):
                            newThoughts = self.president["current"].getThoughts()
                            newThoughts[suspect] = 100
                            self.president["current"].changeThoughts(newThoughts)
                            for p in self.getPlayers():
                                if (isinstance(p, Liberal) or isinstance(p, Hitler)) and p != self.president["current"] and suspect in p.getThoughts():
                                    newThoughtsP = p.getThoughts()
                                    newThoughtsP[suspect] = int(p.getThoughts()[suspect] - (self.president["current"].getInfo().eloquence / 16  + p.getInfo().luck / 16 + p.getInfo().smart / 16 + suspect.getInfo().eloquence / 16 + p.getInfo().luck / 16 + p.getInfo().smart / 16 + random.randint(-8, 8)))
                                    p.changeThoughts(newThoughtsP)
                        time.sleep(1)
                        self.log("Президент проверил Player " + str(suspect.id))

                    if isinstance(self.president["current"], Fascist):
                        suspect = random.choice(self.getPlayers())
                        if isinstance(suspect, Liberal):
                            for p in self.getPlayers():
                                if (isinstance(p, Liberal) or isinstance(p, Hitler)) and p != self.president["current"] and suspect in p.getThoughts():
                                    newThoughtsP = p.getThoughts()
                                    newThoughtsP[suspect] += random.randint(-2, 10)
                                    p.changeThoughts(newThoughtsP)
                        if isinstance(suspect, Fascist) or isinstance(suspect, Hitler):
                            for p in self.getPlayers():
                                if (isinstance(p, Liberal) or isinstance(p, Hitler)) and p != self.president["current"] and suspect in p.getThoughts():
                                    newThoughtsP = p.getThoughts()
                                    newThoughtsP[suspect] += random.randint(-10, 2)
                                    p.changeThoughts(newThoughtsP)
                        time.sleep(1)
                        self.log("Президент проверил Player " + str(suspect.id))              
                if lastLaw != self.applied_laws["fascist"] and (self.applied_laws["fascist"] == 3 and (len(self.getPlayers()) >= 7 and len(self.getPlayers()) <= 10)):
                    if isinstance(self.president["current"], Liberal):
                        nextoneF = sorted(self.president["current"].getThoughts().items(), key=lambda i: i[1])[0][0]
                    elif isinstance(self.president["current"], Hitler):
                        nextoneF = sorted(self.president["current"].getThoughts().items(), key=lambda i: i[1])[-1][0]
                    elif isinstance(self.president["current"], Fascist):
                        nextoneF = random.choice(self.getPlayers())
                        while isinstance(nextone, Liberal):
                            nextoneF = random.choice(self.getPlayers())
                    forcepresident = nextoneF
                    self.log("Президент выбрал следующим Player " + str(nextoneF.id))
                if lastLaw != self.applied_laws["fascist"] and (self.applied_laws["fascist"] == 4 or self.applied_laws["fascist"] == 5):
                    if isinstance(self.president["current"], Liberal):
                        pki = sorted(self.president["current"].getThoughts().items(), key=lambda i: i[1], reverse=True)[0][0]
                        pki.kill()
                    elif isinstance(self.president["current"], Hitler):
                        pki = sorted(self.president["current"].getThoughts().items(), key=lambda i: i[1], reverse=True)[-1][0]
                        pki.kill()
                    elif isinstance(self.president["current"], Fascist):
                        pki = random.choice(self.getPlayers())
                        while isinstance(pki, Liberal):
                            pki = random.choice(self.getPlayers())
                        pki.kill()
                    self.log("Президент убил Player " + str(pki.id))
                lastLaw = self.applied_laws["fascist"]

            if self.voteCounter == 3:
                time.sleep(1)
                self.log("Выборы провалились в 3-й раз!")
                time.sleep(1)
                self.voteCounter = 0
                self.applyLaw(self.laws[0])
                self.laws.pop(0)
                self.log("Был принят закон с вершины стопки")
                nextone = self.getPlayers()[0]

            time.sleep(1)
            if self.applied_laws["liberal"] == 5:
                self.log2("Игра окончена!", "Победили либералы1")
                break
            elif self.applied_laws["fascist"] == 6:
                self.log2("Игра окончена!", "Победили фашисты2")
                break
            elif self.applied_laws["fascist"] > 3 and isinstance(self.cancellor["current"], Hitler):
                self.log2("Игра окончена!", "Победили фашисты3")
                break
            else:
                hd = False
                for p in self.getPlayers():
                    if isinstance(p, Hitler) and p.getInfo().dead == True:
                        hd = True
                if hd:
                    self.log2("Игра окончена!", "Победили либералы4")
                    break
def newPlayerInfo():
    return [random.choice([1, 2]), random.randint(14, 45), random.randint(10, 100), random.randint(10, 100), random.randint(10, 100), random.randint(10, 100)]

def grayscale(img):
    arr = pygame.surfarray.array3d(img)
    avgs = [[(r*0.298 + g*0.587 + b*0.114) for (r,g,b) in col] for col in arr]
    arr = numpy.array([[[avg,avg,avg] for avg in col] for col in avgs])
    return pygame.surfarray.make_surface(arr)

def start():
    screen = pygame.display.set_mode((1280, 752))
    screen.fill((255, 255, 255))

    newGame = Game()
    num_players = random.randint(5, 10)

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
    
    thread1 = Thread(target=newGame.draw, args=(screen,), daemon=True)
    thread2 = Thread(target=newGame.game, daemon=True)

    thread1.start()
    thread2.start()    

def main():
    clock = pygame.time.Clock()

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
    IMGS["VOTE-JA"] = pygame.image.load('imgs\\ja.png')
    IMGS["VOTE-NEIN"] = pygame.image.load('imgs\\nein.png')
    IMGS["LAW-LIBERAL"] = pygame.image.load('imgs\\law-liberal.png')
    IMGS["LAW-FASCIST"] = pygame.image.load('imgs\\law-fascist.png')
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

    menu = True
    while True:
        if menu:
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
        clock.tick(40)

        for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    print("Closed")
                elif a != "NONE" and menu:
                    if e.type == pygame.MOUSEBUTTONUP:
                        if a == "EXIT":
                            pygame.quit()
                            quit()
                        elif a == "PLAY":
                            start()
                            menu = False

main()