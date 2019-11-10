import math
import numpy as np
from drawable import Drawable


class IdealCamera(Drawable):
    def __init__(self, env_map):
        self._map = env_map
        self._last_observations = []
        self._last_camera_pose = None

    def observe(self, camera_pose):
        result = []
        for landmark in self._map._landmarks:
            p = self._observation_function(camera_pose, landmark._position)
            result.append(p)
        self._last_observations = result
        self._last_camera_pose = camera_pose
        return result

    def draw(self, ax):
        drawn_objects = []
        for observation in self._last_observations:
            x, y, theta = self._last_camera_pose
            distance, direction = observation[0], observation[1]

            lx = x + distance*math.cos(direction + theta)
            ly = y + distance*math.sin(direction + theta)
            drawn_objects.extend(ax.plot([x, lx], [y, ly], color="pink"))
        return drawn_objects

    @classmethod
    def _fit_angle_in_range(cls, rad):
        while rad >= np.pi:
            rad -= 2*np.pi
        while rad < -np.pi:
            rad += 2*np.pi
        return rad

    @classmethod
    def _observation_function(cls, camera_pose, object_position):
        pose_diff = object_position - camera_pose[0:2]
        phi = math.atan2(pose_diff[1], pose_diff[0]) - camera_pose[2]
        phi = cls._fit_angle_in_range(phi)
        return np.array([np.hypot(*pose_diff), phi]).T


if __name__ == "__main__":
    from map import Map
    from landmark import Landmark
    landmark1 = Landmark(2, -2)
    landmark2 = Landmark(-1, -3)
    landmark3 = Landmark(3, 3)

    world_map = Map()
    world_map.append_landmark(landmark1)
    world_map.append_landmark(landmark2)
    world_map.append_landmark(landmark3)

    camera = IdealCamera(world_map)
    robot_pose = np.array([-2, -1, math.pi/5*6])
    observation = camera.observe(robot_pose)
    print(observation)
