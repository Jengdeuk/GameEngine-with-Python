import pygame
import numpy as np

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from GameObject import *

class Player(GameObject):
    def __init__(self, id, filename, half_lengths, position=[0, 0, 0], scale=[1, 1, 1], rotation=[0, 0, 0], speed=0.2):
        super().__init__(id, filename, half_lengths, position, scale, rotation)
        self.speed = speed
        self.turn = 25
        self.forward = np.array([0.0, 0.0, 1.0])

    def update(self):
        keys = pygame.key.get_pressed()

        # Turn
        if keys[K_LEFT]:
            self.rotation[1] += self.turn
        if keys[K_RIGHT]:
            self.rotation[1] -= self.turn

        # Go_Straight
        if keys[K_UP]:
            self.position += rotate_vector(self.forward, self.rotation) * self.speed
        if keys[K_DOWN]:
            self.position -= rotate_vector(self.forward, self.rotation) * self.speed

        self.orientation = update_orientation(rotate_vector(self.forward, self.rotation))