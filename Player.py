from GameObject import *

class Player(GameObject):
    def __init__(self, id, filename, speed, turn, half_lengths, position=[0, 0, 0], scale=[1, 1, 1], rotation=[0, 0, 0]):
        super().__init__(id, filename, speed, turn, half_lengths, position, scale, rotation)

    def Update(self):
        keys = pygame.key.get_pressed()

        # Move
        if keys[K_UP]:
            self.physics.MoveForward()
        if keys[K_DOWN]:
            self.physics.MoveBackward()

        # Turn
        if keys[K_LEFT]:
            self.physics.TurnLeft()
        if keys[K_RIGHT]:
            self.physics.TurnRight()

        super().Update()

    def Render(self):
        super().Render()