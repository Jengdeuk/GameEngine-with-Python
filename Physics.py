import numpy as np

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Collision Detection: OBB
# Collision Detection: Moving Objects
class Physics:
    def __init__(self, speed, turn, half_lengths, position, scale, rotation):
        self.speed = speed
        self.turn = turn
        self.position = np.array(position)
        self.scale = np.array(scale)
        self.rotation = np.array(rotation)
        self.half_lengths = np.array(half_lengths)
        self.forward = np.array([0.0, 0.0, 1.0])
        self.orientation = np.array(np.identity(3))

    def OBBCollision(self, other):
        distance = other.position - self.position

        # obb1의 축을 기준으로 obb2의 좌표를 변환
        for i in range(3):
            axis = self.orientation[i]
            projection = np.abs(np.dot(distance, axis))
            extent = np.dot(other.half_lengths, np.abs(other.orientation[i]))
            if projection > self.half_lengths[i] + extent:
                return False

        # obb2의 축을 기준으로 obb1의 좌표를 변환
        for i in range(3):
            axis = other.orientation[i]
            projection = np.abs(np.dot(distance, axis))
            extent = np.dot(self.half_lengths, np.abs(self.orientation[i]))
            if projection > other.half_lengths[i] + extent:
                return False

        # 두 OBB가 겹치는 경우
        return True

    def MoveForward(self):
        self.position += self.GetForwardVector() * self.speed

    def MoveBackward(self):
        self.position -= self.GetForwardVector() * self.speed

    def TurnLeft(self):
        self.rotation[1] += self.turn

    def TurnRight(self):
        self.rotation[1] -= self.turn

    def GetForwardVector(self):
        pitch, yaw, roll = np.radians(self.rotation)

        # pitch
        rotation_matrix_pitch = np.array([
            [1, 0, 0],
            [0, np.cos(pitch), -np.sin(pitch)],
            [0, np.sin(pitch), np.cos(pitch)]
        ])

        # yaw
        rotation_matrix_yaw = np.array([
            [np.cos(yaw), 0, np.sin(yaw)],
            [0, 1, 0],
            [-np.sin(yaw), 0, np.cos(yaw)]
        ])

        # roll
        rotation_matrix_roll = np.array([
            [np.cos(roll), -np.sin(roll), 0],
            [np.sin(roll), np.cos(roll), 0],
            [0, 0, 1]
        ])

        rotation_matrix = rotation_matrix_yaw @ rotation_matrix_pitch @ rotation_matrix_roll
        return np.dot(rotation_matrix, self.forward)

    def UpdateOrientationMatrix(self):
        forward = self.GetForwardVector()

        # Calculate right and up vectors
        right = np.cross([0.0, 1.0, 0.0], forward)
        right /= np.linalg.norm(right)
        up = np.cross(forward, right)

        # Create rotation matrix
        rotation_matrix = np.array([
            [right[0], up[0], -forward[0]],
            [right[1], up[1], -forward[1]],
            [right[2], up[2], -forward[2]]
        ])

        self.orientation = rotation_matrix

    def PushTransformMatrix(self):
        glPushMatrix()

        glTranslatef(*self.position)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        glScalef(*self.scale)

    def PushOBBMatrix(self):
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

        return vertices, edges

    def PopMatrix(self):
        glPopMatrix()