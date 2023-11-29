import pygame
import numpy as np

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from Physics import *
from Graphics import *

def calculate_distance(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))

class Camera:
    def __init__(self, position=(0, 0, 5), target=(0, 0, 0), up=(0, 1, 0)):
        self.position = list(position)
        self.target = list(target)
        self.up = list(up)

    def apply(self):
        gluLookAt(*self.position, *self.target, *self.up)