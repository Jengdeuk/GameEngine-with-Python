import pygame

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def RenderGrid(size, step):
    glBegin(GL_LINES)
    glColor3f(0, 0.5, 0)

    for i in range(-size, size + 1, step):
        glVertex3f(i, 0, -size)
        glVertex3f(i, 0, size)

        glVertex3f(-size, 0, i)
        glVertex3f(size, 0, i)

    glEnd()

# Modeling: obj Reader
# Rendering: Texture Mapping
class Graphics:
    def __init__(self, filename):
        self.id = id
        self.objpath = "Resources/Model/" + filename + ".obj"
        self.texpath = "Resources/Texture/" + filename + ".jpg"
        self.vertices, self.texcoords, self.faces, self.texture = self.LoadObj()

    def LoadObj(self):
        vertices = []
        texcoords = []
        faces = []

        with open(self.objpath, "r") as file:
            for line in file:
                if line.startswith("v "):
                    vertices.append(list(map(float, line[2:].split())))
                elif line.startswith("vt "):
                    texcoords.append(list(map(float, line[3:].split()[:2])))
                elif line.startswith("f "):
                    faces.append([list(map(int, vertex.split('/'))) for vertex in line[2:].split()])

        texture = glGenTextures(1)
        texture_data = pygame.image.load(self.texpath)
        texture_surface = pygame.image.tostring(texture_data, 'RGB', 1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture_data.get_width(), texture_data.get_height(), 0,
                    GL_RGB, GL_UNSIGNED_BYTE, texture_surface)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return vertices, texcoords, faces, texture
    
    def Render(self):
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

    def RenderOBB(self, vertices, edges):
        glBegin(GL_LINES)
        glColor3f(1, 0, 0)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()