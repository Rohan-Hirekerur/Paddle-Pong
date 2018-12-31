import pygame
import numpy as np
import pyglet

white = (255,255,255)
red = (255,0,0)
black = (0,0,0)

pygame.init()
page_width = 2000
page_height = 1000
size = page_width,page_height
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Paddle Pong")
#pygame.draw.rect(screen,white,[100,100,70,333])
pygame.display.update()
clock = pyglet.clock.Clock()

class paddle:
    speed = 20
    height = 333
    width = 70
    def __init__(self,x,y):
        self.x = x
        self.y = y
        pygame.draw.rect(screen,white,[self.x,self.y,self.width,self.height])
        
    def show(self):
        pygame.draw.rect(screen,white,[self.x,self.y,self.width,self.height])
        
    def moveup(self):
        if self.y > 0:
            self.y -= self.speed
        pygame.draw.rect(screen,white,[self.x,self.y,self.width,self.height])
            
    def movedown(self):
        if (self.y + self.height) < page_height:
            self.y += self.speed        
        pygame.draw.rect(screen,white,[self.x,self.y,self.width,self.height])
        
class pong:
    speed_x = 20
    speed_y = 10
    height = 70
    width = 70
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        pygame.draw.rect(screen,red,[self.x,self.y,self.width,self.height])
        
    
    def show(self):
        pygame.draw.rect(screen,red,[self.x,self.y,self.width,self.height])
        
def play():
    left_paddle = paddle(0,300)
    right_paddle = paddle(1930,300)
    p1 = pong(1000,500)
    gameover = False
    while not gameover:
        clock.tick(100)
        pygame.draw.rect(screen,black,[0,0,page_width,page_height])
        left_paddle.show()
        right_paddle.show()
        p1.show()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break;
                
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            left_paddle.moveup()

        if keys[pygame.K_s]:
            left_paddle.movedown()

        if keys[pygame.K_UP]:
            right_paddle.moveup()

        if keys[pygame.K_DOWN]:
            right_paddle.movedown()
                
        pygame.display.update()
        
play()
#pg.quit()