
import time
import pygame
from pygame.locals import *
import random

pygame.init()

WIDTH = 864
HEIGHT =936

screen = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("Flappy bird :D")

city = pygame.image.load("city.png")
flying = False
ground = pygame.image.load("ground.png")
restart = pygame.image.load("bigredsignthatsaysrestart.png")
ground_scroll = 0
scroll_speed = 4
fps = 60
clock = pygame.time.Clock()
gameover = False
pipe_gap = 150
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
font = pygame.font.SysFont('Bauhasu 93', 60)




def drawtext(text,font,textcolour,x,y):

    text_render = font.render(text,True,True,textcolour)

    screen.blit(text_render,(x,y))

def reset():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(HEIGHT/2)
    score = 0

    return score



class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("pipe.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        
        # pos1 is top pos-1 is from bottom
        if pos == 1:
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft = [x,y -int(pipe_gap/2)]
        if pos == -1:
            self.rect.topleft = [x,y +int(pipe_gap/2)]

    

    def update(self):
        self.rect.x -= scroll_speed

        if self.rect.right < 0:
            self.kill()





class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)


    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                action = True
                


        screen.blit(self.image,(self.rect.x,self.rect.y))
        return action




                
            
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
        self.vel = 0
        self.clicked = False

    def update(self):


        # gravity
        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            # print(f"bird vel = {self.vel}")
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

            

        #jump
        if gameover == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # handel animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #birb rotate
            self.image = pygame.transform.rotate(self.images[self.index],self.vel*-2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index],-90)
        
birb_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()


flappy = Birb(100,int(HEIGHT/2))
birb_group.add(flappy)
button = Button(WIDTH//2-50,HEIGHT//2-100,restart)

while True:
    clock.tick(fps)
    screen.blit(city,(0,0))

    birb_group.draw(screen)
    birb_group.update()

    pipe_group.update()
    pipe_group.draw(screen)




    screen.blit(ground,(ground_scroll,768))

    if len(pipe_group) > 0:
        if birb_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
            and birb_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pass_pipe== False:
            pass_pipe = True
        if pass_pipe == True:
            if birb_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
        drawtext(str(score),font,"white",int(WIDTH/2),20)
    #look for collision
    if pygame.sprite.groupcollide(birb_group,pipe_group,False,False) or flappy.rect.top < 0:

        gameover = True
    if flappy.rect.bottom > 768:
        gameover = True 
        flying = False

    if gameover == False and flying == True:
        


        current_time = pygame.time.get_ticks()
        #genereating new pipes
        if current_time - last_pipe > pipe_frequency:

            pipe_height = random.randint(-100,100)

            bottom_pipe = Pipe(WIDTH,int(HEIGHT/2) +pipe_height,-1)
            top_pipe = Pipe(WIDTH,int(HEIGHT/2 ) +pipe_height,1)
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe = current_time
            

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()
   
      
    if gameover == True:
        if button.draw() == True:
            gameover = False
            score = restart()
        


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()        
        if event.type == MOUSEBUTTONDOWN and flying == False and gameover == False:
            flying = True

    pygame.display.update()

        

        
