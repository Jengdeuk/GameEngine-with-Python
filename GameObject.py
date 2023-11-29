import pygame
import numpy as np

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from Physics import *
from Graphics import *

class GameObject:
    def __init__(self, id, filename, half_lengths, position=[0, 0, 0], scale=[1, 1, 1], rotation=[0, 0, 0]):
        self.id = id
        objpath = "Resources/Model/" + filename + ".obj"
        texpath = "Resources/Model/" + filename + ".jpg"
        self.vertices, self.texcoords, self.faces, self.texture = load_obj(objpath, texpath)
        self.position = np.array(position)
        self.scale = np.array(scale)
        self.rotation = np.array(rotation)
        self.half_lengths = np.array(half_lengths)
        self.orientation = np.array(np.identity(3))

    def update(self):
        pass

    def render(self):
        glPushMatrix()

        glTranslatef(*self.position)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        glScalef(*self.scale)

        glEnable(GL_TEXTURE_2D)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        
        glEnable(GL_DEPTH_TEST)
        glClear(GL_DEPTH_BUFFER_BIT)

        for face in self.faces:
            if len(face) == 3:
                glBegin(GL_TRIANGLES)
            else:
                glBegin(GL_QUADS)
            for vertex in face:
                vertex_index, texture_index, _ = vertex
                glTexCoord2fv(self.texcoords[texture_index - 1])
                glVertex3fv(self.vertices[vertex_index - 1])
            glEnd()

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glDisable(GL_TEXTURE_2D)

        glPopMatrix()

    def draw_obb(self):
        glPushMatrix()

        glTranslatef(*self.position)
        rotation_matrix = np.eye(4)
        rotation_matrix[:3, :3] = self.orientation
        glMultMatrixf(rotation_matrix.flatten())

        half_lengths = self.half_lengths
        vertices = [
            [-half_lengths[0], -half_lengths[1], -half_lengths[2]],
            [half_lengths[0], -half_lengths[1], -half_lengths[2]],
            [half_lengths[0], half_lengths[1], -half_lengths[2]],
            [-half_lengths[0], half_lengths[1], -half_lengths[2]],
            [-half_lengths[0], -half_lengths[1], half_lengths[2]],
            [half_lengths[0], -half_lengths[1], half_lengths[2]],
            [half_lengths[0], half_lengths[1], half_lengths[2]],
            [-half_lengths[0], half_lengths[1], half_lengths[2]],
        ]

        edges = (
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        )

        glBegin(GL_LINES)
        glColor3f(1, 0, 0)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()

        glPopMatrix()