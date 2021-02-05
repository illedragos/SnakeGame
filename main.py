import sys
import time

import pygame
import random

import pygame as pygame
from pygame import Vector2
from os import path

SPEED = 150

def draw_game_over():
    game_over_text = "GAME OVER"
    game_over_surface = game_font_superbig.render(game_over_text, True, (156, 102, 12))
    screen.blit(game_over_surface, (470, 420))
    pygame.display.update()
    time.sleep(1.5)

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load('img/HEAD_UP.png').convert_alpha()
        self.head_up = pygame.transform.scale(self.head_up, (CELL_SIZE, CELL_SIZE))
        self.head_down = pygame.image.load('img/HEAD_DOWN.png').convert_alpha()
        self.head_down = pygame.transform.scale(self.head_down, (CELL_SIZE, CELL_SIZE))
        self.head_right = pygame.image.load('img/HEAD_RIGHT.png').convert_alpha()
        self.head_right = pygame.transform.scale(self.head_right, (CELL_SIZE, CELL_SIZE))
        self.head_left = pygame.image.load('img/HEAD_LEFT.png').convert_alpha()
        self.head_left = pygame.transform.scale(self.head_left, (CELL_SIZE, CELL_SIZE))

        self.tail_up = pygame.image.load('img/TAIL_UP.png').convert_alpha()
        self.tail_up = pygame.transform.scale(self.tail_up, (CELL_SIZE, CELL_SIZE))
        self.tail_down = pygame.image.load('img/TAIL_DOWN.png').convert_alpha()
        self.tail_down = pygame.transform.scale(self.tail_down, (CELL_SIZE, CELL_SIZE))
        self.tail_right = pygame.image.load('img/TAIL_RIGHT.png').convert_alpha()
        self.tail_right = pygame.transform.scale(self.tail_right, (CELL_SIZE, CELL_SIZE))
        self.tail_left = pygame.image.load('img/TAIL_LEFT.png').convert_alpha()
        self.tail_left = pygame.transform.scale(self.tail_left, (CELL_SIZE, CELL_SIZE))

        self.body_vertical = pygame.image.load('img/CENTER_UP_DOWN.png').convert_alpha()
        self.body_vertical = pygame.transform.scale(self.body_vertical, (CELL_SIZE, CELL_SIZE))
        self.body_horizontal = pygame.image.load('img/CENTER_LEFT_RIGHT.png').convert_alpha()
        self.body_horizontal = pygame.transform.scale(self.body_horizontal, (CELL_SIZE, CELL_SIZE))

        self.body_top_right = pygame.image.load('img/TURN3.png')
        self.body_top_right = pygame.transform.scale(self.body_top_right, (CELL_SIZE, CELL_SIZE))
        self.body_top_left = pygame.image.load('img/TURN4.png')
        self.body_top_left = pygame.transform.scale(self.body_top_left, (CELL_SIZE, CELL_SIZE))
        self.body_buttom_left = pygame.image.load('img/TURN2.png')
        self.body_buttom_left = pygame.transform.scale(self.body_buttom_left, (CELL_SIZE, CELL_SIZE))
        self.body_buttom_right = pygame.image.load('img/TURN1.png')
        self.body_buttom_right = pygame.transform.scale(self.body_buttom_right, (CELL_SIZE, CELL_SIZE))

        self.chew_sound = pygame.mixer.Sound('sound/chew.wav')
        self.highscore_sound = pygame.mixer.Sound('sound/i_feel_good.wav')
        self.game_over_sound = pygame.mixer.Sound('sound/game_over.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_top_left, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_buttom_left, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_top_right, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_buttom_right, block_rect)
        # for block in self.body:
        # snake_block_rect = pygame.Rect(int(block.x*CELL_SIZE), int(block.y*CELL_SIZE), CELL_SIZE,CELL_SIZE)
        # pygame.draw.rect(screen,(183,101,122),snake_block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]  # first element to last element before the last
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.chew_sound.play()

    def play_highscore_sound(self):
        self.highscore_sound.play()

    def play_game_over_sound(self):
        self.game_over_sound.play()
        draw_game_over()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        # we don't have to reset the score because the score checks how long the snake is


class Fruit:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)

        screen.blit(fruit_list[self.random_nr], fruit_rect)
        # pygame.draw.rect(screen,(126,166,114),fruit_rect)

    def randomize(self):
        global SPEED
        SPEED = SPEED - 10
        pygame.time.set_timer(SCREEN_UPDATE, SPEED)
        self.x = random.randint(2, CELL_NUMBERY - 3)
        self.y = random.randint(2, CELL_NUMBER - 3)
        self.random_nr = random.randint(0, 5)
        self.pos = pygame.math.Vector2(self.x, self.y)


