import pygame
import random
import sys
from pygame.math import Vector2


# board properties
window_width = 600
window_height = 600
cell_size = 20
num_cells = window_width // cell_size

# colours
white = (255, 255, 255)
black = (0, 0, 0)
light_green = (0, 140, 0)
dark_green = (0, 120, 0)
background_green = (0, 80, 0)
light_blue = (0, 153, 255)
dark_blue = (0, 0, 255)
red = (255, 0, 0)

# time period for snake movement
snake_period = 100


def draw_board():
    # grid
    game_window.fill(background_green)
    for row in range(2, num_cells-2):
        if row % 2 == 0:
            for col in range(2, num_cells-2, 2):
                pygame.draw.rect(game_window, dark_green, (col*cell_size, row*cell_size, cell_size, cell_size))
            for col in range(3, num_cells - 2, 2):
                pygame.draw.rect(game_window, light_green, (col * cell_size, row * cell_size, cell_size, cell_size))
        else:
            for col in range(3, num_cells-2, 2):
                pygame.draw.rect(game_window, dark_green, (col*cell_size, row*cell_size, cell_size, cell_size))
            for col in range(2, num_cells - 2, 2):
                pygame.draw.rect(game_window, light_green, (col * cell_size, row * cell_size, cell_size, cell_size))

    # box boundary
    pygame.draw.rect(game_window, black, (2 * cell_size - 5, 2 * cell_size - 5, window_width - 4 * cell_size + 9, window_height - 4 * cell_size + 9), 8)


def redraw_window():
    draw_board()  # board
    game_window.blit(snake.return_score(), (window_width / 2 - 50, window_height - cell_size - 10))  # score
    pygame.draw.rect(game_window, red, apple.draw_apple())  # apple
    for chunk in snake.draw_snake():  # snake
        if chunk == snake.draw_snake()[0]:
            pygame.draw.rect(game_window, dark_blue, chunk)  # draws head
        else:
            pygame.draw.rect(game_window, light_blue, chunk)  # draws body
    pygame.display.update()


class Snake(object):
    def __init__(self):
        self.move_vector = Vector2(1, 0)
        self.centre = num_cells // 2
        # initial position and length (3 chunks)
        self.body = [Vector2(self.centre-2, self.centre), Vector2(self.centre-3, self.centre), Vector2(self.centre-4,
                                                                                                       self.centre)]
        self.score = 0

    def draw_snake(self):
        rect_body = []
        for chunk in self.body:
            rect = pygame.Rect(chunk[0] * cell_size, chunk[1] * cell_size, cell_size, cell_size)
            rect_body.append(rect)
        return rect_body

    def move(self):
        new_head = self.body[0] + self.move_vector  # "moves" head by creating new head position
        self.body.insert(0, new_head)
        self.body.pop()  # deletes tail position

    def add_chunk(self):
        new_head = self.body[0] + self.move_vector  # "moves" head by creating new head position
        self.body.insert(0, new_head)

    def collide_with_apple(self, apple):
        if self.body[0] == apple.position:
            apple.set_random_pos(self.body)
            self.add_chunk()
            self.score += 1

    def return_score(self):
        return score_font.render("Score: " + (str(self.score)), 1, white)

    def collide_with_boundary(self):
        if self.body[0][0] == num_cells-2 or self.body[0][0] == 1:
            self.move_vector = Vector2(0, 0)
            self.reset()
            return True
        if self.body[0][1] == num_cells-2 or self.body[0][1] == 1:
            self.move_vector = Vector2(0, 0)
            self.reset()
            return True

    def collide_with_self(self):
        for chunk in range(1, len(self.body)):
            if self.body[chunk] == self.body[0]:
                self.move_vector = Vector2(0, 0)
                self.reset()
                return True

    def reset(self):
        # resets body back to original length and position
        self.body = [Vector2(self.centre-2, self.centre), Vector2(self.centre-3, self.centre), Vector2(self.centre-4, self.centre)]
        self.move_vector = Vector2(1, 0)
        self.score = 0


class Apple(object):
    def __init__(self):
        self.position = Vector2(random.randint(3, num_cells - 3), random.randint(3, num_cells - 3))
        self.set_random_pos()

    def set_random_pos(self, snake_body=None):
        if snake_body is None:
            snake_body = []
        found = False
        while found is False:
            random_position = Vector2(random.randint(3, num_cells - 3), random.randint(3, num_cells - 3))
            if random_position not in snake_body:  # stops apple from spawning on top of snake
                self.position = Vector2(random.randint(3, num_cells - 3), random.randint(3, num_cells - 3))
                found = True

    def draw_apple(self):
        rect = pygame.Rect(self.position[0] * cell_size, self.position[1] * cell_size, cell_size, cell_size)
        return rect


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    score_font = pygame.font.SysFont("newyork", 20)
    clock = pygame.time.Clock()
    start = False

    moveSnake = pygame.USEREVENT
    pygame.time.set_timer(moveSnake, snake_period)  # only moves snake every certain time period

    game_window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Snake!")

    snake = Snake()
    apple = Apple()

    score = 0

    score_label = score_font.render("Score: 0", 1, white)  # score starts at 0

    while True:

        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                start = True

            if event.type == moveSnake and start is True:
                snake.move()
                snake.collide_with_apple(apple)
                if snake.collide_with_boundary():
                    pygame.time.wait(snake_period)  # pause before game restarts
                if snake.collide_with_self():
                    pygame.time.wait(snake_period)  # pause before game restarts

        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            start = True

        if key[pygame.K_UP] or key[pygame.K_w]:
            if snake.move_vector != Vector2(0, 1):
                snake.move_vector = Vector2(0, -1)
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            if snake.move_vector != Vector2(0, -1):
                snake.move_vector = Vector2(0, 1)
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            if snake.move_vector != Vector2(1, 0):
                snake.move_vector = Vector2(-1, 0)
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            if snake.move_vector != Vector2(-1, 0):
                snake.move_vector = Vector2(1, 0)

        redraw_window()
