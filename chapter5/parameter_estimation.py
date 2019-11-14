import sys
sys.path.append("chapter3")
sys.path.append("chapter4")

import copy
import numpy as np

from real_robot import RealRobot
from world import World
from fixed_input_agent import FixedInputAgent

if __name__ == "__main__":
    init_pose = np.array([0, 0, 0]).T
    robots = []
    
    robot = RealRobot(init_pose, None)
    world = World(time_span=40, time_interval=0.1)

    for i in range(100):
        copied_robot = copy.copy(robot)
        copied_robot._distance_until_noise = copied_robot._noise_pdf.rvs()
        agent = FixedInputAgent(copied_robot, vel=0.1, omega=0.0)
        world.append_agent(agent)
    
    world.draw()
