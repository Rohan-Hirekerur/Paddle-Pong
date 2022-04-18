import pygame
import pyglet
import math
from consts import Colors
from random import randrange

class Paddle:
    speed = 20
    height = 150
    width = 25
    score = 0

    def __init__(self, x, y, window_width, window_height, screen):
        """create an instance of paddle and initialize coordinates

        Args:
            x (float): x coordinate of paddle's top left corner
            y (float): y coordinate of paddle's top left corner
            window_width (float): width of window in which paddle is being rendered
            window_height (float): height of window in which paddle is being rendered
            screen: pygame screen object
        """
            
        self.x = x
        self.y = y
        self.window_width = window_width
        self.window_height = window_height

        self.draw(screen)

    def get_pos(self):
        """Get the position of the paddle

        Returns:
            [top_left_x, top_left_y, bottom_right_x, bottom_right_y]: coordinates of top left and bottom right corner of paddle
        """
        return [self.x, self.y, self.x + self.width, self.y + self.height]

    def draw(self, screen):
        """Draw the paddle on to the screen

        Args:
            screen: pygame screen oject
        """
        pygame.draw.rect(screen, Colors.White.value, [
                         self.x, self.y, self.width, self.height])

    def move_up(self, screen):
        """Move the paddle up

        Args:
            screen: pygame screen oject
        """
        if self.y > 0:
            self.y -= self.speed
        self.draw(screen)

    def move_down(self, screen):
        """Move the paddle down

        Args:
            screen: pygame screen oject
        """
        if (self.y + self.height) < self.window_height:
            self.y += self.speed
        self.draw(screen)

    def inc_score(self):
        """Increment score of the paddle instance
        """
        self.score += 1


class Pong:
    speed = 10
    height = 25
    width = 25

    def __init__(self, window_width, window_height, screen):
        self.window_width = window_width
        self.window_height = window_height
        self.x = window_width / 2 - self.width / 2
        self.y = window_height / 2 - self.height / 2
        self.direction = randrange(-45, 45)
        if randrange(2) == 0:
            self.direction += 180
        self.draw(screen)

    def get_pos(self):
        return [self.x, self.y, self.x + self.width, self.y + self.height]

    def get_pos(self):
        return [self.x, self.y, self.x + self.width, self.y + self.height]

    def reset(self, screen):
        self.x = self.window_width / 2 - self.width / 2
        self.y = self.window_height / 2 - self.height / 2
        self.direction = randrange(-60, 60)
        self.speed = 10
        if randrange(2) == 0:
            self.direction += 180
        self.draw(screen)

    def bounce(self):
        self.direction = (180 - self.direction) % 360
        self.direction += randrange(-5, 5)
        if self.speed < 37:
            self.speed *= 1.05

    def draw(self, screen):
        pygame.draw.rect(screen, Colors.White.value, [
                         self.x, self.y, self.width, self.height])

    def move(self, screen):
        direction_radians = math.radians(self.direction)

        self.x += self.speed * math.cos(direction_radians)
        self.y -= self.speed * math.sin(direction_radians)

        if self.x + self.width < 0:
            self.reset(screen)
            return 0

        if self.x > self.window_width:
            self.reset(screen)
            return 1

        if self.y <= 0:
            self.direction = (360 - self.direction) % 360

        if self.y > self.window_height - self.height:
            self.direction = (360 - self.direction) % 360

        return -1

def left_collision(r1, r2):
    y_mid = int(r2[1] + 12.5)
    if y_mid in range(int(r1[1] - 12.5), int(r1[3] + 12.5)):
        if r2[0] <= r1[2]:
            return True
    return False


def right_collision(r1, r2):
    y_mid = int(r2[1] + 12.5)
    if y_mid in range(int(r1[1] - 12.5), int(r1[3] + 12.5)):
        if r2[2] >= r1[0]:
            return True
    return False


def play():

    pygame.init()
    window_width = 1000
    window_height = 500
    size = window_width, window_height
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Paddle Pong")
    pygame.display.update()
    clock = pyglet.clock.Clock()
    clock.set_fps_limit(60)
    font = pygame.font.Font(None, 50)

    left_paddle = Paddle(0, 150, window_width, window_height, screen)
    right_paddle = Paddle(975, 150, window_width, window_height, screen)
    p1 = Pong(window_width, window_height, screen)

    while True:
        clock.tick()
        pygame.draw.rect(screen, Colors.Black.value, [
                         0, 0, window_width, window_height])
        point = p1.move(screen)
        left_paddle_pos = left_paddle.get_pos()
        right_paddle_pos = right_paddle.get_pos()
        pong_pos = p1.get_pos()

        left_paddle.draw(screen)
        right_paddle.draw(screen)
        p1.draw(screen)

        if point != -1:
            pygame.time.delay(1000)
            if point == 0:
                right_paddle.inc_score()
            else:
                left_paddle.inc_score()

        score_print = str(left_paddle.score)
        text = font.render(score_print, 1, Colors.White.value)
        text_pos = (50, 12)
        screen.blit(text, text_pos)

        score_print = str(right_paddle.score)
        text = font.render(score_print, 1, Colors.White.value)
        text_pos = (950, 12)
        screen.blit(text, text_pos)

        if left_collision(left_paddle_pos, pong_pos) or right_collision(right_paddle_pos, pong_pos):
            p1.bounce()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            left_paddle.move_up(screen)

        if keys[pygame.K_s]:
            left_paddle.move_down(screen)

        if p1.y + p1.height / 2 < right_paddle.y + right_paddle.height / 2 and p1.x > (window_width - (window_width / 3)):
            right_paddle.move_up(screen)

        if p1.y + p1.height / 2 > right_paddle.y + right_paddle.height / 2 and p1.x > (window_width - (window_width / 3)):
            right_paddle.move_down(screen)

        pygame.display.update()

        if left_paddle.score == 5 or right_paddle.score == 5:
            pygame.time.delay(2000)
            break


play()
pygame.quit()
