
import time
import pygame
from pygame.locals import *

pygame.init()

WIDTH = 864
HEIGTH =936

screen = pygame.display.set_mode((WIDTH,HEIGTH))

pygame.display.set_caption("Flappy bird :D")

city = pygame.image.load("city.png")
ground = pygame.image.load("ground.png")
ground_scroll = 0
scroll_speed = 4
fps = 60
clock = pygame.time.Clock()

class Birb(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0 
        for i in range(1,4):
            img = pygame.image.load(f"birb{i}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def update(self):
        self.counter += 1
        flap_cooldown = 5

        if self.counter > flap_cooldown:
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]


        
birb_group = pygame.sprite.Group()

flappy = Birb(100,int(HEIGTH/2))
birb_group.add(flappy)










while True:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.blit(city,(0,0))
    screen.blit(ground,(ground_scroll,768))
    birb_group.draw(screen)
    birb_group.update()

    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 35:
        ground_scroll = 0
        


        
    pygame.display.update()

        

        