import pygame
import numpy as np

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def load_obj(obj_name, tex_name):
    vertices = []
    texcoords = []
    faces = []

    with open(obj_name, "r") as file:
        for line in file:
            if line.startswith("v "):
                vertices.append(list(map(float, line[2:].split())))
            elif line.startswith("vt "):
                texcoords.append(list(map(float, line[3:].split()[:2])))
            elif line.startswith("f "):
                faces.append([list(map(int, vertex.split('/'))) for vertex in line[2:].split()])

    texture = glGenTextures(1)
    texture_data = pygame.image.load(tex_name)
    texture_surface = pygame.image.tostring(texture_data, 'RGB', 1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture_data.get_width(), texture_data.get_height(), 0,
                 GL_RGB, GL_UNSIGNED_BYTE, texture_surface)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return vertices, texcoords, faces, texture

def draw_grid(size, step):
    glBegin(GL_LINES)
    glColor3f(0, 0.5, 0)  # 그리드 색상

    for i in range(-size, size + 1, step):
        glVertex3f(i, 0, -size)
        glVertex3f(i, 0, size)

        glVertex3f(-size, 0, i)
        glVertex3f(size, 0, i)

    glEnd()