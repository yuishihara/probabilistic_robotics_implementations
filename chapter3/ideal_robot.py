from drawable import Drawable
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


class IdealRobot(Drawable):
    def __init__(self, initial_pose, camera=None, color='black'):
        self._pose = initial_pose
        self._radius = 0.2
        self._color = color
        self._trajectory = [initial_pose]
        self._camera = camera

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

        # 軌跡を書く
        drawn_objects.extend(ax.plot(
            [pose[0] for pose in self._trajectory],
            [pose[1] for pose in self._trajectory],
            linewidth=0.5, color='black'))

        # カメラのデータを描画
        if self._camera is not None:
            drawn_objects.extend(self._camera.draw(ax))

        return drawn_objects

    def one_step(self, ut, delta_t):
        vel, omega = ut
        self._pose = self.transition_function(vel, omega, delta_t, self._pose)
        self._trajectory.append(self._pose)
        return self._camera.observe(self._pose) if self._camera else None

    @classmethod
    def transition_function(cls, vel, omega, delta_t, pose):
        theta = pose[2]
        if math.fabs(omega) < 1e-10:
            delta_x = vel * math.cos(theta) * delta_t
            delta_y = vel * math.sin(theta) * delta_t
            delta_theta = omega * delta_t
        else:
            delta_x = vel/omega * \
                (math.sin(theta + omega * delta_t) - math.sin(theta))
            delta_y = -vel/omega * \
                (math.cos(theta + omega * delta_t) - math.cos(theta))
            delta_theta = omega * delta_t
        delta_pose = np.array([delta_x, delta_y, delta_theta])
        return pose + delta_pose


if __name__ == "__main__":
    print(IdealRobot.transition_function(
        0.1, 0.0, 1.0, np.array([0, 0, 0]).T))
    print(IdealRobot.transition_function(
        0.1, 10.0/180*math.pi, 9.0, np.array([0, 0, 0]).T))
    print(IdealRobot.transition_function(
        0.1, 10.0/180*math.pi, 18.0, np.array([0, 0, 0]).T))
