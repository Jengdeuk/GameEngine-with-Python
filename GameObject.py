from Physics import *
from Graphics import *

class GameObject:
    def __init__(self, id, filename, speed, turn, half_lengths, position, scale, rotation):
        self.id = id
        self.graphics = Graphics(filename)
        self.physics = Physics(speed, turn, half_lengths, position, scale, rotation)

    def Update(self):
        self.physics.UpdateOrientationMatrix()

    def Render(self):
        # Mesh & Texture
        self.physics.PushTransformMatrix()
        self.graphics.Render()
        self.physics.PopMatrix()

        # Collider
        vertices, edges = self.physics.PushOBBMatrix()
        self.graphics.RenderOBB(vertices, edges)
        self.physics.PopMatrix()