class MAIN():
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        self.draw_high_score()
        self.draw_credentials()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:  # check if fruit is over the snake without head
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        # if self.snake.body[1].y== CELL_NUMBER-1:
        #   pass
        # else:
        if not 2 <= self.snake.body[0].x < CELL_NUMBERY - 2 or not 2 <= self.snake.body[0].y < CELL_NUMBER - 2:
            self.snake.play_game_over_sound()
            self.game_over()

        for block in self.snake.body[1:]:  # elements after the head
            if block == self.snake.body[0]:
                if (self.snake.direction.x == 0 and self.snake.direction.y == 0):
                    pass
                else:
                    self.snake.play_game_over_sound()
                self.game_over()

    def game_over(self):
        global SPEED
        SPEED = 150
        pygame.time.set_timer(SCREEN_UPDATE, SPEED)
        self.snake.reset()
        # pygame.quit()
        # sys.exit()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(CELL_NUMBER):
            if row % 2 == 0:
                for col in range(CELL_NUMBERY):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(CELL_NUMBERY):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, grass_color, grass_rect)
        for row in range(CELL_NUMBER):
            for col in range(CELL_NUMBERY):
                if row == 0 or row == CELL_NUMBER - 1 or row == 1 or row == CELL_NUMBER - 2:
                    tower = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, (224, 224, 224), tower)
                if col == 0 or col == CELL_NUMBERY - 1 or col == 1 or col == CELL_NUMBERY - 2:
                    tower = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, (224, 224, 224), tower)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        my_file = open('highscore.txt', 'r')
        data = my_file.readlines()
        my_file.close()
        if len(self.snake.body) - 3 > int(data[0]):
            my_file = open('highscore.txt', 'w')
            self.snake.play_highscore_sound()
            my_file.write(str(len(self.snake.body) - 3))
            my_file.close()

        score_surface = game_font.render("SCORE:" + score_text, True, (56, 74, 12))
        score_x = int(CELL_SIZE * CELL_NUMBER - 60)
        score_y = int(CELL_SIZE * CELL_NUMBER - 60)
        score_rect = score_surface.get_rect(center=(1350, 50))
        apple_rect = apple.get_rect(midleft=(score_rect.left + 130, score_rect.y - 10))
        # bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 150, apple_rect.height + 30)

        # pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(fruits, apple_rect)
        # pygame.draw.rect(screen, (255, 255, 255), bg_rect, 2)

    def draw_high_score(self):
        my_file = open('highscore.txt', 'r')
        high_score_text = "HIGH SCORE :" + my_file.read()
        my_file.close()
        high_score_surface = game_font.render(high_score_text, True, (56, 122, 12))
        screen.blit(high_score_surface, (110, 35))


    def draw_credentials(self):
        credential_text = "Made by DragoShell"
        credential1_surface = game_font_big.render(credential_text, True, (56, 122, 12))
        screen.blit(credential1_surface, (600, 15))

        snake_long_rect = pygame.Rect(int(9 * CELL_SIZE), int(16 * CELL_SIZE), CELL_SIZE * 2, CELL_SIZE * 2)
        screen.blit(snake_long, snake_long_rect)


CELL_SIZE = 55
CELL_NUMBER = 18
CELL_NUMBERY = 32
FRAMERATE = 360

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

pygame.display.set_caption('Snake made by Dragoshell')
programIcon = pygame.image.load('img/snake_img_bar.png')
pygame.display.set_icon(programIcon)

screen = pygame.display.set_mode(((CELL_NUMBERY) * CELL_SIZE, CELL_NUMBER * CELL_SIZE))
clock = pygame.time.Clock()

apple = pygame.image.load('img/apple.png').convert_alpha()
apple = pygame.transform.scale(apple, (CELL_SIZE, CELL_SIZE))
mango = pygame.image.load('img/mango.png').convert_alpha()
mango = pygame.transform.scale(mango, (CELL_SIZE, CELL_SIZE))
strawberry = pygame.image.load('img/strawberry.png').convert_alpha()
strawberry = pygame.transform.scale(strawberry, (CELL_SIZE, CELL_SIZE))
banana = pygame.image.load('img/banana.png').convert_alpha()
banana = pygame.transform.scale(banana, (CELL_SIZE, CELL_SIZE))
orange = pygame.image.load('img/orange.png').convert_alpha()
orange = pygame.transform.scale(orange, (CELL_SIZE, CELL_SIZE))
blackberry = pygame.image.load('img/blackberry.png').convert_alpha()
blackberry = pygame.transform.scale(blackberry, (CELL_SIZE, CELL_SIZE))
snake_long = pygame.image.load('img/snake_long.png').convert_alpha()
snake_long = pygame.transform.scale(snake_long, (CELL_SIZE * 14, CELL_SIZE * 2))
fruits = pygame.image.load('img/fruits.png').convert_alpha()
fruits = pygame.transform.scale(fruits, (CELL_SIZE * 4, CELL_SIZE * 2))

fruit_list = [apple, mango, strawberry, banana, orange, blackberry]
fruits_list = [pygame.transform.scale(fruit, (CELL_SIZE, CELL_SIZE)) for fruit in fruit_list]

# for fruit in fruit_list:
# fruit = pygame.transform.scale(fruit, (CELL_SIZE, CELL_SIZE))

# for i, e in enumerate(elements):
#   if want_to_change_this_element(e):
#      elements[i] = "%{}%".format(e)

game_font = pygame.font.SysFont('gadugi', 30)
game_font_big = pygame.font.SysFont('leelawadeeuisemilight', 60)
game_font_superbig = pygame.font.SysFont('georgia', 120)
# snake_body_png = pygame.image.load(('img/CENTER_LEFT_RIGHT.png'))
# snake_body_png = pygame.transform.scale(snake_body_png, (CELL_SIZE, CELL_SIZE))

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, SPEED)

main_game = MAIN()

while True:
    # here we are going to draw all our elements, snake, fruits...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # pygame.QUIT close the window by pressing the X button
            pygame.quit()
            sys.exit()  # ends any kind of code that it's being run on
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
    # screen.fill(pygame.Color('gold'))
    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(FRAMERATE)

