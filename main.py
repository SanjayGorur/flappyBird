import pygame
import random
import os

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

class Player:

    def __init__(self, player_img, screen):
        # constants
        self.screen = screen
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = screen.get_size()
        self.img = player_img
        self.x = self.SCREEN_WIDTH // 4
        self.g = 0.45
        self.jump_vel = -10
        # vars
        self.y = self.SCREEN_HEIGHT // 2
        self.vy = 0

    def move(self):
        self.vy += self.g
        self.y += self.vy

    def jump(self):
        self.vy = self.jump_vel

    def get_rect(self):
        rect = self.img.get_rect()
        rect.move(self.x, self.y) # move rectangle to position
        return rect

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def draw(self):
        self.screen.blit(self.img, (self.x, self.y))
        # debug, draw mask outline
        # pygame.draw.lines(screen, (200, 150, 150), 1, self.get_mask().outline())

    def update(self):
        self.move()
        self.draw()

class Pipe:

    def __init__(self, pipe_img, isInverted, height, screen):
        # constants
        self.screen = screen
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = screen.get_size()
        self.img = pipe_img
        if isInverted:
            self.img = pygame.transform.flip(self.img, False, True)
        self.width = self.img.get_width()
        self.height = height
        self.img = pygame.transform.scale(self.img, (self.width, self.height))
        self.y = 0 if isInverted else self.SCREEN_HEIGHT - self.height
        # vars
        self.x = self.SCREEN_WIDTH - self.width
        self.has_added = False # used in driver class AllPipes

    def move(self, pipe_speed):
        self.x -= pipe_speed

    def get_rect(self):
        rect = self.img.get_rect()
        rect.move(self.x, self.y)
        return rect

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def draw(self):
        self.screen.blit(self.img, (round(self.x), round(self.y)))
        # debug, draw mask
        # pygame.draw.polygon(screen, (200, 150, 150),self.get_mask().outline(), 0)

    def used_to_add(self):
        self.has_added = True


class AllPipes:

    def __init__(self, pipe_img, screen):
        # constants
        self.screen = screen
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = screen.get_size()
        self.pipe_img = pipe_img
        self.left_lim = self.SCREEN_WIDTH // 2
        self.pipe_speed = 3
        self.gap_size = 120
        self.gap_buffer = 30
        self.pass_buffer = 27
        # vars
        self.pipes = []

    def add(self):
        h = random.randint(self.gap_buffer, self.SCREEN_HEIGHT - self.gap_size - self.gap_buffer)
        pipe_top = Pipe(self.pipe_img, True, h, self.screen)
        pipe_bot = Pipe(self.pipe_img, False, self.SCREEN_HEIGHT - h - self.gap_size, self.screen)
        # append as a pair
        self.pipes.append((pipe_top, pipe_bot))

    def shift(self):
        for pair in self.pipes:
            pair[0].move(self.pipe_speed)
            pair[1].move(self.pipe_speed)

    def add_del(self, player):
        # skip every other pipe (pairs)
        for pair in self.pipes:
            # for this purpose, we can just use one element of pair
            e = pair[0]
            # add new pipe for each existing pipe passing benchmark
            if e.x <= self.left_lim and not e.has_added:
                e.used_to_add()
                self.add()
            # delete pipe if player has passed it
            if e.x + e.width + self.pass_buffer <= player.x:
                # remove pair
                self.pipes.remove(pair)


    def isCollision(self, player):
        # pixel perfect collisions
        for pair in self.pipes:
            offset_top = (round(pair[0].x - player.x), round(pair[0].y - player.y))
            offset_bot = (round(pair[1].x - player.x), round(pair[1].y - player.y))
            t_point = player.get_mask().overlap(pair[0].get_mask(), offset_top)
            b_point = player.get_mask().overlap(pair[1].get_mask(), offset_bot)

            if t_point or b_point:
                # if t_point is not None:
                #     pygame.draw.circle(screen, red, (t_point[0] + player.x, t_point[1] + player.y), 10)
                # if b_point is not None:
                #     pygame.draw.circle(screen, red, (b_point[0] + player.x, b_point[1] + player.y), 10)
                return True

        return False

    def draw(self):
        for pair in self.pipes:
            for e in pair:
                self.screen.blit(e.img, (e.x, e.y))

    def update(self, player):
        self.shift()
        self.add_del(player)
        isCollided = self.isCollision(player)
        self.draw()
        return isCollided

class Game:

    def __init__(self):
        self.run = True

    def main_loop(self):

        pygame.init()
        WIDTH, HEIGHT = 700, 700
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        screen.fill(white)

        bg = pygame.image.load(os.path.join(os.getcwd(), "imgs/bg.png"))
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

        bird = Player(pygame.image.load("imgs/bird1.png"), screen)
        obstacles = AllPipes(pygame.image.load("imgs/pipe.png"), screen)
        obstacles.add()
        while self.run:
            pygame.time.delay(5)
            screen.fill(white)
            screen.blit(bg, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.run = False
                    if event.key == pygame.K_SPACE:
                        bird.jump()

            bird.update()
            isCollided = obstacles.update(bird)
            if isCollided:
                self.run = False

            pygame.display.update()

def message_to_screen(text, color, x, y):
    font = pygame.font.SysFont(None, 30)
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, (x, y))

if __name__ == "__main__":
    g = Game()
    g.main_loop()
