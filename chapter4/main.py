import numpy as np
import math
import sys
sys.path.append("chapter3")

from landmark import Landmark
from map import Map
from fixed_input_agent import FixedInputAgent
from ideal_camera import IdealCamera
from real_robot import RealRobot
from world import World


def main():
    landmark1 = Landmark(2, -2)
    landmark2 = Landmark(-1, -3)
    landmark3 = Landmark(3, 3)
    world_map = Map()
    world_map.append_landmark(landmark1)
    world_map.append_landmark(landmark2)
    world_map.append_landmark(landmark3)

    world = World(time_span=30, time_interval=0.1)
    for _ in range(10):
        robot = RealRobot(
            np.array([-2, -1, math.pi * 5 / 6]).T, camera=IdealCamera(world_map))
        agent = FixedInputAgent(robot, vel=0.2, omega=10.0 / 180 * math.pi)
        world.append_agent(agent)

    world.append_object(world_map)
    world.draw()


if __name__ == "__main__":
    main()
