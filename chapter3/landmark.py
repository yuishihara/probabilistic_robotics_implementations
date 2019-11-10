from drawable import Drawable
import numpy as np


class Landmark(Drawable):
    def __init__(self, x, y):
        self._position = np.array([x, y]).T
        self._id = None

    def set_id(self, id):
        self._id = id

    def draw(self, ax):
        drawn_objects = []
        x, y = self._position[0], self._position[1]
        drawn_objects.append(ax.scatter(
            x, y, s=100, marker="*", label="landmarks", color="orange"))
        drawn_objects.append(ax.text(x, y, "id:" + str(self._id), fontsize=10))
        return drawn_objects
