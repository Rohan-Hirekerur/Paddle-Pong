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
        return [self.x, self.y, self.x + self.width, self.y + self.height]

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
        self.x = page_width / 2 - self.width / 2
        self.y = page_height / 2 - self.height / 2
        self.direction = randrange(-45, 45)
        if randrange(2) == 0:
            self.direction += 180
        pygame.draw.rect(screen, white, [self.x, self.y, self.width, self.height])

    def get_pos(self):
        return [self.x, self.y, self.x + self.width, self.y + self.height]

    def reset(self):
        self.x = page_width / 2 - self.width / 2
        self.y = page_height / 2 - self.height / 2
        self.direction = randrange(-45, 45)
        self.speed = 10
        if randrange(2) == 0:
            self.direction += 180
        pygame.draw.rect(screen, white, [self.x, self.y, self.width, self.height])

    def bounce(self):
        self.direction = (180 - self.direction) % 360
#        self.direction -= randrange(-10,10)
        self.speed *= 1.05

    def show(self):
        pygame.draw.rect(screen, white, [self.x, self.y, self.width, self.height])

    def move(self):
        direction_radians = math.radians(self.direction)

        self.x += self.speed * math.cos(direction_radians)
        self.y -= self.speed * math.sin(direction_radians)

        if self.x <= 0:
            self.direction = (180 - self.direction) % 360
            return 0

        if self.x > page_width - self.width:
            self.reset()
            return 1

        if self.y <= 0:
            self.direction = (360 - self.direction) % 360

        if self.y > page_height - self.height:
            self.direction = (360 - self.direction) % 360

        return -1


def collision(r1, r2):
    return (r1[0] < r2[2]) and (r2[0] < r1[2]) and \
           (r1[1] < r2[3]) and (r2[1] < r1[3])


def play():
    right_paddle = Paddle(975, 150)
    p1 = Pong()
    while True:
        clock.tick()
        pygame.draw.rect(screen, black, [0, 0, page_width, page_height])
        point = p1.move()
        right_paddle_pos = right_paddle.get_pos()
        pong_pos = p1.get_pos()

        right_paddle.show()
        p1.show()

        if point == 1:
            right_paddle.score = 0

        score_print = str(right_paddle.score)
        text = font.render(score_print, 1, white)
        text_pos = (950, 12)
        screen.blit(text, text_pos)

        if collision(right_paddle_pos, pong_pos):
            right_paddle.inc_score()
            p1.bounce()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        keys = pygame.key.get_pressed()

        if keys[pygame.K_i]:
            right_paddle.move_up()

        if keys[pygame.K_k]:
            right_paddle.move_down()

        pygame.display.update()


play()
pygame.quit()
