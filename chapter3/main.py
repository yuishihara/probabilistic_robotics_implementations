import numpy as np
import math
from world import World
from ideal_robot import IdealRobot
from ideal_camera import IdealCamera
from fixed_input_agent import FixedInputAgent
from map import Map
from landmark import Landmark


def main():
    landmark1 = Landmark(2, -2)
    landmark2 = Landmark(-1, -3)
    landmark3 = Landmark(3, 3)
    world_map = Map()
    world_map.append_landmark(landmark1)
    world_map.append_landmark(landmark2)
    world_map.append_landmark(landmark3)

    robot1 = IdealRobot(np.array([2, 3, math.pi/6]).T,
                        camera=IdealCamera(world_map))
    agent1 = FixedInputAgent(robot1, vel=0.2, omega=0.0)

    robot2 = IdealRobot(np.array([-2, -1, math.pi*5/6]).T,
                        camera=IdealCamera(world_map),
                        color="red")
    agent2 = FixedInputAgent(robot2, vel=0.2, omega=10.0/180*math.pi)

    world = World(time_span=1000, time_interval=0.1)
    world.append_agent(agent1)
    world.append_agent(agent2)
    world.append_object(world_map)

    world.draw()


if __name__ == "__main__":
    main()
