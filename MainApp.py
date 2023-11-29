import sys

from Camera import *
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
        Player(1, "Umbreon", 0.2, 25, [0.5, 1.0, 1.0], position=[0.0, 0.0, -1.0], scale=[0.5, 0.5, 0.5]),
        Fish(2, "fish", 0.1, 15, [0.5, 0.5, 0.5], position=[3.0, 0.0, -1.0], scale=[0.15, 0.15, 0.15]),
        Fish(2, "fish", 0.1, 15, [0.5, 0.5, 0.5], position=[-3.0, 0.0, -1.0], scale=[0.15, 0.15, 0.15]),
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Scene Update
        for obj in objects:
            obj.Update()

        # Player eats fish - id_ 1: player, 2: fish
        for player in objects:
            if player.id != 1:
                continue
            for fish in objects:
                if fish.id == 1:
                    continue
                if player.physics.OBBCollision(fish.physics):
                    objects.remove(fish)

        # Sort Objects by Camera Distance
        objects.sort(key=lambda obj: CalcuateDistance(obj.physics.position, camera.position), reverse=True)

        # Scene Render
        glClearColor(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        RenderGrid(size=20, step=1)
        for obj in objects:
            obj.Render()

        pygame.display.flip()

if __name__ == "__main__":
    main()