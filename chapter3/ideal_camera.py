import math
import numpy as np
from camera import Camera


class IdealCamera(Camera):
    def __init__(self, env_map,
                 distance_range=(0.5, 6.0),
                 direction_range=(-math.pi / 3.0, math.pi / 3.0)):
        super(IdealCamera, self).__init__(
            env_map, distance_range, direction_range)

    def observe(self, camera_pose):
        result = []
        for landmark in self._map._landmarks:
            if self._is_visible(camera_pose, landmark):
                p = self._observation_function(camera_pose, landmark._position)
                result.append(p)
        self._last_observations = result
        self._last_camera_pose = camera_pose
        return result


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
    robot_pose = np.array([-2, -1, math.pi / 5 * 6])
    observation = camera.observe(robot_pose)
    print(observation)
