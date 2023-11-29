import pygame
import numpy as np

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def obb_collision(obb1, obb2):
    # OBB 간의 상대 위치 계산
    t = obb2.position - obb1.position

    # obb1의 축을 기준으로 obb2의 좌표를 변환
    for i in range(3):
        axis = obb1.orientation[i]
        projection = np.abs(np.dot(t, axis))
        extent = np.dot(obb2.half_lengths, np.abs(obb2.orientation[i]))

        if projection > obb1.half_lengths[i] + extent:
            return False

    # obb2의 축을 기준으로 obb1의 좌표를 변환
    for i in range(3):
        axis = obb2.orientation[i]
        projection = np.abs(np.dot(t, axis))
        extent = np.dot(obb1.half_lengths, np.abs(obb1.orientation[i]))

        if projection > obb2.half_lengths[i] + extent:
            return False

    # 두 OBB가 겹치는 경우
    return True

def rotate_vector(vector, rotation):
    pitch, yaw, roll = np.radians(rotation)

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
    rotated_vector = np.dot(rotation_matrix, vector)

    return rotated_vector

def update_orientation(forward):
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

    return rotation_matrix