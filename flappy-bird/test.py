import pygame
from random import random, randint
from time import time
from math import ceil

#Bird Sprites from https://www.freepik.com/free-vector/hand-drawn-animation-frames-element-collection_33591451.htm

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Flappy Bird")
font = pygame.font.SysFont('Brandish', 50)
clock = pygame.time.Clock()
click = False
pillars = []
score = 0


gameActive = True

class Bird:
    vOnClick = 8
    vMax = -10
    vReal = 0
    posX = 170
    posY = 200
    lastSpriteUpdate = time()
    spriteUpdateTime = .1
    spriteIndex = 0
    sprites = []
    for i in range(1,9): sprites.append(pygame.image.load("img/bird"+str(i)+".png").convert_alpha())
    spriteH = sprites[0].get_height()
    spriteW = sprites[0].get_width()
    rectHead = pygame.rect.Rect(posX+47, posY-40,48,45)
    rectBody = pygame.rect.Rect(posX, posY-19,65,40)

    def update():
        Bird.movement()
        Bird.updateAnimation()
        Bird.draw()
        
        
    def movement():
        time = clock.get_time()
        if click: Bird.vReal = Bird.vOnClick
        else: Bird.vReal = max(Bird.vMax, Bird.vReal - time/16.7)
        
        dh = int(Bird.vReal*time/16.7)
        Bird.posY -= dh
        Bird.rectHead.centery -= dh
        Bird.rectBody.centery -= dh
        
    def updateAnimation():
        if time()-Bird.lastSpriteUpdate > Bird.spriteUpdateTime:
            Bird.lastSpriteUpdate = time()
            Bird.spriteIndex = (Bird.spriteIndex+1)%8
        
    def checkForDeath():
        for i in pillars:
            for j in i.getHitboxes():
                if Bird.rectBody.colliderect(j): return True
                if Bird.rectHead.colliderect(j): return True
        return (not 30 < Bird.posY < screen.get_height()-30)
    
    def draw():
        screen.blit(Bird.sprites[Bird.spriteIndex], (Bird.posX, Bird.posY-Bird.spriteH/2))

    def getPos():
        return Bird.posX, Bird.posY

class Pillar:
    
    vX = 10
    gapHeight = 180
    pillarWidth = 100
    pillarEntry = pygame.image.load("img/pillarEntry.png")
    pillarEntrySize = pillarEntry.get_size()
    scoreCounted = False
    def __init__(self):
        self.posX = screen.get_width()
        self.gapStart = random()*(screen.get_height()-Pillar.gapHeight-84)+42
        self.upperBodyHeight = self.gapStart-42
        self.lowerBodyStart = self.gapStart + Pillar.gapHeight + 42
        self.lowerEntryStart = self.gapStart + Pillar.gapHeight
        self.lowerBodyHeight = screen.get_height()-self.lowerBodyStart
        self.upperBody = pygame.transform.scale(pygame.image.load("img/pillarBody.png"),(100,self.upperBodyHeight))
        self.lowerBody = pygame.transform.scale(pygame.image.load("img/pillarBody.png"),(100,self.lowerBodyHeight))
    
    def move(self):
        self.posX -= Pillar.vX*clock.get_time()/40
            
    def checkForRemove(self):
        if self.posX < -135: 
            pillars.remove(self)
            Pillar.scoreCounted = False
            return True
        return False
    
    def checkForScore(self):
        global score
        if not Pillar.scoreCounted and self.posX < Bird.posX:
            score += 1
            Pillar.scoreCounted = True
        
    def getHitboxes(self):
        return [pygame.Rect((self.posX+17, 0), self.upperBody.get_size()),
                pygame.Rect((self.posX+17, self.lowerBodyStart), self.lowerBody.get_size()),
                pygame.Rect((self.posX, self.upperBodyHeight), Pillar.pillarEntrySize),
                pygame.Rect((self.posX, self.lowerEntryStart), Pillar.pillarEntrySize)
                ]
    
    def draw(self):
        screen.blit(self.upperBody, (self.posX+17, 0))
        screen.blit(Pillar.pillarEntry, (self.posX, self.gapStart-42))
        screen.blit(self.lowerBody, (self.posX+17, self.gapStart+self.gapHeight+42))
        screen.blit(Pillar.pillarEntry, (self.posX, self.gapStart+self.gapHeight))
        
    def createPillarIfNecessary():
        if pillars[0].posX < 100 and len(pillars) < 2: pillars.append(Pillar())
            
    def updateAll():
        for p in pillars:
            p.move()
            p.draw()
        pillars[0].checkForRemove()
        pillars[0].checkForScore()
        Pillar.createPillarIfNecessary()
    
