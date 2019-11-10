import sys
sys.path.append('chapter3')
import math
import numpy as np

from scipy.stats import expon, norm, uniform
from camera import Camera


class RealCamera(Camera):
    def __init__(self, env_map,
                 distance_range=(0.5, 6.0),
                 direction_range=(-math.pi / 3.0, math.pi / 3.0),
                 distance_noise_rate=0.1,
                 direction_noise=math.pi / 90):
        super(RealCamera, self).__init__(
            env_map, distance_range, direction_range)
        self._distance_noise_rate = distance_noise_rate
        self._direction_noise = direction_noise

    def observe(self, camera_pose):
        result = []
        for landmark in self._map._landmarks:
            if self._is_visible(camera_pose, landmark):
                observation = self._observation_function(
                    camera_pose, landmark._position)
                observation = self._add_noise(observation)
                result.append(observation)
        self._last_observations = result
        self._last_camera_pose = camera_pose
        return result

    def _add_noise(self, observation):
        observed_l = observation[0]
        observed_phi = observation[1]
        l = norm.rvs(loc=observed_l, scale=observed_l
                     * self._distance_noise_rate)
        phi = norm.rvs(loc=observed_phi, scale=self._direction_noise)
        return np.array([l, phi]).T


if __name__ == "__main__":
    from map import Map
    from world import World
    from landmark import Landmark
    from ideal_robot import IdealRobot
    from fixed_input_agent import FixedInputAgent
    landmark1 = Landmark(2, -2)
    landmark2 = Landmark(-1, -3)
    landmark3 = Landmark(3, 3)

    world_map = Map()
    world_map.append_landmark(landmark1)
    world_map.append_landmark(landmark2)
    world_map.append_landmark(landmark3)

    camera = RealCamera(world_map)
    world = World(time_span=30, time_interval=0.1)
    for _ in range(10):
        robot = IdealRobot(
            np.array([-2, -1, 0.0]).T, camera=RealCamera(world_map))
        agent = FixedInputAgent(robot, vel=0.2, omega=10.0 / 180 * math.pi)
        world.append_agent(agent)

    world.append_object(world_map)
    world.draw()
