from drawable import Drawable
import math
import numpy as np


class Camera(Drawable):
    def __init__(self, env_map, distance_range, direction_range):
        self._map = env_map
        self._last_observations = []
        self._last_camera_pose = None
        self._distance_range = distance_range
        self._direction_range = direction_range

    def observe(self, camera_pose):
        raise NotImplementedError("observe() is not implemented!!")

    def draw(self, ax):
        drawn_objects = []
        for observation in self._last_observations:
            x, y, theta = self._last_camera_pose
            distance, direction = observation[0], observation[1]

            lx = x + distance * math.cos(direction + theta)
            ly = y + distance * math.sin(direction + theta)
            drawn_objects.extend(ax.plot([x, lx], [y, ly], color="pink"))
        return drawn_objects

    def _is_visible(self, camera_pose, landmark):
        if landmark is None:
            return False
        l, theta = self._relative_polar_position(
            camera_pose, landmark._position)
        l_min = self._distance_range[0]
        l_max = self._distance_range[1]
        theta_min = self._direction_range[0]
        theta_max = self._direction_range[1]
        return (l_min <= l <= l_max) and (theta_min <= theta <= theta_max)

    @classmethod
    def _fit_angle_in_range(cls, rad):
        while rad >= np.pi:
            rad -= 2 * np.pi
        while rad < -np.pi:
            rad += 2 * np.pi
        return rad

    @classmethod
    def _relative_polar_position(cls, camera_pose, object_position):
        pose_diff = object_position - camera_pose[0:2]
        phi = math.atan2(pose_diff[1], pose_diff[0]) - camera_pose[2]
        phi = cls._fit_angle_in_range(phi)
        l = np.hypot(*pose_diff)
        return l, phi

    @classmethod
    def _observation_function(cls, camera_pose, object_position):
        l, phi = cls._relative_polar_position(camera_pose, object_position)
        return np.array([l, phi]).T
