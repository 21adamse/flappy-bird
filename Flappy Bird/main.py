import pygame

pygame.init()
WIDTH=780
HEIGHT=780

gameover=False
flying=False

screen=pygame.display.set_mode((WIDTH,HEIGHT))

background=pygame.image.load("Images/flappybackground.png")
floor=pygame.image.load("Images/flappyfloor.png")
floorx=0

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
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
        if not gameover:
            self.delay+=1
            if self.delay > 5:
                self.index+=1
                self.delay=0
                if self.index >= len(self.images):
                    self.index=0
                self.image=self.images[self.index]
            self.image=pygame.transform.rotate(self.image,self.velocity*-2)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked=True
                self.velocity=-12
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked=False
        else:
            self.image=pygame.transform.rotate(self.image,-180)
        if flying:
            self.velocity+=0.5
            if self.velocity > 7:
                self.velocity = 7
            if self.rect.y < 600:
                self.rect.y += int(self.velocity)

birdgroup=pygame.sprite.Group()
bird=Bird(80,390)
birdgroup.add(bird)

while True:
    screen.blit(background,(0,0))

    birdgroup.draw(screen)
    birdgroup.update()
    screen.blit(floor,(floorx,600))
    
    if bird.rect.bottom >= 600:
        gameover = True
        flying = False
    if gameover == False and flying:
        floorx=floorx-1
        if floorx<-50:
            floorx=0
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and gameover == False:
            flying = True
