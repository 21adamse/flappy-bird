import pygame, random

pygame.init()
WIDTH=780
HEIGHT=780

gameover=False
run=True
flying=False

screen=pygame.display.set_mode((WIDTH,HEIGHT))

background=pygame.image.load("Images/flappybackground.png")
floor=pygame.image.load("Images/flappyfloor.png")
floorx=0
movespeed=4
pipegap=160
pipefrequency=2000
lastpipe=pygame.time.get_ticks() - pipefrequency
passpipe=False
score = 0
font = "Bauhaus"

clock = pygame.time.Clock()

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img1=pygame.image.load("Images/flappy1.png")
        img2=pygame.image.load("Images/flappy2.png")
        img3=pygame.image.load("Images/flappy3.png")
        self.images=[img1,img2,img3]
        self.image=self.images[0]
        self.index=0
        self.delay=0
        self.velocity=0
        self.clicked=False
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
    def update(self):
        if gameover == False:
            self.delay+=1
            if self.delay > 5:
                self.index+=1
                self.delay=0
                if self.index >= len(self.images):
                    self.index=0
            self.image=self.images[self.index]
            self.image=pygame.transform.rotate(self.images[self.index],self.velocity*-2)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked=True
                self.velocity=-10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked=False
        else:
            self.image=pygame.transform.rotate(self.image,-180)
        if flying:
            self.velocity += 0.5
            if self.velocity > 5:
                self.velocity = 5
            if self.rect.bottom < 625:
                self.rect.y += int(self.velocity)

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,pos):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.pos=pos
        self.image=pygame.image.load("Images/flappypillar.png")
        self.rect=self.image.get_rect()
        if self.pos == 1:
            self.image=pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft=[self.x,self.y-int(pipegap/2)]
        elif self.pos == -1:
            self.rect.topleft=[self.x,self.y+int(pipegap/2)]

    def update(self):
        self.rect.x -= movespeed
        if self.rect.right < 0:
            self.kill()

def drawtext(text,colour,x,y):
    font1=pygame.font.SysFont(font,60)
    text1 = font1.render(text,True,colour)
    screen.blit(text1,(x,y))

def restart():
    global score,gameover,flying
    score=0
    gameover=False
    pipegroup.empty()
    birdgroup.empty()
    bird=Bird(80,280)
    birdgroup.add(bird)

birdgroup=pygame.sprite.Group()
bird=Bird(80,280)
birdgroup.add(bird)
pipegroup=pygame.sprite.Group()
while run:
    clock.tick(60)
    screen.blit(background,(0,0))
    birdgroup.draw(screen)
    pipegroup.draw(screen)
    screen.blit(floor,(floorx,630))
    drawtext("Score:"+str(score),"white",WIDTH/2-70,30)
    if birdgroup.sprites()[0].rect.bottom >= 625 or birdgroup.sprites()[0].rect.top < 0:
        gameover = True
        flying = False
    if gameover == False and flying:
        birdgroup.update()
        currenttime = pygame.time.get_ticks()
        if currenttime - lastpipe > pipefrequency:
            pipeheight = random.randint(-100,100)
            toppipe=Pipe(WIDTH,int(HEIGHT/2) + pipeheight,1)
            bottompipe=Pipe(WIDTH,int(HEIGHT/2) + pipeheight,-1)
            pipegroup.add(toppipe)
            pipegroup.add(bottompipe)
            lastpipe = currenttime
        pipegroup.update()
        floorx=floorx-movespeed
        if floorx<-50:
            floorx=0
    elif gameover == True:
        drawtext("Gameover","red",WIDTH/2-105,HEIGHT/2-40)
        drawtext("Press space to restart","white",WIDTH/2-220,HEIGHT/2+10)
    if pygame.sprite.groupcollide(birdgroup,pipegroup,False,False):
        gameover=True
    if len(pipegroup) > 0:
        if birdgroup.sprites()[0].rect.left > pipegroup.sprites()[0].rect.left\
        and birdgroup.sprites()[0].rect.right < pipegroup.sprites()[0].rect.right\
        and passpipe == False:
            passpipe = True
        if passpipe == True:
            if birdgroup.sprites()[0].rect.left > pipegroup.sprites()[0].rect.right:
                score+=1
                passpipe = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and gameover == False:
            flying = True
        if event.type == pygame.KEYDOWN:
            if gameover == True:
                if event.key == pygame.K_SPACE:
                    restart()

    pygame.display.update()
pygame.quit()