import sys
import pygame
import numpy as np

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from Physics import *
from Graphics import *

from Camera import *
from GameObject import *
from Player import *
from Fish import *

def main():
    pygame.init()
    width, height = 800, 600
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Project3# Game Engine")
    gluPerspective(45, (width / height), 0.1, 50.0)
    camera = Camera(position=(0, 5, 7), target=(0, 0, 0), up=(0, 1, 0))
    camera.apply()

    objects = [
        Player(1, "Umbreon", [0.5, 1.0, 1.0], position=[0.0, 0.0, -1.0], scale=[0.5, 0.5, 0.5]),
        Fish(2, "fish", [0.5, 0.5, 0.5], position=[3.0, 0.0, -1.0], scale=[0.15, 0.15, 0.15]),
        Fish(2, "fish", [0.5, 0.5, 0.5], position=[-3.0, 0.0, -1.0], scale=[0.15, 0.15, 0.15]),
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        glClearColor(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        draw_grid(size=20, step=1)

        objects.sort(key=lambda obj: calculate_distance(obj.position, camera.position), reverse=True)

        for obj in objects:
            obj.update()
            obj.render()
            obj.draw_obb()

        for obj in objects:
            if obj.id != 1:
                continue
            for fish in objects:
                if fish.id == 1:
                    continue
                if obb_collision(obj, fish):
                    objects.remove(fish)

        pygame.display.flip()

if __name__ == "__main__":
    main()