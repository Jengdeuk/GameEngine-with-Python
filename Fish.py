import pygame
import numpy as np

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from GameObject import *

class Fish(GameObject):
    def __init__(self, id, filename, half_lengths, position=[0, 0, 0], scale=[1, 1, 1], rotation=[0, 0, 0], speed=0.1):
        super().__init__(id, filename, half_lengths, position, scale, rotation)
        self.speed = speed
        self.turn = 15
        self.forward = np.array([0.0, 0.0, 1.0])

    def update(self):
        self.rotation[1] += self.turn

        self.orientation = update_orientation(rotate_vector(self.forward, self.rotation))