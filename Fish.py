from GameObject import *

class Fish(GameObject):
    def __init__(self, id, filename, speed, turn, half_lengths, position=[0, 0, 0], scale=[1, 1, 1], rotation=[0, 0, 0]):
        super().__init__(id, filename, speed, turn, half_lengths, position, scale, rotation)

    def Update(self):
        # Turn
        self.physics.TurnLeft()

        super().Update()

    def Render(self):
        super().Render()