class Deathscreen:
    class img:
        score = pygame.image.load("img/deathscreenScoreBG.png").convert_alpha()
        silver = pygame.image.load("img/silber.png").convert_alpha()
        bronce = pygame.image.load("img/bronze.png").convert_alpha()
        gold = pygame.image.load("img/gold.png").convert_alpha()
        btn = pygame.image.load("img/deathscreenBtn.png").convert_alpha()
        youLost = pygame.image.load("img/deathscreenYouLost.png").convert_alpha()
    scoreBronce = 10
    scoreSilver = 20
    scoreGold = 30
    best = 0
    
    def darkenMedals(): 
        g = Deathscreen.img.gold.copy()
        s = Deathscreen.img.silver.copy()
        b = Deathscreen.img.bronce.copy()
        g.fill((255,255,255,70), special_flags=pygame.BLEND_RGBA_MULT)
        s.fill((255,255,255,70), special_flags=pygame.BLEND_RGBA_MULT)
        b.fill((255,255,255,70), special_flags=pygame.BLEND_RGBA_MULT)
        return g,s,b
    
    def default():
        global gameActive
        if Deathscreen.best < score: Deathscreen.best = score
        screen.fill((0,255,0))
        imgGold, imgSilver, imgBronce = Deathscreen.darkenMedals()
        screen.blit(Deathscreen.img.youLost, (200, 100))
        screen.blit(Deathscreen.img.score, (200, 200))
        scorestr = font.render(str(score), True, (0, 0, 0))
        beststr = font.render(str(Deathscreen.best), True, (0, 0, 0))
        screen.blit(scorestr, (301 - scorestr.get_width()/2, 233))
        screen.blit(beststr, (499 - beststr.get_width()/2,233))
        screen.blit(imgGold, (500, 300))
        screen.blit(imgSilver, (350, 300))
        screen.blit(imgBronce, (200, 300))
        screen.blit(Deathscreen.img.btn, (200, 420))
        if pygame.Rect((200, 420),Deathscreen.img.btn.get_size()).collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.Cursor(pygame.SYSTEM_CURSOR_HAND))
            if True in pygame.mouse.get_pressed(3):
                gameActive = True
                init_game()
        else: pygame.mouse.set_cursor(pygame.Cursor(pygame.SYSTEM_CURSOR_ARROW))



def updateEvents():
    global click
    click=False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: quit()
        elif event.type == pygame.MOUSEBUTTONDOWN: click = True

def init_game():
    global score
    pygame.mouse.set_cursor(pygame.Cursor(pygame.SYSTEM_CURSOR_ARROW))
    pillars.append(Pillar())
    Bird.vReal = 0
    Bird.posX = 170
    Bird.posY = 200
    Bird.rectHead = pygame.rect.Rect(Bird.posX+47, Bird.posY-40,48,45)
    Bird.rectBody = pygame.rect.Rect(Bird.posX, Bird.posY-19,65,40)
    score = 0

def main():
    global gameActive, pillars
    init_game()
    while 1:
        screen.fill((50,50,255))
        updateEvents()
        if gameActive:
            Pillar.updateAll()
            Bird.update()
            if Bird.checkForDeath():
                gameActive = False
                pillars = []
        else:
            Deathscreen.default()
        
        if score == 1: screen.blit(font.render("1 Punkt", True, (0, 0, 0)), (20,20))
        else: screen.blit(font.render(str(score) + " Punkte", True, (0, 0, 0)), (20,20))
        clock.tick(60)
        pygame.display.flip()
        
main()
