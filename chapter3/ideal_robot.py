from drawable import Drawable
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


class IdealRobot(Drawable):
    def __init__(self, initial_pose, color='black'):
        self._pose = initial_pose
        self._radius = 0.2
        self._color = color

    def draw(self, ax):
        x, y, theta = self._pose
        xn = x + self._radius * math.cos(theta)
        yn = y + self._radius * math.sin(theta)

        # 描画したobject
        drawn_objects = []
        # 方向を表す線分の描画
        drawn_objects.extend(ax.plot([x, xn], [y, yn], color=self._color))
        # ロボットを円として表現して描画
        robot = patches.Circle(
            xy=(x, y), radius=self._radius, fill=False, color=self._color)
        drawn_objects.append(ax.add_patch(robot))
        return drawn_objects
