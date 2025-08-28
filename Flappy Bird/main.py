import pygame

pygame.init()
WIDTH=780
HEIGHT=780

screen=pygame.display.set_mode((WIDTH,HEIGHT))

background=pygame.image.load("Images/flappybackground.png")
floor=pygame.image.load("Images/flappyfloor.png")
floorx=0

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super.__init__()
        img1=pygame.image.load("Images/flappy1.png")
        img2=pygame.image.load("Images/flappy2.png")
        img3=pygame.image.load("Images/flappy3.png")
        self.images=[img1,img2,img3]
        self.index=0
        self.delay=0
        self.rect=self.images[0].get_rect()
        self.rect.center=[x,y]

while True:
    screen.blit(background,(0,0))
    screen.blit(floor,(floorx,600))
    floorx=floorx-1
    if floorx<-50:
        floorx=0
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)