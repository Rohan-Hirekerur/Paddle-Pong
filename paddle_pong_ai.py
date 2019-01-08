import pygame
import pyglet
import math
from random import randrange
import numpy as np
import tensorflow as tf
#from trainer.helpers import discount_rewards, prepro

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

pygame.init()
page_width = 500
page_height = 250
size = page_width, page_height
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Paddle Pong")
pygame.display.update()
clock = pyglet.clock.Clock()
clock.set_fps_limit(60)
font = pygame.font.Font(None, 25)

observations = tf.placeholder(shape=None, dtype=tf.float32)
actions = tf.placeholder(shape=None, dtype=tf.int32)
rewards = tf.placeholder(shape=None, dtype=tf.float32)


def cnn(X):
    W_conv1 = tf.Variable(tf.truncated_normal([5, 5, 1, 2]))
    W_conv2 = tf.Variable(tf.truncated_normal([5, 5, 2, 4]))
    W_fc = tf.Variable(tf.truncated_normal([125*63*4, 300]))
    W_out = tf.Variable(tf.truncated_normal([300, 3]))

    B_conv1 = tf.Variable(tf.truncated_normal([32]))
    B_conv2 = tf.Variable(tf.truncated_normal([64]))
    B_fc = tf.Variable(tf.truncated_normal([300]))
    B_out = tf.Variable(tf.truncated_normal([3]))

    X = X.astype(dtype=np.float32)
    X = tf.reshape(X, shape=[-1, 500, 250, 1])

    conv1 = tf.nn.conv2d(X, W_conv1, strides=[1, 1, 1, 1], padding='SAME')
    conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    conv2 = tf.nn.conv2d(conv1, W_conv2, strides=[1, 1, 1, 1], padding='SAME')
    conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    fc = tf.reshape(conv2, [-1, 125*63*4])
    fc = tf.nn.relu(tf.matmul(fc, W_fc) + B_fc)

    out = tf.matmul(fc, W_out) + B_out

    return out


class Paddle:
    speed = 10
    height = 75
    width = 12.5
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
        self.speed = 5
        self.height = 12.5
        self.width = 12.5
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
        self.speed = 5
        if randrange(2) == 0:
            self.direction += 180
        pygame.draw.rect(screen, white, [self.x, self.y, self.width, self.height])

    def bounce(self):
        self.direction = (180 - self.direction) % 360
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
            self.direction = (360 - self.direction) % 360

        if self.y > page_height - self.height:
            self.direction = (360 - self.direction) % 360

        return -1


# def left_collision(r1, r2):
#    return (r1[0] < r2[2]) and (r2[0] < r1[2]) and \
#            (r1[1] < r2[3]) and (r2[1] < r1[3])

def left_collision(r1, r2):
    y_mid = int(r2[1] + 6.25)
    if y_mid in range(int(r1[1] - 6.25), int(r1[3] + 6.25)):
        if r2[0] <= r1[2]:
            return True
    return False


def right_collision(r1, r2):
    y_mid = int(r2[1] + 6.25)
    if y_mid in range(int(r1[1] - 6.25), int(r1[3] + 6.25)):
        if r2[2] >= r1[0]:
            return True
    return False


def play():
    obvs = []
    acs = []
    rews = []
    prev_pix = pygame.surfarray.array2d(screen)
    prediction = cnn(prev_pix)
    sample = tf.multinomial(prediction, num_samples=1)
    print(sample)
    print(tf.one_hot(sample, 3))
    print(actions)
    print(tf.one_hot(actions, 3))
    cross_entropies = tf.losses.softmax_cross_entropy(onehot_labels=tf.one_hot(actions, 3), logits=prediction)
    loss = tf.reduce_sum(rewards * cross_entropies)
    optimizer = tf.train.RMSPropOptimizer(learning_rate=0.1, decay=0.99)
    train_op = optimizer.minimize(loss)

    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(init)
        left_paddle = Paddle(0, 75)
        right_paddle = Paddle(487, 75)
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

            score_print = str(left_paddle.score)
            text = font.render(score_print, 1, white)
            text_pos = (50, 12)
            screen.blit(text, text_pos)

            score_print = str(right_paddle.score)
            text = font.render(score_print, 1, white)
            text_pos = (488, 12)
            screen.blit(text, text_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

#            keys = pygame.key.get_pressed()
            curr_pix = pygame.surfarray.array2d(screen)
            observation = curr_pix - prev_pix
            prev_pix = curr_pix

            action = sess.run(sample, feed_dict={observations: [observation]})
            #print(action)

            if p1.y + p1.height / 2 < left_paddle.y + left_paddle.height/2 and p1.x < page_width/3:
                left_paddle.move_up()

            if p1.y + p1.height / 2 > left_paddle.y + left_paddle.height/2 and p1.x < page_width/3:
                left_paddle.move_down()

            if action[0] == [0]:
                right_paddle.move_up()

            if action[0] == [2]:
                right_paddle.move_down()

            if left_collision(left_paddle_pos, pong_pos) or right_collision(right_paddle_pos, pong_pos):
                p1.bounce()

            reward = [0]

            if point != -1:
                #pygame.time.delay(500)
                if point == 0:
                    right_paddle.inc_score()
                    reward = [1]
                else:
                    left_paddle.inc_score()
                    reward = [-1]

            pygame.display.update()

            acs.append(action)
            obvs.append(observation)
            rews.append(reward)

            if left_paddle.score == 3 or right_paddle.score == 3:
                #pygame.time.delay(2000)
                break

    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(init)
        sess.run(train_op, feed_dict={observations: obvs, actions: acs, rewards: rews})


for i in range(0, 100):
    play()
pygame.quit()
