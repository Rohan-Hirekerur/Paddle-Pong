import pygame
import pyglet
import math
from random import randrange

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

pygame.init()
page_width = 1000
page_height = 500
size = page_width, page_height
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Paddle Pong")
pygame.display.update()
clock = pyglet.clock.Clock()
clock.set_fps_limit(60)
font = pygame.font.Font(None, 50)


class Paddle:
    speed = 20
    height = 150
    width = 25
    score = 0
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.draw.rect(screen, white, [self.x, self.y, self.width, self.height])
    
    def get_pos(self):
        return [self.x, self.y, self.x+self.width, self.y+self.height]
        
    def show(self):
        pygame.draw.rect(screen, white, [self.x, self.y, self.width, self.height])
        
    def move_up(self):
        if self.y > 0:
            self.y -= self.speed
        pygame.draw.rect(screen, white, [self.x, self.y, self.width, self.height])
            
    def move_down(self):
        if (self.y + self.height) < page_height:
            self.y += self.speed        
        pygame.draw.rect(screen, white, [self.x, self.y, self.width, self.height])
        
    def inc_score(self):
        self.score += 1

        
class Pong:
    def __init__(self):
        self.speed = 10
        self.height = 25
        self.width = 25
        self.x = page_width/2-self.width/2
        self.y = page_height/2-self.height/2
        self.direction = randrange(-45, 45)
        if randrange(2) == 0:
            self.direction += 180
        pygame.draw.rect(screen, white, [self.x, self.y, self.width, self.height])
        
    def get_pos(self):
        return [self.x, self.y, self.x+self.width, self.y+self.height]
        
    def reset(self):
        self.x = page_width/2-self.width/2
        self.y = page_height/2-self.height/2
        self.direction = randrange(-45, 45)
        self.speed = 10
        if randrange(2) == 0:
            self.direction += 180
        pygame.draw.rect(screen, white, [self.x, self.y, self.width, self.height])

    def bounce(self,diff):
        self.direction = (180-self.direction) % 360
#        self.direction -= randrange(-10,10)
        self.direction += diff
        self.speed *= 1.05
        
    def show(self):
        pygame.draw.rect(screen, white, [self.x, self.y, self.width, self.height])
        
    def move(self):
        direction_radians = math.radians(self.direction)
 
        self.x += self.speed * math.cos(direction_radians)
        self.y -= self.speed * math.sin(direction_radians)
 
        if self.x + self.width < 0:
            self.reset()
            return 0
 
        if self.x > page_width:
            self.reset()
            return 1
  
        if self.y <= 0:
            self.direction = (360-self.direction) % 360
 
        if self.y > page_height-self.height:
            self.direction = (360-self.direction) % 360
        
        return -1

            
#def left_collision(r1, r2):
#    return (r1[0] < r2[2]) and (r2[0] < r1[2]) and \
#            (r1[1] < r2[3]) and (r2[1] < r1[3])
            
def left_collision(r1, r2):
    y_mid = int(r2[1]+12.5)
    if y_mid in range(int(r1[1]-12.5),int(r1[3]+12.5)):
        if r2[0] <= r1[2]:
            return True
    return False

def right_collision(r1, r2):
    y_mid = int(r2[1]+12.5)
    if y_mid in range(int(r1[1]-12.5),int(r1[3]+12.5)):
        if r2[2] >= r1[0]:
            return True
    return False
        


def play():
    left_paddle = Paddle(0, 150)
    right_paddle = Paddle(975, 150)
    p1 = Pong()
    while True:
        clock.tick()
        pygame.draw.rect(screen, black, [0, 0, page_width, page_height])
        point = p1.move()
        left_paddle_pos = left_paddle.get_pos()
        right_paddle_pos = right_paddle.get_pos()
        pong_pos = p1.get_pos()
        
        left_paddle.show()
        right_paddle.show()
        p1.show()
        
        if point != -1:
            pygame.time.delay(1000)
            if point == 0:
                right_paddle.inc_score()
            else:
                left_paddle.inc_score()
                
        score_print = str(left_paddle.score)
        text = font.render(score_print, 1, white)
        text_pos = (50, 12)
        screen.blit(text, text_pos)
        
        score_print = str(right_paddle.score)
        text = font.render(score_print, 1, white)
        text_pos = (950, 12)
        screen.blit(text, text_pos)
        
        if left_collision(left_paddle_pos, pong_pos):
            diff = (left_paddle.y + left_paddle.height/2) - (p1.y + p1.height/2)
            diff = 20*diff/left_paddle.height
            p1.bounce(diff)
            
        if right_collision(right_paddle_pos, pong_pos):
            diff = (right_paddle.y + right_paddle.height/2) - (p1.y + p1.height/2)
            diff = 20*diff/right_paddle.height
            p1.bounce(diff)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
                
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            left_paddle.move_up()

        if keys[pygame.K_s]:
            left_paddle.move_down()

        if keys[pygame.K_i]:
            right_paddle.move_up()

        if keys[pygame.K_k]:
            right_paddle.move_down()

        pygame.display.update()
        
        if left_paddle.score == 10 or right_paddle.score == 10:
            pygame.time.delay(2000)
            break


play()
pygame.quit()
