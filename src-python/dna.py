import tensorflow as tf
import numpy as np
import pygame
import random


class DNA:

    def __init__(self, screen_dim):
        """
        Initializes attributes of DNA
        Input screen_dim tuple for size of screen
        self.has_collided: False if no collision occured yet, True otherwise
        self.model: brain
            5 -> hidden layer () -> 1 (sigmoid, > 0.5 then jump)
        self.fitness: calculated based on self.score
        """
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = screen_dim
        self.img = pygame.image.load("imgs/bird1.png")
        self.x = self.SCREEN_WIDTH // 4
        self.y = self.SCREEN_HEIGHT // 2
        self.vy = 0
        self.v_jump = -8
        self.g = 0.45
        self.score = 1
        self.has_collided = False
        # AI
        self.num_hidden_layers = 10
        self.model = None
        with tf.device("/cpu:0"):
            self.model = tf.keras.Sequential([
                tf.keras.layers.Dense(self.num_hidden_layers, activation='relu', input_shape=(5,)),
                tf.keras.layers.Dense(1, activation='sigmoid')])
        self.fitness = 0

    def move(self):
        """
        Natural motion of bird falling
        Discretized kinematics
        """
        self.vy += self.g
        self.y += self.vy

    def jump(self):
        """
        Jumping mechanism
        Velocity set to fixed negative value
        """
        self.vy = self.v_jump

    def get_rect(self):
        """
        Returns frame for object
        """
        rect = self.img.get_rect()
        rect.move(self.x, self.y)
        return rect

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def on_screen(self,):
        """
        Blocks player from going off the screen
        Avoids edge buffering by setting velocity to 0 at bottom
        """
        if self.y + self.img.get_height() >= self.SCREEN_HEIGHT:
            self.y = self.SCREEN_HEIGHT - self.img.get_height()
            self.vy = 0  # avoids edge buffering
        elif self.y <= 0:
            self.y = 0

    def add_score(self):
        self.score += 1

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def update(self, input, screen):
        """
        Updates bird position
        Brain (neural net) is used to decide whether to jump or not based on positional data
        """

        self.move()
        if self.think(input):
            self.jump()
        self.draw(screen)
        self.on_screen()

    def think(self, neural_input):
        """
        Input is neural_input [del_x, player.y, player.vy, y of bottom of top pipe, y of top of bottom pipe]
        Returns prediction : > 0.5, jump
        """
        with tf.device("/cpu:0"):
            neural_input = np.asarray(neural_input)
            neural_input = np.atleast_2d(neural_input)
            output = self.model.predict(neural_input)
            if output[0] > 0.5:
                return True
            return False

    def mutate(self, mutation_rate):
        """
        Randomly changes up weights based on mutation_rate
        """
        with tf.device("/cpu:0"):
            for layerNum, layer in enumerate(self.model.layers):
                weights = layer.get_weights()[0]
                biases = layer.get_weights()[1]
                for row in weights.shape[0]:
                    for col in weights.shape[1]:
                        prob = random.uniform(0, 1)
                        if prob < mutation_rate:
                            weights[row][col] = random.random()
                self.model.layers[layerNum].set_weights(weights, biases)

    def crossover(self, parent1, parent2):
        """
        Hereditary function for crossover
        Randomly generates split gene and takes first set of genes from one parent and next set from other
        """
        with tf.device("/cpu:0"):
            weights1 = parent1.model.get_weights()
            weights2 = parent2.model.get_weights()
            new_weights = weights1
            split_layer = random.randint(0, len(weights1) - 1)
            for i in range(len(new_weights)):
                if i <= split_layer:
                    new_weights[i] = weights1[i]
                else:
                    new_weights[i] = weights2[i]
            self.model.set_weights(new_weights)
