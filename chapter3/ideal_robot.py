from robot import Robot
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


class IdealRobot(Robot):
    def __init__(self, initial_pose, camera=None, color='black'):
        super(IdealRobot, self).__init__(initial_pose, camera, 0.2, color)

    def one_step(self, ut, delta_t):
        vel, omega = ut
        self._pose = self.transition_function(vel, omega, delta_t, self._pose)
        self._trajectory.append(self._pose)
        return self._camera.observe(self._pose) if self._camera else None


if __name__ == "__main__":
    print(IdealRobot.transition_function(
        0.1, 0.0, 1.0, np.array([0, 0, 0]).T))
    print(IdealRobot.transition_function(
        0.1, 10.0 / 180 * math.pi, 9.0, np.array([0, 0, 0]).T))
    print(IdealRobot.transition_function(
        0.1, 10.0 / 180 * math.pi, 18.0, np.array([0, 0, 0]).T))
