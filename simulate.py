import pygame
import random
import os

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


class Pipe:

    def __init__(self, pipe_img, isInverted, height, screen_dim):
        # constants
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = screen_dim
        self.img = pipe_img
        if isInverted:
            self.img = pygame.transform.flip(self.img, False, True)
        self.width = self.img.get_width()
        self.height = height
        self.img = pygame.transform.scale(self.img, (self.width, self.height))
        self.y = 0 if isInverted else self.SCREEN_HEIGHT - self.height
        # vars
        self.x = self.SCREEN_WIDTH - self.width
        self.has_added = False  # used in driver class AllPipes

    def move(self, pipe_speed):
        self.x -= pipe_speed

    def get_rect(self):
        rect = self.img.get_rect()
        rect.move(self.x, self.y)
        return rect

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    # def draw(self, screen):
    #     self.screen.blit(self.img, (round(self.x), round(self.y)))

    def used_to_add(self):
        self.has_added = True


class AllPipes:

    def __init__(self, screen_dim):
        """
        Initializes attributes of AllPipes class
        """
        # constants
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = screen_dim
        self.pipe_img = pygame.image.load("imgs/pipe.png")
        self.left_lim = self.SCREEN_WIDTH // 2
        self.pipe_speed = 3
        self.gap_size = 120
        self.gap_buffer = 30
        self.pass_buffer = 27
        # vars
        self.pipes = []

    def add(self):
        """
        Appends a pair of pipes to the game
        Each pipe is a Pipe object
        """
        h = random.randint(self.gap_buffer, self.SCREEN_HEIGHT - self.gap_size - self.gap_buffer)
        pipe_top = Pipe(self.pipe_img, True, h, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pipe_bot = Pipe(self.pipe_img, False, self.SCREEN_HEIGHT - h - self.gap_size, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        # append as a pair
        self.pipes.append((pipe_top, pipe_bot))

    def shift(self):
        """
        Moves all pipes left
        """
        for pair in self.pipes:
            pair[0].move(self.pipe_speed)
            pair[1].move(self.pipe_speed)

    def add_del(self, bird):
        """
        Input bird to compare against
        Adds pipes for each pair that passes benchmark
        Updates score of bird if it passes the pipe
        Deletes pipe once it goes off screen
        """
        # skip every other pipe (pairs)
        for pair in self.pipes:
            # for this purpose, we can just use one element of pair
            e = pair[0]
            # add new pipe for each existing pipe passing benchmark
            if e.x <= self.left_lim and not e.has_added:
                e.used_to_add()
                self.add()
            # if bird has passed it
            if e.x + e.width + self.pass_buffer <= bird.x:
                # add to bird's score
                bird.add_score()
            if e.x + e.width <= 0:
                # remove pair
                self.pipes.remove(pair)

    def isCollision(self, bird):
        """
        Updates collision status of the bird, static after one collision
        Uses pixel perfect collisions
        If bird.has_collided is True, do nothing
        If bird.has_collided is False, check if it has just collided
        """
        if not bird.has_collided:
            for pair in self.pipes:
                offset_top = (round(pair[0].x - bird.x), round(pair[0].y - bird.y))
                offset_bot = (round(pair[1].x - bird.x), round(pair[1].y - bird.y))
                t_point = bird.get_mask().overlap(pair[0].get_mask(), offset_top)
                b_point = bird.get_mask().overlap(pair[1].get_mask(), offset_bot)

                if t_point or b_point:
                    bird.has_collided = True

    def draw(self, screen):
        """
        Input screen
        Draws pipes onto screen
        """
        for pair in self.pipes:
            for e in pair:
                screen.blit(e.img, (e.x, e.y))

    def update(self, bird, screen):
        self.shift()
        self.add_del(bird)
        self.isCollision(bird)
        self.draw(screen)

    def get_neural_input(self, bird):
        """
        Returns neural input for bird's NN to make a decision
        neural input [del_x, bird.y, bird.vy, y of bottom of top pipe, y of top of bottom pipe]
        Reverses pipes list and locates first pipe in front of the bird
        """
        del_x = 0
        pipe_y_top = 0
        pipe_y_bot = 0
        for pair in reversed(self.pipes):
            if pair[0].x >= bird.x:
                del_x = pair[0].x - bird.x
                pipe_y_top = pair[0].height
                pipe_y_bot = self.SCREEN_HEIGHT - pair[0].height
        return [del_x, bird.y, bird.vy, pipe_y_top, pipe_y_bot]


class Game:

    def __init__(self, population):
        self.run = True
        self.population = population

    def get_population(self):
        return self.population

    def main_loop(self):

        pygame.init()
        WIDTH, HEIGHT = 700, 700
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        screen.fill(white)

        bg = pygame.image.load(os.path.join(os.getcwd(), "imgs/bg.png"))
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

        obstacles = AllPipes(screen.get_size())
        obstacles.add()
        while self.run:
            pygame.time.delay(5)
            screen.fill(white)
            screen.blit(bg, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            for bird in self.population:
                # locate first bird that has not collided
                if bird.has_collided:
                    continue
                input = obstacles.get_neural_input(bird)
                bird.update(input, screen)
                obstacles.update(bird, screen)

            num_dead = 0
            for bird in self.population:
                if bird.has_collided:
                    num_dead += 1
            if num_dead == len(self.population):
                self.run = False

            pygame.display.update()
