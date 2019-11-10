import sys
sys.path.append('chapter3')

from drawable import Drawable
from ideal_robot import IdealRobot


class RealRobot(Drawable):
    def __init__(self, initial_pose, camera=None, color='black'):
        self._delegate = IdealRobot(initial_pose, camera, color)

    def draw(self, ax):
        return self._delegate.draw(ax)

    def one_step(self, ut, delta_t):
        self._delegate.one_step(ut, delta_t)
