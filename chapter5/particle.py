import math
import sys
sys.path.append("chapter3")
sys.path.append("chapter4")

from drawable import Drawable


class Particle(Drawable):
    def __init__(self, init_pose):
        self._pose = init_pose

    def draw(self, ax):
        xs = self._pose[0]
        ys = self._pose[1]
        vxs = math.cos(self._pose[2])
        vys = math.sin(self._pose[2])
        return ax.quiver(xs, ys, vxs, vys, color="blue", alpha=0.5)
